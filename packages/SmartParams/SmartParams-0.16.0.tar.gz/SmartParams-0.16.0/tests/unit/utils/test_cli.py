from pathlib import Path
from unittest.mock import Mock, patch

from smartparams.utils.cli import Arguments, create_argument_parser, parse_arguments
from tests.unit import UnitCase


class TestParseArguments(UnitCase):
    def setUp(self) -> None:
        self.parser = create_argument_parser(
            default_path=Path('/home/params.yaml'),
        )
        self.expected = Arguments(
            path=Path('/home/params.yaml'),
            dump=False,
            skip_defaults=False,
            merge_params=False,
            print=None,
            format='yaml',
            params=[],
            strict=False,
            debug=False,
        )

    @patch('smartparams.utils.cli.sys')
    def test(self, sys: Mock) -> None:
        sys.argv = 'script.py'.split()

        actual = parse_arguments(self.parser)

        self.assertEqual(self.expected, actual)

    @patch('smartparams.utils.cli.sys')
    def test__override_path(self, sys: Mock) -> None:
        sys.argv = 'script.py --path /home/cli_params.yaml'.split()
        self.expected.path = Path('/home/cli_params.yaml')

        actual = parse_arguments(self.parser)

        self.assertEqual(self.expected, actual)

    @patch('smartparams.utils.cli.sys')
    def test__mode(self, sys: Mock) -> None:
        sys.argv = 'script.py --mode env'.split()
        self.expected.path = Path('/home/params.env.yaml')

        actual = parse_arguments(self.parser)

        self.assertEqual(self.expected, actual)

    @patch('smartparams.utils.cli.sys')
    def test__dump(self, sys: Mock) -> None:
        sys.argv = 'script.py --dump -sm'.split()
        self.expected.dump = True
        self.expected.skip_defaults = True
        self.expected.merge_params = True

        actual = parse_arguments(self.parser)

        self.assertEqual(self.expected, actual)

    @patch('smartparams.utils.cli.sys')
    def test__print_params(self, sys: Mock) -> None:
        sys.argv = 'script.py --print params --merge-params'.split()
        self.expected.merge_params = True
        self.expected.print = 'params'

        actual = parse_arguments(self.parser)

        self.assertEqual(self.expected, actual)

    @patch('smartparams.utils.cli.sys')
    def test__print_keys(self, sys: Mock) -> None:
        sys.argv = 'script.py --print keys --format yaml'.split()
        self.expected.print = 'keys'

        actual = parse_arguments(self.parser)

        self.assertEqual(self.expected, actual)

    @patch('smartparams.utils.cli.sys')
    def test__dump_print_error(self, sys: Mock) -> None:
        sys.argv = 'script.py --dump --print params'.split()

        self.assertRaises(SystemExit, parse_arguments, self.parser)

    @patch('smartparams.utils.cli.sys')
    def test__dump_format_error(self, sys: Mock) -> None:
        sys.argv = 'script.py --dump --format yaml'.split()

        self.assertRaises(SystemExit, parse_arguments, self.parser)

    @patch('smartparams.utils.cli.sys')
    def test__print_keys_skip_default_error(self, sys: Mock) -> None:
        sys.argv = 'script.py --print keys -s'.split()

        self.assertRaises(SystemExit, parse_arguments, self.parser)

    @patch('smartparams.utils.cli.sys')
    def test__print_keys_merge_params_error(self, sys: Mock) -> None:
        sys.argv = 'script.py --print keys -m'.split()

        self.assertRaises(SystemExit, parse_arguments, self.parser)
