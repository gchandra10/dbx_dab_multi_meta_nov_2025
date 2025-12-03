# Key Points

- DABS can’t deploy a single pipeline in isolation. Splitting the monolithic bundle into per-source folders gives you room to deploy, test, and iterate independently. This is an alternate we can discuss about.
  
```
cards-etl
  |- conf
  |- resources
  |- src
  databricks.yml

consumer-etl
  |- conf
  |- resources
  |- src
  databricks.yml

sales-etl
  |- conf
  |- resources
  |- src
  databricks.yml
```

- Variable substitution in JSON config files is handled through a Python script. Keep template JSON files in a dedicated folder and write the substituted output into the conf directory.

```
python bundle_script.py cards-etl/conf
```

- Included Git Pre Commit webhook, that gets fired when Developer issues a commit. 

```
git add .
git commit -m "message"
```

When precommit hook executes, it automatically converts the .template to .json.

- Added *.JSON to .gitignore so the .template will be copied in Repo and no one manually edits the JSON files.

- Substitution can be done locally before running:
  
```
databricks bundle deploy -t dev
```

------

- For Validate and Prod, run: ```python bundle_script.py <>```

as part of the CI/CD pipeline, and only process config files touched in the new PR rather than all of them.


```
cd cards-etl

python bundle_script.py cards-etl/conf

databricks bundle validate

databricks bundle deploy -t dev
```

## One time Onboarding for a given source

**It calls onboard_bronze_silver.py, if bronze and silver dataflowspec table exists overwrite is set to False. For first time its True.**

```
databricks bundle run cards_onboarding_job

databricks bundle run cards_onboarding_job2
```

## Raw to Bronze to Silver Pipeline. Deploy once run it as many times, manually or triggered.

```
databricks bundle run cards_r2s_job



```

<!-- ## CICD UAT / PROD

```
#!/usr/bin/env bash
set -euo pipefail

# Find all top-level directories ending with "-etl"
# Using -print0 + read -d '' to safely handle special characters in names

find . -maxdepth 1 -type d -name '*-etl' -print0 | while IFS= read -r -d '' dir; do
  # Strip leading ./ for nicer output
  bundle_dir="${dir#./}"

  # Ensure this looks like a bundle (must have databricks.yml)
  if [[ ! -f "${bundle_dir}/databricks.yml" ]]; then
    echo "Skipping ${bundle_dir}: no databricks.yml"
    continue
  fi

  echo "Validating and deploying ${bundle_dir} to prod..."
  (
    cd "${bundle_dir}"
    databricks bundle validate
    databricks bundle deploy -t prod
  )
done

``` -->