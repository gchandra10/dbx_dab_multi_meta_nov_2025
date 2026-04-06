from pyspark.sql import DataFrame
from pyspark.sql.functions import *
from src.dataflow_pipeline import DataflowPipeline

def bronze_pci_encrypt(df: DataFrame, dataflow_spec) -> DataFrame:
    props = dataflow_spec.tableProperties or {}

    pci_flag = str(props.get("pci", "false")).lower() == "true"
    if not pci_flag:
        return df.withColumn("last_updated_on", current_date())

    pci_cols_str = props.get("pci_columns", "")
    pci_cols = [c.strip() for c in pci_cols_str.split(",") if c.strip()]
    
    target_details = dataflow_spec.targetDetails or {}
    catalog = target_details.get("catalog")
    schema = target_details.get("database")
    
    func_name = f"{catalog}.{schema}.encrypt_pci"

    for c in pci_cols:
        df = df.withColumn(c, expr(f"{func_name}({c})"))

    df = df.withColumn("last_updated_on", current_date())
    return df

layer = spark.conf.get("layer", None)

DataflowPipeline.invoke_dlt_pipeline(
    spark,
    layer, 
    bronze_custom_transform_func=bronze_pci_encrypt,
    silver_custom_transform_func=bronze_pci_encrypt
)