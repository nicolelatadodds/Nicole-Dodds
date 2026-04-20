import logging
from datetime import date, datetime
from typing import Optional

import smartsheet

from models import SheetData, TaskRow

logger = logging.getLogger(__name__)

# Match these exactly to your Smartsheet column headers
COL_TASK_NAME = "Task Name"
COL_START_DATE = "Start Date"
COL_END_DATE = "End Date"
COL_NOTES = "Notes"


def _build_column_map(sheet) -> dict[str, int]:
    """Returns {column_title: column_id} for all columns in the sheet."""
    return {col.title: col.id for col in sheet.columns}


def _parse_date(value) -> Optional[date]:
    """Parses an ISO 8601 date string from Smartsheet into a date object."""
    if value is None:
        return None
    try:
        return datetime.strptime(str(value), "%Y-%m-%d").date()
    except ValueError:
        logger.warning("Could not parse date value: %r", value)
        return None


def _get_cell_value(row, column_id: int):
    """
    Reads a cell value by column ID. Uses display_value (formatted string)
    preferentially — correct for dates and text cells.
    """
    if column_id == -1:
        return None
    cell = row.get_column(column_id)
    if cell is None:
        return None
    return cell.display_value if cell.display_value is not None else cell.value


def fetch_sheet_data(token: str, sheet_id: int) -> SheetData:
    """
    Fetches all task rows from the given Smartsheet sheet.

    Raises:
        smartsheet.exceptions.ApiError on auth failure, 404, or rate limit.
    """
    client = smartsheet.Smartsheet(token)
    client.errors_as_exceptions(True)

    sheet = client.Sheets.get_sheet(sheet_id)
    col_map = _build_column_map(sheet)

    for col in [COL_TASK_NAME, COL_START_DATE, COL_END_DATE, COL_NOTES]:
        if col not in col_map:
            logger.warning("Column '%s' not found. Available: %s", col, list(col_map.keys()))

    task_name_id = col_map.get(COL_TASK_NAME, -1)
    start_id = col_map.get(COL_START_DATE, -1)
    end_id = col_map.get(COL_END_DATE, -1)
    notes_id = col_map.get(COL_NOTES, -1)

    rows: list[TaskRow] = []
    for row in sheet.rows:
        name = _get_cell_value(row, task_name_id)
        if not name:
            continue
        rows.append(TaskRow(
            name=str(name).strip(),
            start_date=_parse_date(_get_cell_value(row, start_id)),
            end_date=_parse_date(_get_cell_value(row, end_id)),
            notes=str(_get_cell_value(row, notes_id) or "").strip() or None,
        ))

    logger.info("Fetched %d task rows from sheet %d", len(rows), sheet_id)
    return SheetData(rows=rows)
