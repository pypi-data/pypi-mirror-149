from typing import Any, Literal, TypedDict, Union

__all__ = [
    "RFC6902_OPERATION_OBJECT_ADD",
    "RFC6902_OPERATION_OBJECT_REMOVE",
    "RFC6902_OPERATION_OBJECT_REPLACE",
    "RFC6902_OPERATION_OBJECT_MOVE",
    "RFC6902_OPERATION_OBJECT_COPY",
    "RFC6902_OPERATION_OBJECT_TEST",
    "RFC6902_OPERATION_OBJECT",
]

RFC6902_OPERATIONS = Literal["add", "remove", "replace", "move", "copy", "test"]
RFC6902_OPERATION_OBJECT_BASE = TypedDict(
    "RFC6902_OPERATION_OBJECT_BASE",
    {
        "op": RFC6902_OPERATIONS,
        "path": str,
    }
)
RFC6902_OPERATION_OBJECT_ADD = TypedDict(
    "RFC6902_OPERATION_OBJECT_ADD",
    {
        "op": Literal["add"],
        "path": str,
        "value": Any
    }
)
RFC6902_OPERATION_OBJECT_REMOVE = TypedDict(
    "RFC6902_OPERATION_OBJECT_REMOVE",
    {
        "op": Literal["remove"],
        "path": str
    }
)
RFC6902_OPERATION_OBJECT_REPLACE = TypedDict(
    "RFC6902_OPERATION_OBJECT_REPLACE",
    {
        "op": Literal["replace"],
        "path": str,
        "value": Any
    }
)
RFC6902_OPERATION_OBJECT_MOVE = TypedDict(
    "RFC6902_OPERATION_OBJECT_MOVE",
    {
        "op": Literal["move"],
        "path": str,
        "from": str
    }
)
RFC6902_OPERATION_OBJECT_COPY = TypedDict(
    "RFC6902_OPERATION_OBJECT_COPY",
    {
        "op": Literal["copy"],
        "path": str,
        "from": str
    }
)
RFC6902_OPERATION_OBJECT_TEST = TypedDict(
    "RFC6902_OPERATION_OBJECT_TEST",
    {
        "op": Literal["test"],
        "path": str,
        "value": Any
    }
)
RFC6902_OPERATION_OBJECT = Union[
    RFC6902_OPERATION_OBJECT_ADD,
    RFC6902_OPERATION_OBJECT_REMOVE,
    RFC6902_OPERATION_OBJECT_REPLACE,
    RFC6902_OPERATION_OBJECT_MOVE,
    RFC6902_OPERATION_OBJECT_COPY,
    RFC6902_OPERATION_OBJECT_TEST,
]
