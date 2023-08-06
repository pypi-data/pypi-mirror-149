# pandas_scd

executing slowly changing dimension type 2

source_table: name of the table with the new source
dim_table: name of the dim table to apply scd2
key: the key to identify a row in the dim/source
tracked_columns: list of columns to check is any update occurred
connection: sqlalchemy connection object

the class will add the following columns to the dataframe (value for new record):
start_ts (now)
end_ts (None)
is_active (True)


## Getting started

pip install pandas-scd2

from pandas_scd import SCD2

SCD2(   source_table: str,
        dim_table: str,
        key: str,
        tracked_columns: list,
        connection: sqlalchemy.engine
    )


