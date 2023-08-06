from unittest.mock import Mock, patch

from smartparams.register import SmartRegister
from tests.custom_classes import Class, ClassChild
from tests.unit import UnitCase


class TestRegisterCase(UnitCase):
    def setUp(self) -> None:
        self.register = SmartRegister()

    def test_register__classes(self) -> None:
        classes = ('origin.1', 'origin.2')

        self.register(*classes)

        self.assertEqual({'origin.1': 'origin.1', 'origin.2': 'origin.2'}, self.register._aliases)
        self.assertEqual({'origin.1': 'origin.1', 'origin.2': 'origin.2'}, self.register._origins)

    def test_register__with_prefix_with_class(self) -> None:
        classes = [Class, ClassChild]
        expected_aliases = {
            'tests.custom_classes.Class': 'some.classes.Class',
            'tests.custom_classes.ClassChild': 'some.classes.ClassChild',
        }
        expected_origins = {
            'some.classes.Class': 'tests.custom_classes.Class',
            'some.classes.ClassChild': 'tests.custom_classes.ClassChild',
        }

        self.register(*classes, prefix='some.classes')

        self.assertEqual(expected_aliases, self.register._aliases)
        self.assertEqual(expected_origins, self.register._origins)

    def test_register_aliases(self) -> None:
        aliases = (('origin.1', 'alias.1'), ('origin.2', 'alias.2'))

        self.register(*aliases)

        self.assertEqual({'origin.1': 'alias.1', 'origin.2': 'alias.2'}, self.register._aliases)
        self.assertEqual({'alias.1': 'origin.1', 'alias.2': 'origin.2'}, self.register._origins)

    def test_register__alias_duplicates(self) -> None:
        self.register._aliases = {'origin': 'alias'}
        self.register._origins = {'alias': 'origin'}
        alias = ('origin.1', 'alias')

        self.assertRaises(ValueError, self.register, alias, force=False)

    def test_register__origin_duplicates(self) -> None:
        self.register._aliases = {'origin': 'alias'}
        self.register._origins = {'alias': 'origin'}
        alias = ('origin', 'alias.1')

        self.assertRaises(ValueError, self.register, alias, force=False)

    @patch('smartparams.register.warnings')
    def test_register__duplicates(self, warnings: Mock) -> None:
        self.register._aliases = {'origin.1': 'alias.1', 'origin.2': 'alias.2'}
        self.register._origins = {'alias.1': 'origin.1', 'alias.2': 'origin.2'}
        alias = ('origin.1', 'alias.2')

        self.register(alias)

        self.assertEqual({'origin.1': 'alias.2'}, self.register._aliases)
        self.assertEqual({'alias.2': 'origin.1'}, self.register._origins)
        warnings.warn.assert_called()

    @patch('smartparams.register.warnings')
    def test_register__duplicates_no_warning(self, warnings: Mock) -> None:
        self.register._aliases = {'origin.1': 'alias.1', 'origin.2': 'alias.2'}
        self.register._origins = {'alias.1': 'origin.1', 'alias.2': 'origin.2'}
        alias = ('origin.1', 'alias.2')

        self.register(alias, force=True)

        self.assertEqual({'origin.1': 'alias.2'}, self.register._aliases)
        self.assertEqual({'alias.2': 'origin.1'}, self.register._origins)
        warnings.warn.assert_not_called()

    def test_register__smart_option(self) -> None:
        self.register(Class, option='smart')

        self.assertEqual({'tests.custom_classes.Class:Smart': 'Class'}, self.register._aliases)

    def test_register__type_option(self) -> None:
        self.register(Class, option='type')

        self.assertEqual({'tests.custom_classes.Class:Type': 'Class'}, self.register._aliases)

    def test_register__unknown_option(self) -> None:
        self.assertRaises(ValueError, self.register, Class, option='unknown')

    def test_register__raise(self) -> None:
        self.assertRaises(TypeError, self.register, 5)

    def test_register__no_str_alias__raise(self) -> None:
        self.assertRaises(TypeError, self.register, ('class', 5))

    def test_register__no_str_and_callable_origin__raise(self) -> None:
        self.assertRaises(TypeError, self.register, (5, 'alias'))

    def test_register__tuple_len__raise(self) -> None:
        self.assertRaises(ValueError, self.register, ('class', 'alias', 'unknown'))
