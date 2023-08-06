from typing import List
from minder.research_portal_client._utils import RestObject


class _Organization(RestObject):
    prop_types = {
        "id": str,
        "name": str,
    }

    attribute_map = {
        "id": "id",
        "name": "name",
    }

    def __init__(self, id: str = None, name: str = None):
        self.id = id
        self.name = name


class OrganizationsResponse(RestObject):
    prop_types = {
        "organizations": "list[_Organization]",
    }

    attribute_map = {
        "organizations": "organizations",
    }

    def __init__(self, organizations: "List[_Organization]" = None):
        self.organizations = organizations
