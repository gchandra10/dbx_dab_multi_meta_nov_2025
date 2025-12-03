import sys

from src.onboard_dataflowspec import OnboardDataflowspec

import argparse
parser = argparse.ArgumentParser(description="Onboard Dataflowspec Parameters")

parser.add_argument("--database", type=str, default="", help="Catalog database name")
parser.add_argument("--onboarding_file_path", type=str, default="", help="Path to the onboarding file")
parser.add_argument("--bronze_dataflowspec_table", type=str, default="bronze_dataflowspec_table", help="Bronze Dataflowspec table name")
parser.add_argument("--silver_dataflowspec_table", type=str, default="silver_dataflowspec_table", help="Silver Dataflowspec table name")
parser.add_argument("--env", type=str, default="dev", help="Environment (e.g., dev, prod)")
parser.add_argument("--import_author", type=str, default="", help="Author of the import")
parser.add_argument("--overwrite", type=str, default="", help="Overwrite existing dataflowspecs (True/False)")
parser.add_argument("--version", type=str, default="v1", help="Version of the onboarding process")
parser.add_argument("--uc_enabled", type=str, default="True", help="Flag to indicate if Unity Catalog is enabled (True/False)")

# parser.add_argument("--onboard_layer", type=str, default="bronze_silver", help="Layer to onboard (e.g., bronze_silver, silver)")

args = parser.parse_args()
database = args.database
onboarding_file_path = args.onboarding_file_path
bronze_dataflowspec_table = args.bronze_dataflowspec_table
silver_dataflowspec_table = args.silver_dataflowspec_table
env = args.env
import_author = args.import_author
uc_enabled = args.uc_enabled
# onboard_layer = args.onboard_layer

# Determine overwrite flag based on existence of tables
bronze_dataflow_exists = spark.catalog.tableExists(f"{database}.{bronze_dataflowspec_table}")
silver_dataflow_exists = spark.catalog.tableExists(f"{database}.{silver_dataflowspec_table}")
overwrite = "False" if (bronze_dataflow_exists and silver_dataflow_exists) else "True"

onboarding_params_map = {}
onboarding_params_map["onboarding_file_path"] = onboarding_file_path
onboarding_params_map["database"] = database
onboarding_params_map["env"] = env
onboarding_params_map["bronze_dataflowspec_table"] = bronze_dataflowspec_table
onboarding_params_map["silver_dataflowspec_table"] = silver_dataflowspec_table
onboarding_params_map["import_author"] = import_author
onboarding_params_map["version"] = "v1"
onboarding_params_map["overwrite"] = overwrite

#onboarding_params_map["uc_enabled"] = uc_enabled
#onboarding_params_map["onboard_layer"] = onboard_layer


print(type(onboarding_params_map), onboarding_params_map)

OnboardDataflowspec(spark, onboarding_params_map, uc_enabled=uc_enabled).onboard_dataflow_specs()