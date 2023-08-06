import asyncio
import os
import random
import shutil
from contextlib import asynccontextmanager
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Coroutine, TypeVar, cast

Fun = TypeVar("Fun", bound=Callable[..., object])
AsyncFun = TypeVar("AsyncFun", bound=Callable[..., Coroutine[Any, Any, object]])
AnyType = TypeVar("AnyType")


def getpath(path: str | Path, expand: str = ''):
    if type(path) is not Path:
        path = Path(path)
    return path.joinpath(expand).resolve()


def getpath_user(expand: str = ''):
    return getpath(Path('~').expanduser(), expand)


def getpath_workspace(expand: str = ''):
    return getpath_user(f'beni.workspace/{expand}')


def getpath_desktop(expand: str = ''):
    return getpath_user(f'Desktop/{expand}')


def open_windir(dir: Path | str):
    os.system(f'start explorer {dir}')


def remove(path: Path | str):
    if type(path) is not Path:
        path = getpath(path)
    if path.is_file():
        path.unlink(True)
    elif path.is_dir():
        shutil.rmtree(path)


def makedir(path: Path | str):
    if type(path) is not Path:
        path = getpath(path)
    path.mkdir(parents=True, exist_ok=True)


def cleardir(dir: Path):
    for sub in dir.iterdir():
        remove(sub)


def copy(src: Path | str, dst: Path | str):
    if type(src) is not Path:
        src = getpath(src)
    if type(dst) is not Path:
        dst = getpath(dst)
    makedir(dst.parent)
    if src.is_file():
        shutil.copyfile(src, dst)
    elif src.is_dir():
        shutil.copytree(src, dst)
    else:
        if not src.exists():
            raise Exception(f'copy error: src not exists {src}')
        else:
            raise Exception(f'copy error: src not support {src}')


def move(src: Path | str, dst: Path | str, force: bool = False):
    if type(src) is not Path:
        src = getpath(src)
    if type(dst) is not Path:
        dst = getpath(dst)
    if dst.exists():
        if force:
            remove(dst)
        else:
            raise Exception(f'move error: dst exists {dst}')
    makedir(dst.parent)
    os.rename(src, dst)


def json_dumpsmini(value: Any):
    import json
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def list_path(path: Path | str, recursive: bool = False):
    '''获取指定路径下文件以及目录列表'''
    if type(path) is not Path:
        path = getpath(path)
    if recursive:
        return list(path.glob('**/*'))
    else:
        return list(path.glob("*"))


def list_file(path: Path | str, recursive: bool = False):
    '''获取指定路径下文件列表'''
    if type(path) is not Path:
        path = getpath(path)
    if recursive:
        return list(filter(lambda x: x.is_file(), path.glob('**/*')))
    else:
        return list(filter(lambda x: x.is_file(), path.glob('*')))


def list_dir(path: Path | str, recursive: bool = False):
    '''获取指定路径下目录列表'''
    if type(path) is not Path:
        path = getpath(path)
    if recursive:
        return list(filter(lambda x: x.is_dir(), path.glob('**/*')))
    else:
        return list(filter(lambda x: x.is_dir(), path.glob('*')))


def md5bytes(data: bytes):
    import hashlib
    return hashlib.md5(data).hexdigest()


def md5str(content: str):
    return md5bytes(content.encode())


def md5data(data: Any):
    return md5str(
        json_dumpsmini(data)
    )


def crcbytes(data: bytes):
    import binascii
    return hex(binascii.crc32(data))[2:].zfill(8)


def crcstr(content: str):
    return crcbytes(content.encode())


def crcdata(data: Any):
    return crcstr(
        json_dumpsmini(data)
    )


def retry(times: int):
    def fun(func: AsyncFun) -> AsyncFun:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any):
            current = 0
            while True:
                try:
                    return await func(*args, **kwargs)
                except:
                    current += 1
                    if current >= times:
                        raise
        return cast(AsyncFun, wrapper)
    return fun


@asynccontextmanager
async def timeout(timeout: float):
    import async_timeout
    async with async_timeout.timeout(timeout):
        yield


def async_run(coroutine: Coroutine[Any, Any, AnyType]) -> AnyType:
    # 避免出现 RuntimeError: Event loop is closed
    # asyncio.get_event_loop().run_until_complete(coroutine)
    import nest_asyncio
    nest_asyncio.apply()
    return asyncio.run(coroutine)


def hold(msg: str | None = None, password: bool = False, *exitvalue_list: str):
    msg = msg or '测试暂停，输入exit可以退出'
    exitvalue_list = exitvalue_list or ('exit',)
    import getpass
    inputFunc = password and getpass.getpass or input
    while True:
        inputValue = inputFunc(f'{msg}: ')
        if (inputValue in exitvalue_list) or ('*' in exitvalue_list):
            return inputValue


IntFloatStr = TypeVar("IntFloatStr", int, float, str)


def tofloat(value: IntFloatStr, default: float = 0):
    result = default
    try:
        result = float(value)
    except:
        pass
    return result


def toint(value: IntFloatStr, default: int = 0):
    result = default
    try:
        result = int(value)
    except:
        pass
    return result


def getvalue_inside(value: IntFloatStr, minValue: IntFloatStr, maxValue: IntFloatStr):
    '包括最小值和最大值'
    value = min(value, maxValue)
    value = max(value, minValue)
    return value


def init_error_format():
    import pretty_errors
    pretty_errors.configure(
        separator_character='*',
        filename_display=pretty_errors.FILENAME_COMPACT,
        # line_number_first   = True,
        display_link=True,
        lines_before=5,
        lines_after=2,
        line_color=pretty_errors.RED + '> ' + pretty_errors.default_config.line_color,
        code_color='  ' + pretty_errors.default_config.line_color,
        truncate_code=False,
        display_locals=True
    )
    # pretty_errors.blacklist('c:/python')


def go_ahead(msg: str = '确认'):
    code = str(random.randint(1000, 9999))
    hold(f'{msg} [ {code} ]', False, code)


_xPar = '0123456789abcdefghijklmnopqrstuvwxyz'


def xint_tostr(value: int) -> str:
    n = len(_xPar)
    return ((value == 0) and '0') or (xint_tostr(value // n).lstrip('0') + _xPar[value % n])


def xint_fromstr(value: str):
    return int(value, len(_xPar))
