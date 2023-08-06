'''
async process module
'''

from cbutil import Path
import asyncio
import aiofile
from typing import *
from .path import *
from .rand import *
from .config import *

__all__ = ['run_cmd_async', 'run_shellscript_async']

async def run_cmd_async(cmd, cwd=None, env=None):
    if cwd is not None:
        Path(cwd).mkdir()
        cwd = str(cwd)

    if env is not None:
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=cwd,
            env=env
        )
    else:
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=cwd,
        )

    stdout, stderr = await proc.communicate()
    return stdout, stderr


async def run_shellscript_async(shellscript: str, tmp_file_path:Path=None, cwd=None, env=None):
    if tmp_file_path is None:
        tmp_file_path = path.make_tmp(suffix='.bat')
    async with aiofile.AIOFile(tmp_file_path, 'w') as fw:
        await fw.write(shellscript)
        
    cmd = tmp_file_path.quote
    return await run_cmd_async(cmd, cwd, env)


    