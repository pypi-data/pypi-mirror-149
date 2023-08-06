from algoralabs.common.requests import __post_request, __get_request


def query_dataset(id: str, data=None, json=None):
    """
    Query dataset by ID

    Args:
        id: UUID of dataset
        data: (Optional) Data to POST
        json: (Optional) Data to POST

    Returns: HTTP Response Object
    """
    endpoint = f"data/datasets/query/{id}"
    return __post_request(endpoint, data=data, json=json)


# TODO add data query override in URL param
def query_dataset_csv(id: str):
    """
    Query dataset by ID

    Args:
        id: UUID of dataset
        data: (Optional) Data to POST
        json: (Optional) Data to POST

    Returns: HTTP Response Object
    """
    endpoint = f"data/datasets/query/{id}.csv"
    return __get_request(endpoint)
