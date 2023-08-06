from typing import Any, Final

import beni
import beni.file as bfile


async def get(key: str, default: Any = None):
    storageFile = _get_storage_file(key)
    if storageFile.is_file():
        return await bfile.read_yaml(storageFile)
    else:
        return default


async def set(key: str, value: Any):
    storageFile = _get_storage_file(key)
    await bfile.write_yaml(storageFile, value)


async def clear(*keyList: str):
    for key in keyList:
        storageFile = _get_storage_file(key)
        beni.remove(storageFile)


async def clear_all():
    for storageFile in beni.list_file(_storage_path):
        beni.remove(storageFile)

# ------------------------------------------------------------------------------------------

_storage_path: Final = beni.getpath_workspace('.storage')


def _get_storage_file(key: str):
    return beni.getpath(_storage_path, f'{key}.yaml')
