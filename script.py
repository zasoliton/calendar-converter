import sys
import calendar
import typer
from functools import partial

app = typer.Typer()

DAY = "o"
HOL = "x"
NA = "-"


def weekly(year, month, day):
    weekday = calendar.weekday(year, month, day)
    return DAY if weekday == 6 else HOL


def monthly(year, month, day):
    return DAY if day == 1 else HOL


def quarterly(year, month, day, start_month=1):
    is_quarter = start_month % 3 == month % 3
    return DAY if is_quarter and day == 1 else HOL


def annually(year, month, day, start_month=1):
    return DAY if month == start_month and day == 1 else HOL


def generate_year_string(year, fn):
    year = int(year)
    year_string = ""

    for month in range(1, 13):
        for day in range(1, calendar.monthrange(year, month)[1] + 1):
            year_string += fn(year, month, day)

    if not calendar.isleap(year):  # Non-leap year, mark last day with '-'
        year_string += "-"

    return year_string


@app.command()
def generate(
    year: int, month: int = typer.Option(1, help="Optional Fiscal Start Month")
):
    result = generate_year_string(year, weekly)
    print(f"Weekly: {result}")
    result = generate_year_string(year, monthly)
    print(result)
    print(f"Monthly: {result}")
    quarter = partial(quarterly, start_month=month)
    result = generate_year_string(year, quarter)
    print(result)
    print(f"Quarterly: {result}")
    annual = partial(annually, start_month=month)
    result = generate_year_string(year, annual)
    print(f"yearly: {result}")


if __name__ == "__main__":
    app()
