# Interview Project
Small project to test developper skills. In this project you are required to deploy a simple
application then investigate and attempt to resolve a few issues that have been inserted for the
purpose of this exercise. The source files are provided.

## Getting Started

You should first clone this repository and work from your local machine. Do not push your changes to
this repository.

## Deployment

Chose a Kubernetes environment of your choice like GKE, EKS, or AKS. Deploy the manifest included as
part of this project.

	kubectl apply -f manifest.yaml


## Expected Results

Once the application has been deployed and issues resolved, you should be able to port forward to the
`webapp` on port 5000.

	kubectl port-forward service/webapp 5000

Then from your browser navigate to `http://localhost:5000`. If everything is working as expected you
will see 1 row of data:

![](https://github.com/antanguay/interview-project/blob/main/png/expected.png)

## Optional Bonus Enhancements

With the base application working, you can go for extra bonus points be creating  a new application
that interacts with the existing one. The new application should populate the database with data from
a file located in a blob store.

Here are the guidelines for the application:

- The application should run in its own namespace
- Use minio as the blob store
- Read a CSV file from the blob store and write each row of data with timestamp and value to postgres
- Add a feature such that anyone can drop in a file of this format into the blobstore and the application
  will automatically find it and write the results into postgres
- You can use any langage of your choice
- Deliver your solution as if it was a professional project

---

## Action Items

- dev improvement
    - [x] add .gitignore(python)
    - [x] setup pre-commit
        - pre-commit hooks
        - ruff
        - github actions lint
- webapp improvement
    - [x] use poetry as package manager
        - generate pyproject.yaml
        - upgrade dependencies, remove original requirements.txt
        - working with venv
        ```
        python -m venv .venv
        poetry install --no-root
        poetry run flask run
        ```
    - [x] add docker-compose.yaml that includes postgres for local testing
    - webapp fix
        - re-organize webapp project structure
            - replace app.py with app module + run.py
            - add sqlalchemy as ORM
        - update `/` endpoint to query and show data
        - remove the original insertion while-loop
            - add an `/insert` endpoint for data insertion
            - make a script to insert through this endpoint as a client and run this script as a cronjob
                - to replicate what implemented originally inserting every 5 seconds
    - improve webapp dockerfile, add gunicorn
- event-driven ingestion
    - minio upload event hook
    - queue
    - worker
- create AWS account
- deployment
    - github actions, local test with act
        - terraform for infra provision/teardown
        - system deployment
