import numpy as np
import pandas as pd
import numba
from numba.extending import overload
from bodo.utils.utils import alloc_arr_tup
MIN_MERGE = 32


@numba.njit(no_cpython_wrapper=True, cache=True)
def sort(key_arrs, lo, hi, data):
    vdmdc__eyayc = hi - lo
    if vdmdc__eyayc < 2:
        return
    if vdmdc__eyayc < MIN_MERGE:
        mwaq__ino = countRunAndMakeAscending(key_arrs, lo, hi, data)
        binarySort(key_arrs, lo, hi, lo + mwaq__ino, data)
        return
    stackSize, runBase, runLen, tmpLength, tmp, tmp_data, minGallop = (
        init_sort_start(key_arrs, data))
    rgnej__yvfoh = minRunLength(vdmdc__eyayc)
    while True:
        jtik__jko = countRunAndMakeAscending(key_arrs, lo, hi, data)
        if jtik__jko < rgnej__yvfoh:
            zfja__cjgek = (vdmdc__eyayc if vdmdc__eyayc <= rgnej__yvfoh else
                rgnej__yvfoh)
            binarySort(key_arrs, lo, lo + zfja__cjgek, lo + jtik__jko, data)
            jtik__jko = zfja__cjgek
        stackSize = pushRun(stackSize, runBase, runLen, lo, jtik__jko)
        stackSize, tmpLength, tmp, tmp_data, minGallop = mergeCollapse(
            stackSize, runBase, runLen, key_arrs, data, tmpLength, tmp,
            tmp_data, minGallop)
        lo += jtik__jko
        vdmdc__eyayc -= jtik__jko
        if vdmdc__eyayc == 0:
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
        eatro__gvtp = getitem_arr_tup(key_arrs, start)
        aii__tggnq = getitem_arr_tup(data, start)
        zjf__ory = lo
        mdad__ppi = start
        assert zjf__ory <= mdad__ppi
        while zjf__ory < mdad__ppi:
            ritcy__oap = zjf__ory + mdad__ppi >> 1
            if eatro__gvtp < getitem_arr_tup(key_arrs, ritcy__oap):
                mdad__ppi = ritcy__oap
            else:
                zjf__ory = ritcy__oap + 1
        assert zjf__ory == mdad__ppi
        n = start - zjf__ory
        copyRange_tup(key_arrs, zjf__ory, key_arrs, zjf__ory + 1, n)
        copyRange_tup(data, zjf__ory, data, zjf__ory + 1, n)
        setitem_arr_tup(key_arrs, zjf__ory, eatro__gvtp)
        setitem_arr_tup(data, zjf__ory, aii__tggnq)
        start += 1


@numba.njit(no_cpython_wrapper=True, cache=True)
def countRunAndMakeAscending(key_arrs, lo, hi, data):
    assert lo < hi
    qlih__fdr = lo + 1
    if qlih__fdr == hi:
        return 1
    if getitem_arr_tup(key_arrs, qlih__fdr) < getitem_arr_tup(key_arrs, lo):
        qlih__fdr += 1
        while qlih__fdr < hi and getitem_arr_tup(key_arrs, qlih__fdr
            ) < getitem_arr_tup(key_arrs, qlih__fdr - 1):
            qlih__fdr += 1
        reverseRange(key_arrs, lo, qlih__fdr, data)
    else:
        qlih__fdr += 1
        while qlih__fdr < hi and getitem_arr_tup(key_arrs, qlih__fdr
            ) >= getitem_arr_tup(key_arrs, qlih__fdr - 1):
            qlih__fdr += 1
    return qlih__fdr - lo


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
    miclk__vopu = 0
    while n >= MIN_MERGE:
        miclk__vopu |= n & 1
        n >>= 1
    return n + miclk__vopu


MIN_GALLOP = 7
INITIAL_TMP_STORAGE_LENGTH = 256


@numba.njit(no_cpython_wrapper=True, cache=True)
def init_sort_start(key_arrs, data):
    minGallop = MIN_GALLOP
    hvyfl__aarg = len(key_arrs[0])
    tmpLength = (hvyfl__aarg >> 1 if hvyfl__aarg < 2 *
        INITIAL_TMP_STORAGE_LENGTH else INITIAL_TMP_STORAGE_LENGTH)
    tmp = alloc_arr_tup(tmpLength, key_arrs)
    tmp_data = alloc_arr_tup(tmpLength, data)
    stackSize = 0
    oss__aco = (5 if hvyfl__aarg < 120 else 10 if hvyfl__aarg < 1542 else 
        19 if hvyfl__aarg < 119151 else 40)
    runBase = np.empty(oss__aco, np.int64)
    runLen = np.empty(oss__aco, np.int64)
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
    nmz__fbqv = gallopRight(getitem_arr_tup(key_arrs, base2), key_arrs,
        base1, len1, 0)
    assert nmz__fbqv >= 0
    base1 += nmz__fbqv
    len1 -= nmz__fbqv
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
    fut__bjzgu = 0
    wguao__vyg = 1
    if key > getitem_arr_tup(arr, base + hint):
        eppz__rqcu = _len - hint
        while wguao__vyg < eppz__rqcu and key > getitem_arr_tup(arr, base +
            hint + wguao__vyg):
            fut__bjzgu = wguao__vyg
            wguao__vyg = (wguao__vyg << 1) + 1
            if wguao__vyg <= 0:
                wguao__vyg = eppz__rqcu
        if wguao__vyg > eppz__rqcu:
            wguao__vyg = eppz__rqcu
        fut__bjzgu += hint
        wguao__vyg += hint
    else:
        eppz__rqcu = hint + 1
        while wguao__vyg < eppz__rqcu and key <= getitem_arr_tup(arr, base +
            hint - wguao__vyg):
            fut__bjzgu = wguao__vyg
            wguao__vyg = (wguao__vyg << 1) + 1
            if wguao__vyg <= 0:
                wguao__vyg = eppz__rqcu
        if wguao__vyg > eppz__rqcu:
            wguao__vyg = eppz__rqcu
        tmp = fut__bjzgu
        fut__bjzgu = hint - wguao__vyg
        wguao__vyg = hint - tmp
    assert -1 <= fut__bjzgu and fut__bjzgu < wguao__vyg and wguao__vyg <= _len
    fut__bjzgu += 1
    while fut__bjzgu < wguao__vyg:
        uqcii__pqpz = fut__bjzgu + (wguao__vyg - fut__bjzgu >> 1)
        if key > getitem_arr_tup(arr, base + uqcii__pqpz):
            fut__bjzgu = uqcii__pqpz + 1
        else:
            wguao__vyg = uqcii__pqpz
    assert fut__bjzgu == wguao__vyg
    return wguao__vyg


@numba.njit(no_cpython_wrapper=True, cache=True)
def gallopRight(key, arr, base, _len, hint):
    assert _len > 0 and hint >= 0 and hint < _len
    wguao__vyg = 1
    fut__bjzgu = 0
    if key < getitem_arr_tup(arr, base + hint):
        eppz__rqcu = hint + 1
        while wguao__vyg < eppz__rqcu and key < getitem_arr_tup(arr, base +
            hint - wguao__vyg):
            fut__bjzgu = wguao__vyg
            wguao__vyg = (wguao__vyg << 1) + 1
            if wguao__vyg <= 0:
                wguao__vyg = eppz__rqcu
        if wguao__vyg > eppz__rqcu:
            wguao__vyg = eppz__rqcu
        tmp = fut__bjzgu
        fut__bjzgu = hint - wguao__vyg
        wguao__vyg = hint - tmp
    else:
        eppz__rqcu = _len - hint
        while wguao__vyg < eppz__rqcu and key >= getitem_arr_tup(arr, base +
            hint + wguao__vyg):
            fut__bjzgu = wguao__vyg
            wguao__vyg = (wguao__vyg << 1) + 1
            if wguao__vyg <= 0:
                wguao__vyg = eppz__rqcu
        if wguao__vyg > eppz__rqcu:
            wguao__vyg = eppz__rqcu
        fut__bjzgu += hint
        wguao__vyg += hint
    assert -1 <= fut__bjzgu and fut__bjzgu < wguao__vyg and wguao__vyg <= _len
    fut__bjzgu += 1
    while fut__bjzgu < wguao__vyg:
        uqcii__pqpz = fut__bjzgu + (wguao__vyg - fut__bjzgu >> 1)
        if key < getitem_arr_tup(arr, base + uqcii__pqpz):
            wguao__vyg = uqcii__pqpz
        else:
            fut__bjzgu = uqcii__pqpz + 1
    assert fut__bjzgu == wguao__vyg
    return wguao__vyg


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
        wymc__syxg = 0
        vzias__dbidy = 0
        while True:
            assert len1 > 1 and len2 > 0
            if getitem_arr_tup(arr, cursor2) < getitem_arr_tup(tmp, cursor1):
                copyElement_tup(arr, cursor2, arr, dest)
                copyElement_tup(arr_data, cursor2, arr_data, dest)
                cursor2 += 1
                dest += 1
                vzias__dbidy += 1
                wymc__syxg = 0
                len2 -= 1
                if len2 == 0:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            else:
                copyElement_tup(tmp, cursor1, arr, dest)
                copyElement_tup(tmp_data, cursor1, arr_data, dest)
                cursor1 += 1
                dest += 1
                wymc__syxg += 1
                vzias__dbidy = 0
                len1 -= 1
                if len1 == 1:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            if not wymc__syxg | vzias__dbidy < minGallop:
                break
        while True:
            assert len1 > 1 and len2 > 0
            wymc__syxg = gallopRight(getitem_arr_tup(arr, cursor2), tmp,
                cursor1, len1, 0)
            if wymc__syxg != 0:
                copyRange_tup(tmp, cursor1, arr, dest, wymc__syxg)
                copyRange_tup(tmp_data, cursor1, arr_data, dest, wymc__syxg)
                dest += wymc__syxg
                cursor1 += wymc__syxg
                len1 -= wymc__syxg
                if len1 <= 1:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            copyElement_tup(arr, cursor2, arr, dest)
            copyElement_tup(arr_data, cursor2, arr_data, dest)
            cursor2 += 1
            dest += 1
            len2 -= 1
            if len2 == 0:
                return len1, len2, cursor1, cursor2, dest, minGallop
            vzias__dbidy = gallopLeft(getitem_arr_tup(tmp, cursor1), arr,
                cursor2, len2, 0)
            if vzias__dbidy != 0:
                copyRange_tup(arr, cursor2, arr, dest, vzias__dbidy)
                copyRange_tup(arr_data, cursor2, arr_data, dest, vzias__dbidy)
                dest += vzias__dbidy
                cursor2 += vzias__dbidy
                len2 -= vzias__dbidy
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
            if not wymc__syxg >= MIN_GALLOP | vzias__dbidy >= MIN_GALLOP:
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
        wymc__syxg = 0
        vzias__dbidy = 0
        while True:
            assert len1 > 0 and len2 > 1
            if getitem_arr_tup(tmp, cursor2) < getitem_arr_tup(arr, cursor1):
                copyElement_tup(arr, cursor1, arr, dest)
                copyElement_tup(arr_data, cursor1, arr_data, dest)
                cursor1 -= 1
                dest -= 1
                wymc__syxg += 1
                vzias__dbidy = 0
                len1 -= 1
                if len1 == 0:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            else:
                copyElement_tup(tmp, cursor2, arr, dest)
                copyElement_tup(tmp_data, cursor2, arr_data, dest)
                cursor2 -= 1
                dest -= 1
                vzias__dbidy += 1
                wymc__syxg = 0
                len2 -= 1
                if len2 == 1:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            if not wymc__syxg | vzias__dbidy < minGallop:
                break
        while True:
            assert len1 > 0 and len2 > 1
            wymc__syxg = len1 - gallopRight(getitem_arr_tup(tmp, cursor2),
                arr, base1, len1, len1 - 1)
            if wymc__syxg != 0:
                dest -= wymc__syxg
                cursor1 -= wymc__syxg
                len1 -= wymc__syxg
                copyRange_tup(arr, cursor1 + 1, arr, dest + 1, wymc__syxg)
                copyRange_tup(arr_data, cursor1 + 1, arr_data, dest + 1,
                    wymc__syxg)
                if len1 == 0:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            copyElement_tup(tmp, cursor2, arr, dest)
            copyElement_tup(tmp_data, cursor2, arr_data, dest)
            cursor2 -= 1
            dest -= 1
            len2 -= 1
            if len2 == 1:
                return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            vzias__dbidy = len2 - gallopLeft(getitem_arr_tup(arr, cursor1),
                tmp, 0, len2, len2 - 1)
            if vzias__dbidy != 0:
                dest -= vzias__dbidy
                cursor2 -= vzias__dbidy
                len2 -= vzias__dbidy
                copyRange_tup(tmp, cursor2 + 1, arr, dest + 1, vzias__dbidy)
                copyRange_tup(tmp_data, cursor2 + 1, arr_data, dest + 1,
                    vzias__dbidy)
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
            if not wymc__syxg >= MIN_GALLOP | vzias__dbidy >= MIN_GALLOP:
                break
        if minGallop < 0:
            minGallop = 0
        minGallop += 2
    return len1, len2, tmp, cursor1, cursor2, dest, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def ensureCapacity(tmpLength, tmp, tmp_data, key_arrs, data, minCapacity):
    zqin__afki = len(key_arrs[0])
    if tmpLength < minCapacity:
        dmahz__mjdlk = minCapacity
        dmahz__mjdlk |= dmahz__mjdlk >> 1
        dmahz__mjdlk |= dmahz__mjdlk >> 2
        dmahz__mjdlk |= dmahz__mjdlk >> 4
        dmahz__mjdlk |= dmahz__mjdlk >> 8
        dmahz__mjdlk |= dmahz__mjdlk >> 16
        dmahz__mjdlk += 1
        if dmahz__mjdlk < 0:
            dmahz__mjdlk = minCapacity
        else:
            dmahz__mjdlk = min(dmahz__mjdlk, zqin__afki >> 1)
        tmp = alloc_arr_tup(dmahz__mjdlk, key_arrs)
        tmp_data = alloc_arr_tup(dmahz__mjdlk, data)
        tmpLength = dmahz__mjdlk
    return tmpLength, tmp, tmp_data


def swap_arrs(data, lo, hi):
    for arr in data:
        swwre__txl = arr[lo]
        arr[lo] = arr[hi]
        arr[hi] = swwre__txl


@overload(swap_arrs, no_unliteral=True)
def swap_arrs_overload(arr_tup, lo, hi):
    adas__epaew = arr_tup.count
    wyddr__mpj = 'def f(arr_tup, lo, hi):\n'
    for i in range(adas__epaew):
        wyddr__mpj += '  tmp_v_{} = arr_tup[{}][lo]\n'.format(i, i)
        wyddr__mpj += '  arr_tup[{}][lo] = arr_tup[{}][hi]\n'.format(i, i)
        wyddr__mpj += '  arr_tup[{}][hi] = tmp_v_{}\n'.format(i, i)
    wyddr__mpj += '  return\n'
    pyuwl__lybs = {}
    exec(wyddr__mpj, {}, pyuwl__lybs)
    yvdxg__yutpr = pyuwl__lybs['f']
    return yvdxg__yutpr


@numba.njit(no_cpython_wrapper=True, cache=True)
def copyRange(src_arr, src_pos, dst_arr, dst_pos, n):
    dst_arr[dst_pos:dst_pos + n] = src_arr[src_pos:src_pos + n]


def copyRange_tup(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):
    for src_arr, dst_arr in zip(src_arr_tup, dst_arr_tup):
        dst_arr[dst_pos:dst_pos + n] = src_arr[src_pos:src_pos + n]


@overload(copyRange_tup, no_unliteral=True)
def copyRange_tup_overload(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):
    adas__epaew = src_arr_tup.count
    assert adas__epaew == dst_arr_tup.count
    wyddr__mpj = 'def f(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):\n'
    for i in range(adas__epaew):
        wyddr__mpj += (
            '  copyRange(src_arr_tup[{}], src_pos, dst_arr_tup[{}], dst_pos, n)\n'
            .format(i, i))
    wyddr__mpj += '  return\n'
    pyuwl__lybs = {}
    exec(wyddr__mpj, {'copyRange': copyRange}, pyuwl__lybs)
    scwsj__bun = pyuwl__lybs['f']
    return scwsj__bun


@numba.njit(no_cpython_wrapper=True, cache=True)
def copyElement(src_arr, src_pos, dst_arr, dst_pos):
    dst_arr[dst_pos] = src_arr[src_pos]


def copyElement_tup(src_arr_tup, src_pos, dst_arr_tup, dst_pos):
    for src_arr, dst_arr in zip(src_arr_tup, dst_arr_tup):
        dst_arr[dst_pos] = src_arr[src_pos]


@overload(copyElement_tup, no_unliteral=True)
def copyElement_tup_overload(src_arr_tup, src_pos, dst_arr_tup, dst_pos):
    adas__epaew = src_arr_tup.count
    assert adas__epaew == dst_arr_tup.count
    wyddr__mpj = 'def f(src_arr_tup, src_pos, dst_arr_tup, dst_pos):\n'
    for i in range(adas__epaew):
        wyddr__mpj += (
            '  copyElement(src_arr_tup[{}], src_pos, dst_arr_tup[{}], dst_pos)\n'
            .format(i, i))
    wyddr__mpj += '  return\n'
    pyuwl__lybs = {}
    exec(wyddr__mpj, {'copyElement': copyElement}, pyuwl__lybs)
    scwsj__bun = pyuwl__lybs['f']
    return scwsj__bun


def getitem_arr_tup(arr_tup, ind):
    ufg__ltmsu = [arr[ind] for arr in arr_tup]
    return tuple(ufg__ltmsu)


@overload(getitem_arr_tup, no_unliteral=True)
def getitem_arr_tup_overload(arr_tup, ind):
    adas__epaew = arr_tup.count
    wyddr__mpj = 'def f(arr_tup, ind):\n'
    wyddr__mpj += '  return ({}{})\n'.format(','.join(['arr_tup[{}][ind]'.
        format(i) for i in range(adas__epaew)]), ',' if adas__epaew == 1 else
        '')
    pyuwl__lybs = {}
    exec(wyddr__mpj, {}, pyuwl__lybs)
    cyce__wzawb = pyuwl__lybs['f']
    return cyce__wzawb


def setitem_arr_tup(arr_tup, ind, val_tup):
    for arr, xsjyo__bim in zip(arr_tup, val_tup):
        arr[ind] = xsjyo__bim


@overload(setitem_arr_tup, no_unliteral=True)
def setitem_arr_tup_overload(arr_tup, ind, val_tup):
    adas__epaew = arr_tup.count
    wyddr__mpj = 'def f(arr_tup, ind, val_tup):\n'
    for i in range(adas__epaew):
        if isinstance(val_tup, numba.core.types.BaseTuple):
            wyddr__mpj += '  arr_tup[{}][ind] = val_tup[{}]\n'.format(i, i)
        else:
            assert arr_tup.count == 1
            wyddr__mpj += '  arr_tup[{}][ind] = val_tup\n'.format(i)
    wyddr__mpj += '  return\n'
    pyuwl__lybs = {}
    exec(wyddr__mpj, {}, pyuwl__lybs)
    cyce__wzawb = pyuwl__lybs['f']
    return cyce__wzawb


def test():
    import time
    zbk__fmqlt = time.time()
    bvdg__arz = np.ones(3)
    data = np.arange(3), np.ones(3)
    sort((bvdg__arz,), 0, 3, data)
    print('compile time', time.time() - zbk__fmqlt)
    n = 210000
    np.random.seed(2)
    data = np.arange(n), np.random.ranf(n)
    mmx__semo = np.random.ranf(n)
    lfb__yhxfp = pd.DataFrame({'A': mmx__semo, 'B': data[0], 'C': data[1]})
    zbk__fmqlt = time.time()
    awsi__dli = lfb__yhxfp.sort_values('A', inplace=False)
    khrxm__tnmm = time.time()
    sort((mmx__semo,), 0, n, data)
    print('Bodo', time.time() - khrxm__tnmm, 'Numpy', khrxm__tnmm - zbk__fmqlt)
    np.testing.assert_almost_equal(data[0], awsi__dli.B.values)
    np.testing.assert_almost_equal(data[1], awsi__dli.C.values)


if __name__ == '__main__':
    test()
