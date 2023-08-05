import pathlib
import os
import boto3.s3.transfer
import tqdm
from typing import Union
from . import utils as djsciops_utils
import collections.abc


def _generate_transfer_mapping(
    session, s3_bucket: str, source: Union[str, list], destination: Union[str, list]
) -> tuple:
    if (
        isinstance(source, list)
        and isinstance(destination, list)
        and len(source) == len(destination)
    ):
        djsciops_utils.log(f"Upload mapping provided.")
        # expect file_paths to be list of Path, object_paths to be list of PurePosixPath
        file_paths, object_paths = (source, destination)
        existing_objects = {
            pathlib.PurePosixPath(op.key)
            for op in session.s3.Bucket(s3_bucket).objects.filter(
                Prefix=os.path.commonprefix(object_paths)
            )
        }
        file_paths, object_paths = tuple(
            zip(
                *(
                    (fp, op)
                    for fp, op in zip(file_paths, object_paths)
                    if op not in existing_objects
                )
            )
        )
        assert file_paths, "All files already exist in object store."
    else:
        # modes: file -> directory, directory -> directory
        assert destination[-1] == "/", "Must point to a directory in object store."
        source = pathlib.Path(source).resolve()
        # recursively list files that are not hidden or directories
        file_paths = {
            fp.relative_to(source)
            for fp in source.rglob("*")
            if not fp.is_dir() and not str(fp.name).startswith(".")
        }
        file_paths = (
            {pathlib.PurePosixPath(_) for _ in file_paths}
            if file_paths
            else {pathlib.PurePosixPath(source.name)}
        )  # if specified a single file
        # recursively list objects
        existing_objects = {
            pathlib.PurePosixPath(op.key.replace(destination, ""))
            for op in session.s3.Bucket(s3_bucket).objects.filter(Prefix=destination)
        }
        # exclude objects that exist and verify that new objects are present
        file_paths = file_paths - existing_objects
        assert file_paths, "All files already exist in object store."
        object_paths = [pathlib.PurePosixPath(destination, fp) for fp in file_paths]
        file_paths = [
            pathlib.Path(source if source.is_dir() else source.parent, fp)
            for fp in file_paths
        ]

    return file_paths, object_paths


def list_files(
    session,
    s3_bucket: str,
    s3_prefix: str,
):
    objects = [
        dict(key=op.key, _size=op.size)
        for op in session.s3.Bucket(s3_bucket).objects.filter(Prefix=s3_prefix)
    ]
    objects = sorted(objects, key=lambda o: o["key"])

    tree = {}
    for o in objects:
        node = tree  # local node
        levels = o["key"].split("/")
        for level in levels:
            node = node.setdefault(level, dict())
            node["_size"] = (
                o["_size"] + node["_size"] if "_size" in node else o["_size"]
            )

    def update(d):
        for k, v in d.items():
            if isinstance(v, collections.abc.Mapping) and len(v) > 1:
                if k != "_size":
                    size = d[k].pop("_size")
                    d[k] = update(d.get(k, {}))
            else:
                d[k] = None
        return d

    return update(tree)


def upload_files(
    session, s3_bucket: str, source: Union[str, list], destination: Union[str, list]
):
    djsciops_utils.log("axon copy", message_type="header")
    file_paths, object_paths = _generate_transfer_mapping(
        session=session, s3_bucket=s3_bucket, source=source, destination=destination
    )
    djsciops_utils.log("Starting upload\n")
    with tqdm.tqdm(
        total=sum(os.stat(fp).st_size for fp in file_paths),
        unit="B",
        unit_scale=True,
        desc="",
    ) as pbar:
        for fp, op in zip(file_paths, object_paths):
            pbar.write(f"{fp}->{op}")
            ## hash metadata
            contents_hash = djsciops_utils.uuid_from_file(fp)
            # djsciops_utils.log(f"contents_hash: {contents_hash.hex}")
            ## upload
            session.s3.Bucket(s3_bucket).upload_file(
                Filename=str(fp),
                Key=str(op),
                Config=boto3.s3.transfer.TransferConfig(
                    multipart_threshold=1024 * 25,
                    max_concurrency=10,
                    multipart_chunksize=1024 * 25,
                    use_threads=True,
                ),
                Callback=lambda bytes_transferred: pbar.update(bytes_transferred),
                ExtraArgs={"Metadata": {"contents_hash": contents_hash.hex}},
            )
