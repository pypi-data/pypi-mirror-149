
import io
import posixpath

import boto3
from botocore.exceptions import ClientError

from build_utils.artifact_store.base import BaseArtifactStore

class S3ArtifactStore(BaseArtifactStore):
    def __init__(self, config):
        self.bucket = config['bucket']
        self.prefix = config['prefix']

    def has_artifact(self, name: str, input_hash: str):
        artifact_file_key = self._try_get_artifact_file_key(name, input_hash)
        return artifact_file_key is not None

    def get_artifact_location(self, name, input_hash):
        return {
            'type': 's3',
            'input_hash': input_hash,
            'bucket': self.bucket,
            'key': self._get_artifact_file_key(name, input_hash)
        }

    def store_artifact_file(self, file_path, artifact_name, input_hash, file_name=None):
        artifact_key = self._get_artifact_key(artifact_name, input_hash)
        if file_name is not None:
            artifact_file_key = posixpath.join(artifact_key, file_name)
        else:
            artifact_file_key = artifact_key

        s3_client = boto3.client('s3')
        s3_client.upload_file(file_path, self.bucket, artifact_file_key)

        return {
            'type': 's3',
            'input_hash': input_hash,
            'bucket': self.bucket,
            'key': artifact_file_key
        }

    def store_artifact_fileobj(self, fileobj, artifact_name, input_hash, file_name=None):
        artifact_key = self._get_artifact_key(artifact_name, input_hash)
        if file_name is not None:
            artifact_file_key = posixpath.join(artifact_key, file_name)
        else:
            artifact_file_key = artifact_key

        s3_client = boto3.client('s3')
        s3_client.upload_fileobj(fileobj, self.bucket, artifact_file_key)

        return {
            'type': 's3',
            'input_hash': input_hash,
            'bucket': self.bucket,
            'key': artifact_file_key
        }

    def get_artifact_fileobj(self, artifact_name: str, input_hash: str):
        artifact_file_key = self._get_artifact_file_key(artifact_name, input_hash)

        s3_client = boto3.resource('s3')

        data = io.BytesIO()
        s3_client.download_fileobj(self.bucket, artifact_file_key, data)
        data.seek(0)
        return data

    def _get_artifact_key(self, artifact_name, input_hash):
        return posixpath.join(self.prefix, artifact_name, input_hash)

    def _try_get_artifact_file_key(self, artifact_name, input_hash):
        s3 = boto3.client('s3')

        artifact_key = self._get_artifact_key(artifact_name, input_hash)

        list_objects_response = s3.list_objects_v2(
            Bucket=self.bucket,
            Prefix=artifact_key
        )

        object_keys = [x["Key"] for x in list_objects_response.get("Contents", [])]

        dir_prefix = posixpath.join(artifact_key, "")
        dir_prefix_keys = [x for x in object_keys if x.startswith(dir_prefix)]

        if artifact_key in object_keys:
            return artifact_key

        elif dir_prefix_keys:
            if len(dir_prefix_keys) != 1:
                raise RuntimeError(
                    "Expected the prefix path ({}) to contain exactly one file, got keys {}".format(
                        dir_prefix, dir_prefix_keys
                    )
                )

            return dir_prefix_keys[0]

        else:
            return None

    def _get_artifact_file_key(self, artifact_name, input_hash):
        artifact_file_key = self._try_get_artifact_file_key(artifact_name, input_hash)
        if artifact_file_key is None:
            raise ValueError("The artifact with the given input hash does not exist")

        return artifact_file_key
