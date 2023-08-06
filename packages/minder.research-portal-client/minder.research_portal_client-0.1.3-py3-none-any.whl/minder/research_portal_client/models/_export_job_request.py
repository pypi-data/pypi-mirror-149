from abc import ABC
from typing import List, Dict
from datetime import datetime
from minder.research_portal_client._utils import RestObject


class DatasetFilter(RestObject, ABC):
    @classmethod
    def get_real_child_model(cls, data):
        if not isinstance(data, dict):
            return None

        if "value" in data:
            return DatasetValueFilter

        if "dataset" in data:
            return DatasetSourceFilter

        return None


class ExportJobRequestDataset(RestObject):
    prop_types = {
        "columns": "list[str]",
        "filter": DatasetFilter,
    }

    attribute_map = {
        "columns": "columns",
        "filter": "filter",
    }

    def __init__(self, columns: "List[str]" = None, filter: DatasetFilter = None):
        if columns is not None:
            self.columns = columns

        if filter is not None:
            self.filter = filter


class ExportJobRequest(RestObject):
    prop_types = {
        "since": datetime,
        "until": datetime,
        "common_observation_columns": "list[str]",
        "omit_units": bool,
        "datasets": "dict(str, ExportJobRequestDataset)",
        "organizations": "list[str]",
    }

    attribute_map = {
        "since": "since",
        "until": "until",
        "common_observation_columns": "commonObservationColumns",
        "omit_units": "omitUnits",
        "datasets": "datasets",
        "organizations": "organizations",
    }

    def __init__(
        self,
        since: datetime = None,
        until: datetime = None,
        common_observation_columns: "List[str]" = None,
        omit_units: bool = None,
        datasets: Dict[str, ExportJobRequestDataset] = None,
        organizations=None,
    ):
        if since is not None:
            self.since = since

        if until is not None:
            self.until = until

        if common_observation_columns is not None:
            self.common_observation_columns = common_observation_columns

        if omit_units is not None:
            self.omit_units = omit_units

        self.datasets = datasets if datasets is not None else {}

        if organizations is not None:
            self.organizations = organizations


class DatasetValueFilter(DatasetFilter):
    prop_types = {
        "value": "list[str]",
    }

    attribute_map = {
        "value": "value",
    }

    def __init__(self, value: "List[str]"):
        self.value = value


class DatasetSourceFilter(DatasetFilter):
    prop_types = {
        "dataset": "list[str]",
    }

    attribute_map = {
        "dataset": "dataset",
    }

    def __init__(self, dataset: "List[str]"):
        self.dataset = dataset
