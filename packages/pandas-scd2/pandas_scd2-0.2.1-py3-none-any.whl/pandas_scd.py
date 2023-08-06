import pandas as pd
from datetime import datetime
import sqlalchemy

dialects = {
    "postgresql": sqlalchemy.TIMESTAMP(),
    "mysql": sqlalchemy.DATETIME(),
    "sqlite": sqlalchemy.DATETIME(),
    "mariadb": sqlalchemy.DATETIME(),
    # mssql:
    # oracle:
    # bigquery:
    # snowflake:
    # redshift:
}


class SCD2:
    """
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
    """

 

    def __init__(
        self,
        source_table: str,
        dim_table: str,
        key: str,
        tracked_columns: list,
        connection: sqlalchemy.engine,
    ) -> None:
        self.table_name = dim_table
        self.key = key
        self.columns = list(set(tracked_columns) | {key})
        self.conn = connection
        self.src = pd.read_sql_table(source_table, self.conn)
        self.dest = self.get_dest_table()
        self.now = datetime.now()
        self.run_scd2()
 

    def get_dest_table(self):
        """
        get only active rows from existing table.
        if destination table doesnt exists, will create empty dataframe based om source table columns + scd columns
        """

        if sqlalchemy.inspect(self.conn).has_table(self.table_name):
            return pd.read_sql(f"select * from {self.table_name} where is_active = True", self.conn)
        else:
            cols = list(self.src.columns) + ["start_ts", "end_ts", "is_active"]
            return pd.DataFrame(columns=cols)

 

    def hash_rows(self, df: pd.DataFrame, cols: list) -> pd.DataFrame:
        """create a string from all the columns provided, hash it and return the value in a new column called hash"""
        df["hash"] = df[cols].apply(lambda x: hash("".join(map(str, x))), axis=1)
        return df

 

    def get_changed_keys(self, existing_keys: pd.DataFrame):
        """return only rows that changed between the two dataframes, in any of the tracked columns"""

        # get hash values for all rows in dest and src
        dest = self.hash_rows(self.dest, self.columns)
        existing_keys = self.hash_rows(existing_keys, self.columns)

        # create a dataframe with only updated rows
        changed = existing_keys.merge(dest, how="inner", on=self.key, suffixes=("", "_right"))
        changed = changed[changed["hash"] != changed["hash_right"]]    

        # remove unnecessary columns from join
        to_drop = [col for col in changed.columns if "_right" in col] + ["hash"]
        changed.drop(columns=to_drop, inplace=True)
        return changed
 

    def separate_new_and_existing_keys(self):
        """split the source dataframe to existing keys and new keys"""

        all_records = self.src.merge(self.dest, on=self.key, how="left", suffixes=("", "_right"), indicator=True)
        cols_to_remove = {c for c in all_records.columns if "_right" in c} | {"_merge"}

        new_keys = all_records[all_records["_merge"] == "left_only"]
        existing_keys = all_records[all_records["_merge"] == "both"]

        for df in [new_keys, existing_keys]:
            df.drop(columns=cols_to_remove, inplace=True)

        return new_keys, existing_keys

 

    def update_end_ts(self, key_list: list) -> None:
        """updating the destination table with end date and not active for changed keys"""

        if key_list:
            keys = ",".join([str(i) for i in key_list])
            sql = f"update {self.table_name} set end_ts = '{self.now}', is_active = False where {self.key} in ({keys}) and is_active = True"
            self.conn.execute(sql)
 

    def add_data_to_new_records(self, df: pd.DataFrame) -> pd.DataFrame:
        """adding scd columns to dataframe"""

        df["start_ts"] = self.now
        df["end_ts"] = None
        df["is_active"] = True
        return df


    def run_scd2(self):
        new_keys, existing_keys = self.separate_new_and_existing_keys()
        changed = self.get_changed_keys(existing_keys)
        self.update_end_ts(changed[self.key].to_list())

        new_keys = self.add_data_to_new_records(new_keys)
        changed = self.add_data_to_new_records(changed)

        new_keys.to_sql(self.table_name, self.conn, if_exists="append", index=False, dtype={'end_ts': dialects[self.conn.name]})
        changed.to_sql(self.table_name, self.conn, if_exists="append", index=False)

        print(
        f"SCD2 process for {self.table_name} finished\
        \n{len(new_keys.index)} new {self.key} added\
        \n{len(changed.index)} {self.key} updated"
        )
