import os
import platform
import random
import re
import shutil
import sys
import uuid
from datetime import datetime
from pathlib import Path
from secrets import token_hex
from time import sleep, time
from typing import Any, Dict, Optional

import pkg_resources
from dvc.lock import LockError
from dvc.repo import Repo as DVCRepo
from git.repo import Repo as GITRepo

from smartparams.utils.io import load_data, save_data
from smartparams.utils.vocab import VOCABULARY

PATTERNS = dict(
    number=r'\d+',
    hash=r'[a-zA-Z0-9]+',
    uuid=r'\w{8}-\w{4}-\w{4}-\w{4}-\w{12}',
    adjective=r'[a-zA-Z\-]+',
    noun=r'[a-zA-Z\-]+',
    year=r'\d{2}|\d{4}',
    month=r'\d{1,2}',
    day=r'\d{1,2}',
    hour=r'\d{1,2}',
    minute=r'\d{1,2}',
    second=r'\d{1,2}',
    microsecond=r'\d+',
)


class SmartLab:
    remote: str = 'origin'

    def new(
        self,
        save_dir: Path,
        version: Optional[str] = '{number:03d}_{adjective}_{noun}',
    ) -> Path:
        """Creates directory for new experiment.

        Args:
            save_dir: Main directory for experiments.
            version: Pattern for new folder name. Available fields: number, hash, uuid, adjective,
                noun, year, month, day, hour, minute, second, microsecond.

        Returns:
            Path to newly created experiment directory.

        """
        if version:
            date = datetime.now()
            save_dir = save_dir.joinpath(
                version.format(
                    number=self._get_next_number(
                        save_dir=save_dir,
                        version=version,
                    ),
                    hash=token_hex(16),
                    uuid=uuid.uuid4(),
                    adjective=random.choice(VOCABULARY['adjectives']),
                    noun=random.choice(VOCABULARY['nouns']),
                    year=date.year,
                    month=date.month,
                    day=date.day,
                    hour=date.hour,
                    minute=date.minute,
                    second=date.second,
                    microsecond=date.microsecond,
                )
            )

        save_dir.mkdir(parents=True, exist_ok=True)
        return save_dir

    def download(
        self,
        target: Path,
        recursive: bool = True,
        remote: Optional[str] = None,
        jobs: Optional[int] = None,
        skip_exists: bool = False,
        force: bool = True,
        timeout: int = 3600,
    ) -> Path:
        """Automatically downloads files from DVC storage of given remote.

        Args:
            target: Path to file or directory to download.
            recursive: Download files in all subdirectories.
            remote: Name of the remote storage to download from.
            jobs: Parallelism level for DVC to download data from remote storage.
            skip_exists: Skips fetching DVC cache if target path exists.
            force: Overrides workspace files without asking.
            timeout: Waiting time for release of DVC lock.

        Returns:
            Path to downloaded file or directory.

        """
        target_path = target.resolve()

        if skip_exists and target_path.exists():
            return target_path

        root_dir = DVCRepo.find_root(root=target if target.is_dir() else target.parent)
        while not target.with_name(target.name + '.dvc').exists():
            target = target.parent
            if target.is_mount():
                raise RuntimeError(f"Target {target_path} is not versioned by DVC.")

        dvc_repo = DVCRepo(root_dir)
        self._wait_on_dvc_lock_release(
            dvc_repo=dvc_repo,
            timeout=timeout,
        )
        dvc_repo.pull(
            targets=str(target),
            remote=remote or self.remote,
            force=force,
            recursive=recursive,
            jobs=jobs,
        )

        if not target_path.exists():
            raise RuntimeError(f"Target {target_path} does not exist after completed download.")

        return target_path

    def upload(
        self,
        target: Path,
        recursive: bool = False,
        remote: Optional[str] = None,
        sync: bool = True,
        jobs: Optional[int] = None,
        timeout: int = 3600,
    ) -> None:
        """Uploads files to DVC storage of given remote.

        Args:
            target: Path to the file or directory to be uploaded.
            recursive: Uploads each file in all subdirectories separately.
            remote: Name of the remote storage to be uploaded.
            sync: Uploads to remote storage, otherwise save only to local cache.
            jobs: Parallelism level for DVC to upload data to remote storage.
            timeout: Waiting time for release of DVC lock.

        """
        root_dir = DVCRepo.find_root(root=target if target.is_dir() else target.parent)

        args: Dict[str, Any] = dict()
        if sync:
            args.update(
                jobs=jobs,
                remote=remote or self.remote,
                to_remote=True,
            )

        dvc_repo = DVCRepo(root_dir)
        self._wait_on_dvc_lock_release(
            dvc_repo=dvc_repo,
            timeout=timeout,
        )
        dvc_repo.add(
            targets=str(target),
            recursive=recursive,
            **args,
        )

    @staticmethod
    def remove(path: Path) -> None:
        """Removes given file or directory with DVC metadata.

        Args:
            path: Path to the file or directory to remove.

        """
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink(missing_ok=True)

        path.with_suffix(path.suffix + '.dvc').unlink(missing_ok=True)

    def metadata(
        self,
        /,
        include_date: bool = True,
        include_system: bool = True,
        include_git: bool = True,
        include_dependencies: bool = True,
        save_to: Optional[Path] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Returns most important information about platform and project versions.

        Args:
            include_date: Whether to include date and time.
            include_system: Whether to include system info data.
            include_git: Whether to include git branch and commit hash.
            include_dependencies: Whether to include list of packages and versions.
            save_to: Path to save metadata.

        Returns:
            Dictionary with metadata.

        """
        metadata = {
            **(self._date_metadata() if include_date else {}),
            **(self._system_metadata() if include_system else {}),
            **(self._git_metadata() if include_git else {}),
            **(self._dependencies_metadata() if include_dependencies else {}),
            **kwargs,
        }

        if save_to:
            metadata_history = load_data(save_to) if save_to.exists() else dict()
            metadata_history[f'run{len(metadata_history) + 1:03d}'] = metadata
            save_data(
                data=metadata_history,
                path=save_to,
            )

        return metadata

    @staticmethod
    def _date_metadata() -> Dict[str, Any]:
        date = datetime.now()
        return dict(
            date=date.strftime('%Y-%m-%d'),
            time=date.strftime('%H:%M:%S'),
        )

    @staticmethod
    def _system_metadata() -> Dict[str, Any]:
        return dict(
            user=os.getlogin(),
            host=platform.node(),
            os=platform.platform(),
            python=platform.python_version(),
            args=sys.argv[1:],
        )

    @staticmethod
    def _git_metadata() -> Dict[str, Any]:
        repo = GITRepo(sys.argv[0], search_parent_directories=True)
        return dict(
            branch=repo.active_branch.name,
            commit=repo.active_branch.commit.hexsha if repo.active_branch.is_valid() else None,
        )

    @staticmethod
    def _dependencies_metadata() -> Dict[str, Any]:
        return dict(
            packages=[f'{package.key}=={package.version}' for package in pkg_resources.working_set],
        )

    @staticmethod
    def _build_pattern(string: str) -> str:
        offset = 0
        for match in re.finditer(r'{(?P<name>\w+)(?::.+?)?}', string):
            name = match.group('name')
            replacement = rf'(?P<{name}>{PATTERNS[name]})'
            string = string[: match.start() + offset] + replacement + string[match.end() + offset :]
            offset += len(replacement) - (match.end() - match.start())

        return string

    def _get_next_number(
        self,
        save_dir: Path,
        version: str,
    ) -> int:
        if not save_dir.exists():
            return 1

        pattern = self._build_pattern(version)
        version_number = 0
        for path in save_dir.iterdir():
            if path.is_dir() and (match := re.fullmatch(pattern, path.name)):
                if number := match.group('number'):
                    version_number = max(version_number, int(number))

        return version_number + 1

    def _wait_on_dvc_lock_release(
        self,
        dvc_repo: DVCRepo,
        timeout: int = 3600,
        delay: float = 2.0,
    ) -> None:
        time_start = time()
        while self._is_dvc_locked(dvc_repo):
            print("Waiting for release of DVC lock")
            sleep(delay)
            if time() - time_start > timeout:
                raise TimeoutError(
                    "DVC repository is locked. Most likely another DVC process is running "
                    "or was terminated abruptly."
                )

    @staticmethod
    def _is_dvc_locked(dvc_repo: DVCRepo) -> bool:
        try:
            dvc_repo.lock.lock()
        except LockError:
            return True
        else:
            dvc_repo.lock.unlock()
            return False
