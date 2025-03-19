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
        - detect-secrets
        - terraform fmt/lint
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
    - [x] webapp fix
        - [x] re-organize webapp project structure
            - replace app.py with app module + run.py
            - add sqlalchemy as ORM, and models.py
        - [x] update `/` endpoint to query and show data
        - [x] remove the original insertion while-loop
            - add an `/insert` endpoint for data insertion
        - [x] add `/healthcheck` endpoint for readiness/liveness probe
    - [x] make a standalone process to `curl` the `/insert` endpoint as client in every 5 secs
        ```
        while true; do
            curl -X POST http://127.0.0.1:5000/insert \
                -H "Content-Type: application/json" \
                -d '{"ts": "'$$(date -u +"%Y-%m-%dT%H:%M:%S.%3N")'", "value": "'$$(awk 'BEGIN{srand(); print rand()}')'"}';
            sleep 5;
        done
        ```
        - to replicate what was implemented originally
    - [x] improve webapp dockerfile, add gunicorn
    - [ ] add unit and integration test with pytest
    - [ ] pagination
    - [ ] nice to be reactive refresh
- event-driven ingestion
    - [x] webapp minio-upload-event webhook endpoint
    - minio
        - [x] config webhook integration through env
        - [x] manually create
            - bucket
            - config event hook
        - [ ] terraform automate minio event hook config
            - create bucket
            - config bucket event hook with rabbitmq
            - create user
            - create policy for user to access bucket
            - create user access key/secret
    - [x] rabbitmq
    - celery
        - [x] integrate with flask, rabbitmq, redis(just for fun, keep failed job status)
        - [x] insert csv to postgres sql
        - [x] with flower monitoring
        - [ ] reprocess failed job
        - [x] BUG, failure return incorrect status - fixed
- [x] cross-platform image linux/amd64 and linux/arm64
- [x] CI push image with Github Actions
    - [ ] automate following tasks by terraform
        - [x] create an IAM user `actionbot` with ECR push access
        - [x] add secrets to repo secrets
    - [ ] docker + github actions cache builder stage dependencies
    - docker compose doesn't load to github actions default image store, causing 'tag does not exist' even build successfully [doc](https://docs.docker.com/build/ci/github-actions/multi-platform/#build-and-load-multi-platform-images)
        - [x] switch to docker/build-push-action with load=true
- [x] create a new AWS account
    - manually init new AWS account
        - setup root MFA
        - enable IAM Identity Center
        - create an admin user, admin group, permission set, associate group/set/account
        - configure local aws cli profile with sso(don't forget `cli-pager=`)
        - [x] terraform state bucket, IAM user `terraformer`, policy, user's aws access credentials
            - [ ] `terraformer`'s creds are printing to console and need manual aws profile config
            - [ ] IAM policies are not fully created yet, use admin for now
        - [ ] automate above
    - choose to use `us-west-1`
- manual deployment
    - manually terraform for infra provision/teardown
        - [x] VPC
            - CIDR: `10.0.1.0/24`, the last octet is enough(256 IPs) for this example
            - 2 AZs: us-west-1a/b
                - For each AZ:
                    - 1 public subnet for ingress
                    - ~~2 private subnet for cluster and worker nodes~~
                    - CIDR: `10.0.1.X/27, (32 - reserved) = 27 IPs` are enough
            - IGW, RT
        - [x] ECR, public registry
        - [x] EKS, going to try [EKS Auto](https://docs.aws.amazon.com/eks/latest/best-practices/automode.html), since it's new
            - [x] control plane, v1.31
            - [ ] ~~cluster, worker nodes~~ going to use built-in node pools for now
                - c6g.large system, c5a.large general-purpose
                - [ ] roll back to only default public subnet for now, image pull error -> network issue - doing
    - pre init cluster
        - [x] comes with metric-server
        - [x] gp3 storage class
        - [x] coredns
        - not required since port forwarding, but just for fun
            - [x] cert-manager + letsencrypt issuer
            - [ ] aws lb controller -> IMDS issue TODO
                    - create IAM policy
                    - associate IAM OIDC
                    - IAM service account
            - [ ] nginx ingress controller
                - ingress to work with route53
            - [ ] external secret operator + vault
    - manually kubectl
        - [x] postgres
        - [x] webapp
            - after port forwarding webapp, this inserts a row, and it'll show on the page after refresh
              ```
              curl -sX POST http://localhost:5000/insert \
              -H "Content-Type: application/json" \
              -d '{"ts": "'$(date -u +"%Y-%m-%dT%H:%M:%S.%6N")'", "value": "'$(awk 'BEGIN{srand(); print rand()}')'"}'
              ```
        - [x] minio
            - need manually create a bucket and add upload event webhook to the bucket
        - [x] redis
        - [x] rabbitmq
        - [x] celery
            - after port forwarding minio, and upload a sample csv
            ```
            [2025-03-18 22:30:05,369: INFO/MainProcess] Connected to amqp://rabbit:**@rabbitmq.webapp.svc.cluster.local:5672//
            [2025-03-18 22:30:05,375: INFO/MainProcess] mingle: searching for neighbors
            [2025-03-18 22:30:06,392: INFO/MainProcess] mingle: all alone
            [2025-03-18 22:30:06,406: INFO/MainProcess] celery@celery-68d69b95c5-wppcm ready.
            [2025-03-18 22:30:39,604: INFO/MainProcess] Task app.tasks.ingest_csv[920b29f5-04f8-448a-b57e-29120908fb0e] received
            [2025-03-18 22:30:39,659: INFO/ForkPoolWorker-2] Successfully ingested test/sample.csv.
            [2025-03-18 22:30:39,664: INFO/ForkPoolWorker-2] Task app.tasks.ingest_csv[920b29f5-04f8-448a-b57e-29120908fb0e] succeeded in 0.05905050200090045s: {'bucket': 'test', 'key': 'sample.csv', 'status': 'success'}
            ```
            - then refresh the webapp, new records were ingested
        - [x] flower
- [ ] CD with github actions, local test with act
- make a diagram and documentation
