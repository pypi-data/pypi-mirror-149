import datetime
import logging
import os
import os.path
from typing import Dict, List, Optional, Union

from github import Github
from github.Commit import Commit
from github.ContentFile import ContentFile


class BaseRepo:
    def __init__(self, location: str, access_token: Optional[str] = None):
        self.location = location
        self.access_token = access_token

    def last_update(self, path: str) -> Optional[datetime.datetime]:
        raise NotImplementedError()

    def read_file(self, path: str) -> str:
        raise NotImplementedError()

    def update_file(self, path: str, content: str) -> None:
        raise NotImplementedError()

    def list_items(self, path: str = "") -> List[str]:
        raise NotImplementedError()

    def is_dir(self, path: str) -> bool:
        raise NotImplementedError()

    def is_file(self, path: str) -> bool:
        raise NotImplementedError()


class GithubRepo(BaseRepo):
    def __init__(self, location: str, access_token: Optional[str] = None):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(os.environ.get("LOGLEVEL", "INFO"))
        self._github_client: Github = Github(login_or_token=access_token)
        self._repo = self._github_client.get_repo(location)
        self._content_file_map: Dict[str, ContentFile] = {}
        super().__init__(location, access_token)

    def last_update(self, path: str) -> Optional[datetime.datetime]:
        commits = self._repo.get_commits(path=path)

        if commits.totalCount == 0:
            return None

        # We only care about the most recent commit, so just grab the first item off the paged commits iterator
        most_recent_commit: Commit = next(iter(commits), None)  # type: ignore

        if not most_recent_commit or not most_recent_commit.stats.last_modified:
            return None

        last_modified_string = most_recent_commit.stats.last_modified
        last_modified_timestamp = datetime.datetime.strptime(
            last_modified_string, "%a, %d %b %Y %H:%M:%S %Z"
        )

        return last_modified_timestamp

    def list_items(self, path: str = "") -> List[str]:
        contents: Union[List[ContentFile], ContentFile] = self._repo.get_contents(path)

        # If doing a "ls" on a single item, return just that file
        if not isinstance(contents, list):
            contents = [contents]

        results = []
        for content_item in contents:
            self._content_file_map[content_item.path] = content_item
            results.append(content_item.path)

        return results

    def read_file(self, path: str) -> str:
        self.logger.info(f"Github Repo: Reading Data Catalog file from: {path}")
        contents: Union[List[ContentFile], ContentFile] = self._repo.get_contents(path)
        if not isinstance(contents, ContentFile) or contents.type != "file":
            raise IOError(f'"{path}" is a directory, not a file')

        decoded_contents: str = contents.decoded_content.decode("utf-8")

        # Store a copy of the file sha since this is needed for updating
        self._content_file_map[contents.path] = contents

        return decoded_contents

    def update_file(self, path: str, content: str) -> None:
        try:
            # get the latest version and set it in _contentfile_map to avoid conflict
            self.read_file(path=path)
            sha = self._content_file_map[path].sha
        except KeyError:
            raise IOError(
                f"Trying to modify file {path} in Github without previously fetching file."
            )

        result = self._repo.update_file(
            path=path,
            message="updated by helix-catalog",
            content=content,
            sha=sha,
        )

        # Update mapping for latest file info
        self._content_file_map[path] = result.get("content")  # type: ignore

    def is_dir(self, path: str) -> bool:
        content_file = self._content_file_map[path]
        return content_file.type == "dir"

    def is_file(self, path: str) -> bool:
        content_file = self._content_file_map[path]
        return content_file.type == "file"


class DirectoryRepo(BaseRepo):
    @staticmethod
    def _check_existance(path: str) -> None:
        if not os.path.exists(path):
            raise IOError(f'File/Directory "{path} does not exist')

    def _full_path(self, path: str) -> str:
        full_path = os.path.join(self.location, path)
        self._check_existance(full_path)
        return full_path

    def last_update(self, path: str) -> Optional[datetime.datetime]:
        try:
            most_recent_timestamp = max(
                (
                    os.stat(os.path.join(root, name)).st_mtime
                    for root, dirs, files in os.walk(path)
                    for name in files
                )
            )
        except ValueError:
            return None
        return datetime.datetime.fromtimestamp(most_recent_timestamp)

    def list_items(self, path: str = "") -> List[str]:
        return [
            os.path.join(path, result)
            for result in os.listdir(os.path.join(self.location, path))
        ]

    def read_file(self, path: str) -> str:
        full_path = self._full_path(path)
        content = open(full_path).read()
        return content

    def update_file(self, path: str, content: str) -> None:
        full_path = self._full_path(path)
        with open(full_path, "w") as fp:
            fp.write(content)

    def is_dir(self, path: str) -> bool:
        full_path = self._full_path(path)
        return os.path.isdir(full_path)

    def is_file(self, path: str) -> bool:
        full_path = self._full_path(path)
        return os.path.isfile(full_path)
