from __future__ import annotations

import abc
import hashlib
from enum import Enum
from typing import Any, List, Optional, Tuple, Union

from pydantic import BaseModel, PrivateAttr, validator
from typing_extensions import Literal

from igenius_adapters_sdk.entities import attribute, numeric_binning, params, uri

SqlTemplate = Tuple[str, Optional[List[Any]]]  # e.g. ("A = ? AND B = ?", [1,"test"])
NamedSqlTemplate = Tuple[str, SqlTemplate]


class OrderByDirection(str, Enum):
    DESC = "desc"
    ASC = "asc"


class AliasableAttribute(BaseModel):
    alias: Optional[str] = None
    name: Optional[str] = None
    _shortened_alias: str = PrivateAttr()
    _original_alias: str = PrivateAttr()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if not self.alias:
            if self.name:
                self.alias = self.name
            else:
                raise ValueError("Alias not found.")
        object.__setattr__(self, "_original_alias", self.alias)
        object.__setattr__(
            self,
            "_shortened_alias",
            str(hashlib.md5(self.alias.encode("utf-8")).hexdigest()),
        )

    def switch_to_shortened_alias(self):
        self.alias = self._shortened_alias

    def get_original_alias(self):
        return self._original_alias

    def has_been_shortened(self):
        return self.alias != self._original_alias


class StaticValueAttribute(AliasableAttribute):
    value: str
    default_bin_interpolation: Optional[Any]


class BaseAttribute(AliasableAttribute, abc.ABC):
    attribute_uri: uri.AttributeUri


class ProjectionAttribute(BaseAttribute):
    pass


class OrderByAttribute(AliasableAttribute):
    direction: OrderByDirection = OrderByDirection.ASC


class FunctionUri(BaseModel):
    function_type: Literal["group_by", "aggregation"]
    function_uid: str
    function_params: Optional[Union[numeric_binning.BinningRules, attribute.StaticTypes]]

    @validator("function_uid")
    def check_uid_existence(cls, v, values):
        if "function_type" in values:
            if values["function_type"] == "group_by":
                attribute.GroupByFunction.from_uid(v)
            if values["function_type"] == "aggregation":
                attribute.AggregationFunction.from_uid(v)
        return v

    @validator("function_params")
    def check_binning_rules_consistency(cls, v, values):
        if v and values["function_uid"] == attribute.GroupByFunction.NUMERIC_BINNING.uid:
            if not isinstance(v, numeric_binning.BinningRules):
                raise ValueError("function_params does not contain BinningRules")
        return v


class AggregationAttribute(BaseAttribute):
    function_uri: FunctionUri
    default_bin_interpolation: Optional[Any]

    @validator("function_uri")
    def check_type(cls, v):
        if v and v.function_type and v.function_type != "aggregation":
            raise ValueError("Function type should be aggregation")
        return v


class CriteriaType(str, Enum):
    AND = "and"
    OR = "or"


class Expression(BaseModel):
    attribute_uri: uri.AttributeUri
    operator: str
    value: Any

    @validator("operator")
    def check_uid_existance(cls, v):
        params.ParamOperation.from_uid(v)
        return v

    @validator("value")
    def validate_operation_schema(cls, v, values):
        if "operator" in values:
            schema = params.ParamOperation.from_uid(values["operator"]).properties_schema
            operation_schema = params.OperationSchemas.from_jsonschema(schema)
            if v is None:
                v = {}
            if not isinstance(v, dict):
                key = next(iter(params.OperationPropertiesSchema.SingleValue.__fields__))
                v = {key: v}
            return operation_schema.model(**v).dict()
        return v


class MultiExpression(BaseModel):
    criteria: CriteriaType
    expressions: List[Union["MultiExpression", Expression]]


WhereExpression = Union[MultiExpression, Expression]
# see https://pydantic-docs.helpmanual.io/usage/postponed_annotations/#self-referencing-models
MultiExpression.update_forward_refs()


class AggregationOperations(BaseModel):
    family: Literal["AGGREGATION"] = "AGGREGATION"
    type: attribute.AggregationIDs


class BasicOperations(BaseModel):
    family: Literal["BASIC"] = "BASIC"
    type: Literal["+", "/", "*", "-"]


OperationDetails = Union[AggregationOperations, BasicOperations]


class CustomOperation(BaseModel):
    details: OperationDetails
    elements: CustomOperationElements


CustomOperationElements = List[Union[uri.AttributeUri, CustomOperation, int, float]]
# see https://pydantic-docs.helpmanual.io/usage/postponed_annotations/#self-referencing-models
CustomOperation.update_forward_refs()


class CustomColumnAttribute(AliasableAttribute):
    """ A Custom Column attribute is defined by either an operation or a template """

    name: str
    operation: Optional[CustomOperation] = None
    where: Optional[WhereExpression] = None
    template: Optional[NamedSqlTemplate] = None


class BinningAttribute(BaseAttribute):
    function_uri: FunctionUri

    @validator("function_uri")
    def check_type(cls, v):
        if v and v.function_type and v.function_type != "group_by":
            raise ValueError("Function type should be group_by")
        return v
