from typing import List, Dict
from minder.research_portal_client.models import DatasetFilter
from minder.research_portal_client._utils import RestObject


class _Parameters(RestObject):
    prop_types = {
        "common_observation_columns": "list[str]",
    }

    attribute_map = {
        "common_observation_columns": "commonObservationColumns",
    }

    def __init__(self, common_observation_columns: "List[str]" = None):
        self.common_observation_columns = common_observation_columns


class _DatasetDefinition(RestObject):
    prop_types = {
        "available_columns": "list[str]",
        "available_filters": DatasetFilter,
    }

    attribute_map = {
        "available_columns": "availableColumns",
        "available_filters": "availableFilters",
    }

    def __init__(
        self,
        available_columns: "List[str]" = None,
        available_filters: DatasetFilter = None,
    ):
        self.available_columns = available_columns
        self.available_filters = available_filters


class AvailableDatasetsResponse(RestObject):
    prop_types = {
        "parameters": _Parameters,
        "categories": "dict(str, dict(str, _DatasetDefinition))",
    }

    attribute_map = {
        "parameters": "Parameters",
        "categories": "Categories",
    }

    def __init__(self, parameters: _Parameters = None, categories: "Dict[str, Dict[str, _DatasetDefinition]]" = None):
        self.parameters = parameters
        self.categories = categories
