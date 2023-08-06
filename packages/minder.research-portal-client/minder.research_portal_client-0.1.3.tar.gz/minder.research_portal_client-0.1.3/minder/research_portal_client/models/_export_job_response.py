from typing import List
from datetime import datetime
from minder.research_portal_client.models import ExportJobRequest
from minder.research_portal_client._utils import RestObject


class _ExportJobProgress(RestObject):
    prop_types = {
        "progress": str,
    }

    attribute_map = {
        "progress": "progress",
    }

    def __init__(self, progress: str = None):
        self.progress = progress


class _ExportJobOutput(RestObject):
    prop_types = {
        "type": str,
        "url": str,
        "count": int,
    }

    attribute_map = {
        "type": "type",
        "url": "url",
        "count": "count",
    }

    def __init__(self, type: str = None, url: str = None, count: int = None):
        self.type = type
        self.url = url
        self.count = count


class _ExportJobRecord(RestObject):
    prop_types = {
        "transaction_time": datetime,
        "request": ExportJobRequest,
        "requires_access_token": bool,
        "output": "list[_ExportJobOutput]",
        "error": "list[str]",
    }

    attribute_map = {
        "transaction_time": "transactionTime",
        "request": "request",
        "requires_access_token": "requiresAccessToken",
        "output": "output",
        "error": "error",
    }

    def __init__(
        self,
        transaction_time: datetime = None,
        request: ExportJobRequest = None,
        requires_access_token: bool = None,
        output: "List[_ExportJobOutput]" = None,
        error: "List[str]" = None,
    ):
        self.transaction_time = transaction_time
        self.request = request
        self.requires_access_token = requires_access_token
        self.output = output
        self.error = error


class ExportJobResponse(RestObject):
    prop_types = {
        "id": str,
        "status": int,
        "job_record": _ExportJobRecord,
        "job_progress": _ExportJobProgress,
    }

    attribute_map = {
        "id": "id",
        "status": "status",
        "job_record": "jobRecord",
        "job_progress": "jobProgress",
    }

    def __init__(
        self,
        id: str = None,
        status: int = None,
        job_record: _ExportJobRecord = None,
        job_progress: _ExportJobProgress = None,
    ):
        self.id = id
        self.status = status
        self.job_record = job_record
        self.job_progress = job_progress
