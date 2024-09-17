from abc import (
    ABC,
    abstractmethod,
)


class BaseRepository(ABC):
    @abstractmethod
    def get_all_objects(self) -> list[object]:
        ...

    @abstractmethod
    def get_object(self, object_id: int) -> object:
        ...

    @abstractmethod
    def create_object(self, obj: object) -> object:
        ...

    @abstractmethod
    def update_object(self, object_id: int, obj: object) -> None:
        ...

    @abstractmethod
    def delete_object(self, object_id: int) -> None:
        ...
