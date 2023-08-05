from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.flow_preview_value_modules_item_input_transform import FlowPreviewValueModulesItemInputTransform
from ..models.flow_preview_value_modules_item_value import FlowPreviewValueModulesItemValue

T = TypeVar("T", bound="FlowPreviewValueModulesItem")


@attr.s(auto_attribs=True)
class FlowPreviewValueModulesItem:
    """
    Attributes:
        input_transform (FlowPreviewValueModulesItemInputTransform):
        value (FlowPreviewValueModulesItemValue):
    """

    input_transform: FlowPreviewValueModulesItemInputTransform
    value: FlowPreviewValueModulesItemValue
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
        input_transform = FlowPreviewValueModulesItemInputTransform.from_dict(d.pop("input_transform"))

        value = FlowPreviewValueModulesItemValue.from_dict(d.pop("value"))

        flow_preview_value_modules_item = cls(
            input_transform=input_transform,
            value=value,
        )

        flow_preview_value_modules_item.additional_properties = d
        return flow_preview_value_modules_item

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
