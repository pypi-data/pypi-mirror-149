""" Tools to find the name of the Query Object parameter by its type

In JessiQL, the query argument can have any name.
It is found by its type: "QueryObjectInput" (defined as const QUERY_OBJECT_INPUT_NAME)
"""

import graphql
from typing import Optional


# Input type name for JessiQL Query
# In JessiQL, the query object argument can have any name. It's located by its type.
QUERY_OBJECT_INPUT_NAME = 'QueryObjectInput'

# Object type for JessiQL Query
QUERY_OBJECT_NAME = 'QueryObject'


def get_query_argument_name_for(field_def: graphql.GraphQLField, *, query_object_type_name: str = None) -> Optional[str]:
    """ Get the name of the `query` argument (found by its type)

    Example:
        '''
        type Query {
            users (q: QueryObjectInput): [User!]
            posts (query: QueryObjectInput): [Post!]
        }
        '''

        get_query_argument_name_for(users) -> 'q'
        get_query_argument_name_for(posts) -> 'query'

    Args:
        field_def: Field definition.
            Example: graphql.utilities.type_info.get_field_def(info.schema, info.parent_type, field_node)
    Returns:
        argument name (str), or None if not found.
    """
    # Default override?
    # NOTE: intentionally NOT provided as a default value so that you can patch the module
    query_object_input_name = query_object_type_name or QUERY_OBJECT_INPUT_NAME

    # Find it
    for arg_name, arg in field_def.args.items():
        field_type = unwrap_type(arg.type)
        if field_type.name == query_object_input_name:  # type: ignore[union-attr]
            return arg_name
    else:
        return None


def has_query_argument(field_def: graphql.GraphQLField) -> bool:
    """ Test whether the field has a `query` argument (found by its type) """
    return get_query_argument_name_for(field_def) is not None


unwrap_type = graphql.get_named_type  # Unwrap GraphQL wrapper types (List, NonNull, etc)
