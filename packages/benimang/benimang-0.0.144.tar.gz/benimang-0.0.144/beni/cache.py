import inspect
from functools import wraps
from typing import Any, NamedTuple, cast

import beni


class _CachedResult(NamedTuple):
    par: Any
    result: Any


_cached_func_result: dict[str, dict[Any, list[_CachedResult]]] = {}


def cache(*groupname_list: str):
    groupname_list = groupname_list or ('',)

    def wraperfun(func: beni.AsyncFun) -> beni.AsyncFun:
        @wraps(func)
        async def wraper(*args: Any, **kwargs: Any):
            target_func = inspect.unwrap(func)
            par = [args, kwargs]
            cached_list: list[_CachedResult] = []
            for groupname in groupname_list:
                if groupname not in _cached_func_result:
                    _cached_func_result[groupname] = {}
                if target_func not in _cached_func_result[groupname]:
                    _cached_func_result[groupname][target_func] = cached_list
                else:
                    cached_list = _cached_func_result[groupname][target_func]
            for cached_result in cached_list:
                if cached_result.par == par:
                    return cached_result.result
            result = await func(*args, **kwargs)
            cached_list.append(_CachedResult(par, result))
            return result
        return cast(Any, wraper)
    return wraperfun


def clear(*groupname_list: str):
    groupname_list = groupname_list or ('',)
    clear_cache(*groupname_list)

    def wraperfun(func: beni.AsyncFun) -> beni.AsyncFun:
        @wraps(func)
        async def wraper(*args: Any, **kwargs: Any):
            return await func(*args, **kwargs)
        return cast(Any, wraper)
    return wraperfun


def clear_cache(*func_or_groupname_list: Any):
    for func_or_groupname in func_or_groupname_list:
        if type(func_or_groupname) is str:
            groupname = func_or_groupname
            if groupname in _cached_func_result:
                for cached_list in _cached_func_result[groupname].values():
                    cached_list.clear()
        else:
            func = inspect.unwrap(func_or_groupname)
            for data in _cached_func_result.values():
                for k in data.keys():
                    if k == func:
                        data[k].clear()
