from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.flow_module_input_transform import FlowModuleInputTransform
from ..models.flow_module_value import FlowModuleValue

T = TypeVar("T", bound="FlowModule")


@attr.s(auto_attribs=True)
class FlowModule:
    """
    Attributes:
        input_transform (FlowModuleInputTransform):
        value (FlowModuleValue):
    """

    input_transform: FlowModuleInputTransform
    value: FlowModuleValue
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        input_transform = self.input_transform.to_dict()

        value = self.value.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "input_transform": input_transform,
                "value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        input_transform = FlowModuleInputTransform.from_dict(d.pop("input_transform"))

        value = FlowModuleValue.from_dict(d.pop("value"))

        flow_module = cls(
            input_transform=input_transform,
            value=value,
        )

        flow_module.additional_properties = d
        return flow_module

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
