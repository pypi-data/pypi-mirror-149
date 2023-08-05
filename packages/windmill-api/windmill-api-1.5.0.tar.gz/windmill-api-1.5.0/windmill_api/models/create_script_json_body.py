from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.create_script_json_body_schema import CreateScriptJsonBodySchema
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateScriptJsonBody")


@attr.s(auto_attribs=True)
class CreateScriptJsonBody:
    """
    Attributes:
        path (str):
        summary (str):
        description (str):
        content (str):
        parent_hash (Union[Unset, str]):
        schema (Union[Unset, CreateScriptJsonBodySchema]):
        is_template (Union[Unset, bool]):
        lock (Union[Unset, List[str]]):
    """

    path: str
    summary: str
    description: str
    content: str
    parent_hash: Union[Unset, str] = UNSET
    schema: Union[Unset, CreateScriptJsonBodySchema] = UNSET
    is_template: Union[Unset, bool] = UNSET
    lock: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        summary = self.summary
        description = self.description
        content = self.content
        parent_hash = self.parent_hash
        schema: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.schema, Unset):
            schema = self.schema.to_dict()

        is_template = self.is_template
        lock: Union[Unset, List[str]] = UNSET
        if not isinstance(self.lock, Unset):
            lock = self.lock

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "path": path,
                "summary": summary,
                "description": description,
                "content": content,
            }
        )
        if parent_hash is not UNSET:
            field_dict["parent_hash"] = parent_hash
        if schema is not UNSET:
            field_dict["schema"] = schema
        if is_template is not UNSET:
            field_dict["is_template"] = is_template
        if lock is not UNSET:
            field_dict["lock"] = lock

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        path = d.pop("path")

        summary = d.pop("summary")

        description = d.pop("description")

        content = d.pop("content")

        parent_hash = d.pop("parent_hash", UNSET)

        _schema = d.pop("schema", UNSET)
        schema: Union[Unset, CreateScriptJsonBodySchema]
        if isinstance(_schema, Unset):
            schema = UNSET
        else:
            schema = CreateScriptJsonBodySchema.from_dict(_schema)

        is_template = d.pop("is_template", UNSET)

        lock = cast(List[str], d.pop("lock", UNSET))

        create_script_json_body = cls(
            path=path,
            summary=summary,
            description=description,
            content=content,
            parent_hash=parent_hash,
            schema=schema,
            is_template=is_template,
            lock=lock,
        )

        create_script_json_body.additional_properties = d
        return create_script_json_body

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
