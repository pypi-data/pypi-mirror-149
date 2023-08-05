from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.input_transform_type import InputTransformType
from ..types import UNSET, Unset

T = TypeVar("T", bound="InputTransform")


@attr.s(auto_attribs=True)
class InputTransform:
    """
    Attributes:
        type (Union[Unset, InputTransformType]):
        step (Union[Unset, float]):
        value (Union[Unset, Any]):
        expr (Union[Unset, str]):
    """

    type: Union[Unset, InputTransformType] = UNSET
    step: Union[Unset, float] = UNSET
    value: Union[Unset, Any] = UNSET
    expr: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        step = self.step
        value = self.value

        expr = self.expr

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type is not UNSET:
            field_dict["type"] = type
        if step is not UNSET:
            field_dict["step"] = step
        if value is not UNSET:
            field_dict["value"] = value
        if expr is not UNSET:
            field_dict["expr"] = expr

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _type = d.pop("type", UNSET)
        type: Union[Unset, InputTransformType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = InputTransformType(_type)

        step = d.pop("step", UNSET)

        value = d.pop("value", UNSET)

        expr = d.pop("expr", UNSET)

        input_transform = cls(
            type=type,
            step=step,
            value=value,
            expr=expr,
        )

        input_transform.additional_properties = d
        return input_transform

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
