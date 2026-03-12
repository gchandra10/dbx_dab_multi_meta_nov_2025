# Sales Bundle

This bundle demonstrates how to use DABS for building across various developers, various feature branches incrementally.

Checkout the `databricks.yml` under  the `dev` target.

```
root_path: /Workspace/Users/${workspace.current_user.userName}/.bundle/${bundle.name}/${bundle.target}/${var.branch_name}

state_path: ${workspace.root_path}/state
```

And a new variable under `variables` section

```
  branch_name:
    description: The name of the current git branch
    default: main
``` 
----

## Feature Branch 1

```
git checkout main
git pull origin main
git checkout -b feature/sales1

# make changes

databricks bundle validate -t dev --var="branch_name=feature_sales1"
databricks bundle deploy -t dev --var="branch_name=feature_sales1"

git add .
git commit -m "Add sales1 pipeline"
git push -u origin feature/sales1
```

## Feature Branch 2

```
git checkout main
git pull origin main
git checkout -b feature/sales2

# make changes

databricks bundle validate -t dev --var="branch_name=feature_sales2"
databricks bundle deploy -t dev --var="branch_name=feature_sales2"

git add .
git commit -m "Add sales2 pipeline"
git push -u origin feature/sales2
```

> Create PRs and merge them into `main`

## CI/CD after PR Merge

```
git checkout main
git pull origin main

git status

databricks bundle validate -t uat
databricks bundle deploy -t uat
```

## Notes:

Check whether the PR process already deleted the remote feature branch

```
git branch -r
```

If not, delete the remote & local feature branch after update.

```
git checkout main
git pull origin main

git push origin --delete feature/sales1
git push origin --delete feature/sales2

git branch -d feature/sales1
git branch -d feature/sales2
```
