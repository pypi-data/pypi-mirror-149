from typing import Optional
from dataclasses import dataclass

@dataclass
class Meals:
    no: int
    schl_cd: str
    ara: str
    schl_nm: str
    total_cnt: str

@dataclass
class MealsInfo:
    ara: str
    month: str
    no: int
    pre_last_week: str
    schl_cd: str
    schl_nm: str
    week: str
    year: str

@dataclass
class WeekYearList:
    no: int
    year: str
    total_cnt: str

@dataclass
class MealsDetail:
    dd_date: str
    inqry_mm: str
    no: int
    schl_cd: str
    week_day: str
    week_dvs: str
    lunch: Optional[str] = None