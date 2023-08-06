import json
import logging
import boto3
import fnmatch
import os
from datetime import datetime, timedelta
from types import SimpleNamespace
from typing import List, Optional, Tuple, Dict, Union

from helix_catalog_sdk.data_source import DataSource, ResourceItem

from helix_catalog_sdk.enums import HelixEnvironment
from helix_catalog_sdk.repo import BaseRepo


class Catalog:
    def __init__(
        self,
        repo: BaseRepo,
        environment: HelixEnvironment = HelixEnvironment.PRODUCTION,
    ) -> None:
        """
        Implementation of the data catalog
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(os.environ.get("LOGLEVEL", "INFO"))
        self._repo: BaseRepo = repo
        self.environment: HelixEnvironment = environment
        self._last_updated_data_source_dttm: datetime = datetime.utcnow() + timedelta(
            days=-1
        )
        self._all_data_sources: List[Tuple[str, DataSource]] = []
        self._all_data_sources = self.get_all_data_sources()

    def get_data_source(
        self, data_source: str, environment: HelixEnvironment
    ) -> Optional[DataSource]:
        self.logger.info(
            f"Data Catalog is reading data source: {data_source} for environment {environment}"
        )
        decoded_contents = self._repo.read_file(data_source)
        contents: SimpleNamespace = json.loads(
            decoded_contents, object_hook=lambda d: SimpleNamespace(**d)
        )

        # Currently, only data_sources of type "file" are working in the catalog.
        if getattr(contents, "connection_type", None) != "file":
            return None

        return DataSource(data_source, contents, environment)

    def update_data_source_resource(self, file_path: str) -> Optional[DataSource]:
        for data_source_path, data_source in self._all_data_sources:
            if data_source.matches_path(file_path):
                data_source.update_path_with_latest_file(file_path)
                self.update_data_source(data_source_path, data_source.to_json())
                return data_source
        return None

    def update_resource_last_processed(
        self,
        resource_name: str,
        last_processed_value: str,
        data_source: DataSource,
        environment: HelixEnvironment,
    ) -> None:
        for resource in data_source.resources:
            if resource_name == resource.name and resource.last_processed is not None:
                resource.last_processed.set_last_processed(
                    last_processed_value, environment
                )
                self.update_data_source(data_source.name, data_source.to_json())

    def update_resource_last_processed_date_segment(
        self,
        resource_name: str,
        updated_date: datetime,
        data_source: DataSource,
        environment: HelixEnvironment,
    ) -> None:
        """
        Updates the last_processed path with the passed in date using the date_format of the resource


        :param resource_name: resource name to update
        :param updated_date: date to update last_processed with
        :param data_source: data source to update
        :param environment: environment
        """
        resource: ResourceItem
        resources = list(
            filter(
                lambda r: r.name == resource_name and r.last_processed is not None,
                data_source.resources,
            )
        )
        assert (
            len(resources) > 0
        ), f"No matching resource found for resource name [{resource_name}] that has last_processed"
        for resource in resources:
            if resource_name == resource.name and resource.last_processed is not None:
                date_segment: Union[int, List[int]] = (
                    resource.date_segment if resource.date_segment else 0
                )
                self.logger.info(f"Using date_segment: {date_segment}")
                date_format: str = (
                    resource.date_format if resource.date_format else "%Y-%m-%d"
                )
                last_processed_path: str = resource.last_processed.get_last_processed(
                    environment
                )
                last_processed_path_parts: List[str] = list(
                    filter(None, last_processed_path.replace("s3:/", "").split("/"))
                )
                if isinstance(date_segment, int):
                    # replace that part of the path with new one
                    last_processed_path_parts[date_segment] = updated_date.strftime(
                        date_format
                    )
                elif isinstance(date_segment, list):
                    date_format_parts = []
                    i: int = -1
                    for char in date_format:
                        if char == "%":
                            i = i + 1
                            date_format_parts.append("")
                            date_format_parts[i] = date_format_parts[i] + char
                        elif i >= 0:
                            date_format_parts[i] = date_format_parts[i] + char

                    for segment, date_format_part in zip(
                        date_segment, date_format_parts
                    ):
                        last_processed_path_parts[segment] = updated_date.strftime(
                            date_format_part
                        )

                new_last_processed_path: str = "/".join(last_processed_path_parts)

                self.logger.info(
                    f"Updating last_processed from {last_processed_path} to {new_last_processed_path}"
                    f" for environment {environment}"
                )

                resource.last_processed.set_last_processed(
                    new_last_processed_path, environment
                )
                self.update_data_source(data_source.name, data_source.to_json())

    def update_data_source(self, data_source_name: str, updated_contents: str) -> None:
        self._repo.update_file(data_source_name, updated_contents)

    def get_resource_unprocessed_directories(
        self, resource_name: str, data_source: DataSource, environment: HelixEnvironment
    ) -> List[str]:
        paths_to_process: Dict[datetime, str] = {}
        sorted_paths_to_process = []
        resource: ResourceItem = [
            r for r in data_source.resources if r.name == resource_name
        ][0]
        if resource.last_processed:
            date_segment: Union[int, List[int]] = (
                resource.date_segment if resource.date_segment else 0
            )
            self.logger.info(f"Using date_segment: {date_segment}")

            date_format: str = (
                resource.date_format if resource.date_format else "%Y-%m-%d"
            )
            last_processed_path: str = resource.last_processed.get_last_processed(
                environment
            )
            self.logger.info(
                f"Found last processed path {last_processed_path} for resource {resource.name}"
            )
            all_paths: List[str] = self.get_all_directories(
                resource, last_processed_path
            )
            self.logger.debug(
                f"---- Found paths for last processed path [{last_processed_path}] ------"
            )
            for path in all_paths:
                self.logger.debug(f"{path}")
            self.logger.debug(
                "-----------------------------------------------------------"
            )
            path_parts: List[str] = list(
                filter(None, last_processed_path.replace("s3:/", "").split("/"))
            )

            last_processed_date: Optional[datetime] = None
            if isinstance(date_segment, int):
                last_processed_date = datetime.strptime(
                    path_parts[date_segment], date_format
                )
            elif isinstance(date_segment, list):
                last_processed_date_str: str = ""
                for segment in date_segment:
                    last_processed_date_str = (
                        last_processed_date_str + path_parts[segment]
                    )
                last_processed_date = datetime.strptime(
                    last_processed_date_str, date_format
                )

            self.logger.info(
                f"Using last_processed_date: {last_processed_date} {type(last_processed_date)}"
            )

            for path in all_paths:
                path_parts = list(filter(None, path.replace("s3:/", "").split("/")))
                path_date: Optional[datetime] = None
                if isinstance(date_segment, int):
                    path_date = datetime.strptime(path_parts[date_segment], date_format)
                elif isinstance(date_segment, list):
                    path_date_str = ""
                    for segment in date_segment:
                        path_date_str = path_date_str + path_parts[segment]
                    path_date = datetime.strptime(path_date_str, date_format)
                if path_date is not None and (
                    not last_processed_date or path_date > last_processed_date
                ):
                    self.logger.info(
                        f"Adding path for {path_date} compared to {last_processed_date}"
                    )
                    paths_to_process[path_date] = path
                else:
                    self.logger.debug(
                        f"Skipped path for {path_date} compared to {last_processed_date}"
                    )

            for path_date in sorted(paths_to_process):
                sorted_paths_to_process.append(paths_to_process[path_date])

            self.logger.info(
                f"---- Sorted paths for last processed path [{last_processed_path}] ------"
            )
            for path in sorted_paths_to_process:
                self.logger.info(f"{path}")
            self.logger.info(
                "-----------------------------------------------------------"
            )

            return sorted_paths_to_process
        else:
            return []

    def get_all_directories(
        self, resource: ResourceItem, last_processed: str
    ) -> List[str]:
        full_path = resource.full_path
        all_paths: List[str] = []
        if full_path.startswith("s3://"):
            path = full_path.replace("s3://", "")
            bucket = path.split("/")[0]
            prefix = path.replace(f"{bucket}/", "")
            s3 = boto3.client("s3")
            paginator = s3.get_paginator("list_objects_v2")
            pages = paginator.paginate(Bucket=bucket, Prefix=prefix)
            for response in pages:
                for s3_file in response["Contents"]:
                    s3_path_parts = s3_file["Key"].split("/")
                    last_processed_file_name: str = last_processed.split("/")[-1]
                    s3_file_name = s3_path_parts[-1]
                    # 1. if they are exactly the same length then add this path
                    # 2. if the file name matches then add this path
                    # 3. if the glob pattern matches then add this path
                    if (
                        len(list(filter(None, s3_path_parts))) == resource.date_segment
                        or last_processed_file_name == s3_file_name
                        or fnmatch.fnmatch(s3_file_name, last_processed_file_name)
                    ):
                        all_paths.append(f"s3://{bucket}/{s3_file['Key']}")
                    else:
                        self.logger.debug(
                            f"Did not match {s3_file['Key']} to {last_processed_file_name}"
                        )
            return all_paths
        else:
            paths = [
                os.path.join(dp, f)
                for dp, dn, fn in os.walk(os.path.expanduser(full_path))
                for f in fn
            ]
            for path in paths:
                all_paths.append(path)
            return all_paths

    def get_all_data_sources(
        self, base_path: str = "catalog"
    ) -> List[Tuple[str, DataSource]]:
        last_repo_update = self._repo.last_update(base_path)
        needs_update = (
            last_repo_update is None
            or last_repo_update > self._last_updated_data_source_dttm
        )
        self._last_updated_data_source_dttm = datetime.utcnow()
        if needs_update or len(self._all_data_sources) == 0:
            self.logger.info("Getting all data sources")
            catalog_contents = self._repo.list_items(base_path)
            data_sources: List[Tuple[str, DataSource]] = []
            while catalog_contents:
                file_path = catalog_contents.pop(0)
                if self._repo.is_dir(file_path):
                    catalog_contents.extend(self._repo.list_items(file_path))
                elif file_path.endswith(".json"):
                    data_source = self.get_data_source(file_path, self.environment)
                    if data_source:
                        data_sources.append((file_path, data_source))
            self._all_data_sources = data_sources
            self.logger.info("Finished all data sources")
            return data_sources
        else:
            self.logger.info("Returning cached data sources")
            return self._all_data_sources

    # noinspection PyMethodMayBeStatic
    def get_last_processed_dates_for_resources(
        self,
        data_source: DataSource,
        environment: HelixEnvironment,
        resource_name: Optional[str] = None,
    ) -> Dict[str, Optional[datetime]]:
        """
        Get the last processed dates of all the resources in this data source


        :param data_source: data source to get
        :param resource_name: (Optional) limit results to this resource
        :param environment: environment
        """
        resource: ResourceItem
        resources = list(
            filter(
                lambda r: r.last_processed is not None
                and (not resource_name or r.name == resource_name),
                data_source.resources,
            )
        )
        if len(resources) == 0:
            return {}

        result: Dict[str, Optional[datetime]] = {}
        for resource in resources:
            result[resource.name] = self.get_last_processed_date_for_resource(
                resource=resource, environment=environment
            )
        return result

    # noinspection PyMethodMayBeStatic
    def get_last_processed_date_for_resource(
        self, environment: HelixEnvironment, resource: ResourceItem
    ) -> Optional[datetime]:
        """
        Gets last processed date for the specified resource


        :param resource:
        :param environment: environment
        """
        if resource.last_processed:
            date_segment: Union[int, List[int]] = (
                resource.date_segment if resource.date_segment else 0
            )
            date_format: str = (
                resource.date_format if resource.date_format else "%Y%m%d"
            )
            last_processed_path: str = resource.last_processed.get_last_processed(
                environment
            )
            last_processed_path_parts: List[str] = list(
                filter(None, last_processed_path.replace("s3:/", "").split("/"))
            )
            if isinstance(date_segment, int):
                return datetime.strptime(
                    last_processed_path_parts[date_segment], date_format
                )
            elif isinstance(date_segment, list):
                date_text = "".join(
                    [last_processed_path_parts[index] for index in date_segment]
                )
                return datetime.strptime(date_text, date_format)
        return None
