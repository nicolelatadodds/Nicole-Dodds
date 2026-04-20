from dataclasses import dataclass, field
from datetime import date
from typing import Optional


@dataclass
class TaskRow:
    name: str
    start_date: Optional[date]
    end_date: Optional[date]
    notes: Optional[str]


@dataclass
class SheetData:
    rows: list[TaskRow] = field(default_factory=list)

    @property
    def final_end_date(self) -> Optional[date]:
        dates = [r.end_date for r in self.rows if r.end_date is not None]
        return max(dates) if dates else None
