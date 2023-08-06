from math import ceil
from datetime import datetime

def weekcount():
    first = datetime.now()
    first = first.replace(day=1)

    day = first.day + first.weekday()

    return str(
        int(
            ceil(day / 7.0)
        )
    )

week_count = weekcount()
now = datetime.now()
month = str(now.month)
year = str(now.year)