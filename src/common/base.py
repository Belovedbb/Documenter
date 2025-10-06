import sys
from abc import ABC, abstractmethod
from typing import TextIO

from common.parser import Parser
from common.util import Program


class BaseAnalyzer(ABC):

    def __init__(self):
        self._input = ''

    @abstractmethod
    def document(self, _input: str, _output: TextIO = sys.stdout) -> str:
        pass

    def fetch_program(self) -> Program:
        parser = Parser()
        parser.build(debug=True)
        return parser.parse(self._input)
