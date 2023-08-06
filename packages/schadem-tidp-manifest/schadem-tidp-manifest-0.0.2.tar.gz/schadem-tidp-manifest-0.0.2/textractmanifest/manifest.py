from dataclasses import dataclass
import marshmallow as m
import logging
from typing import List

logger = logging.getLogger(__name__)


class BaseSchema(m.Schema):
    """
    skip null values when generating JSON
    https://github.com/marshmallow-code/marshmallow/issues/229#issuecomment-134387999
    """
    SKIP_VALUES = set([None])

    @m.post_dump
    def remove_skip_values(self, data, many, pass_many=False):
        return {
            key: value
            for key, value in data.items()
            if isinstance(value, (dict, list, set, tuple, range,
                                  frozenset)) or value not in self.SKIP_VALUES
        }


@dataclass
class Query():
    text: str
    alias: str
    pages: List[str]


@dataclass
class IDPManifest():
    s3_path: str
    queries_config: List[Query]
    textract_features: List[str]


class QuerySchema(BaseSchema):
    text = m.fields.String(data_key="Text", required=True)
    alias = m.fields.String(data_key="Alias", required=False)
    pages = m.fields.List(m.fields.String, data_key="Pages", required=False)

    @m.post_load
    def make_query(self, data, **kwargs):
        return Query(**data)


class IDPManifestSchema(BaseSchema):
    queries_config = m.fields.List(m.fields.Nested(QuerySchema),
                                   data_key="QueriesConfig",
                                   required="False")
    textract_features = m.fields.List(m.fields.String,
                                      data_key="TextractFeatures",
                                      required=False)
    s3_path = m.fields.String(data_key="S3Path", required=True)

    @m.post_load
    def make_queries_config(self, data, **kwargs):
        return IDPManifest(**data)
