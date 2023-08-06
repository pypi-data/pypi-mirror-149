import inspect
from typing import Any, Dict, Tuple
from unittest.mock import Mock

import smartparams.utils.typing as typeutil
from smartparams import Smart
from smartparams.exceptions import ObjectNotCallableError, ObjectNotFoundError
from tests.custom_classes import Class, ClassCompositionChild
from tests.unit import UnitCase


class TestImportCallable(UnitCase):
    def test(self) -> None:
        actual = typeutil.import_callable('tests.custom_classes.Class', trace='')

        self.assertIs(Class, actual)

    def test__no_existing(self) -> None:
        name = 'NoExistingClass'

        self.assertRaises(ObjectNotFoundError, typeutil.import_callable, name, trace='')

    def test__no_callable(self) -> None:
        name = 'tests.custom_classes.CONSTANT'

        self.assertRaises(ObjectNotCallableError, typeutil.import_callable, name, trace='')


class TestGetName(UnitCase):
    def test(self) -> None:
        test_cases = (
            (Mock, 'Mock'),
            (Mock(), 'Mock'),
            (123, 'int'),
            (type, 'type'),
            (None, 'NoneType'),
            (lambda: ..., 'TestGetName.test.<locals>.<lambda>'),
            ((i for i in range(1)), 'TestGetName.test.<locals>.<genexpr>'),
        )

        for cls, expected in test_cases:
            with self.subTest(expected=expected):
                actual = typeutil.get_name(cls)

                self.assertEqual(expected, actual)


class TestGetTypeHints(UnitCase):
    def test(self) -> None:
        test_cases = (
            (
                ClassCompositionChild,
                {
                    'vanilla_cls': Class,
                    'smart_cls': Smart[Class],
                    'smart': Smart,
                    'unknown': Any,
                    'no_type': Any,
                    'args': Tuple[Any, ...],
                    'with_only_default_primitive': int,
                    'kwargs': Dict[str, Any],
                },
            ),
        )

        for cls, expected in test_cases:
            signature = inspect.signature(cls)

            with self.subTest(cls=cls.__name__):
                actual = typeutil.get_type_hints(signature)

                self.assertEqual(expected, actual)


class TestConvertToPrimitives(UnitCase):
    def test(self) -> None:
        data = (True, None, {'known': 9.0, 'unknown': set()})
        expected = [True, None, {'known': 9.0, 'unknown': '???'}]

        actual = typeutil.convert_to_primitives(data, unknown_type='???')

        self.assertEqual(expected, actual)
