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
  
- Substitution can be done locally before running:
  
```databricks bundle deploy -t dev```

- For Validate and Prod, run: ```python bundle_script.py <>```

as part of the CI/CD pipeline, and only process config files touched in the new PR rather than all of them.


```
cd cards-etl

python bundle_script.py cards-etl/conf

databricks bundle validate

databricks bundle deploy

## One time Onboarding for a given source

databricks bundle run cards_onboarding_job

## Raw to Bronze to Silver Pipeline. Deploy once run it as many times, manually or triggered.

databricks bundle run cards_r2s_job

```

Similar steps for other folders