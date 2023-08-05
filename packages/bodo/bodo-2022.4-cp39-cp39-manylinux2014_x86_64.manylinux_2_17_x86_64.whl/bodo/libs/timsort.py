import numpy as np
import pandas as pd
import numba
from numba.extending import overload
from bodo.utils.utils import alloc_arr_tup
MIN_MERGE = 32


@numba.njit(no_cpython_wrapper=True, cache=True)
def sort(key_arrs, lo, hi, data):
    tldi__isno = hi - lo
    if tldi__isno < 2:
        return
    if tldi__isno < MIN_MERGE:
        skfx__lrm = countRunAndMakeAscending(key_arrs, lo, hi, data)
        binarySort(key_arrs, lo, hi, lo + skfx__lrm, data)
        return
    stackSize, runBase, runLen, tmpLength, tmp, tmp_data, minGallop = (
        init_sort_start(key_arrs, data))
    sql__prh = minRunLength(tldi__isno)
    while True:
        stfn__ccg = countRunAndMakeAscending(key_arrs, lo, hi, data)
        if stfn__ccg < sql__prh:
            zsru__kld = tldi__isno if tldi__isno <= sql__prh else sql__prh
            binarySort(key_arrs, lo, lo + zsru__kld, lo + stfn__ccg, data)
            stfn__ccg = zsru__kld
        stackSize = pushRun(stackSize, runBase, runLen, lo, stfn__ccg)
        stackSize, tmpLength, tmp, tmp_data, minGallop = mergeCollapse(
            stackSize, runBase, runLen, key_arrs, data, tmpLength, tmp,
            tmp_data, minGallop)
        lo += stfn__ccg
        tldi__isno -= stfn__ccg
        if tldi__isno == 0:
            break
    assert lo == hi
    stackSize, tmpLength, tmp, tmp_data, minGallop = mergeForceCollapse(
        stackSize, runBase, runLen, key_arrs, data, tmpLength, tmp,
        tmp_data, minGallop)
    assert stackSize == 1


@numba.njit(no_cpython_wrapper=True, cache=True)
def binarySort(key_arrs, lo, hi, start, data):
    assert lo <= start and start <= hi
    if start == lo:
        start += 1
    while start < hi:
        aya__bnwbg = getitem_arr_tup(key_arrs, start)
        khjmg__mkr = getitem_arr_tup(data, start)
        pofkk__rge = lo
        dkm__iat = start
        assert pofkk__rge <= dkm__iat
        while pofkk__rge < dkm__iat:
            epg__jpr = pofkk__rge + dkm__iat >> 1
            if aya__bnwbg < getitem_arr_tup(key_arrs, epg__jpr):
                dkm__iat = epg__jpr
            else:
                pofkk__rge = epg__jpr + 1
        assert pofkk__rge == dkm__iat
        n = start - pofkk__rge
        copyRange_tup(key_arrs, pofkk__rge, key_arrs, pofkk__rge + 1, n)
        copyRange_tup(data, pofkk__rge, data, pofkk__rge + 1, n)
        setitem_arr_tup(key_arrs, pofkk__rge, aya__bnwbg)
        setitem_arr_tup(data, pofkk__rge, khjmg__mkr)
        start += 1


@numba.njit(no_cpython_wrapper=True, cache=True)
def countRunAndMakeAscending(key_arrs, lo, hi, data):
    assert lo < hi
    kxdx__nitrp = lo + 1
    if kxdx__nitrp == hi:
        return 1
    if getitem_arr_tup(key_arrs, kxdx__nitrp) < getitem_arr_tup(key_arrs, lo):
        kxdx__nitrp += 1
        while kxdx__nitrp < hi and getitem_arr_tup(key_arrs, kxdx__nitrp
            ) < getitem_arr_tup(key_arrs, kxdx__nitrp - 1):
            kxdx__nitrp += 1
        reverseRange(key_arrs, lo, kxdx__nitrp, data)
    else:
        kxdx__nitrp += 1
        while kxdx__nitrp < hi and getitem_arr_tup(key_arrs, kxdx__nitrp
            ) >= getitem_arr_tup(key_arrs, kxdx__nitrp - 1):
            kxdx__nitrp += 1
    return kxdx__nitrp - lo


@numba.njit(no_cpython_wrapper=True, cache=True)
def reverseRange(key_arrs, lo, hi, data):
    hi -= 1
    while lo < hi:
        swap_arrs(key_arrs, lo, hi)
        swap_arrs(data, lo, hi)
        lo += 1
        hi -= 1


@numba.njit(no_cpython_wrapper=True, cache=True)
def minRunLength(n):
    assert n >= 0
    mkpym__ftw = 0
    while n >= MIN_MERGE:
        mkpym__ftw |= n & 1
        n >>= 1
    return n + mkpym__ftw


MIN_GALLOP = 7
INITIAL_TMP_STORAGE_LENGTH = 256


@numba.njit(no_cpython_wrapper=True, cache=True)
def init_sort_start(key_arrs, data):
    minGallop = MIN_GALLOP
    pwj__qrucd = len(key_arrs[0])
    tmpLength = (pwj__qrucd >> 1 if pwj__qrucd < 2 *
        INITIAL_TMP_STORAGE_LENGTH else INITIAL_TMP_STORAGE_LENGTH)
    tmp = alloc_arr_tup(tmpLength, key_arrs)
    tmp_data = alloc_arr_tup(tmpLength, data)
    stackSize = 0
    aat__ngowz = (5 if pwj__qrucd < 120 else 10 if pwj__qrucd < 1542 else 
        19 if pwj__qrucd < 119151 else 40)
    runBase = np.empty(aat__ngowz, np.int64)
    runLen = np.empty(aat__ngowz, np.int64)
    return stackSize, runBase, runLen, tmpLength, tmp, tmp_data, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def pushRun(stackSize, runBase, runLen, runBase_val, runLen_val):
    runBase[stackSize] = runBase_val
    runLen[stackSize] = runLen_val
    stackSize += 1
    return stackSize


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeCollapse(stackSize, runBase, runLen, key_arrs, data, tmpLength,
    tmp, tmp_data, minGallop):
    while stackSize > 1:
        n = stackSize - 2
        if n >= 1 and runLen[n - 1] <= runLen[n] + runLen[n + 1
            ] or n >= 2 and runLen[n - 2] <= runLen[n] + runLen[n - 1]:
            if runLen[n - 1] < runLen[n + 1]:
                n -= 1
        elif runLen[n] > runLen[n + 1]:
            break
        stackSize, tmpLength, tmp, tmp_data, minGallop = mergeAt(stackSize,
            runBase, runLen, key_arrs, data, tmpLength, tmp, tmp_data,
            minGallop, n)
    return stackSize, tmpLength, tmp, tmp_data, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeForceCollapse(stackSize, runBase, runLen, key_arrs, data,
    tmpLength, tmp, tmp_data, minGallop):
    while stackSize > 1:
        n = stackSize - 2
        if n > 0 and runLen[n - 1] < runLen[n + 1]:
            n -= 1
        stackSize, tmpLength, tmp, tmp_data, minGallop = mergeAt(stackSize,
            runBase, runLen, key_arrs, data, tmpLength, tmp, tmp_data,
            minGallop, n)
    return stackSize, tmpLength, tmp, tmp_data, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeAt(stackSize, runBase, runLen, key_arrs, data, tmpLength, tmp,
    tmp_data, minGallop, i):
    assert stackSize >= 2
    assert i >= 0
    assert i == stackSize - 2 or i == stackSize - 3
    base1 = runBase[i]
    len1 = runLen[i]
    base2 = runBase[i + 1]
    len2 = runLen[i + 1]
    assert len1 > 0 and len2 > 0
    assert base1 + len1 == base2
    runLen[i] = len1 + len2
    if i == stackSize - 3:
        runBase[i + 1] = runBase[i + 2]
        runLen[i + 1] = runLen[i + 2]
    stackSize -= 1
    adq__vmw = gallopRight(getitem_arr_tup(key_arrs, base2), key_arrs,
        base1, len1, 0)
    assert adq__vmw >= 0
    base1 += adq__vmw
    len1 -= adq__vmw
    if len1 == 0:
        return stackSize, tmpLength, tmp, tmp_data, minGallop
    len2 = gallopLeft(getitem_arr_tup(key_arrs, base1 + len1 - 1), key_arrs,
        base2, len2, len2 - 1)
    assert len2 >= 0
    if len2 == 0:
        return stackSize, tmpLength, tmp, tmp_data, minGallop
    if len1 <= len2:
        tmpLength, tmp, tmp_data = ensureCapacity(tmpLength, tmp, tmp_data,
            key_arrs, data, len1)
        minGallop = mergeLo(key_arrs, data, tmp, tmp_data, minGallop, base1,
            len1, base2, len2)
    else:
        tmpLength, tmp, tmp_data = ensureCapacity(tmpLength, tmp, tmp_data,
            key_arrs, data, len2)
        minGallop = mergeHi(key_arrs, data, tmp, tmp_data, minGallop, base1,
            len1, base2, len2)
    return stackSize, tmpLength, tmp, tmp_data, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def gallopLeft(key, arr, base, _len, hint):
    assert _len > 0 and hint >= 0 and hint < _len
    gaxvc__elwz = 0
    dndf__bgtl = 1
    if key > getitem_arr_tup(arr, base + hint):
        lhdf__vwuet = _len - hint
        while dndf__bgtl < lhdf__vwuet and key > getitem_arr_tup(arr, base +
            hint + dndf__bgtl):
            gaxvc__elwz = dndf__bgtl
            dndf__bgtl = (dndf__bgtl << 1) + 1
            if dndf__bgtl <= 0:
                dndf__bgtl = lhdf__vwuet
        if dndf__bgtl > lhdf__vwuet:
            dndf__bgtl = lhdf__vwuet
        gaxvc__elwz += hint
        dndf__bgtl += hint
    else:
        lhdf__vwuet = hint + 1
        while dndf__bgtl < lhdf__vwuet and key <= getitem_arr_tup(arr, base +
            hint - dndf__bgtl):
            gaxvc__elwz = dndf__bgtl
            dndf__bgtl = (dndf__bgtl << 1) + 1
            if dndf__bgtl <= 0:
                dndf__bgtl = lhdf__vwuet
        if dndf__bgtl > lhdf__vwuet:
            dndf__bgtl = lhdf__vwuet
        tmp = gaxvc__elwz
        gaxvc__elwz = hint - dndf__bgtl
        dndf__bgtl = hint - tmp
    assert -1 <= gaxvc__elwz and gaxvc__elwz < dndf__bgtl and dndf__bgtl <= _len
    gaxvc__elwz += 1
    while gaxvc__elwz < dndf__bgtl:
        rjkqu__hgs = gaxvc__elwz + (dndf__bgtl - gaxvc__elwz >> 1)
        if key > getitem_arr_tup(arr, base + rjkqu__hgs):
            gaxvc__elwz = rjkqu__hgs + 1
        else:
            dndf__bgtl = rjkqu__hgs
    assert gaxvc__elwz == dndf__bgtl
    return dndf__bgtl


@numba.njit(no_cpython_wrapper=True, cache=True)
def gallopRight(key, arr, base, _len, hint):
    assert _len > 0 and hint >= 0 and hint < _len
    dndf__bgtl = 1
    gaxvc__elwz = 0
    if key < getitem_arr_tup(arr, base + hint):
        lhdf__vwuet = hint + 1
        while dndf__bgtl < lhdf__vwuet and key < getitem_arr_tup(arr, base +
            hint - dndf__bgtl):
            gaxvc__elwz = dndf__bgtl
            dndf__bgtl = (dndf__bgtl << 1) + 1
            if dndf__bgtl <= 0:
                dndf__bgtl = lhdf__vwuet
        if dndf__bgtl > lhdf__vwuet:
            dndf__bgtl = lhdf__vwuet
        tmp = gaxvc__elwz
        gaxvc__elwz = hint - dndf__bgtl
        dndf__bgtl = hint - tmp
    else:
        lhdf__vwuet = _len - hint
        while dndf__bgtl < lhdf__vwuet and key >= getitem_arr_tup(arr, base +
            hint + dndf__bgtl):
            gaxvc__elwz = dndf__bgtl
            dndf__bgtl = (dndf__bgtl << 1) + 1
            if dndf__bgtl <= 0:
                dndf__bgtl = lhdf__vwuet
        if dndf__bgtl > lhdf__vwuet:
            dndf__bgtl = lhdf__vwuet
        gaxvc__elwz += hint
        dndf__bgtl += hint
    assert -1 <= gaxvc__elwz and gaxvc__elwz < dndf__bgtl and dndf__bgtl <= _len
    gaxvc__elwz += 1
    while gaxvc__elwz < dndf__bgtl:
        rjkqu__hgs = gaxvc__elwz + (dndf__bgtl - gaxvc__elwz >> 1)
        if key < getitem_arr_tup(arr, base + rjkqu__hgs):
            dndf__bgtl = rjkqu__hgs
        else:
            gaxvc__elwz = rjkqu__hgs + 1
    assert gaxvc__elwz == dndf__bgtl
    return dndf__bgtl


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeLo(key_arrs, data, tmp, tmp_data, minGallop, base1, len1, base2, len2
    ):
    assert len1 > 0 and len2 > 0 and base1 + len1 == base2
    arr = key_arrs
    arr_data = data
    copyRange_tup(arr, base1, tmp, 0, len1)
    copyRange_tup(arr_data, base1, tmp_data, 0, len1)
    cursor1 = 0
    cursor2 = base2
    dest = base1
    setitem_arr_tup(arr, dest, getitem_arr_tup(arr, cursor2))
    copyElement_tup(arr_data, cursor2, arr_data, dest)
    cursor2 += 1
    dest += 1
    len2 -= 1
    if len2 == 0:
        copyRange_tup(tmp, cursor1, arr, dest, len1)
        copyRange_tup(tmp_data, cursor1, arr_data, dest, len1)
        return minGallop
    if len1 == 1:
        copyRange_tup(arr, cursor2, arr, dest, len2)
        copyRange_tup(arr_data, cursor2, arr_data, dest, len2)
        copyElement_tup(tmp, cursor1, arr, dest + len2)
        copyElement_tup(tmp_data, cursor1, arr_data, dest + len2)
        return minGallop
    len1, len2, cursor1, cursor2, dest, minGallop = mergeLo_inner(key_arrs,
        data, tmp_data, len1, len2, tmp, cursor1, cursor2, dest, minGallop)
    minGallop = 1 if minGallop < 1 else minGallop
    if len1 == 1:
        assert len2 > 0
        copyRange_tup(arr, cursor2, arr, dest, len2)
        copyRange_tup(arr_data, cursor2, arr_data, dest, len2)
        copyElement_tup(tmp, cursor1, arr, dest + len2)
        copyElement_tup(tmp_data, cursor1, arr_data, dest + len2)
    elif len1 == 0:
        raise ValueError('Comparison method violates its general contract!')
    else:
        assert len2 == 0
        assert len1 > 1
        copyRange_tup(tmp, cursor1, arr, dest, len1)
        copyRange_tup(tmp_data, cursor1, arr_data, dest, len1)
    return minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeLo_inner(arr, arr_data, tmp_data, len1, len2, tmp, cursor1,
    cursor2, dest, minGallop):
    while True:
        gkv__meno = 0
        rirw__tlt = 0
        while True:
            assert len1 > 1 and len2 > 0
            if getitem_arr_tup(arr, cursor2) < getitem_arr_tup(tmp, cursor1):
                copyElement_tup(arr, cursor2, arr, dest)
                copyElement_tup(arr_data, cursor2, arr_data, dest)
                cursor2 += 1
                dest += 1
                rirw__tlt += 1
                gkv__meno = 0
                len2 -= 1
                if len2 == 0:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            else:
                copyElement_tup(tmp, cursor1, arr, dest)
                copyElement_tup(tmp_data, cursor1, arr_data, dest)
                cursor1 += 1
                dest += 1
                gkv__meno += 1
                rirw__tlt = 0
                len1 -= 1
                if len1 == 1:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            if not gkv__meno | rirw__tlt < minGallop:
                break
        while True:
            assert len1 > 1 and len2 > 0
            gkv__meno = gallopRight(getitem_arr_tup(arr, cursor2), tmp,
                cursor1, len1, 0)
            if gkv__meno != 0:
                copyRange_tup(tmp, cursor1, arr, dest, gkv__meno)
                copyRange_tup(tmp_data, cursor1, arr_data, dest, gkv__meno)
                dest += gkv__meno
                cursor1 += gkv__meno
                len1 -= gkv__meno
                if len1 <= 1:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            copyElement_tup(arr, cursor2, arr, dest)
            copyElement_tup(arr_data, cursor2, arr_data, dest)
            cursor2 += 1
            dest += 1
            len2 -= 1
            if len2 == 0:
                return len1, len2, cursor1, cursor2, dest, minGallop
            rirw__tlt = gallopLeft(getitem_arr_tup(tmp, cursor1), arr,
                cursor2, len2, 0)
            if rirw__tlt != 0:
                copyRange_tup(arr, cursor2, arr, dest, rirw__tlt)
                copyRange_tup(arr_data, cursor2, arr_data, dest, rirw__tlt)
                dest += rirw__tlt
                cursor2 += rirw__tlt
                len2 -= rirw__tlt
                if len2 == 0:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            copyElement_tup(tmp, cursor1, arr, dest)
            copyElement_tup(tmp_data, cursor1, arr_data, dest)
            cursor1 += 1
            dest += 1
            len1 -= 1
            if len1 == 1:
                return len1, len2, cursor1, cursor2, dest, minGallop
            minGallop -= 1
            if not gkv__meno >= MIN_GALLOP | rirw__tlt >= MIN_GALLOP:
                break
        if minGallop < 0:
            minGallop = 0
        minGallop += 2
    return len1, len2, cursor1, cursor2, dest, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeHi(key_arrs, data, tmp, tmp_data, minGallop, base1, len1, base2, len2
    ):
    assert len1 > 0 and len2 > 0 and base1 + len1 == base2
    arr = key_arrs
    arr_data = data
    copyRange_tup(arr, base2, tmp, 0, len2)
    copyRange_tup(arr_data, base2, tmp_data, 0, len2)
    cursor1 = base1 + len1 - 1
    cursor2 = len2 - 1
    dest = base2 + len2 - 1
    copyElement_tup(arr, cursor1, arr, dest)
    copyElement_tup(arr_data, cursor1, arr_data, dest)
    cursor1 -= 1
    dest -= 1
    len1 -= 1
    if len1 == 0:
        copyRange_tup(tmp, 0, arr, dest - (len2 - 1), len2)
        copyRange_tup(tmp_data, 0, arr_data, dest - (len2 - 1), len2)
        return minGallop
    if len2 == 1:
        dest -= len1
        cursor1 -= len1
        copyRange_tup(arr, cursor1 + 1, arr, dest + 1, len1)
        copyRange_tup(arr_data, cursor1 + 1, arr_data, dest + 1, len1)
        copyElement_tup(tmp, cursor2, arr, dest)
        copyElement_tup(tmp_data, cursor2, arr_data, dest)
        return minGallop
    len1, len2, tmp, cursor1, cursor2, dest, minGallop = mergeHi_inner(key_arrs
        , data, tmp_data, base1, len1, len2, tmp, cursor1, cursor2, dest,
        minGallop)
    minGallop = 1 if minGallop < 1 else minGallop
    if len2 == 1:
        assert len1 > 0
        dest -= len1
        cursor1 -= len1
        copyRange_tup(arr, cursor1 + 1, arr, dest + 1, len1)
        copyRange_tup(arr_data, cursor1 + 1, arr_data, dest + 1, len1)
        copyElement_tup(tmp, cursor2, arr, dest)
        copyElement_tup(tmp_data, cursor2, arr_data, dest)
    elif len2 == 0:
        raise ValueError('Comparison method violates its general contract!')
    else:
        assert len1 == 0
        assert len2 > 0
        copyRange_tup(tmp, 0, arr, dest - (len2 - 1), len2)
        copyRange_tup(tmp_data, 0, arr_data, dest - (len2 - 1), len2)
    return minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeHi_inner(arr, arr_data, tmp_data, base1, len1, len2, tmp, cursor1,
    cursor2, dest, minGallop):
    while True:
        gkv__meno = 0
        rirw__tlt = 0
        while True:
            assert len1 > 0 and len2 > 1
            if getitem_arr_tup(tmp, cursor2) < getitem_arr_tup(arr, cursor1):
                copyElement_tup(arr, cursor1, arr, dest)
                copyElement_tup(arr_data, cursor1, arr_data, dest)
                cursor1 -= 1
                dest -= 1
                gkv__meno += 1
                rirw__tlt = 0
                len1 -= 1
                if len1 == 0:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            else:
                copyElement_tup(tmp, cursor2, arr, dest)
                copyElement_tup(tmp_data, cursor2, arr_data, dest)
                cursor2 -= 1
                dest -= 1
                rirw__tlt += 1
                gkv__meno = 0
                len2 -= 1
                if len2 == 1:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            if not gkv__meno | rirw__tlt < minGallop:
                break
        while True:
            assert len1 > 0 and len2 > 1
            gkv__meno = len1 - gallopRight(getitem_arr_tup(tmp, cursor2),
                arr, base1, len1, len1 - 1)
            if gkv__meno != 0:
                dest -= gkv__meno
                cursor1 -= gkv__meno
                len1 -= gkv__meno
                copyRange_tup(arr, cursor1 + 1, arr, dest + 1, gkv__meno)
                copyRange_tup(arr_data, cursor1 + 1, arr_data, dest + 1,
                    gkv__meno)
                if len1 == 0:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            copyElement_tup(tmp, cursor2, arr, dest)
            copyElement_tup(tmp_data, cursor2, arr_data, dest)
            cursor2 -= 1
            dest -= 1
            len2 -= 1
            if len2 == 1:
                return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            rirw__tlt = len2 - gallopLeft(getitem_arr_tup(arr, cursor1),
                tmp, 0, len2, len2 - 1)
            if rirw__tlt != 0:
                dest -= rirw__tlt
                cursor2 -= rirw__tlt
                len2 -= rirw__tlt
                copyRange_tup(tmp, cursor2 + 1, arr, dest + 1, rirw__tlt)
                copyRange_tup(tmp_data, cursor2 + 1, arr_data, dest + 1,
                    rirw__tlt)
                if len2 <= 1:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            copyElement_tup(arr, cursor1, arr, dest)
            copyElement_tup(arr_data, cursor1, arr_data, dest)
            cursor1 -= 1
            dest -= 1
            len1 -= 1
            if len1 == 0:
                return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            minGallop -= 1
            if not gkv__meno >= MIN_GALLOP | rirw__tlt >= MIN_GALLOP:
                break
        if minGallop < 0:
            minGallop = 0
        minGallop += 2
    return len1, len2, tmp, cursor1, cursor2, dest, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def ensureCapacity(tmpLength, tmp, tmp_data, key_arrs, data, minCapacity):
    ief__igdjj = len(key_arrs[0])
    if tmpLength < minCapacity:
        metke__ruf = minCapacity
        metke__ruf |= metke__ruf >> 1
        metke__ruf |= metke__ruf >> 2
        metke__ruf |= metke__ruf >> 4
        metke__ruf |= metke__ruf >> 8
        metke__ruf |= metke__ruf >> 16
        metke__ruf += 1
        if metke__ruf < 0:
            metke__ruf = minCapacity
        else:
            metke__ruf = min(metke__ruf, ief__igdjj >> 1)
        tmp = alloc_arr_tup(metke__ruf, key_arrs)
        tmp_data = alloc_arr_tup(metke__ruf, data)
        tmpLength = metke__ruf
    return tmpLength, tmp, tmp_data


def swap_arrs(data, lo, hi):
    for arr in data:
        ugxy__himsx = arr[lo]
        arr[lo] = arr[hi]
        arr[hi] = ugxy__himsx


@overload(swap_arrs, no_unliteral=True)
def swap_arrs_overload(arr_tup, lo, hi):
    hgzxf__por = arr_tup.count
    dedl__wfk = 'def f(arr_tup, lo, hi):\n'
    for i in range(hgzxf__por):
        dedl__wfk += '  tmp_v_{} = arr_tup[{}][lo]\n'.format(i, i)
        dedl__wfk += '  arr_tup[{}][lo] = arr_tup[{}][hi]\n'.format(i, i)
        dedl__wfk += '  arr_tup[{}][hi] = tmp_v_{}\n'.format(i, i)
    dedl__wfk += '  return\n'
    sfv__banjh = {}
    exec(dedl__wfk, {}, sfv__banjh)
    kqp__srdy = sfv__banjh['f']
    return kqp__srdy


@numba.njit(no_cpython_wrapper=True, cache=True)
def copyRange(src_arr, src_pos, dst_arr, dst_pos, n):
    dst_arr[dst_pos:dst_pos + n] = src_arr[src_pos:src_pos + n]


def copyRange_tup(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):
    for src_arr, dst_arr in zip(src_arr_tup, dst_arr_tup):
        dst_arr[dst_pos:dst_pos + n] = src_arr[src_pos:src_pos + n]


@overload(copyRange_tup, no_unliteral=True)
def copyRange_tup_overload(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):
    hgzxf__por = src_arr_tup.count
    assert hgzxf__por == dst_arr_tup.count
    dedl__wfk = 'def f(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):\n'
    for i in range(hgzxf__por):
        dedl__wfk += (
            '  copyRange(src_arr_tup[{}], src_pos, dst_arr_tup[{}], dst_pos, n)\n'
            .format(i, i))
    dedl__wfk += '  return\n'
    sfv__banjh = {}
    exec(dedl__wfk, {'copyRange': copyRange}, sfv__banjh)
    ddf__lpz = sfv__banjh['f']
    return ddf__lpz


@numba.njit(no_cpython_wrapper=True, cache=True)
def copyElement(src_arr, src_pos, dst_arr, dst_pos):
    dst_arr[dst_pos] = src_arr[src_pos]


def copyElement_tup(src_arr_tup, src_pos, dst_arr_tup, dst_pos):
    for src_arr, dst_arr in zip(src_arr_tup, dst_arr_tup):
        dst_arr[dst_pos] = src_arr[src_pos]


@overload(copyElement_tup, no_unliteral=True)
def copyElement_tup_overload(src_arr_tup, src_pos, dst_arr_tup, dst_pos):
    hgzxf__por = src_arr_tup.count
    assert hgzxf__por == dst_arr_tup.count
    dedl__wfk = 'def f(src_arr_tup, src_pos, dst_arr_tup, dst_pos):\n'
    for i in range(hgzxf__por):
        dedl__wfk += (
            '  copyElement(src_arr_tup[{}], src_pos, dst_arr_tup[{}], dst_pos)\n'
            .format(i, i))
    dedl__wfk += '  return\n'
    sfv__banjh = {}
    exec(dedl__wfk, {'copyElement': copyElement}, sfv__banjh)
    ddf__lpz = sfv__banjh['f']
    return ddf__lpz


def getitem_arr_tup(arr_tup, ind):
    pvvui__wdnp = [arr[ind] for arr in arr_tup]
    return tuple(pvvui__wdnp)


@overload(getitem_arr_tup, no_unliteral=True)
def getitem_arr_tup_overload(arr_tup, ind):
    hgzxf__por = arr_tup.count
    dedl__wfk = 'def f(arr_tup, ind):\n'
    dedl__wfk += '  return ({}{})\n'.format(','.join(['arr_tup[{}][ind]'.
        format(i) for i in range(hgzxf__por)]), ',' if hgzxf__por == 1 else '')
    sfv__banjh = {}
    exec(dedl__wfk, {}, sfv__banjh)
    aoc__nxfpb = sfv__banjh['f']
    return aoc__nxfpb


def setitem_arr_tup(arr_tup, ind, val_tup):
    for arr, qdme__axvr in zip(arr_tup, val_tup):
        arr[ind] = qdme__axvr


@overload(setitem_arr_tup, no_unliteral=True)
def setitem_arr_tup_overload(arr_tup, ind, val_tup):
    hgzxf__por = arr_tup.count
    dedl__wfk = 'def f(arr_tup, ind, val_tup):\n'
    for i in range(hgzxf__por):
        if isinstance(val_tup, numba.core.types.BaseTuple):
            dedl__wfk += '  arr_tup[{}][ind] = val_tup[{}]\n'.format(i, i)
        else:
            assert arr_tup.count == 1
            dedl__wfk += '  arr_tup[{}][ind] = val_tup\n'.format(i)
    dedl__wfk += '  return\n'
    sfv__banjh = {}
    exec(dedl__wfk, {}, sfv__banjh)
    aoc__nxfpb = sfv__banjh['f']
    return aoc__nxfpb


def test():
    import time
    fxzy__yhktz = time.time()
    hhq__evutz = np.ones(3)
    data = np.arange(3), np.ones(3)
    sort((hhq__evutz,), 0, 3, data)
    print('compile time', time.time() - fxzy__yhktz)
    n = 210000
    np.random.seed(2)
    data = np.arange(n), np.random.ranf(n)
    lhso__kuce = np.random.ranf(n)
    tfs__fyqp = pd.DataFrame({'A': lhso__kuce, 'B': data[0], 'C': data[1]})
    fxzy__yhktz = time.time()
    anb__hwy = tfs__fyqp.sort_values('A', inplace=False)
    qcgg__iyadu = time.time()
    sort((lhso__kuce,), 0, n, data)
    print('Bodo', time.time() - qcgg__iyadu, 'Numpy', qcgg__iyadu - fxzy__yhktz
        )
    np.testing.assert_almost_equal(data[0], anb__hwy.B.values)
    np.testing.assert_almost_equal(data[1], anb__hwy.C.values)


if __name__ == '__main__':
    test()
