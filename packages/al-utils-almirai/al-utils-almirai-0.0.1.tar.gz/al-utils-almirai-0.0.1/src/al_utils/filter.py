from logging import Filter, LogRecord
from typing import List, Union


class RangeLevelFilter(Filter):
    """Subclass of :class:``Filter`` that allow the list of customized levelnos"""

    def __init__(self, level: Union[int, List[int]], name: str = '') -> None:
        """
        Create a :class:``SingleLevelFilter`` instance.

        :param level: Levelno or list of levelno. such as ``logging.DEBUG``, ``logging.INFO`` ...
        :param name: see also ``logging.Filter#__init__``
        """
        super().__init__(name=name)
        self.level = level if isinstance(level, list) else [level]

    def filter(self, record: LogRecord) -> bool:
        return record.levelno in self.level
