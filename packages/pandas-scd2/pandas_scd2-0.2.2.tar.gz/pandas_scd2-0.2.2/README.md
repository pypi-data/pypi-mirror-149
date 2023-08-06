# pandas_scd

  

executing slowly changing dimension type 2

supported databases: 
 - postgressql
 - mysql
 - mariadb
 - sqlite



## Installation  
     pip install pandas-scd2  


## Getting started
 

    from pandas_scd import SCD2
    
    SCD2(source_table: str, dim_table: str, key: str, columns: list, engine: sqlalchemy.engine)


**source_table:** name of the table with the new source
**dim_table:** name of the dim table to apply scd2
**key:** the key to identify a row in the dim/source (the column type in the database must be of type Int)
**tracked_columns:** list of columns to check is any update occurred
**connection:** sqlalchemy connection engine