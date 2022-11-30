from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetByEmailRequest(_message.Message):
    __slots__ = ["email"]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    email: str
    def __init__(self, email: _Optional[str] = ...) -> None: ...

class GetByEmailResponse(_message.Message):
    __slots__ = ["data"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedCompositeFieldContainer[ScrapperEmail]
    def __init__(self, data: _Optional[_Iterable[_Union[ScrapperEmail, _Mapping]]] = ...) -> None: ...

class GetByFaceRequest(_message.Message):
    __slots__ = ["chunk_data", "metadata"]
    CHUNK_DATA_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    chunk_data: bytes
    metadata: MetaData
    def __init__(self, metadata: _Optional[_Union[MetaData, _Mapping]] = ..., chunk_data: _Optional[bytes] = ...) -> None: ...

class GetByFaceResponse(_message.Message):
    __slots__ = ["data"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedCompositeFieldContainer[ScrapperFace]
    def __init__(self, data: _Optional[_Iterable[_Union[ScrapperFace, _Mapping]]] = ...) -> None: ...

class GetByNameRequest(_message.Message):
    __slots__ = ["demo", "firstName", "lastName"]
    DEMO_FIELD_NUMBER: _ClassVar[int]
    FIRSTNAME_FIELD_NUMBER: _ClassVar[int]
    LASTNAME_FIELD_NUMBER: _ClassVar[int]
    demo: bool
    firstName: str
    lastName: str
    def __init__(self, lastName: _Optional[str] = ..., firstName: _Optional[str] = ..., demo: bool = ...) -> None: ...

class GetByNameResponse(_message.Message):
    __slots__ = ["data"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedCompositeFieldContainer[ScrapperName]
    def __init__(self, data: _Optional[_Iterable[_Union[ScrapperName, _Mapping]]] = ...) -> None: ...

class GetByResumeRequest(_message.Message):
    __slots__ = ["chunk_data", "metadata"]
    CHUNK_DATA_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    chunk_data: bytes
    metadata: MetaDataResume
    def __init__(self, metadata: _Optional[_Union[MetaDataResume, _Mapping]] = ..., chunk_data: _Optional[bytes] = ...) -> None: ...

class GetByResumeResponse(_message.Message):
    __slots__ = ["data"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: ScrapperResume
    def __init__(self, data: _Optional[_Union[ScrapperResume, _Mapping]] = ...) -> None: ...

class MetaData(_message.Message):
    __slots__ = ["extension", "filename", "firstName", "lastName"]
    EXTENSION_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    FIRSTNAME_FIELD_NUMBER: _ClassVar[int]
    LASTNAME_FIELD_NUMBER: _ClassVar[int]
    extension: str
    filename: str
    firstName: str
    lastName: str
    def __init__(self, filename: _Optional[str] = ..., extension: _Optional[str] = ..., lastName: _Optional[str] = ..., firstName: _Optional[str] = ...) -> None: ...

class MetaDataResume(_message.Message):
    __slots__ = ["extension", "filename"]
    EXTENSION_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    extension: str
    filename: str
    def __init__(self, filename: _Optional[str] = ..., extension: _Optional[str] = ...) -> None: ...

class ScrapperEmail(_message.Message):
    __slots__ = ["has_password", "hash", "password", "sha1", "sources"]
    HASH_FIELD_NUMBER: _ClassVar[int]
    HAS_PASSWORD_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    SHA1_FIELD_NUMBER: _ClassVar[int]
    SOURCES_FIELD_NUMBER: _ClassVar[int]
    has_password: bool
    hash: str
    password: str
    sha1: str
    sources: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, has_password: bool = ..., password: _Optional[str] = ..., sha1: _Optional[str] = ..., hash: _Optional[str] = ..., sources: _Optional[_Iterable[str]] = ...) -> None: ...

class ScrapperFace(_message.Message):
    __slots__ = ["link", "metadata"]
    LINK_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    link: str
    metadata: _containers.RepeatedCompositeFieldContainer[ScrapperMetadata]
    def __init__(self, link: _Optional[str] = ..., metadata: _Optional[_Iterable[_Union[ScrapperMetadata, _Mapping]]] = ...) -> None: ...

class ScrapperMetadata(_message.Message):
    __slots__ = ["name", "value"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    name: str
    value: str
    def __init__(self, name: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class ScrapperName(_message.Message):
    __slots__ = ["found", "link", "metadata", "name"]
    FOUND_FIELD_NUMBER: _ClassVar[int]
    LINK_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    found: bool
    link: str
    metadata: _containers.RepeatedCompositeFieldContainer[ScrapperMetadata]
    name: str
    def __init__(self, name: _Optional[str] = ..., link: _Optional[str] = ..., found: bool = ..., metadata: _Optional[_Iterable[_Union[ScrapperMetadata, _Mapping]]] = ...) -> None: ...

class ScrapperResume(_message.Message):
    __slots__ = ["addresses", "cities", "emails", "phones", "urls"]
    ADDRESSES_FIELD_NUMBER: _ClassVar[int]
    CITIES_FIELD_NUMBER: _ClassVar[int]
    EMAILS_FIELD_NUMBER: _ClassVar[int]
    PHONES_FIELD_NUMBER: _ClassVar[int]
    URLS_FIELD_NUMBER: _ClassVar[int]
    addresses: _containers.RepeatedScalarFieldContainer[str]
    cities: _containers.RepeatedScalarFieldContainer[str]
    emails: _containers.RepeatedScalarFieldContainer[str]
    phones: _containers.RepeatedScalarFieldContainer[str]
    urls: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, emails: _Optional[_Iterable[str]] = ..., cities: _Optional[_Iterable[str]] = ..., addresses: _Optional[_Iterable[str]] = ..., phones: _Optional[_Iterable[str]] = ..., urls: _Optional[_Iterable[str]] = ...) -> None: ...
