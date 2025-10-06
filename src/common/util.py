from dataclasses import dataclass, field
from typing import List, Optional
from pathlib import Path


@dataclass
class Program:
    name: str
    variables: List['Variable'] = field(default_factory=list)
    paragraphs: List['Paragraph'] = field(default_factory=list)

@dataclass
class Variable:
    level: int
    name: str
    picture: Optional[str] = None
    value: Optional[str] = None

@dataclass
class Paragraph:
    name: str
    statements: List['Statement'] = field(default_factory=list)

@dataclass
class Statement:
    type: str
    data: dict = field(default_factory=dict)

@dataclass
class ProcedureMetadata:
    purpose: str
    called_by: List[str] = field(default_factory=list)
    calls: List[str] = field(default_factory=list)
    input_vars: List[str] = field(default_factory=list)
    output_vars: List[str] = field(default_factory=list)
    statement_count: int = 0


@dataclass
class VariableMetadata:
    purpose: str

@dataclass
class DataFlow:
    variable: str
    purpose: str
    writers: List[str] = field(default_factory=list)
    readers: List[str] = field(default_factory=list)

def read_file(filename: str) -> str:
    return Path(filename).read_text()