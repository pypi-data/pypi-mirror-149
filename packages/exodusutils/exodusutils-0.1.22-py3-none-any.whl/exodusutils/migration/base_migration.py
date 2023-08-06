import abc

from pymongo.collection import Collection


class BaseMigration(abc.ABC):
    """
    The base class for migration scripts.

    User will need to implement the `up` and `down` methods.
    """

    def __init__(self, timestamp: int, name: str) -> None:
        """
        Initialize this migration script.

        Parameters
        ----------
        timestamp : int
            The timestamp as an `int`.
        name : str
            The name of this migration script.
        """
        self.timestamp = timestamp
        self.name = name
        self.mongo_name = f"{self.timestamp}_{self.name}"

    @abc.abstractmethod
    def up(self, collection: Collection) -> None:
        """
        The up step of this migration script.

        Parameters
        ----------
        collection : Collection
            The MongoDB collection this script will operate on.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def down(self, collection: Collection) -> None:
        """
        The down step of this migration script. Should either do the inverse
        of the `up` step, or do nothing if the `up` step is irreversible.

        Parameters
        ----------
        collection : Collection
            The MongoDB collection this script will operate on.
        """
        raise NotImplementedError
