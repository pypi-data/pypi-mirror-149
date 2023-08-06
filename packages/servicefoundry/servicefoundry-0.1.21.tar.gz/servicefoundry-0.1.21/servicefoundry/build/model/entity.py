import dataclasses
from typing import Dict, Any, List, ClassVar


# TODO: Hide id fields from display columns
# TODO: switch to datetime.datetime for createdAt and updatedAt
# TODO: switch to Enums for str literals
# TODO: Implement NotImplementedError sections


@dataclasses.dataclass
class Entity:
    display_columns: ClassVar[List[str]] = []

    @classmethod
    def from_dict(cls, dct):
        known_attr_names = {field.name for field in dataclasses.fields(cls)}
        known_attrs = {}
        extra_attrs = {}
        for k, v in dct.items():
            if k in known_attr_names:
                known_attrs[k] = v
            else:
                extra_attrs[k] = v

        instance = cls(**known_attrs)
        for attr_name, attr_value in extra_attrs.items():
            if not hasattr(instance, attr_name):
                setattr(instance, attr_name, attr_value)
        return instance


@dataclasses.dataclass
class Cluster(Entity):
    id: str
    name: str
    fqn: str
    region: str
    createdAt: str
    updatedAt: str
    display_columns: ClassVar[List[str]] = [
        "id",
        "name",
        "fqn",
        "region",
        "createdAt",
        "updatedAt",
    ]

    def to_dict_for_session(self) -> Dict[str, Any]:
        return dataclasses.asdict(self)

    @property
    def workspaces(self) -> List["Workspace"]:
        raise NotImplementedError


@dataclasses.dataclass
class Workspace(Entity):
    id: str
    fqn: str
    name: str
    clusterId: str
    createdBy: str
    status: str
    createdAt: str
    updatedAt: str
    display_columns: ClassVar[List[str]] = [
        "id",
        "name",
        "createdBy",
        "status",
        "createdAt",
    ]

    def to_dict_for_session(self) -> Dict[str, Any]:
        return dataclasses.asdict(self)

    @property
    def cluster(self) -> Cluster:
        raise NotImplementedError

    @property
    def services(self) -> List["Service"]:
        raise NotImplementedError


@dataclasses.dataclass
class Service(Entity):
    id: str
    name: str
    fqn: str
    workspaceId: str
    status: str
    metadata: Dict[str, Any]  # TODO: flatten if needed
    display_columns: ClassVar[List[str]] = ["id", "name", "status", "metadata"]

    @property
    def workspace(self) -> Workspace:
        raise NotImplementedError

    @property
    def deployments(self) -> List["Deployment"]:
        raise NotImplementedError


@dataclasses.dataclass
class Deployment(Entity):
    id: str
    name: str
    fqn: str
    serviceId: str
    status: int
    createdBy: str
    display_columns: ClassVar[List[str]] = [
        "id",
        "name",
        "serviceId",
        "createdBy",
        "status",
    ]

    @property
    def service(self) -> Service:
        raise NotImplementedError


# TODO: Should treat displaying and handling these with more respect as it is sensitive data


@dataclasses.dataclass
class Secret(Entity):
    id: str
    name: str
    secretGroupId: str
    value: str
    fqn: str
    createdBy: str
    createdAt: str
    updatedAt: str
    display_columns: ClassVar[List[str]] = [
        "id",
        "name",
        "secretGroupId",
        "createdAt",
        "updatedAt",
    ]

    @property
    def secret_group(self) -> "SecretGroup":
        raise NotImplementedError


@dataclasses.dataclass
class SecretGroup(Entity):
    id: str
    fqn: str
    name: str
    createdBy: str
    createdAt: str
    updatedAt: str
    associatedSecrets: List[Secret]
    display_columns: ClassVar[List[str]] = ["id", "name", "createdAt", "updatedAt"]

    @classmethod
    def from_dict(cls, dct):
        dct["associatedSecrets"] = [
            Secret.from_dict(s) for s in dct.get("associatedSecrets", [])
        ]
        super().from_dict(dct)
