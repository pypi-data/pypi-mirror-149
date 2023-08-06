import json
import os
from types import SimpleNamespace
from typing import List, Dict, Any, Optional

from helix_catalog_sdk.enums import HelixEnvironment


class ResourceItem:
    JSON_KEYS = (
        "name",
        "path",
        "path_slug",
        "last_processed",
        "date_segment",
        "date_format",
    )

    def __init__(
        self,
        content: SimpleNamespace,
        base_connection_formatted: str,
        environment: HelixEnvironment,
    ):
        self.name = content.name
        self.path = content.path
        self.path_slug = getattr(content, "path_slug", None)
        self.base_connection_formatted = base_connection_formatted
        self.date_segment = None
        if hasattr(content, "date_segment") and content.date_segment is not None:
            self.date_segment = content.date_segment
        self.date_format = None
        if hasattr(content, "date_format") and content.date_format is not None:
            self.date_format = content.date_format
        self.last_processed = None
        if hasattr(content, "last_processed") and content.last_processed is not None:
            self.last_processed = LastProcessed(content.last_processed, environment)
        self.path_extension = None
        if hasattr(content, "path_extension") and content.path_extension is not None:
            self.path_extension = content.path_extension

    @property
    def full_path_slug(self) -> Optional[str]:
        return self.path_slug and os.path.join(
            self.base_connection_formatted, self.path_slug
        )

    @property
    def full_path(self) -> str:
        return os.path.join(self.base_connection_formatted, self.path)

    def matches_path(self, path: str) -> bool:
        if self.full_path_slug and self.full_path_slug in path:
            if self.path_extension:
                return path.endswith(self.path_extension)
            else:
                return True
        return False

    @property
    def json_dict(self) -> Dict[str, Any]:
        return dict(
            (key, value)
            for key, value in self.__dict__.items()
            if key in self.JSON_KEYS
        )

    def to_json(self) -> str:
        return json.dumps(self.json_dict)


class DataSource:
    def __init__(
        self,
        data_source_name: str,
        content: SimpleNamespace,
        environment: HelixEnvironment,
    ):
        self.name = data_source_name
        self.base_connection = content.base_connection
        self.base_connection_formatted = self.get_connection(content, environment)
        self.production = getattr(content, "production", None)
        self.staging = getattr(content, "staging", None)
        self.qa = getattr(content, "qa", None)
        self.dev = getattr(content, "dev", None)
        self.connection_type = content.connection_type
        self.resources: List[ResourceItem] = []
        for resource_item in content.resources:
            self.resources.append(
                ResourceItem(resource_item, self.base_connection_formatted, environment)
            )
        self.pipeline_subscriptions: List[PipelineSubscription] = []
        for pipeline_subscription in content.pipeline_subscriptions:
            self.pipeline_subscriptions.append(
                PipelineSubscription(pipeline_subscription)
            )

    def get_connection(
        self, content: SimpleNamespace, environment: HelixEnvironment
    ) -> str:
        base_connection_formatted: str = content.base_connection
        if environment == HelixEnvironment.PRODUCTION:
            base_connection_formatted = content.base_connection.format(
                env=content.production
            )
        elif environment == HelixEnvironment.STAGING:
            base_connection_formatted = content.base_connection.format(
                env=content.staging
            )
        elif environment == HelixEnvironment.QA:
            base_connection_formatted = content.base_connection.format(env=content.qa)
        elif environment == HelixEnvironment.DEV:
            base_connection_formatted = content.base_connection.format(env=content.dev)

        return base_connection_formatted

    @property
    def json_dict(self) -> Dict[str, Any]:
        json_obj = dict(
            (key, value)
            for key, value in self.__dict__.items()
            if value is not None and key not in ["base_connection_formatted"]
        )
        return json_obj

    def to_json(self) -> str:
        """
        convert the instance of this class to json
        """
        return json.dumps(
            self,
            indent=4,
            default=lambda o: o.json_dict if hasattr(o, "json_dict") else o,
        )

    def matches_path(self, path: str) -> bool:
        for resource in self.resources:
            if resource.matches_path(path):
                return True
        return False

    def get_matching_resource(self, path: str) -> Optional[ResourceItem]:
        for resource in self.resources:
            if resource.matches_path(path):
                return resource
        return None

    def update_path_with_latest_file(self, file_path: str) -> None:
        resource = self.get_matching_resource(file_path)
        if resource is not None and resource.path_slug is not None:
            index: int = file_path.find(resource.path_slug)
            resource.path = file_path[index:]


class PipelineSubscription:
    def __init__(self, content: SimpleNamespace):
        if isinstance(content, str):
            self.flow_name: str = content
            self.flow_parameters: List[str] = []
        else:
            self.flow_name = content.flow_name
            self.flow_parameters = []
            if hasattr(content, "flow_parameters"):
                self.flow_parameters = content.flow_parameters

    @property
    def json_dict(self) -> Dict[str, Any]:
        return self.__dict__


class LastProcessed:
    def __init__(self, content: SimpleNamespace, environment: HelixEnvironment):
        self.dev = content.dev
        self.production = content.production
        self.staging = content.staging
        self.qa = content.qa

    @property
    def json_dict(self) -> Dict[str, Any]:
        return self.__dict__

    def set_last_processed(
        self, last_processed_value: str, environment: HelixEnvironment
    ) -> None:
        self.json_dict[environment.name.lower()] = last_processed_value

    def get_last_processed(self, environment: HelixEnvironment) -> str:
        last_processed_item: str = self.dev
        if environment == HelixEnvironment.PRODUCTION:
            last_processed_item = self.production
        elif environment == HelixEnvironment.STAGING:
            last_processed_item = self.staging
        elif environment == HelixEnvironment.QA:
            last_processed_item = self.qa
        return last_processed_item
