from algoralabs.common.requests import __get_request, __put_request, __delete_request
from algoralabs.data.transformations.response_transformers import no_transform
from algoralabs.decorators.data import data_request


@data_request
def get_users():
    return __get_request(endpoint="users", params={"max": 500}, url_key="keycloak")


@data_request(transformer=no_transform)
def get_user(user_id: str):
    return __get_request(endpoint=f"users/{user_id}", url_key="keycloak")


@data_request(transformer=no_transform)
def get_groups():
    return __get_request(endpoint=f"groups", url_key="keycloak")


@data_request(transformer=no_transform)
def get_group_members(id: str):
    return __get_request(endpoint=f"groups/{id}/members", url_key="keycloak")


@data_request(transformer=no_transform, process_response=lambda r: r)
def add_group_to_user(user_id: str, group_id: str):
    return __put_request(endpoint=f"users/{user_id}/groups/{group_id}", url_key="keycloak")


@data_request(transformer=no_transform, process_response=lambda r: r)
def delete_group_from_user(user_id: str, group_id: str):
    return __delete_request(endpoint=f"users/{user_id}/groups/{group_id}", url_key="keycloak")
