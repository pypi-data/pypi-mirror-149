from typing import Callable

import pytest

from dart_context.dart_context import DartConfig


class PrimitiveConfig(DartConfig):
    test_field_1 = None
    test_field_2 = None

    def set_field_1(self, value) -> None:
        self.test_field_1 = value

    def set_field_2(self, value) -> None:
        self.test_field_2 = value

    def sub_config_fields(self) -> dict[str, DartConfig]:
        return {}

    def primitive_fields(self) -> dict[str, (Callable[[], any], Callable[[any], None])]:
        return {'test-field-1': (lambda: self.test_field_1, lambda x: self.set_field_1(x)), 'test-field-2': (lambda: self.test_field_2, lambda x: self.set_field_2(x))}


class SubConfigConfig(DartConfig):
    test_field_a: PrimitiveConfig = PrimitiveConfig()
    test_field_b = None

    def set_field_b(self, value) -> None:
        self.test_field_b = value

    def sub_config_fields(self) -> dict[str, DartConfig]:
        return {'test-field-a': self.test_field_a}

    def primitive_fields(self) -> dict[str, (Callable[[], any], Callable[[any], None])]:
        return {'test-field-b': (lambda: self.test_field_b, lambda x: self.set_field_b(x))}


def test_from_json_and_back():
    test_conf = SubConfigConfig()
    test_dict = {
        'test-field-a': {
            'test-field-1': 'world',
            'test-field-2': 234234
        },
        'test-field-b': 'hello'
    }
    assert test_conf.test_field_a.test_field_1 is None
    assert test_conf.test_field_a.test_field_2 is None
    assert test_conf.test_field_b is None

    test_conf.from_dict(test_dict)

    assert test_conf.test_field_a.test_field_1 is 'world'
    assert test_conf.test_field_a.test_field_2 is 234234
    assert test_conf.test_field_b is 'hello'

    res_dict = test_conf.to_dict()
    assert res_dict['test-field-a']['test-field-1'] is 'world'
    assert res_dict['test-field-a']['test-field-2'] is 234234
    assert res_dict['test-field-b'] is 'hello'
