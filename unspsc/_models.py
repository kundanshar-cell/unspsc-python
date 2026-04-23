from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Segment:
    code: int
    title: str
    definition: Optional[str]


@dataclass
class Family:
    code: int
    title: str
    definition: Optional[str]
    segment_code: int


@dataclass
class Class:
    code: int
    title: str
    definition: Optional[str]
    family_code: int


@dataclass
class Commodity:
    code: int
    title: str
    definition: Optional[str]
    class_code: int


@dataclass
class Hierarchy:
    segment: Segment
    family: Family
    cls: Class
    commodity: Commodity

    def __str__(self) -> str:
        return (
            f"{self.segment.code} {self.segment.title} → "
            f"{self.family.code} {self.family.title} → "
            f"{self.cls.code} {self.cls.title} → "
            f"{self.commodity.code} {self.commodity.title}"
        )


@dataclass
class MatchResult:
    code: int
    title: str
    definition: Optional[str]
    score: float
    hierarchy: Optional["Hierarchy"] = None
