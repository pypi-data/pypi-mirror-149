from unittest.mock import Mock, patch

from smartparams.register import SmartRegister
from tests.custom_classes import Class, ClassChild
from tests.unit import UnitCase


class TestRegisterCase(UnitCase):
    def setUp(self) -> None:
        self.register = SmartRegister()

    def test_register__classes(self) -> None:
        classes = ('origin.1', 'origin.2')

        self.register(classes)

        self.assertEqual({'origin.1': 'origin.1', 'origin.2': 'origin.2'}, self.register._aliases)
        self.assertEqual({'origin.1': 'origin.1', 'origin.2': 'origin.2'}, self.register._origins)

    def test_register__with_prefix_with_class(self) -> None:
        aliases = [Class, ClassChild]
        expected_aliases = {
            'tests.custom_classes.Class': 'some.classes.Class',
            'tests.custom_classes.ClassChild': 'some.classes.ClassChild',
        }
        expected_origins = {
            'some.classes.Class': 'tests.custom_classes.Class',
            'some.classes.ClassChild': 'tests.custom_classes.ClassChild',
        }

        self.register(aliases, prefix='some.classes')

        self.assertEqual(expected_aliases, self.register._aliases)
        self.assertEqual(expected_origins, self.register._origins)

    def test_register_aliases(self) -> None:
        aliases = {'origin.1': 'alias.1', 'origin.2': 'alias.2'}

        self.register(aliases)

        self.assertEqual({'origin.1': 'alias.1', 'origin.2': 'alias.2'}, self.register._aliases)
        self.assertEqual({'alias.1': 'origin.1', 'alias.2': 'origin.2'}, self.register._origins)

    def test_register__alias_duplicates(self) -> None:
        self.register._aliases = {'origin': 'alias'}
        self.register._origins = {'alias': 'origin'}
        aliases = {'origin.1': 'alias'}

        self.assertRaises(ValueError, self.register, aliases, force=False)

    def test_register__origin_duplicates(self) -> None:
        self.register._aliases = {'origin': 'alias'}
        self.register._origins = {'alias': 'origin'}
        aliases = {'origin': 'alias.1'}

        self.assertRaises(ValueError, self.register, aliases, force=False)

    @patch('smartparams.register.warnings')
    def test_register__duplicates(self, warnings: Mock) -> None:
        self.register._aliases = {'origin.1': 'alias.1', 'origin.2': 'alias.2'}
        self.register._origins = {'alias.1': 'origin.1', 'alias.2': 'origin.2'}
        aliases = {'origin.1': 'alias.2'}

        self.register(aliases)

        self.assertEqual({'origin.1': 'alias.2'}, self.register._aliases)
        self.assertEqual({'alias.2': 'origin.1'}, self.register._origins)
        warnings.warn.assert_called()

    @patch('smartparams.register.warnings')
    def test_register__duplicates_no_warning(self, warnings: Mock) -> None:
        self.register._aliases = {'origin.1': 'alias.1', 'origin.2': 'alias.2'}
        self.register._origins = {'alias.1': 'origin.1', 'alias.2': 'origin.2'}
        aliases = {'origin.1': 'alias.2'}

        self.register(aliases, force=True)

        self.assertEqual({'origin.1': 'alias.2'}, self.register._aliases)
        self.assertEqual({'alias.2': 'origin.1'}, self.register._origins)
        warnings.warn.assert_not_called()

    def test_register__raise(self) -> None:
        self.assertRaises(TypeError, self.register, Mock())
