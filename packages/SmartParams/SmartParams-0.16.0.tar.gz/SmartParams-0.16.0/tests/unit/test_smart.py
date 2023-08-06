from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union
from unittest.mock import Mock, patch

from smartparams.exceptions import (
    MissingArgument,
    ObjectInvalidOptionError,
    ObjectNotRegistered,
    UnexpectedTypeOptionArguments,
)
from smartparams.smart import Smart
from tests.custom_classes import Class, some_function
from tests.unit import UnitCase


class TestSmart(UnitCase):
    def test(self) -> None:
        smart: Smart = Smart()

        self.assertIs(smart.type, dict)

    def test__class(self) -> None:
        smart = Smart(Class)

        self.assertIs(smart.type, Class)

    def test__smart_init(self) -> None:
        smart_init = Mock()

        smart = Smart(Mock(__smart_init__=smart_init))

        smart_init.assert_called_once_with(smart)

    def test__function(self) -> None:
        smart = Smart(some_function)

        self.assertIs(smart.type, None)

    def test__lambda(self) -> None:
        smart = Smart(lambda x: x)

        self.assertIs(smart.type, Any)

    def test__not_callable(self) -> None:
        self.assertRaises(TypeError, Smart, 'not_callable')


class TestSmartCallCase(UnitCase):
    def setUp(self) -> None:
        self.smart = Smart(Class, arg1='arg1', arg2=10)

    def test_call(self) -> None:
        obj = self.smart()

        self.assertIsInstance(obj, Class)
        self.assertEqual('arg1', obj.arg1)
        self.assertEqual(10, obj.arg2)

    def test_call__with_dict(self) -> None:
        smart = Smart(Class)

        obj = smart('a1', arg2=15)

        self.assertIsInstance(obj, Class)
        self.assertEqual('a1', obj.arg1)
        self.assertEqual(15, obj.arg2)

    def test_call__with_duplicated_dict(self) -> None:
        smart = Smart(Class, arg1='arg1')

        self.assertRaises(MissingArgument, smart, 'a1')

    def test_call__without_class(self) -> None:
        smart: Smart = Smart()

        obj = smart()

        self.assertIsInstance(obj, dict)


class TestSmartDictCase(UnitCase):
    def setUp(self) -> None:
        self.smart: Smart = Smart(arg1='arg1', arg2=['arg2'], arg3={'arg31': 'a31', 'arg32': 'a32'})

    def test_dict(self) -> None:
        expected = {'arg1': 'arg1', 'arg2': ['arg2'], 'arg3': {'arg31': 'a31', 'arg32': 'a32'}}

        params = self.smart.dict

        self.assertEqual(expected, params)
        self.assertIsInstance(self.smart._params, dict)
        self.assertIsNot(self.smart._params, params)

    def test_keys(self) -> None:
        keys = self.smart.keys()

        self.assertTupleEqual(('arg1', 'arg2', 'arg3'), tuple(keys))

    def test_keys__flatten(self) -> None:
        value = self.smart.keys(flatten=True)

        self.assertTupleEqual(('arg1', 'arg2', 'arg3.arg31', 'arg3.arg32'), tuple(value))

    def test_keys__flatten_pattern(self) -> None:
        value = self.smart.keys(flatten=True, pattern='arg[1,3].*')

        self.assertTupleEqual(('arg1', 'arg3.arg31', 'arg3.arg32'), tuple(value))

    def test_values(self) -> None:
        expected = ('arg1', ['arg2'], {'arg31': 'a31', 'arg32': 'a32'})

        actual = self.smart.values()

        self.assertTupleEqual(expected, tuple(actual))

    def test_items(self) -> None:
        expected = (
            ('arg1', 'arg1'),
            ('arg2', ['arg2']),
            ('arg3', {'arg31': 'a31', 'arg32': 'a32'}),
        )

        actual = self.smart.items()

        self.assertTupleEqual(expected, tuple(actual))

    def test_get(self) -> None:
        value = self.smart.get('arg3.arg31')

        self.assertEqual('a31', value)

    def test_set(self) -> None:
        new_value = 'argument31'

        value = self.smart.set('arg3.arg31', new_value)

        self.assertEqual('argument31', value)
        self.assertEqual('argument31', self.smart.dict['arg3']['arg31'])
        self.assertEqual('a32', self.smart.dict['arg3']['arg32'])

    def test_pop(self) -> None:
        value = self.smart.pop('arg3.arg31')

        self.assertEqual('a31', value)
        self.assertFalse('arg3' in self.smart.dict['arg3'])

    def test_map(self) -> None:
        function = Mock(return_value='argument31')

        value = self.smart.map('arg3.arg31', function)

        self.assertEqual('argument31', value)
        self.assertEqual('argument31', self.smart.dict['arg3']['arg31'])
        self.assertEqual('a32', self.smart.dict['arg3']['arg32'])

    def test_remove(self) -> None:
        actual = self.smart.remove('arg2', 'arg3.arg31')

        self.assertEqual(Smart(arg2=['arg2'], arg3={'arg31': 'a31'}), actual)
        self.assertEqual(Smart(arg1='arg1', arg3={'arg32': 'a32'}), self.smart)

    def test_keep(self) -> None:
        actual = self.smart.keep('arg2', 'arg3.arg31')

        self.assertEqual(Smart(arg1='arg1', arg3={'arg32': 'a32'}), actual)
        self.assertEqual(Smart(arg2=['arg2'], arg3={'arg31': 'a31'}), self.smart)

    def test_keep__required(self) -> None:
        self.assertRaises(KeyError, self.smart.keep, 'arg2', 'arg3.arg31', 'unknown', required=True)

    def test_keep__no_required(self) -> None:
        actual = self.smart.keep('arg2', 'arg3.arg31', 'unknown', required=False)

        self.assertEqual(Smart(arg1='arg1', arg3={'arg32': 'a32'}), actual)
        self.assertEqual(Smart(arg2=['arg2'], arg3={'arg31': 'a31'}), self.smart)

    @patch('smartparams.smart.load_data')
    def test_update(self, load_data: Mock) -> None:
        dictionary = {'arg1': {'nested1': 'argument1'}, 'arg3': {'arg31': 'argument31'}}
        load_data.return_value = dictionary
        test_cases: List[Tuple[Union['Smart', Dict[str, Any], List[str], Path], str]] = [
            (Smart(**dictionary), "smart"),
            (dictionary, "dict"),
            (['arg3.arg31=argument31', 'arg1={"nested1": "argument1"}'], "list"),
            (Path('path/to/file.yaml'), "path"),
        ]

        for source, msg in test_cases:
            smart: Smart = deepcopy(self.smart)

            with self.subTest(msg=msg):
                smart.update_from(source)

                self.assertTrue('arg1' in smart.dict)
                self.assertTrue('arg2' in smart.dict)
                self.assertTrue('arg3' in smart.dict)
                self.assertEqual({'nested1': 'argument1'}, smart.dict['arg1'])
                self.assertListEqual(['arg2'], smart.dict['arg2'])
                self.assertEqual('argument31', smart.dict['arg3']['arg31'])
                self.assertEqual('a32', smart.dict['arg3']['arg32'])

    @patch('smartparams.smart.load_data')
    def test_update__not_override(self, load_data: Mock) -> None:
        dictionary = {'arg1': {'nested1': 'aa1'}, 'arg3': {'arg31': 'aa31'}, 'arg4': {'a4': 'aa4'}}
        load_data.return_value = dictionary
        test_cases: List[Tuple[Union['Smart', Dict[str, Any], List[str], Path], str]] = [
            (Smart(**dictionary), "smart"),
            (dictionary, "dict"),
            (['arg3.arg31=argument31', 'arg1={"nested1": "aa1"}', 'arg4={"a4": "aa4"}'], "list"),
            (Path('path/to/file.yaml'), "path"),
        ]

        for source, msg in test_cases:
            smart: Smart = deepcopy(self.smart)

            with self.subTest(msg=msg):
                smart.update_from(source, override=False)

                self.assertTrue('arg1' in smart.dict)
                self.assertTrue('arg2' in smart.dict)
                self.assertTrue('arg3' in smart.dict)
                self.assertEqual('arg1', smart.dict['arg1'])
                self.assertListEqual(['arg2'], smart.dict['arg2'])
                self.assertEqual('a31', smart.dict['arg3']['arg31'])
                self.assertEqual('a32', smart.dict['arg3']['arg32'])
                self.assertEqual({'a4': 'aa4'}, smart.dict['arg4'])

    def test_update__not_required(self) -> None:
        dictionary = {'arg1': {'nested1': 'aa1'}}
        expected = deepcopy(self.smart.dict)

        self.smart.update_from(dictionary, source_key='arg2', required=False)

        self.assertEqual(expected, self.smart.dict)

    def test_update__with_source_key(self) -> None:
        dictionary = {'arg': {'nested': ['arg3.arg31=argument31', 'arg1={"nested1": "argument1"}']}}

        self.smart.update_from(dictionary, source_key='arg.nested')

        self.assertTrue('arg1' in self.smart.dict)
        self.assertTrue('arg2' in self.smart.dict)
        self.assertTrue('arg3' in self.smart.dict)
        self.assertEqual({'nested1': 'argument1'}, self.smart.dict['arg1'])
        self.assertListEqual(['arg2'], self.smart.dict['arg2'])
        self.assertEqual('argument31', self.smart.dict['arg3']['arg31'])
        self.assertEqual('a32', self.smart.dict['arg3']['arg32'])

    def test_update__with_target_key(self) -> None:
        dictionary = {'arg31': 'argument31'}

        self.smart.update_from(dictionary, target_key='arg3')

        self.assertTrue('arg1' in self.smart.dict)
        self.assertTrue('arg2' in self.smart.dict)
        self.assertTrue('arg3' in self.smart.dict)
        self.assertEqual('argument31', self.smart.dict['arg3']['arg31'])
        self.assertEqual('a32', self.smart.dict['arg3']['arg32'])

    def test_update__with_key_error(self) -> None:
        dictionary = {'arg': {'nested': ['arg3.arg31 argument31']}}

        self.assertRaises(RuntimeError, self.smart.update_from, dictionary, 'arg.nested')

    def test_update__unknown(self) -> None:
        source = set()  # type: ignore

        self.assertRaises(TypeError, self.smart.update_from, source)

    def test_copy(self) -> None:
        smart = self.smart.copy()

        self.assertFalse(smart is self.smart)
        self.assertFalse(smart._params is self.smart._params)
        self.assertTrue(smart._params['arg2'] is self.smart._params['arg2'])
        self.assertEqual(smart._trace, self.smart._trace)
        self.assertTrue(smart._callable is self.smart._callable)

    def test_copy__deep(self) -> None:
        smart = self.smart.copy(deep=True)

        self.assertFalse(smart is self.smart)
        self.assertFalse(smart._params is self.smart._params)
        self.assertFalse(smart._params['arg2'] is self.smart._params['arg2'])
        self.assertEqual(smart._trace, self.smart._trace)
        self.assertTrue(smart._callable is self.smart._callable)


class TestSmartNormalizeCase(UnitCase):
    def setUp(self) -> None:
        self.smart: Smart = Smart(a=dict(b=dict(c=5)))

    def test_init(self) -> None:
        smart: Smart = Smart(**{'a.b.c': 5})

        self.assertEqual(self.smart, smart)

    def test_set(self) -> None:
        actual = self.smart.set('a.b', {'d.e': 10})

        self.assertEqual({'d': {'e': 10}}, actual)
        self.assertEqual({'a': {'b': {'d': {'e': 10}}}}, self.smart._params)

    def test_map(self) -> None:
        actual = self.smart.map('a.b', lambda x: {'d.e': 10})

        self.assertEqual({'d': {'e': 10}}, actual)
        self.assertEqual({'a': {'b': {'d': {'e': 10}}}}, self.smart._params)


class TestSmartInitCase(UnitCase):
    def setUp(self) -> None:
        self.class_name = f"{Class.__module__}.{Class.__qualname__}"
        self.params = dict(
            smart_dict={'class': 'Smart'},
            smart={'class': self.class_name + ':Smart', 'arg1': 'arg1', 'arg2': 10},
            type={'class': self.class_name + ':Type'},
            object={'class': self.class_name, 'arg1': 'arg1', 'arg2': 10},
            value=21,
        )
        self.smart: Smart = Smart(**self.params)

    def tearDown(self) -> None:
        self.smart.register.reset()

    def test_init(self) -> None:
        obj = self.smart.init()

        self.assertIsInstance(obj, dict)
        self.assertEqual(('smart_dict', 'smart', 'type', 'object', 'value'), tuple(obj.keys()))

    def test_init__persist(self) -> None:
        obj = self.smart.init('object')

        self.assertIs(self.smart.get('object'), obj)
        self.assertIsInstance(self.smart.get('object'), Class)
        self.assertTrue('object' in self.smart.dict)

    def test_init__not_persist(self) -> None:
        obj = self.smart.init('object', persist=False)

        self.assertIsNot(self.smart.get('object'), obj)
        self.assertIsInstance(self.smart.get('object'), dict)
        self.assertTrue('object' in self.smart.dict)

    def test_init__any(self) -> None:
        result = self.smart.init('value')

        self.assertEqual(21, result)

    def test_init__smart_dict(self) -> None:
        result = self.smart.init('smart_dict')

        self.assertIsInstance(result, Smart)
        self.assertIs(result.type, dict)

    def test_init__smart(self) -> None:
        result = self.smart.init('smart')

        self.assertIsInstance(result, Smart)
        self.assertIs(result.type, Class)

    def test_init__type(self) -> None:
        result = self.smart.init('type')

        self.assertIs(result, Class)

    def test_init__type__raises(self) -> None:
        self.smart.set('type.argument', 10)

        self.assertRaises(UnexpectedTypeOptionArguments, self.smart.init, 'type')

    def test_init__unknown(self) -> None:
        self.smart.map('smart.class', lambda x: x + 'suffix')

        self.assertRaises(ObjectInvalidOptionError, self.smart.init, 'smart')

    def test_init__object(self) -> None:
        result = self.smart.init('object')

        self.assertIsInstance(result, Class)

    def test_init__with_aliases(self) -> None:
        self.smart.allow_only_registered_classes = True
        self.smart.register({self.class_name: 'Class'})
        self.smart.set('object.class', 'Class')

        result = self.smart.init('object')

        self.assertIsInstance(result, Class)

    def test_init__with_aliases_not_used(self) -> None:
        self.smart.register({self.class_name: 'Class'})

        result = self.smart.init('object')

        self.assertIsInstance(result, Class)

    def test_init__with_aliases_error(self) -> None:
        self.smart.allow_only_registered_classes = True
        self.smart.register({self.class_name: 'Class'})

        self.assertRaises(ObjectNotRegistered, self.smart.init, 'object')
