
import numpy as np
from typing import List, Optional
from parse import parse
from pydantic import BaseModel, ValidationError
from unsync import unsync
from multiprocessing import cpu_count

from ..helpers import tab_to_comma


CPU_COUNT = cpu_count()


class BaseDataStructure:
    """
    Base data structure class
    """

    data_structure = ""  # Data structure string (as per the "parse" package)

    class meta_model(BaseModel):
        """
        Meta data Pydantic model.
        """
        pass

    class row_model(BaseModel):
        """
        Table row Pydantic model.
        """
        pass

    @staticmethod
    def meta_preprocessor(meta: dict) -> dict:
        """
        Meta data preprocessor.

        This method is used to convert the meta data from a given data structure subclass
        in to the meta data format of the parent data structure. A common use case is
        combining "date" and "time" meta data fields into a single "datetime" field.
        """
        return meta

    @staticmethod
    def row_preprocessor(row: dict) -> dict:
        """
        Table row preprocessor.

        This method is used to convert a table row from a given data structure subclass
        in to the table row format of the parent data structure. A common use case is
        combining "date" and "time" meta data fields into a single "datetime" field, 
        converting units or deleting unused columns.

        For more complex preprocessing requiring knowledge of all rows and meta data use
        the `table_preprocessor` method.
        """
        return row

    @staticmethod
    def table_preprocessor(table_rows: List[dict], meta: dict = {}) -> List[dict]:
        """
        Table preprocessor.

        This method is used as a final step before the table rows are validated against
        the table row format of the parent data structure. It is called after the
        `row_preprocessor` method and performs a similar function execpt that the method
        has access to all table rows and any meta data. A common use case is to add an
        sample spacing column, which requires knowledge of both the sample rate (which
        can be passed in as meta data) and the total number of readings.
        """
        return table_rows

    @classmethod
    def extract_meta(cls, data: str) -> dict:
        """
        Extract the meta data from the data sting.

        The meta data is run through meta_preprocessor before being returned.
        """
        parsed = parse(cls.data_structure, data)
        if parsed is None:
            return parsed

        # Run the meta data through the meta_preprocessor and return:
        return cls.meta_preprocessor(parsed.named)

    @classmethod
    def extract_table(cls, data: str, meta: Optional[dict] = None) -> dict:
        """
        Extract the table rows from the data string.

        The table rows are run through the row_preprocessor before being returned.
        """
        parsed = parse(cls.data_structure, data)
        if parsed is None:
            return parsed

        # Extract table data from the last unnamed parameter in data_structure and
        # convert to list of dicts using the row_model fields as the keys:
        table_data = parsed.fixed[-1]
        table_data = [row.split(",") for row in tab_to_comma(table_data).split("\n")]
        table_rows = [dict(zip(cls.row_model.__fields__, row)) for row in table_data]

        # Attempt to validate table rows using the row_model. This will attempt to cast
        # any fields that don't match the corresponding row_model field.
        try:
            tasks = [
                call_row_model(cls.row_model, rows.tolist())
                for rows in np.array_split(table_rows, CPU_COUNT)
            ]
            table_rows = unpack_results(tasks)
        except ValidationError:
            return None  # return None if unable to validate table rows

        # Run the table rows through row_preprocessor:

        tasks = [
            call_row_preprocessor(cls.row_preprocessor, rows.tolist())
            for rows in np.array_split(table_rows, CPU_COUNT)
        ]
        table_rows = unpack_results(tasks)

        # Run the table rows through table_preprocessor and return:
        return cls.table_preprocessor(table_rows, meta)

    @classmethod
    def validate_meta(cls, meta):
        """
        Validate the meta data using meta_model.
        """
        return cls.meta_model(**meta).dict(exclude_unset=True)

    @classmethod
    def validate_table(cls, table_rows):
        """
        Validate the table rows using row_model.
        """
        tasks = [
            call_row_model(cls.row_model, rows.tolist(), True)
            for rows in np.array_split(table_rows, CPU_COUNT)
        ]
        return [rr for tt in tasks for rr in tt.result()]

    @classmethod
    @property
    def children(cls) -> list:
        """
        List of data structure classes derived from this parent class.
        """
        return cls.__subclasses__()

    @classmethod
    @property
    def id(cls) -> str:
        """
        Data structure ID.
        """
        return cls.__name__.split("_")[-1]


def unpack_results(tasks):
    return [rr for tt in tasks for rr in tt.result()]


@unsync(cpu_bound=True)
def call_row_model(row_model, rows, exclude_unset=False):
    return [row_model(**row).dict(exclude_unset=exclude_unset) for row in rows]


@unsync(cpu_bound=True)
def call_row_preprocessor(row_preprocessor, rows):
    return [row_preprocessor(row) for row in rows]
