import smartparams.utils.string as strutil
from smartparams.exceptions import ArgumentParserError
from tests.unit import UnitCase


class TestParseParam(UnitCase):
    def test(self) -> None:
        data = 'key.neste_key=[true, null, "some string", {"1": 9.0}]'

        key, value = strutil.parse_param(data)

        self.assertEqual('key.neste_key', key)
        self.assertListEqual([True, None, "some string", {"1": 9.0}], value)

    def test__not_valid(self) -> None:
        data = 'key.neste_key=[true, null, "some string, {"1": 9.0}]'

        key, value = strutil.parse_param(data)

        self.assertEqual('key.neste_key', key)
        self.assertEqual('[true, null, "some string, {"1": 9.0}]', value)

    def test__raise_no_assignment(self) -> None:
        data = 'key.neste_key [true, null, "some string", {"1": 9.0}]'

        self.assertRaises(ArgumentParserError, strutil.parse_param, data)


class TestToBool(UnitCase):
    def test__true(self) -> None:
        test_cases = (
            'Y',
            'True',
        )

        for value in test_cases:
            with self.subTest(value=value):
                actual = strutil.to_bool(value)

                self.assertTrue(actual)

    def test__false(self) -> None:
        test_cases = (
            'N',
            'False',
        )

        for value in test_cases:
            with self.subTest(value=value):
                actual = strutil.to_bool(value)

                self.assertFalse(actual)

    def test__raise(self) -> None:
        test_cases = (
            '2',
            'D',
        )

        for value in test_cases:
            with self.subTest(value=value):
                self.assertRaises(ValueError, strutil.to_bool, value)
