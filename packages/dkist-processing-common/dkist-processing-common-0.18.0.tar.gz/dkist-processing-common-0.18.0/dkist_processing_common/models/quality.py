"""Support classes used to create a quality report."""
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from pydantic import BaseModel


class Plot2D(BaseModel):
    """Support class use to hold the data for creating a 2D plot in the quality report."""

    xlabel: str
    ylabel: str
    series_data: Dict[str, List[List[Any]]]
    series_name: Optional[str] = None


class SimpleTable(BaseModel):
    """Support class to hold a simple table to be inserted into the quality report."""

    rows: List[List[Any]]
    header_row: Optional[bool] = True
    header_column: Optional[bool] = False


class ReportMetric(BaseModel):
    """
    A Quality Report is made up of a list of metrics with the schema defined by this class.

    Additionally, this class can produce a Flowable or List of Flowables to be render the metric in the PDF Report
    """

    name: str
    description: str
    statement: Optional[str] = None
    plot_data: Optional[Plot2D] = None
    table_data: Optional[SimpleTable] = None
    warnings: Optional[List[str]] = None
