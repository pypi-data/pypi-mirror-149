""" Query Object: the "sort" operation """

from __future__ import annotations

from collections import abc
from typing import Any, Union, Optional
from dataclasses import dataclass

import itertools
import sqlalchemy as sa
import sqlalchemy.orm

from jessiql import exc
from jessiql.util.dataclasses import dataclass_notset
from jessiql.util.funcy import collecting
from jessiql.util.expressions import parse_dot_notation

from .base import OperationInputBase


@dataclass
class FilterQuery(OperationInputBase):
    """ Query Object operation: the "filter" operation

    Supports:
    * Column names
    * JSON sub-objects (via dot-notation)
    """
    # List of conditions: field conditions and/or boolean conditions
    conditions: list[FilterExpressionBase]

    @classmethod
    def from_query_object(cls, filter: dict):  # type: ignore[override]
        # Check types
        if not isinstance(filter, dict):
            raise exc.QueryObjectError(f'"filter" must be an object')

        # Construct
        conditions = cls._parse_input_fields(filter)
        return cls(conditions=conditions)

    def export(self) -> dict:
        res = {}
        for condition in self.conditions:
            res.update(condition.export())
        return res

    @classmethod
    @collecting
    def _parse_input_fields(cls, condition: dict) -> abc.Iterator[FilterExpressionBase]:
        # Iterate the object
        for key, value in condition.items():
            # If a key starts with $ ($and, $or, ...), it is a boolean expression
            if key.startswith('$'):
                yield cls._parse_input_boolean_expression(key, value)
            # If not, then it's a field expression
            else:
                yield from cls._parse_input_field_expressions(key, value)

    @classmethod
    def _parse_input_field_expressions(cls, field_name: str, value: Union[dict[str, Any], Any]):
        name, sub_path = parse_dot_notation(field_name)

        # If the value is not a dict, it's a shortcut: { key: value }
        if not isinstance(value, dict):
            yield FieldFilterExpression(field=name, operator='$eq', value=value, sub_path=sub_path)  # type: ignore[call-arg]
        # If the value is a dict, every item will be an operator and an operand
        else:
            for operator, operand in value.items():
                yield FieldFilterExpression(field=name, operator=operator, value=operand, sub_path=sub_path)  # type: ignore[call-arg]

    @classmethod
    def _parse_input_boolean_expression(cls, operator: str, conditions: Union[dict, list[dict]]):
        # Check types
        # $not is the only unary operator
        if operator == '$not':
            if not isinstance(conditions, dict):
                raise exc.QueryObjectError(f"{operator}'s operand must be an object")

            conditions = [conditions]
        # Every other operator receives a list of conditions
        else:
            if not isinstance(conditions, list):
                raise exc.QueryObjectError(f"{operator}'s operand must be an array")

        # Construct
        return BooleanFilterExpression(
            operator=operator,
            clauses=list(itertools.chain.from_iterable(
                cls._parse_input_fields(condition)
                for condition in conditions
            ))
        )


class FilterExpressionBase:
    """ Base class for filter expressions """

    def export(self) -> dict:
        raise NotImplementedError


@dataclass_notset('property', 'is_array', 'is_json')
@dataclass
class FieldFilterExpression(FilterExpressionBase):
    """ A filter for a field

    Example:
        { age: {$gt: 18} }
    """
    field: str
    operator: str
    value: Any

    # Parsed dot-notation: "field.sub.sub"
    # Applicable to JSON fields
    sub_path: Optional[tuple[str, ...]]

    # Populated when resolved by resolve_filtering_expression()
    property: sa.orm.ColumnProperty
    is_array: bool
    is_json: bool

    __slots__ = 'name', 'operator', 'value', 'sub_path', 'property', 'is_array', 'is_json'

    def export(self) -> dict:
        return {self._field_expression(): {self.operator: self.value}}

    def _field_expression(self):
        if not self.sub_path:
            return self.field
        else:
            return '.'.join((self.name,) + self.sub_path)


@dataclass
class BooleanFilterExpression(FilterExpressionBase):
    """ A filter with a boolean expression

    Example:
        { $or: [ ..., ... ] }
    """
    operator: str
    clauses: list[FilterExpressionBase]

    __slots__ = 'operator', 'clauses'

    def export(self) -> dict:
        return {
            self.operator: [
                clause.export()
                for clause in self.clauses
            ]
        }
