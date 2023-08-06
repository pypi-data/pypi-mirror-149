import io
import logging
import pathlib
import pprint
from typing import Optional

import urllib3
from minio import Minio, S3Error


logger = logging.getLogger(__name__)


class MinioWrapper(object):

    def __init__(self, url: str, access_key: str, secret_key: str, bucket: str, secure=True):
        self.access_key = access_key
        self.url = url
        self.secret_key = secret_key
        self.secure = secure
        self.bucket = bucket

        self.minio = self._get_minio_interface()


    def upload_binary(self, path: str, data: io.BytesIO, length: int, bucket=None) -> None:
        """
        :param bucket: Optional parameter for which bucket to use, defaults to the value used on object initialization.
        :param path: Path and name of the file you wish to upload.
        :param data: Binary contents of the file you want to upload.
        :param length: Size of the binary data in bytes.
        """
        bucket = bucket or self.bucket
        logger.info(f"Uploading binary data into path {str(path)}!")
        self.minio.put_object(bucket_name=bucket, object_name=str(path), data=data, length=length)
        logger.info(f"Uploaded binary data into path {str(path)}!")


    def upload_file(self, path: str, target_path: str, bucket: Optional[str] = None):
        """
        Function for uploading a file on your filesystem into S3.

        :param target_path: Where in S3 you want to upload your file.
        :param path: Path of the file you want to upload.
        :param bucket: Optional parameter for the bucket you want to use.
        """
        bucket = bucket or self.bucket
        path = pathlib.Path(path)
        if path.exists() is False:
            raise ValueError("File with the given path does not exist!")

        with open(path, "rb") as fp:
            buf = io.BytesIO(fp.read())
            file_length = buf.getbuffer().nbytes
            logger.info(f"Uploading file into path {str(path)}!")
            self.minio.put_object(bucket_name=bucket, object_name=target_path, data=buf, length=file_length)
            logger.info(f"Uploaded file into path {str(path)}!")


    def delete_file(self, path: str, version_id: Optional[str] = None, bucket=None):
        """
        :param path: Which file you want to delete.
        :param version_id: Optional parameter for which version of a file you want to delete.
        :param bucket: Optional parameter for which bucket to look inside in.
        """
        bucket = bucket or self.bucket
        kwargs = {} if version_id is None else {"version_id": version_id}
        try:
            logger.info(f"Deleting file from path {str(path)}!")
            self.minio.remove_object(bucket_name=bucket, object_name=str(path), **kwargs)
            logger.info(f"Deleted file from path {str(path)}!")
        except S3Error as e:
            if e.code == "InvalidArgument":
                raise ValueError("Sent invalid version_id towards Minio!")


    def download_file(self, source_path: str, target_path: str, version_id: Optional[str] = None, bucket: Optional[str] = None):
        bucket = bucket or self.bucket
        kwargs = {} if version_id is None else {"version_id": version_id}
        logger.info(f"Downloading file to path {str(target_path)}!")
        self.minio.fget_object(bucket, object_name=source_path, file_path=target_path, **kwargs)
        logger.info(f"Finished downloading file to path {str(target_path)}!")


    def update_django_model_options(self):
        from pipeline.models import ModelOption
        from django.db.models import Q

        for item in self.get_models():
            model, is_created = ModelOption.objects.get_or_create(name=item["name"])
            model.path = item["path"]
            model.model_type = item["type"]
            model.topic = item["topic"]
            model.lang = item["lang"]
            model.size = item["size"]
            model.last_modified = item["last_modified"]
            model.version = item["version_id"]
            model.is_delete = item["is_delete"]
            model.save()

        # Delete leftovers from ORM that do not exist in Minio anymore.
        model_names = [model["name"] for model in self.get_models()]
        not_in_db = ~Q(name__in=model_names)
        to_delete = ModelOption.objects.filter(not_in_db)
        to_delete.delete()


    def _get_minio_interface(self):
        minio = Minio(
            self.url,
            access_key=self.access_key,
            secret_key=self.secret_key,
            secure=self.secure
        )
        return minio


    def get_models(self, include_version=False, filter_extension: Optional[str] = "zip", recursive: bool = True, bucket: Optional[str] = None, include_full_path=False):
        """
        Function for listing all available files in the given bucket.
        :param include_full_path: Whether to include the full path of the object in S3, important for CI purposes.
        :param include_version: Setting this to true will make the output include all the versions too.
        :param filter_extension: Which extension to use for filtering the results.
        :param recursive: Whether files should be looked up recursively.
        :param bucket: Which bucket to search from, defaults to object initialization settings.
        """
        try:
            bucket = bucket or self.bucket
            objects = self.minio.list_objects(bucket, recursive=recursive, include_version=include_version)
            model_list = []
            for o in objects:
                model_path = pathlib.Path(o.object_name)
                if len(model_path.parts) >= 3:
                    path = str(model_path) if include_full_path else str(model_path.relative_to(*model_path.parts[:1]))
                    model_list.append({
                        "path": path,
                        "name": str(model_path.relative_to(*model_path.parts[:-1])),
                        "type": str(model_path.parts[0]),
                        "topic": str(model_path.parts[1]),
                        "lang": str(model_path.parts[2]),
                        "size": o.size,
                        "version_id": o.version_id,
                        "last_modified": o.last_modified,
                        "is_delete": o.is_delete_marker
                    })
                else:
                    model_list.append({
                        "path": o.object_name,
                        "size": o.size,
                        "version_id": o.version_id,
                        "last_modified": o.last_modified,
                        "is_delete": o.is_delete_marker
                    })

            if filter_extension:
                model_list = [model for model in model_list if model["path"].endswith(filter_extension)]

            return model_list
        except urllib3.exceptions.MaxRetryError:
            logging.error("Could not connect to MINIO, is the configuration set correctly?")
            return []
        except Exception as e:
            # log here
            logging.exception(e)
            return []


if __name__ == '__main__':
    import argparse


    parser = argparse.ArgumentParser(description="CLI wrapper for simple S3 related operations through the Minio client.")
    parser.add_argument("--uri", type=str, required=True, help="URI to access S3.")
    parser.add_argument("--access-key", type=str, required=True, help="Access key for S3.")
    parser.add_argument("--secret-key", type=str, required=True, help="Secret key for S3.")
    parser.add_argument("--bucket", type=str, required=True, help="Which bucket to use inside S3.")

    subparser = parser.add_subparsers(dest="command")

    list_models = subparser.add_parser("list")
    list_models.add_argument("--include-version", default=False, action="store_true", help="Whether to include multiple versions.")
    list_models.add_argument("--filter-extension", type=str, default="zip", help="Filter out objects depending on their extension.")
    list_models.add_argument("--not-recursive", action="store_false", help="Whether to parse bucket recursively.")
    list_models.add_argument("--filter", default=None, required=False, help="Show only objects that have this value in their path")

    upload_model = subparser.add_parser("upload")
    upload_model.add_argument("--source-path", type=str, required=True, help="Path of the file that's to be uploaded.")
    upload_model.add_argument("--target-path", type=str, required=True, help="Path inside S3 where to store the file.")

    download_models = subparser.add_parser("download")
    download_models.add_argument("--source-path", type=str, required=True, help="Where into your filesystem to store the file.")
    download_models.add_argument("--target-path", type=str, required=True, help="Path to the file in S3 to be downloaded.")
    download_models.add_argument("--version-id", default=None, required=False, help="Which specific version of the object to download.")

    delete_models = subparser.add_parser("delete")
    delete_models.add_argument("--path", type=str, required=True, help="Path of the file inside S3 to delete.")
    delete_models.add_argument("--version-id", default=None, required=False, help="Specific version of the object to be deleted.")

    args = parser.parse_args()

    minio = MinioWrapper(args.uri, args.access_key, args.secret_key, args.bucket)
    if args.command == "list":
        models = minio.get_models(args.include_version, args.filter_extension, args.not_recursive, include_full_path=True)
        if args.filter:
            models = [model for model in models if args.filter in model.get("path", "")]

        # Replace datetime print representation with a readable string value.
        for model in models:
            key = "last_modified"
            date = model.get(key, None)
            if date:
                model[key] = str(date)

        pprint.pprint(models)

    if args.command == "upload":
        minio.upload_file(args.source_path, args.target_path)

    if args.command == "delete":
        version_id = args.version_id
        kwargs = {"version_id": version_id} if version_id else {}
        minio.delete_file(args.path, **kwargs)

    if args.command == "download":
        version_id = args.version_id
        kwargs = {"version_id": version_id} if version_id else {}
        minio.download_file(args.source_path, args.target_path)
