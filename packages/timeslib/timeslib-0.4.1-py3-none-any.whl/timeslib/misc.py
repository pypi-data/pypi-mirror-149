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

import pathlib
import pandas as pd


def read_data_csv(file_path, table_info):

    if table_info is None:
        print(
            "No info found on how to process: {}. It will be skipped.".format(file_path)
        )
        return None
    table_name = pathlib.Path(file_path).name.removesuffix(".csv")

    if table_name not in table_info.keys():
        print(
            "No info found on how to process: {}. It will be skipped.".format(table_name)
        )
        return None
    if table_info[table_name]["keepDimensions"] is None:
        print(
            "No info found on how to process: {}. It will be skipped.".format(table_name)
        )
        return None
    df = pd.read_csv(file_path)

    df["tableName"] = table_name

    if "Units" not in df.columns:
        if table_info[table_name]["defaultUnit"] is not None:
            df["Units"] = table_info[table_name]["defaultUnit"]
        else:
            df["Units"] = "missing"

    rename_dims_map = {
        "Scenario": "scenario",
        "Period": "year",
        "Region": "region",
        "Pv": "total",
        "Units": "label",
        table_info[table_name]["keepDimensions"]: "seriesName",
    }

    exclude_columns = (
        "UserName",
        "ModelName",
        "Studyname",
        "Attribute",
        "Commodity",
        "Commodityset",
        "Process",
        "Processset",
        "Vintage",
        "Timeslice",
        "Userconstraint",
    )

    # Filter data
    if "filter" in table_info[table_name].keys():
        for k, v in table_info[table_name]["filter"].items():
            df = df[df[k].isin(v)]

    # Rename some columns
    df.rename(columns=rename_dims_map, inplace=True)

    # Remove columns in excludeColumns
    df = df[[i for i in df.columns if i not in exclude_columns]]

    df = df.groupby([i for i in df.columns if not i == "total"]).agg(
        table_info[table_name]["aggregation"]
    )

    if "reverseSign" in table_info[table_name].keys():
        if table_info[table_name]["reverseSign"] is True:
            df = -df

    if "cumulate" in table_info[table_name].keys():
        if table_info[table_name]["cumulate"] is True:
            df = df.unstack(level="year", fill_value=0).stack()
            df['total'] = df.groupby([i for i in df.index.names if not i == "year"])['total'].cumsum()

    return df.reset_index()
