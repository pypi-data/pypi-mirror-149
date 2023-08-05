import io, os
from typing import Optional, Union, List
from datetime import datetime

import numpy as np
from dataclasses import dataclass

from ..constants import AssetsConstants
from ..custom_exceptions import EmbeddingError
from ..models.annotation import Annotation
from ..tools.misc import get_md5_from_json_object, hash_string_into_positive_integer_reproducible, get_md5_from_string, get_guid
from ..tools.naming import get_similarity_index_name


@dataclass(frozen=False)
class UnstructuredInputAsset:
    id: Optional[str] = None
    path: Optional[str] = None
    url: Optional[str] = None
    uri: Optional[str] = None
    bytes: Optional[Union[io.BytesIO, bytes, str]] = None
    sensor: Optional[str] = None
    timestamp: Optional[Union[str, datetime]] = None
    session_uid: Optional[str] = None
    aux_metadata: Optional[dict] = None

    def __post_init__(self):
        # Validate inputs
        assert sum(x is not None for x in [self.path, self.url, self.uri, self.bytes]) == 1, \
            "One and only one of [path, url, uri, bytes] should be specified"

        if self.id is None:
            if self.bytes:
                self.id = get_guid()
            else:
                self.id = get_md5_from_string(self.path or self.url or self.uri)

        assert isinstance(self.id, str), "asset id should be a string"

        if self.timestamp is None:
            self.timestamp = datetime.utcnow()

        if self.path:
            assert os.path.exists(self.path), f"path {self.path} does not exist"


class Image(UnstructuredInputAsset):
    annotations: Optional[List[Annotation]] = None

    def __post_init__(self):
        super(Image, self).__post_init__()
        if self.annotations:
            for annotation in self.annotations:
                assert annotation.media_type == AssetsConstants.IMAGES_ASSET_ID


class Video(UnstructuredInputAsset):
    annotations: Optional[List[Annotation]] = None

    def __post_init__(self):
        super(Video, self).__post_init__()
        if self.annotations:
            for annotation in self.annotations:
                assert annotation.media_type == AssetsConstants.VIDEOS_ASSET_ID


class Lidar(UnstructuredInputAsset):
    pass


class Embedding(object):
    def __init__(self,
                 data: Union[io.BytesIO, bytes, np.array, List[float]],
                 model: str,
                 version: str,
                 asset_id: str,
                 asset_type: str,
                 set_ids: Optional[Union[str, List[str]]] = None,
                 layer: Optional[Union[int, str]] = None,
                 dtype: Optional[Union[type(np.float32), type(np.float64), type(float)]] = np.float32,
                 ndim: Optional[int] = None,
                 ):
        """Create an Embedding.

            Parameters
            ----------
            data:
                Embeddings data.
            model:
                The name of the embeddings model.  Helps to differentiate from other models.
            version:
                The version of the embeddings model.  Helps to differentiate several versions of the same model.
            asset_id:
                The asset ID associated with the embedding passed in `data`. Must refer to an asset ID available on
                SceneBox.
            asset_type:
                The type of the asset referred to in `asset_id`.  Currently, only images and objects are supported.
            set_ids:
                Any associated set_ids with the embedding.
            layer:
                Layer associated with the embedding.
            dtype:
                The datatype of the embedding.  Helps to cast data.  If not listed, assumed to be `np.float32`.
            ndim:
                Number of dimensions in `data`.  Helps to assert that the dimension calculated by
                the platform is correct.  Raises an error of the calculated dimensions does not match this field.
        """

        if not isinstance(data, io.BytesIO) and not isinstance(data, bytes):
            raise NotImplementedError("Currently only embedding bytes are supported")

        # Enforce a cast to float32
        embedding_array = np.float32(np.frombuffer(data, dtype=dtype))
        self.ndim = embedding_array.reshape(1, -1).shape[1]

        if ndim and self.ndim != ndim:
            raise EmbeddingError("ndim passed {} does not match the ndim in data {}".format(ndim, self.ndim))

        self.sets = []
        if set_ids:
            if isinstance(set_ids, str):
                self.sets = [set_ids]
            elif isinstance(set_ids, list):
                self.sets = set_ids

        self.bytes = embedding_array.tobytes()
        self.timestamp = datetime.utcnow()
        self.asset_id = asset_id
        self.asset_type = asset_type
        self.model = model
        self.version = version
        self.layer = layer

        json_object_for_embedding_id = {
            'model': self.model,
            'version': self.version,
            'asset_id': self.asset_id,
            'ndim': self.ndim,
            'layer': self.layer}

        embeddings_hash = get_md5_from_json_object(
            json_object=json_object_for_embedding_id)

        self.id = str(
            hash_string_into_positive_integer_reproducible(embeddings_hash))
        self.metadata = {
                'id': self.id,
                'timestamp': self.timestamp,
                'sets': self.sets,
                'tags': [self.layer] if self.layer else [],
                'media_type': self.asset_type,
                'asset_id': self.asset_id,
                'model': self.model,
                'version': self.version,
                'ndim': self.ndim,
                'index_name': get_similarity_index_name(
                    media_type=self.asset_type,
                    model=self.model,
                    version=self.version)}
