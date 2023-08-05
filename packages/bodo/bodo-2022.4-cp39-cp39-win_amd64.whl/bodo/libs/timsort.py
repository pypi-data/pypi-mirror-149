import numpy as np
import pandas as pd
import numba
from numba.extending import overload
from bodo.utils.utils import alloc_arr_tup
MIN_MERGE = 32


@numba.njit(no_cpython_wrapper=True, cache=True)
def sort(key_arrs, lo, hi, data):
    omme__rimy = hi - lo
    if omme__rimy < 2:
        return
    if omme__rimy < MIN_MERGE:
        deca__qjjy = countRunAndMakeAscending(key_arrs, lo, hi, data)
        binarySort(key_arrs, lo, hi, lo + deca__qjjy, data)
        return
    stackSize, runBase, runLen, tmpLength, tmp, tmp_data, minGallop = (
        init_sort_start(key_arrs, data))
    bttf__htnnl = minRunLength(omme__rimy)
    while True:
        knq__bwv = countRunAndMakeAscending(key_arrs, lo, hi, data)
        if knq__bwv < bttf__htnnl:
            xuar__luure = (omme__rimy if omme__rimy <= bttf__htnnl else
                bttf__htnnl)
            binarySort(key_arrs, lo, lo + xuar__luure, lo + knq__bwv, data)
            knq__bwv = xuar__luure
        stackSize = pushRun(stackSize, runBase, runLen, lo, knq__bwv)
        stackSize, tmpLength, tmp, tmp_data, minGallop = mergeCollapse(
            stackSize, runBase, runLen, key_arrs, data, tmpLength, tmp,
            tmp_data, minGallop)
        lo += knq__bwv
        omme__rimy -= knq__bwv
        if omme__rimy == 0:
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
        rdzvt__efbfc = getitem_arr_tup(key_arrs, start)
        tdlqg__lol = getitem_arr_tup(data, start)
        svkl__pdito = lo
        danb__twx = start
        assert svkl__pdito <= danb__twx
        while svkl__pdito < danb__twx:
            evxij__jyukf = svkl__pdito + danb__twx >> 1
            if rdzvt__efbfc < getitem_arr_tup(key_arrs, evxij__jyukf):
                danb__twx = evxij__jyukf
            else:
                svkl__pdito = evxij__jyukf + 1
        assert svkl__pdito == danb__twx
        n = start - svkl__pdito
        copyRange_tup(key_arrs, svkl__pdito, key_arrs, svkl__pdito + 1, n)
        copyRange_tup(data, svkl__pdito, data, svkl__pdito + 1, n)
        setitem_arr_tup(key_arrs, svkl__pdito, rdzvt__efbfc)
        setitem_arr_tup(data, svkl__pdito, tdlqg__lol)
        start += 1


@numba.njit(no_cpython_wrapper=True, cache=True)
def countRunAndMakeAscending(key_arrs, lo, hi, data):
    assert lo < hi
    oyy__dnlmb = lo + 1
    if oyy__dnlmb == hi:
        return 1
    if getitem_arr_tup(key_arrs, oyy__dnlmb) < getitem_arr_tup(key_arrs, lo):
        oyy__dnlmb += 1
        while oyy__dnlmb < hi and getitem_arr_tup(key_arrs, oyy__dnlmb
            ) < getitem_arr_tup(key_arrs, oyy__dnlmb - 1):
            oyy__dnlmb += 1
        reverseRange(key_arrs, lo, oyy__dnlmb, data)
    else:
        oyy__dnlmb += 1
        while oyy__dnlmb < hi and getitem_arr_tup(key_arrs, oyy__dnlmb
            ) >= getitem_arr_tup(key_arrs, oyy__dnlmb - 1):
            oyy__dnlmb += 1
    return oyy__dnlmb - lo


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
    ewwjk__mfsld = 0
    while n >= MIN_MERGE:
        ewwjk__mfsld |= n & 1
        n >>= 1
    return n + ewwjk__mfsld


MIN_GALLOP = 7
INITIAL_TMP_STORAGE_LENGTH = 256


@numba.njit(no_cpython_wrapper=True, cache=True)
def init_sort_start(key_arrs, data):
    minGallop = MIN_GALLOP
    medy__hkw = len(key_arrs[0])
    tmpLength = (medy__hkw >> 1 if medy__hkw < 2 *
        INITIAL_TMP_STORAGE_LENGTH else INITIAL_TMP_STORAGE_LENGTH)
    tmp = alloc_arr_tup(tmpLength, key_arrs)
    tmp_data = alloc_arr_tup(tmpLength, data)
    stackSize = 0
    svw__wwi = (5 if medy__hkw < 120 else 10 if medy__hkw < 1542 else 19 if
        medy__hkw < 119151 else 40)
    runBase = np.empty(svw__wwi, np.int64)
    runLen = np.empty(svw__wwi, np.int64)
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
    afa__gstla = gallopRight(getitem_arr_tup(key_arrs, base2), key_arrs,
        base1, len1, 0)
    assert afa__gstla >= 0
    base1 += afa__gstla
    len1 -= afa__gstla
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
    ukz__lhs = 0
    hec__ryy = 1
    if key > getitem_arr_tup(arr, base + hint):
        bcoem__iecg = _len - hint
        while hec__ryy < bcoem__iecg and key > getitem_arr_tup(arr, base +
            hint + hec__ryy):
            ukz__lhs = hec__ryy
            hec__ryy = (hec__ryy << 1) + 1
            if hec__ryy <= 0:
                hec__ryy = bcoem__iecg
        if hec__ryy > bcoem__iecg:
            hec__ryy = bcoem__iecg
        ukz__lhs += hint
        hec__ryy += hint
    else:
        bcoem__iecg = hint + 1
        while hec__ryy < bcoem__iecg and key <= getitem_arr_tup(arr, base +
            hint - hec__ryy):
            ukz__lhs = hec__ryy
            hec__ryy = (hec__ryy << 1) + 1
            if hec__ryy <= 0:
                hec__ryy = bcoem__iecg
        if hec__ryy > bcoem__iecg:
            hec__ryy = bcoem__iecg
        tmp = ukz__lhs
        ukz__lhs = hint - hec__ryy
        hec__ryy = hint - tmp
    assert -1 <= ukz__lhs and ukz__lhs < hec__ryy and hec__ryy <= _len
    ukz__lhs += 1
    while ukz__lhs < hec__ryy:
        xuswq__djp = ukz__lhs + (hec__ryy - ukz__lhs >> 1)
        if key > getitem_arr_tup(arr, base + xuswq__djp):
            ukz__lhs = xuswq__djp + 1
        else:
            hec__ryy = xuswq__djp
    assert ukz__lhs == hec__ryy
    return hec__ryy


@numba.njit(no_cpython_wrapper=True, cache=True)
def gallopRight(key, arr, base, _len, hint):
    assert _len > 0 and hint >= 0 and hint < _len
    hec__ryy = 1
    ukz__lhs = 0
    if key < getitem_arr_tup(arr, base + hint):
        bcoem__iecg = hint + 1
        while hec__ryy < bcoem__iecg and key < getitem_arr_tup(arr, base +
            hint - hec__ryy):
            ukz__lhs = hec__ryy
            hec__ryy = (hec__ryy << 1) + 1
            if hec__ryy <= 0:
                hec__ryy = bcoem__iecg
        if hec__ryy > bcoem__iecg:
            hec__ryy = bcoem__iecg
        tmp = ukz__lhs
        ukz__lhs = hint - hec__ryy
        hec__ryy = hint - tmp
    else:
        bcoem__iecg = _len - hint
        while hec__ryy < bcoem__iecg and key >= getitem_arr_tup(arr, base +
            hint + hec__ryy):
            ukz__lhs = hec__ryy
            hec__ryy = (hec__ryy << 1) + 1
            if hec__ryy <= 0:
                hec__ryy = bcoem__iecg
        if hec__ryy > bcoem__iecg:
            hec__ryy = bcoem__iecg
        ukz__lhs += hint
        hec__ryy += hint
    assert -1 <= ukz__lhs and ukz__lhs < hec__ryy and hec__ryy <= _len
    ukz__lhs += 1
    while ukz__lhs < hec__ryy:
        xuswq__djp = ukz__lhs + (hec__ryy - ukz__lhs >> 1)
        if key < getitem_arr_tup(arr, base + xuswq__djp):
            hec__ryy = xuswq__djp
        else:
            ukz__lhs = xuswq__djp + 1
    assert ukz__lhs == hec__ryy
    return hec__ryy


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
        nwc__jiel = 0
        glcln__pvao = 0
        while True:
            assert len1 > 1 and len2 > 0
            if getitem_arr_tup(arr, cursor2) < getitem_arr_tup(tmp, cursor1):
                copyElement_tup(arr, cursor2, arr, dest)
                copyElement_tup(arr_data, cursor2, arr_data, dest)
                cursor2 += 1
                dest += 1
                glcln__pvao += 1
                nwc__jiel = 0
                len2 -= 1
                if len2 == 0:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            else:
                copyElement_tup(tmp, cursor1, arr, dest)
                copyElement_tup(tmp_data, cursor1, arr_data, dest)
                cursor1 += 1
                dest += 1
                nwc__jiel += 1
                glcln__pvao = 0
                len1 -= 1
                if len1 == 1:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            if not nwc__jiel | glcln__pvao < minGallop:
                break
        while True:
            assert len1 > 1 and len2 > 0
            nwc__jiel = gallopRight(getitem_arr_tup(arr, cursor2), tmp,
                cursor1, len1, 0)
            if nwc__jiel != 0:
                copyRange_tup(tmp, cursor1, arr, dest, nwc__jiel)
                copyRange_tup(tmp_data, cursor1, arr_data, dest, nwc__jiel)
                dest += nwc__jiel
                cursor1 += nwc__jiel
                len1 -= nwc__jiel
                if len1 <= 1:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            copyElement_tup(arr, cursor2, arr, dest)
            copyElement_tup(arr_data, cursor2, arr_data, dest)
            cursor2 += 1
            dest += 1
            len2 -= 1
            if len2 == 0:
                return len1, len2, cursor1, cursor2, dest, minGallop
            glcln__pvao = gallopLeft(getitem_arr_tup(tmp, cursor1), arr,
                cursor2, len2, 0)
            if glcln__pvao != 0:
                copyRange_tup(arr, cursor2, arr, dest, glcln__pvao)
                copyRange_tup(arr_data, cursor2, arr_data, dest, glcln__pvao)
                dest += glcln__pvao
                cursor2 += glcln__pvao
                len2 -= glcln__pvao
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
            if not nwc__jiel >= MIN_GALLOP | glcln__pvao >= MIN_GALLOP:
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
        nwc__jiel = 0
        glcln__pvao = 0
        while True:
            assert len1 > 0 and len2 > 1
            if getitem_arr_tup(tmp, cursor2) < getitem_arr_tup(arr, cursor1):
                copyElement_tup(arr, cursor1, arr, dest)
                copyElement_tup(arr_data, cursor1, arr_data, dest)
                cursor1 -= 1
                dest -= 1
                nwc__jiel += 1
                glcln__pvao = 0
                len1 -= 1
                if len1 == 0:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            else:
                copyElement_tup(tmp, cursor2, arr, dest)
                copyElement_tup(tmp_data, cursor2, arr_data, dest)
                cursor2 -= 1
                dest -= 1
                glcln__pvao += 1
                nwc__jiel = 0
                len2 -= 1
                if len2 == 1:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            if not nwc__jiel | glcln__pvao < minGallop:
                break
        while True:
            assert len1 > 0 and len2 > 1
            nwc__jiel = len1 - gallopRight(getitem_arr_tup(tmp, cursor2),
                arr, base1, len1, len1 - 1)
            if nwc__jiel != 0:
                dest -= nwc__jiel
                cursor1 -= nwc__jiel
                len1 -= nwc__jiel
                copyRange_tup(arr, cursor1 + 1, arr, dest + 1, nwc__jiel)
                copyRange_tup(arr_data, cursor1 + 1, arr_data, dest + 1,
                    nwc__jiel)
                if len1 == 0:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            copyElement_tup(tmp, cursor2, arr, dest)
            copyElement_tup(tmp_data, cursor2, arr_data, dest)
            cursor2 -= 1
            dest -= 1
            len2 -= 1
            if len2 == 1:
                return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            glcln__pvao = len2 - gallopLeft(getitem_arr_tup(arr, cursor1),
                tmp, 0, len2, len2 - 1)
            if glcln__pvao != 0:
                dest -= glcln__pvao
                cursor2 -= glcln__pvao
                len2 -= glcln__pvao
                copyRange_tup(tmp, cursor2 + 1, arr, dest + 1, glcln__pvao)
                copyRange_tup(tmp_data, cursor2 + 1, arr_data, dest + 1,
                    glcln__pvao)
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
            if not nwc__jiel >= MIN_GALLOP | glcln__pvao >= MIN_GALLOP:
                break
        if minGallop < 0:
            minGallop = 0
        minGallop += 2
    return len1, len2, tmp, cursor1, cursor2, dest, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def ensureCapacity(tmpLength, tmp, tmp_data, key_arrs, data, minCapacity):
    phb__nin = len(key_arrs[0])
    if tmpLength < minCapacity:
        iyprk__yqj = minCapacity
        iyprk__yqj |= iyprk__yqj >> 1
        iyprk__yqj |= iyprk__yqj >> 2
        iyprk__yqj |= iyprk__yqj >> 4
        iyprk__yqj |= iyprk__yqj >> 8
        iyprk__yqj |= iyprk__yqj >> 16
        iyprk__yqj += 1
        if iyprk__yqj < 0:
            iyprk__yqj = minCapacity
        else:
            iyprk__yqj = min(iyprk__yqj, phb__nin >> 1)
        tmp = alloc_arr_tup(iyprk__yqj, key_arrs)
        tmp_data = alloc_arr_tup(iyprk__yqj, data)
        tmpLength = iyprk__yqj
    return tmpLength, tmp, tmp_data


def swap_arrs(data, lo, hi):
    for arr in data:
        aiw__ccub = arr[lo]
        arr[lo] = arr[hi]
        arr[hi] = aiw__ccub


@overload(swap_arrs, no_unliteral=True)
def swap_arrs_overload(arr_tup, lo, hi):
    assxa__jeee = arr_tup.count
    ojab__ham = 'def f(arr_tup, lo, hi):\n'
    for i in range(assxa__jeee):
        ojab__ham += '  tmp_v_{} = arr_tup[{}][lo]\n'.format(i, i)
        ojab__ham += '  arr_tup[{}][lo] = arr_tup[{}][hi]\n'.format(i, i)
        ojab__ham += '  arr_tup[{}][hi] = tmp_v_{}\n'.format(i, i)
    ojab__ham += '  return\n'
    epxvp__bvtqs = {}
    exec(ojab__ham, {}, epxvp__bvtqs)
    uvf__nmy = epxvp__bvtqs['f']
    return uvf__nmy


@numba.njit(no_cpython_wrapper=True, cache=True)
def copyRange(src_arr, src_pos, dst_arr, dst_pos, n):
    dst_arr[dst_pos:dst_pos + n] = src_arr[src_pos:src_pos + n]


def copyRange_tup(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):
    for src_arr, dst_arr in zip(src_arr_tup, dst_arr_tup):
        dst_arr[dst_pos:dst_pos + n] = src_arr[src_pos:src_pos + n]


@overload(copyRange_tup, no_unliteral=True)
def copyRange_tup_overload(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):
    assxa__jeee = src_arr_tup.count
    assert assxa__jeee == dst_arr_tup.count
    ojab__ham = 'def f(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):\n'
    for i in range(assxa__jeee):
        ojab__ham += (
            '  copyRange(src_arr_tup[{}], src_pos, dst_arr_tup[{}], dst_pos, n)\n'
            .format(i, i))
    ojab__ham += '  return\n'
    epxvp__bvtqs = {}
    exec(ojab__ham, {'copyRange': copyRange}, epxvp__bvtqs)
    jdbih__uuxw = epxvp__bvtqs['f']
    return jdbih__uuxw


@numba.njit(no_cpython_wrapper=True, cache=True)
def copyElement(src_arr, src_pos, dst_arr, dst_pos):
    dst_arr[dst_pos] = src_arr[src_pos]


def copyElement_tup(src_arr_tup, src_pos, dst_arr_tup, dst_pos):
    for src_arr, dst_arr in zip(src_arr_tup, dst_arr_tup):
        dst_arr[dst_pos] = src_arr[src_pos]


@overload(copyElement_tup, no_unliteral=True)
def copyElement_tup_overload(src_arr_tup, src_pos, dst_arr_tup, dst_pos):
    assxa__jeee = src_arr_tup.count
    assert assxa__jeee == dst_arr_tup.count
    ojab__ham = 'def f(src_arr_tup, src_pos, dst_arr_tup, dst_pos):\n'
    for i in range(assxa__jeee):
        ojab__ham += (
            '  copyElement(src_arr_tup[{}], src_pos, dst_arr_tup[{}], dst_pos)\n'
            .format(i, i))
    ojab__ham += '  return\n'
    epxvp__bvtqs = {}
    exec(ojab__ham, {'copyElement': copyElement}, epxvp__bvtqs)
    jdbih__uuxw = epxvp__bvtqs['f']
    return jdbih__uuxw


def getitem_arr_tup(arr_tup, ind):
    xwlbl__dcp = [arr[ind] for arr in arr_tup]
    return tuple(xwlbl__dcp)


@overload(getitem_arr_tup, no_unliteral=True)
def getitem_arr_tup_overload(arr_tup, ind):
    assxa__jeee = arr_tup.count
    ojab__ham = 'def f(arr_tup, ind):\n'
    ojab__ham += '  return ({}{})\n'.format(','.join(['arr_tup[{}][ind]'.
        format(i) for i in range(assxa__jeee)]), ',' if assxa__jeee == 1 else
        '')
    epxvp__bvtqs = {}
    exec(ojab__ham, {}, epxvp__bvtqs)
    uny__ouqkw = epxvp__bvtqs['f']
    return uny__ouqkw


def setitem_arr_tup(arr_tup, ind, val_tup):
    for arr, yffdu__gujd in zip(arr_tup, val_tup):
        arr[ind] = yffdu__gujd


@overload(setitem_arr_tup, no_unliteral=True)
def setitem_arr_tup_overload(arr_tup, ind, val_tup):
    assxa__jeee = arr_tup.count
    ojab__ham = 'def f(arr_tup, ind, val_tup):\n'
    for i in range(assxa__jeee):
        if isinstance(val_tup, numba.core.types.BaseTuple):
            ojab__ham += '  arr_tup[{}][ind] = val_tup[{}]\n'.format(i, i)
        else:
            assert arr_tup.count == 1
            ojab__ham += '  arr_tup[{}][ind] = val_tup\n'.format(i)
    ojab__ham += '  return\n'
    epxvp__bvtqs = {}
    exec(ojab__ham, {}, epxvp__bvtqs)
    uny__ouqkw = epxvp__bvtqs['f']
    return uny__ouqkw


def test():
    import time
    ktlg__lyza = time.time()
    yckf__vzoh = np.ones(3)
    data = np.arange(3), np.ones(3)
    sort((yckf__vzoh,), 0, 3, data)
    print('compile time', time.time() - ktlg__lyza)
    n = 210000
    np.random.seed(2)
    data = np.arange(n), np.random.ranf(n)
    hcn__lwl = np.random.ranf(n)
    ndvn__qnc = pd.DataFrame({'A': hcn__lwl, 'B': data[0], 'C': data[1]})
    ktlg__lyza = time.time()
    jqadi__stl = ndvn__qnc.sort_values('A', inplace=False)
    tsp__lvlb = time.time()
    sort((hcn__lwl,), 0, n, data)
    print('Bodo', time.time() - tsp__lvlb, 'Numpy', tsp__lvlb - ktlg__lyza)
    np.testing.assert_almost_equal(data[0], jqadi__stl.B.values)
    np.testing.assert_almost_equal(data[1], jqadi__stl.C.values)


if __name__ == '__main__':
    test()
