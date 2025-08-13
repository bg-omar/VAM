
import abc

class BaseTest(abc.ABC):
    """
    Base class for VAM simulation tests.
    Subclass this and implement:
      - name (str): short display name
      - description (str): one-paragraph description
      - default_params() -> dict
      - run(params: dict, figure): perform simulation & draw on given matplotlib Figure; return results dict
    """
    name: str = "Unnamed Test"
    description: str = "No description."

    @abc.abstractmethod
    def default_params(self) -> dict:
        ...

    @abc.abstractmethod
    def run(self, params: dict, figure) -> dict:
        ...
