import csv
import os
from pathlib import Path
from typing import List, Optional, Union

import pandas

from w.services.abstract_service import AbstractService
from w.services.technical.filesystem_service import FilesystemService
from w.services.technical.models.csv_dump_options import CsvDumpOptions


class CsvService(AbstractService):
    @classmethod
    def is_csv(cls, filename):
        """ Check if filename is csv (from extension) """
        return FilesystemService.has_suffix(filename, ".csv")

    @classmethod
    def check_is_csv(cls, filename) -> Path:
        """
        Check if filename is csv (from extension) or raise RuntimeError
        """
        filename = FilesystemService.get_path(filename)
        if cls.is_csv(filename):
            return filename
        raise RuntimeError(f"{filename.name} is not a csv file")

    @classmethod
    def load(cls, csv_filename, mapping_columns) -> list:
        """
        Load csv file to list

        Args:
            csv_filename(str|Path): csv file
            mapping_columns(dict): csv header columns mapping to wanted attributes

        Returns:
            list: [{"<mapping name>": < row col value>, ...}, ...]

        Raises:
            RuntimeError :
                - filename is not csv
                - filename does not exists
                - incorrect or missing header
        """
        # TODO use pandas instead of csv module
        csv_filename = cls.check_is_csv(csv_filename)
        FilesystemService.check_file_exists(csv_filename)
        reader = csv.reader(csv_filename.open())
        required_headers = list(mapping_columns.keys())
        headers = [c for c in next(reader)]
        if required_headers != headers:
            raise RuntimeError(
                f"incorrect or missing header, expected '{';'.join(required_headers)}' "
                f"got '{';'.join(headers)}'"
            )
        return [
            {mapping_columns[headers[i]]: value for i, value in enumerate(row)}
            for row in reader
        ]

    @classmethod
    def dump(
        cls,
        filename: Union[str, Path],
        rows: List[dict],
        options: Optional[CsvDumpOptions] = None,
    ):
        """
        Dump rows into csv file.

        Args:
            filename(str|Path): csv filename
            rows([dict]): list of rows [{"<column name>": <row col value>, ...}, ...]
            options(:obj: `CsvDumpOptions`, optional): options like "mapping_columns" to
                rename columns, "field_delimiter" to specify which character to use to
                delimiter fields and "line_terminator" to specify which character or
                character sequence to end lines

        Raises:
            RuntimeError: if file path is invalid or if provided rows are invalid
        """
        cls._check_dump_context(filename, rows)
        formatted_data = cls._format_dump_data(rows, options)
        cls._write(filename, formatted_data, options)

    @classmethod
    def _check_dump_context(cls, filename: Union[str, Path], rows: List[dict]):
        FilesystemService.check_dir_exists(os.path.dirname(filename))
        cls._check_dump_rows(rows)

    @classmethod
    def _check_dump_rows(cls, rows: List[dict]):
        if not cls._are_dump_rows_valid(rows):
            raise RuntimeError(
                "Unable to dump data to csv file : invalid provided rows"
            )

    @classmethod
    def _are_dump_rows_valid(cls, rows: List[dict]) -> bool:
        return rows and all(isinstance(item, dict) for item in rows)

    @classmethod
    def _format_dump_data(
        cls, rows: List[dict], options: Optional[CsvDumpOptions] = None
    ) -> pandas.DataFrame:
        formatted_data = pandas.DataFrame(rows)
        if options:
            formatted_data.rename(columns=(options.mapping_columns), inplace=True)
        return formatted_data

    @classmethod
    def _write(
        cls,
        filename: Union[str, Path],
        formatted_data: pandas.DataFrame,
        options: Optional[CsvDumpOptions] = None,
    ):
        if options:
            formatted_data.to_csv(
                filename,
                sep=options.field_delimiter,
                line_terminator=options.line_terminator,
                index=False,
            )
        else:
            formatted_data.to_csv(filename, index=False)
