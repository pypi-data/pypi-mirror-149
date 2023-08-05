# -*- coding: utf-8 -*-
"""
Copyright 2019-2022 Olexandr Balyk
This file is part of Timeslib.
Timeslib is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
Timeslib is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.
You should have received a copy of the GNU Affero General Public License
along with Timeslib. If not, see <https://www.gnu.org/licenses/>.
"""

import pandas as pd


def print_to_xlsx(df, sheet_by_column, file_name):

    writer = pd.ExcelWriter(file_name, engine="xlsxwriter")

    # Get the xlsxwriter workbook object
    workbook = writer.book

    table_name_row, table_start_col = (4, 1)
    table_unit_row = table_name_row + 1
    table_header_row = table_name_row + 2

    if "Region" not in df.columns:
        df.insert(2, "Region", "Region")

    for sheet_name in df[sheet_by_column].unique():

        table_name = sheet_name
        table_unit = "Unspecified"

        # Get dataframe with data to be written to the sheet
        df_to_sheet = df[df[sheet_by_column] == sheet_name].drop(
            columns=[sheet_by_column]
        )

        # df2.drop(columns=["displayType","chartName"],inplace=True)
        # df2=pd.pivot_table(df2, values = 'total', index=['scenario','serie'], columns = 'year').reset_index()

        df_to_sheet.to_excel(
            writer,
            sheet_name=sheet_name,
            index=False,
            header=False,
            startrow=table_header_row + 1,
            startcol=table_start_col,
        )

        # Get the xlsxwriter worksheet object
        worksheet = writer.sheets[sheet_name]

        # Get the dimensions of the dataframe
        max_row, max_col = df_to_sheet.shape

        # Create a list of column headers
        column_settings = [{"header": column} for column in df_to_sheet.columns]

        # Specify table structure and options
        worksheet.add_table(
            table_header_row,
            table_start_col,
            table_header_row + max_row,
            table_start_col + max_col - 1,
            {"columns": column_settings, "autofilter": False, "style": None},
        )

        worksheet.write(table_name_row, table_start_col, "Table Name: " + table_name)
        worksheet.write(table_unit_row, table_start_col, "Active Unit: " + table_unit)

    writer.close()
