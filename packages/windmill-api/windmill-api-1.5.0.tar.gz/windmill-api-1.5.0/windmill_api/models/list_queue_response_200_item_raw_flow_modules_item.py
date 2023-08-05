from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.list_queue_response_200_item_raw_flow_modules_item_input_transform import (
    ListQueueResponse200ItemRawFlowModulesItemInputTransform,
)
from ..models.list_queue_response_200_item_raw_flow_modules_item_value import (
    ListQueueResponse200ItemRawFlowModulesItemValue,
)

T = TypeVar("T", bound="ListQueueResponse200ItemRawFlowModulesItem")


@attr.s(auto_attribs=True)
class ListQueueResponse200ItemRawFlowModulesItem:
    """
    Attributes:
        input_transform (ListQueueResponse200ItemRawFlowModulesItemInputTransform):
        value (ListQueueResponse200ItemRawFlowModulesItemValue):
    """

    input_transform: ListQueueResponse200ItemRawFlowModulesItemInputTransform
    value: ListQueueResponse200ItemRawFlowModulesItemValue
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
        input_transform = ListQueueResponse200ItemRawFlowModulesItemInputTransform.from_dict(d.pop("input_transform"))

        value = ListQueueResponse200ItemRawFlowModulesItemValue.from_dict(d.pop("value"))

        list_queue_response_200_item_raw_flow_modules_item = cls(
            input_transform=input_transform,
            value=value,
        )

        list_queue_response_200_item_raw_flow_modules_item.additional_properties = d
        return list_queue_response_200_item_raw_flow_modules_item

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
