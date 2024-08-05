import aiofiles
from fastapi import UploadFile

from ad_looper.config import settings


async def write_file(file: UploadFile):
    path = settings.media_folder / str(file.filename)
    async with aiofiles.open(path, "wb") as buffer:
        while True:
            chunk = await file.read(1024)
            if not chunk:
                break
            await buffer.write(chunk)
