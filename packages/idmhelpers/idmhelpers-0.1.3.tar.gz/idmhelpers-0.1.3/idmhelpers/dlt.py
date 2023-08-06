# Delta Live Metadata framework

import dlt
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.window import *

def createNestedFrame(df1,name,keycolumns=[],partitionkeys=[]):
  newcolumns = []
  newcolumns.extend(keycolumns)
  newcolumns.append(name)
  
  nonkeycolumns = list(set(df1.columns)-set(keycolumns)-set(partitionkeys)) # Do not put key joining columns into nested structures

  df = df1.withColumn(name,struct(nonkeycolumns)).select(newcolumns)
  df = df.groupby(keycolumns).agg(collect_list(name).alias(name))
  return df

def getSQLTask(name,sql,type="sql-view",comment="",temporary=True,nested={},path=None):
  if path==None:
    path=f'{storage}/{name}'
  # Define 
  if type=="sql-table":
    @dlt.table(
      name=f"{name}",
      comment=f"SQL:{name}:{comment}",
      temporary=temporary,
      path=path
    )
    def define_sql_table():
      df=spark.sql(sql)
      return df
  # Define a SQL-View
  
  if type=="sql-view":
    @dlt.view(
      name=f"{name}",
      comment=f"SQL:{name}:{comment}"
    )
    def define_sql_table():
      df=spark.sql(sql)
      return df
  if type=="sql-nest":
    @dlt.view(
      name=f"{name}",
      comment=f"SQL:{name}:{comment}"
    )
    def define_nested_table():
      df=spark.sql(sql)
      df_n=createNestedFrame(df,nested['name'],nested['keycolumns'],nested['partitionkeys'])
      return df_n



