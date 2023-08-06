import tempfile
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock, patch

from dvc.lock import LockError
from git import Repo

from smartparams.lab import SmartLab
from tests.unit import UnitCase


class TestRegisterCase(UnitCase):
    def setUp(self) -> None:
        self.lab = SmartLab()

    @patch('smartparams.lab.random.choice', Mock(side_effect=['a', 'b', 'c', 'd']))
    def test_new(self) -> None:
        self.lab._wait_on_dvc_lock_release = Mock()  # type: ignore
        with TemporaryDirectory() as dirname:
            save_dir = Path(dirname, 'experiment')

            self.lab.new(save_dir=save_dir)
            self.lab.new(save_dir=save_dir)

            path_1, path_2 = sorted(save_dir.iterdir())
            self.assertEqual('001_a_b', path_1.name)
            self.assertEqual('002_c_d', path_2.name)

    @patch('smartparams.lab.GITRepo.init', Mock())
    @patch('smartparams.lab.GITRepo.init', Mock())
    @patch('smartparams.lab.DVCRepo')
    def test_download(self, dvc_repo: Mock) -> None:
        self.lab._wait_on_dvc_lock_release = Mock()  # type: ignore
        with TemporaryDirectory() as name:
            directory = Path(name)
            directory.joinpath('folder1').mkdir()
            directory.joinpath('folder2').mkdir()
            directory.joinpath('folder1.dvc').touch()
            target = directory.joinpath('folder1', 'filename.txt')
            target.touch()

            self.lab.download(target)

        dvc_repo().pull.assert_called_once_with(
            targets=str(target.parent),
            remote='origin',
            force=True,
            recursive=True,
            jobs=None,
        )

    @patch('smartparams.lab.GITRepo.init', Mock())
    @patch('smartparams.lab.DVCRepo')
    def test_download__skip_exists(self, dvc_repo: Mock) -> None:
        self.lab._wait_on_dvc_lock_release = Mock()  # type: ignore
        with TemporaryDirectory() as dirname:
            directory = Path(dirname)
            directory.joinpath('folder').mkdir()
            target = directory.joinpath('folder', 'filename.txt')
            target.touch()

            self.lab.download(target, skip_exists=True)

        dvc_repo().pull.assert_not_called()

    @patch('smartparams.lab.GITRepo.init', Mock())
    @patch('smartparams.lab.DVCRepo', Mock())
    def test_download__untracked(self) -> None:
        self.lab._wait_on_dvc_lock_release = Mock()  # type: ignore
        with TemporaryDirectory() as dirname:
            directory = Path(dirname)
            target = directory.joinpath('filename.txt')

            self.assertRaises(RuntimeError, self.lab.download, target)

    @patch('smartparams.lab.GITRepo.init', Mock())
    @patch('smartparams.lab.DVCRepo', Mock())
    def test_download__not_exist_after_completed_download(self) -> None:
        self.lab._wait_on_dvc_lock_release = Mock()  # type: ignore
        with TemporaryDirectory() as dirname:
            directory = Path(dirname)
            target = directory.joinpath('filename.txt')
            directory.joinpath('filename.txt.dvc').touch()

            self.assertRaises(RuntimeError, self.lab.download, target)

    @patch('smartparams.lab.GITRepo.init', Mock())
    @patch('smartparams.lab.DVCRepo')
    def test_upload(self, dvc_repo: Mock) -> None:
        self.lab._wait_on_dvc_lock_release = Mock()  # type: ignore
        dvc_repo().lock.is_locked = False
        target = Path('filename.txt')

        self.lab.upload(target)

        dvc_repo().add.assert_called_once_with(
            targets=str(target),
            recursive=False,
            jobs=None,
            remote='origin',
            to_remote=True,
        )

    def test_remove(self) -> None:
        with TemporaryDirectory() as dirname:
            directory = Path(dirname)
            directory.joinpath('folder1').mkdir()
            directory.joinpath('folder2').mkdir()
            directory.joinpath('folder1.dvc').touch()
            directory.joinpath('folder1', 'filename.txt').touch()
            directory.joinpath('image.jpg').touch()
            directory.joinpath('image.JPG').touch()

            self.lab.remove(directory.joinpath('folder1'))
            self.lab.remove(directory.joinpath('image.jpg'))

            self.assertTrue(directory.joinpath('image.JPG').exists())
            self.assertTrue(directory.joinpath('folder2').exists())
            self.assertFalse(directory.joinpath('image.jpg').exists())
            self.assertFalse(directory.joinpath('folder1').exists())
            self.assertFalse(directory.joinpath('folder1', 'filename.txt').exists())
            self.assertFalse(directory.joinpath('folder1.dvc').exists())

    @patch('smartparams.lab.GITRepo')
    @patch('smartparams.lab.datetime', wraps=datetime)
    @patch('smartparams.lab.os.getlogin', Mock(return_value='user'))
    @patch('smartparams.lab.sys', Mock(argv=['/script.py', 'arg1', 'arg2']))
    @patch('smartparams.lab.pkg_resources', Mock(working_set=[]))
    @patch('smartparams.lab.platform.node', Mock(return_value='node'))
    @patch('smartparams.lab.platform.platform', Mock(return_value='node'))
    @patch('smartparams.lab.platform.python_version', Mock(return_value='python_version'))
    def test_metadata(
        self,
        datetime_mock: Mock,
        git_repo: Mock,
    ) -> None:
        datetime_mock.now = Mock(return_value=datetime(2022, 4, 19, 1, 5, 14))
        expected = {
            'date': '2022-04-19',
            'time': '01:05:14',
            'user': 'user',
            'host': 'node',
            'os': 'node',
            'python': 'python_version',
            'args': ['arg1', 'arg2'],
            'branch': 'master',
            'commit': None,
            'packages': [],
        }
        with TemporaryDirectory() as dirname:
            git_repo.return_value = Repo.init(dirname)

            actual = self.lab.metadata()

            self.assertEqual(expected, actual)

    def test_metadata__save(self) -> None:
        with tempfile.TemporaryDirectory() as dirname:
            filepath = Path(dirname, 'meta.yaml')
            filepath.write_text('run001:\n  user: root\n  params: sth')

            self.lab.metadata(
                include_date=False,
                include_system=False,
                include_git=False,
                include_dependencies=False,
                save_to=filepath,
                user='user',
            )

            self.assertEqual(
                'run001:\n  user: root\n  params: sth\nrun002:\n  user: user\n',
                filepath.read_text(),
            )

    @patch('smartparams.lab.print')
    def test_wait_on_dvc_lock_release(self, print_mock: Mock) -> None:
        dvc_repo = Mock()

        self.lab._wait_on_dvc_lock_release(dvc_repo=dvc_repo)

        print_mock.assert_not_called()

    @patch('smartparams.lab.print')
    def test_wait_on_dvc_lock_release__locked(self, print_mock: Mock) -> None:
        dvc_repo = Mock(lock=Mock(lock=Mock(side_effect=LockError('{}'))))

        self.assertRaises(
            TimeoutError,
            self.lab._wait_on_dvc_lock_release,
            dvc_repo=dvc_repo,
            timeout=0,
            delay=0,
        )
        print_mock.assert_called()
