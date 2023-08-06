from __future__ import annotations

import abc
from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, Field, root_validator

from igenius_adapters_sdk.entities import data, uri


class JoinType(str, Enum):
    INNER = "inner"
    LEFT_OUTER = "left-outer"
    RIGHT_OUTER = "right-outer"


class JoinPart(BaseModel):
    from_: From
    on: uri.AttributeUri


class Join(BaseModel):
    left: JoinPart
    right: JoinPart
    type: JoinType  # noqa: A003


From = Union[uri.CollectionUri, Join]
# see https://pydantic-docs.helpmanual.io/usage/postponed_annotations/#self-referencing-models
JoinPart.update_forward_refs()


class AliasableQueryType(str, Enum):
    WITH = "with_query"
    TEMP = "temporary_table"
    STATEMENT = "statement"


class AliasableQuery(BaseModel):
    alias: str
    query: BaseQuery
    type: AliasableQueryType = AliasableQueryType.WITH


Subqueries = List[AliasableQuery]


class BaseQuery(BaseModel, abc.ABC):
    from_: Optional[From]
    where: Optional[data.WhereExpression]
    order_by: Optional[List[data.OrderByAttribute]]
    limit: Optional[int] = Field(None, ge=0)
    offset: Optional[int] = Field(None, ge=0)
    # If a template is provided, the previous fields will be ignored
    template: Optional[data.NamedSqlTemplate] = None
    subqueries: Optional[Subqueries] = None


# see https://github.com/samuelcolvin/pydantic/issues/1298
AliasableQuery.update_forward_refs()


class SelectQuery(BaseQuery):
    attributes: List[Union[data.ProjectionAttribute, data.StaticValueAttribute]]
    distinct: bool = False


Aggregations = List[Union[data.CustomColumnAttribute, data.AggregationAttribute, data.StaticValueAttribute]]


class AggregationQuery(BaseQuery):
    aggregations: Aggregations


class GroupByQuery(BaseQuery):
    aggregations: Aggregations
    groups: List[data.BinningAttribute]
    bin_interpolation: Optional[bool] = None

    @root_validator
    def bin_interpolation_flag_validator(cls, values):
        flag = values.get("bin_interpolation")
        groups = values.get("groups")
        has_function_params = any([att.function_uri.function_params is not None for att in groups])
        if flag is None and has_function_params:
            values["bin_interpolation"] = True
        elif flag is True and not has_function_params:
            raise ValueError("bin_interpolation flag applys to binning attributes only")
        return values


Query = Union[GroupByQuery, AggregationQuery, SelectQuery]
