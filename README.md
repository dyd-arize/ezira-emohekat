# Table of Contents

> Here is the original [README.md](./README.old.md)

- [Action Items](#action-items)
- [What's in here](#whats-in-here)
- [Run on Docker](#run-on-docker)
- [Run on AWS](#run-on-aws)

## Action Items
> It would be better if I have maken a Github project...

- **dev improvement**
    - [x] add .gitignore(python)
    - [x] setup pre-commit
        - pre-commit hooks
        - ruff
        - github actions lint
        - detect-secrets
        - terraform fmt/lint
- **webapp improvement**
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
- **event-driven ingestion**
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
- [x] **cross-platform image linux/amd64 and linux/arm64**
- [x] **CI push image with Github Actions**
    - [ ] automate following tasks by terraform
        - [x] create an IAM user `actionbot` with ECR push access
        - [x] add secrets to repo secrets
    - [ ] docker + github actions cache builder stage dependencies
    - docker compose doesn't load to github actions default image store, causing 'tag does not exist' even build successfully [doc](https://docs.docker.com/build/ci/github-actions/multi-platform/#build-and-load-multi-platform-images)
        - [x] switch to docker/build-push-action with load=true
- [x] **create a new AWS account**
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
- **manual deployment**
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
            - ~~cluster, worker nodes~~ going to use built-in node pools for now
                - c6g.large system, c5a.large general-purpose
                - [x] ~~roll back to only default public subnet for now, image pull error -> network issue~~ - fixed, public subnets have to turn on auto assign IP
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
        - [ ] would be nice to have a helm chart for above deployment
- [ ] **CD with github actions, local test with act**
    - [ ] tf provision
    - [ ] detect drift by tf refresh and plan on a schedule
    - [ ] deploy manifest
- [x] **make a diagram and documentation**

[Top](#table-of-contents)

## What's in Here

### Diagrams are more than words

#### Infrastructure Diagram:
![](https://github.com/dyd-arize/ezira-emohekat/blob/main/docs/infrastructure.drawio.png)
#### Component Diagram:
![](https://github.com/dyd-arize/ezira-emohekat/blob/main/docs/component.drawio.png)
#### Project Structure

```
.
├── .github
│   └── workflows
│       └── ci.yaml # build/push image
├── .gitignore
├── .pre-commit-config.yaml
├── .secrets.baseline # detect-secrets pre-commit hook
├── README.md
├── README.old.md
├── deployment # extended the original k8s manifests
│   ├── decouple
│   │   ├── celery.env # .env files are made for k8s secrets, all are git ignored
│   │   ├── celery.yaml
│   │   ├── celery_flower.yaml
│   │   ├── example.env # if manifest doesn't specify env, example.env is provided
│   │   ├── rabbitmq.env
│   │   ├── rabbitmq.yaml
│   │   └── redis.yaml
│   ├── minio
│   │   ├── minio.env
│   │   └── minio.yaml
│   ├── postgres
│   │   ├── postgres.env
│   │   └── postgres.yaml
│   ├── pre_init_cluster # k8s addons, some of them are not required for this project, just me playing around
│   │   ├── .env
│   │   ├── example.env
│   │   ├── manifests
│   │   │   ├── cert_manager_issuer.yaml
│   │   │   └── storage_class.yaml # required
│   │   ├── run.sh
│   │   └── scripts
│   │       ├── cert_manager.sh
│   │       ├── core_dns.sh # required
│   │       ├── ingress_controller.sh
│   │       ├── lb_controller.sh
│   │       ├── lb_controller_iam_policy.json
│   │       └── metrics_server.sh
│   ├── test.yaml # test EKS
│   └── webapp
│       ├── example.env
│       ├── webapp.env
│       └── webapp.yaml
├── docs
│   ├── component.drawio
│   ├── component.drawio.png
│   ├── infrastructure.drawio
│   └── infrastructure.drawio.png
├── infrastructure # provision before deployment
│   ├── aws
│   │   ├── .terraform.lock.hcl
│   │   ├── eks.tf
│   │   ├── inputs
│   │   │   └── dev.tfvars
│   │   ├── main.tf
│   │   ├── network.tf
│   │   ├── registry.tf
│   │   └── variables.tf
│   ├── pre_init_account # half way done, TODO
│   │   ├── requirements.txt
│   │   └── run.py
│   └── setup_minio # TODO
├── png
│   └── expected.png
└── webapp # extended the origional webapp
    ├── .dockerignore
    ├── Dockerfile
    ├── Makefile # once you setup .env files following example.env, you can 'make run' to run everything locally
    ├── app
    │   ├── __init__.py
    │   ├── models.py
    │   ├── routes.py
    │   ├── tasks.py
    │   ├── templates
    │   │   ├── base.html
    │   │   └── table.html
    │   └── utils.py
    ├── celery.env
    ├── data
    │   └── sample.csv # sample data for minio webhook
    ├── docker-compose.yaml
    ├── example.env
    ├── make_celery.py
    ├── minio.env
    ├── poetry.lock
    ├── postgres.env
    ├── pyproject.toml
    ├── rabbitmq.env
    ├── scripts
    │   └── source.auth_ecr.sh
    └── webapp.env
```

[Top](#table-of-contents)

## Development Environment
> OS: MacOS 13.6.3
> CPU: arch/amd64
> Docker version 28.0.1, build 068a01e
> Docker Compose version v2.33.1-desktop.1
> Docker Buildx version v0.21.1-desktop.2
> Docker Desktop 4.39.0 (184744)
> Poetry (version 2.1.1)
> Python 3.13.2

## Run with Docker

- Go to `$PROJECT_DIR/webapp/`
- Make individual .env files following by the example.env
- `make run` is going to `docker compose up --build`
    - In [docker-compose.yaml](./webapp/docker-compose.yaml), `services.web.build.platforms` was set to build for both `linux/amd64` and `linux/arm64`, the build process should be done in 10 mins.
        - If you don't have docker configured for multi-platform build [doc here](https://docs.docker.com/build/building/multi-platform/), you most likely will run into `Error: multiple platforms feature is currently not supported for docker driver`, just comment the entire `platforms` section.
- Services:
    - postgres: `psql -h localhost -p 5434 -U postgres -d webapp`
    - web: https://localhost:5000
    - minio: https://localhost:9001
    - rabbitmq
    - redis
    - celery
    - cflower(flower): https://localhost:5555
- Test:
    - For web, you can validate web's insert endpoint by curl, then refresh the page on https://localhost:5000:
    ```
    # once
    curl -sX POST http://web:5000/insert \
            -H "Content-Type: application/json" \
            -d '{"ts": "'$(date -u +"%Y-%m-%dT%H:%M:%S.%6N")'", "value": "'$(awk 'BEGIN{srand(); print rand()}')'"}';

    # continuously randomly 1-5 seconds
    while true; do
        curl -sX POST http://web:5000/insert \
            -H "Content-Type: application/json" \
            -d '{"ts": "'$(date -u +"%Y-%m-%dT%H:%M:%S.%6N")'", "value": "'$(awk 'BEGIN{srand(); print rand()}')'"}';
        sleep $$((RANDOM % 5 + 1));
    done
    ```
    - For minio webhook, you do need to manually configure it for now at http://localhost:9001 `Login -> Create a bucket -> Configure bucket PUT event sent to the webapp webhook`, then upload [sample.csv](./webapp/data/sample.csv) to the bucket.
        - You can go to http://localhost:5555 to check ingestion task status
        - Or you can refresh the page on https://localhost:5000, you should see records been inserted

[Top](#table-of-contents)

## Run on AWS
> This is not fully by CD workflows yet

- Create an AWS account
    - Setup root MFA
    - Enable IAM Identity Center
    - Create an admin user, admin group, permission set, associate group/set/account
    - Configure local aws cli profile with sso (don't forget `cli-pager=`)
    - Go to `$PROJECT_DIR/infrastructure/pre_init_account/`
        ```
        python -m venv .venv
        source .venv/bin/activate
        pip install -r requirements
        python run.py # not fully done
        ```
    - This will create:
        - Terraform state bucket
        - IAM user `terraformer`(currently policies are not in place)
- Provision AWS resources
    - Go to `$PROJECT_DIR/infrastructure/aws/`
    - Make sure you have `terraform` installed, [doc](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)
    - Make a `dev.tfvars` file under `$PROJECT_DIR/infrastructure/aws/stage/` following `example.tfvars`
    ```
    export AWS_PROFILE=<since 'terraformer' isn't ready, use admin profile for now>
    export AWS_REGION=us-west-1
    alias tf='terraform'
    tf init
    tf plan -var-file=./stage/dev.tfvars
    tf apply -var-file=./stage/dev.tfvars
    ```
- Deploy applications to EKS
    - After EKS is created, you need to get the kubeconfig
    ```
    # Also require AWS_PROFILE=admin profile for now
    aws eks update-kubeconfig --region us-west-1 --name <cluster name>
    ```
    - Go to `$PROJECT_DIR/deployment/pre_init_cluster`
        - Make a .env file with `CLUSTER_NAME=<EKS cluster name>`
        - Then run `bash run.sh`
        - This will install required k8s addons/resources and `webapp` namespace
    - Since secret manager isn't in place, k8s secrets need to be created from .env files. Similar to [Run on Docker](#run-on-docker), you need to make .env file for each deployment either following the manifest .yaml or example.env
    - Then run `bash deploy_all.sh`
    - Then these pods should be running
    ```
    k -n webapp get pods
    NAME                       READY   STATUS    RESTARTS        AGE
    celery-68d69b95c5-hz4wt    1/1     Running   0               3m39s
    cflower-5b4b9c67c8-84z7r   1/1     Running   0               3m39s
    minio-0                    1/1     Running   0               5m43s
    postgres-0                 1/1     Running   0               5m46s
    rabbitmq-0                 1/1     Running   0               3m38s
    redis-0                    1/1     Running   0               3m38s
    webapp-6cf45f9869-nb5gq    1/1     Running   2 (5m28s ago)   5m45s
    ```

[Top](#table-of-contents)


## Don't Forget To Teardown
```
# docker
docker compose down
docker system prune -f
```
```
# AWS
# in $PROJECT_DIR/infrastructure/aws/
tf destroy -var-file=./stage/dev.tfvars
```

[Top](#table-of-contents)
