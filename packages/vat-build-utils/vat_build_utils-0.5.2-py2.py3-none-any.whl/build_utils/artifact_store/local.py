import errno
from io import BufferedIOBase, BufferedReader, IOBase
import io
import shutil
import os

import boto3
from botocore.exceptions import ClientError

class LocalArtifactStore(object):
    def __init__(self, config):
        self.path = config['path']

    def has_artifact(self, name, input_hash):
        artifact_path = self._get_artifact_path(name, input_hash)
        return os.path.isfile(artifact_path) or os.path.isdir(artifact_path)

    def get_artifact_location(self, artifact_name: str, input_hash: str):
        artifact_file_path = self._get_artifact_file_path(artifact_name, input_hash)
        return {
            'type': 'local',
            'input_hash': input_hash,
            'path': artifact_file_path
        }

    def store_artifact_file(self, file_path, artifact_name, input_hash, file_name=None):
        base_artifact_path = self._get_artifact_path(artifact_name, input_hash)
        if file_name is not None:
            artifact_path = os.path.join(base_artifact_path, file_name)
        else:
            artifact_path = base_artifact_path

        shutil.copyfile(file_path, artifact_path)

        return {
            'type': 'local',
            'input_hash': input_hash,
            'path': artifact_path
        }

    def store_artifact_fileobj(self, fileobj: BufferedIOBase, artifact_name, input_hash, file_name=None):
        base_artifact_path = self._get_artifact_path(artifact_name, input_hash)
        if file_name is not None:
            artifact_path = os.path.join(base_artifact_path, file_name)
        else:
            artifact_path = base_artifact_path

        artifact_dir_path = os.path.dirname(artifact_path)

        if not os.path.exists(artifact_dir_path):
            try:
                os.makedirs(artifact_dir_path)
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        with open(artifact_path, 'wb') as artifact_fileobj:
            shutil.copyfileobj(fileobj, artifact_fileobj)

        return {
            'type': 'local',
            'input_hash': input_hash,
            'path': artifact_path
        }

    def get_artifact_fileobj(self, artifact_name: str, input_hash: str):
        artifact_file_path = self._get_artifact_file_path(artifact_name, input_hash)

        data = io.BytesIO()
        with open(artifact_file_path, 'rb') as artifact_fileobj:
            shutil.copyfileobj(artifact_fileobj, data)

        data.seek(0)
        return data

    def _get_artifact_path(self, artifact_name, input_hash):
        return os.path.join(self.path, artifact_name, input_hash)

    def _get_artifact_file_path(self, artifact_name, input_hash):
        artifact_path = self._get_artifact_path(artifact_name, input_hash)

        if os.path.isfile(artifact_path):
            return artifact_path
        else:
            artifact_dir_contents = os.listdir(artifact_path)
            if len(artifact_dir_contents) != 1:
                raise RuntimeError("The artifact path ({}) must contain exatly one file".format(artifact_path))

            artifact_file_path = os.path.join(artifact_path, artifact_dir_contents[0])

            if not os.path.isfile(artifact_file_path):
                raise RuntimeError("The artifact path ({}) must contain exatly one file".format(artifact_path))

            return artifact_file_path
