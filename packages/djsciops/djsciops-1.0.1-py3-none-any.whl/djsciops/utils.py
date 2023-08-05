import time
import hashlib
import uuid
import io
from pathlib import Path


def log(message: str, pause_duration: int = 0, message_type: str = "message"):
    if message_type == "message":
        print(f"\n -> {message}", flush=True)
    elif message_type == "header":
        print(f"\n=== {message.upper()} ===", flush=True)
    if pause_duration:
        time.sleep(pause_duration)


def uuid_from_stream(stream, *, init_string=""):
    """
    :return: 16-byte digest of stream data
    :stream: stream object or open file handle
    :init_string: string to initialize the checksum
    """
    hashed = hashlib.md5(init_string.encode())
    chunk = True
    chunk_size = 1 << 14
    while chunk:
        chunk = stream.read(chunk_size)
        hashed.update(chunk)
    return uuid.UUID(bytes=hashed.digest())


def uuid_from_buffer(buffer=b"", *, init_string=""):
    return uuid_from_stream(io.BytesIO(buffer), init_string=init_string)


def uuid_from_file(filepath, *, init_string=""):
    return uuid_from_stream(Path(filepath).open("rb"), init_string=init_string)
