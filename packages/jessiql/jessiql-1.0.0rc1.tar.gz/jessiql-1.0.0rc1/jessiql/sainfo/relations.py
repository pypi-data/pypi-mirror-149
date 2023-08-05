from __future__ import annotations

from sqlalchemy.orm import RelationshipProperty
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm.base import (
    ONETOMANY,
    MANYTOONE,
    MANYTOMANY,
)
from sqlalchemy.orm.dynamic import DynaLoader

try:
    # Python 3.9+
    from functools import cache
except ImportError:
    # Python 3.8
    from functools import lru_cache as cache

from jessiql.sainfo.names import model_name
from jessiql.typing import SAModelOrAlias, SAAttribute
from jessiql import exc


def resolve_relation_by_name(field_name: str, Model: SAModelOrAlias, *, where: str) -> InstrumentedAttribute:
    try:
        attribute = getattr(Model, field_name)
    except AttributeError as e:
        raise exc.InvalidRelationError(model_name(Model), field_name, where=where) from e

    # Check that it actually is a column
    if not is_relation(attribute):
        raise exc.InvalidColumnError(model_name(Model), field_name, where=where)

    # Done
    return attribute


# region: Relation Attribute types

@cache
def is_relation(attr: SAAttribute):
    return (
        is_relation_relationship(attr) or
        is_relation_dynamic_loader(attr)
    )


@cache
def is_relation_relationship(attribute: SAAttribute):
    return (
        isinstance(attribute, InstrumentedAttribute) and
        isinstance(attribute.property, RelationshipProperty) and
        not isinstance(attribute.property.strategy, DynaLoader)
    )


@cache
def is_relation_dynamic_loader(attribute: SAAttribute):
    return (
        isinstance(attribute, InstrumentedAttribute) and
        isinstance(attribute.property, RelationshipProperty) and
        isinstance(attribute.property.strategy, DynaLoader)
    )

# endregion

# region Relation Attribute info

@cache
def is_array(attribute: SAAttribute) -> bool:
    return attribute.property.uselist


@cache
def target_model(attribute: SAAttribute) -> type:
    return attribute.property.mapper.class_

# endregion
