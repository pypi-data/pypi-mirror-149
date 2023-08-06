import json
from typing import List, Dict, Any

from algoralabs.common.requests import __delete_request, __get_request, __put_request, __post_request
from algoralabs.data.datasets.models import SchemaRequest, FieldRequest
from algoralabs.data.transformations.response_transformers import no_transform
from algoralabs.decorators.data import data_request


@data_request(transformer=no_transform)
def get_schema(id: str) -> Dict[str, Any]:
    endpoint = f"config/datasets/schema/{id}"
    return __get_request(endpoint)


@data_request(transformer=no_transform)
def get_schemas() -> List[Dict[str, Any]]:
    endpoint = f"config/datasets/schema"
    return __get_request(endpoint)


@data_request(transformer=no_transform)
def get_schema_fields(id: str) -> Dict[str, Any]:
    endpoint = f"config/datasets/schema/{id}/fields"
    return __get_request(endpoint)


@data_request(transformer=no_transform)
def create_schema(request: SchemaRequest) -> Dict[str, Any]:
    endpoint = f"config/datasets/schema"
    return __put_request(endpoint, json=json.loads(request.json()))


@data_request(transformer=no_transform)
def update_schema(id: str, request: SchemaRequest) -> Dict[str, Any]:
    endpoint = f"config/datasets/schema/{id}"
    return __post_request(endpoint, json=json.loads(request.json()))


@data_request(transformer=no_transform)
def update_schema_fields(id: str, request: List[FieldRequest]) -> List[Dict[str, Any]]:
    fields = list(map(lambda f: json.loads(f.json()), request))
    endpoint = f"config/datasets/schema/{id}/fields"
    return __post_request(endpoint, json=fields)


@data_request(transformer=no_transform)
def delete_schema(id: str) -> None:
    endpoint = f"config/datasets/schema/{id}"
    return __delete_request(endpoint)
