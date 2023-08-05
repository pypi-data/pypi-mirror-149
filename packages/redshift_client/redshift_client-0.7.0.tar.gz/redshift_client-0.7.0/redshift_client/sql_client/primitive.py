from datetime import (
    datetime,
)
from fa_purity.frozen import (
    FrozenList,
)
from fa_purity.json.primitive.core import (
    is_primitive,
    Primitive,
)
from fa_purity.result import (
    Result,
    ResultE,
    UnwrapError,
)
from typing import (
    Callable,
    TypeVar,
    Union,
)


class InvalidType(Exception):
    pass


PrimitiveVal = Union[Primitive, datetime]

_A = TypeVar("_A")
_T = TypeVar("_T")
_R = TypeVar("_R")


def to_prim_val(raw: _T) -> ResultE[PrimitiveVal]:
    if is_primitive(raw) or isinstance(raw, datetime):
        return Result.success(raw)
    return Result.failure(
        InvalidType(f"Got {type(raw)}; expected a PrimitiveVal")
    )


def to_list_of(
    items: _A, assertion: Callable[[_T], ResultE[_R]]
) -> ResultE[FrozenList[_R]]:
    try:
        if isinstance(items, tuple):
            return Result.success(tuple(assertion(i).unwrap() for i in items))
        return Result.failure(InvalidType("Expected tuple"))
    except UnwrapError[FrozenList[_R], Exception] as err:
        return Result.failure(err.container.unwrap_fail())
