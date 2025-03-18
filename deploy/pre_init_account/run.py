import boto3
from botocore.exceptions import ClientError
import json
import os
import logging
import sys

# set logger config
logging.basicConfig(
    format="[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
    handlers=[
        ## log in console
        logging.StreamHandler(sys.stdout),
    ],
)
# set logger level
logger = logging.getLogger(__name__)
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
logger.setLevel(logging.DEBUG if DEBUG else logging.INFO)


BUCKET_NAME = "drewyangdev-arize-state"
IAM_USER = "terraformer"
POLICY_NAME = "TerraformS3Policy"

# Initialize AWS clients
AWS_PROFILE = os.getenv("AWS_PROFILE")
session = boto3.Session(profile_name=AWS_PROFILE)
AWS_REGION = session.region_name
AWS_ACCOUNT = session.client("sts").get_caller_identity()["Account"]
s3_client = session.client("s3")
iam_client = session.client("iam")

# TODO - automate init new account


def create_s3_bucket():
    logger.info(f"Creating S3 bucket: {BUCKET_NAME}...")
    try:
        s3_client.create_bucket(
            Bucket=BUCKET_NAME,
            CreateBucketConfiguration={"LocationConstraint": AWS_REGION},
        )
    except ClientError as e:
        if e.response["Error"]["Code"] == "BucketAlreadyOwnedByYou":
            logger.info("Bucket already exists, continuing...")
        else:
            raise

    # Enable versioning
    logger.info("Enabling versioning on bucket...")
    s3_client.put_bucket_versioning(
        Bucket=BUCKET_NAME, VersioningConfiguration={"Status": "Enabled"}
    )
    logger.info("S3 bucket setup complete.")


def create_iam_user():
    logger.info(f"Creating IAM user: {IAM_USER}...")
    try:
        iam_client.create_user(UserName=IAM_USER)
    except iam_client.exceptions.EntityAlreadyExistsException:
        logger.info("User already exists, continuing...")


def create_and_attach_policies():
    tf_policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": "s3:ListBucket",
                "Resource": f"arn:aws:s3:::{BUCKET_NAME}",
            },
            {
                "Effect": "Allow",
                "Action": ["s3:GetObject", "s3:PutObject"],
                "Resource": [f"arn:aws:s3:::{BUCKET_NAME}/terraform/state.tfstate"],
            },
            {
                "Effect": "Allow",
                "Action": ["s3:GetObject", "s3:PutObject", "s3:DeleteObject"],
                "Resource": [
                    f"arn:aws:s3:::{BUCKET_NAME}/terraform/state.tfstate.tflock"
                ],
            },
        ],
    }
    create_and_attach_policy(tf_policy_document)
    # TODO - other policies to create resources


def create_and_attach_policy(policy_document):
    logger.info("Creating IAM policy...")
    try:
        policy_response = iam_client.create_policy(
            PolicyName=POLICY_NAME, PolicyDocument=json.dumps(policy_document)
        )
    except ClientError as e:
        if e.response["Error"]["Code"] == "EntityAlreadyExists":
            logger.info("Policy already exists, continuing...")
            policy_response = iam_client.get_policy(
                PolicyArn=f"arn:aws:iam::{AWS_ACCOUNT}:policy/{POLICY_NAME}"
            )
        else:
            raise
    policy_arn = policy_response["Policy"]["Arn"]

    logger.info("Attaching policy to user...")
    iam_client.attach_user_policy(UserName=IAM_USER, PolicyArn=policy_arn)


def create_access_keys():
    logger.info("Creating access keys for user...")
    # List existing access keys for the user
    existing_keys = iam_client.list_access_keys(UserName=IAM_USER)

    if existing_keys["AccessKeyMetadata"]:
        logger.info(f"User '{IAM_USER}' already has an access key. Skipping creation.")
        return
    response = iam_client.create_access_key(UserName=IAM_USER)
    # TODO - not secure, need secret manager to automate
    logger.info(f"Access Key: {response['AccessKey']['AccessKeyId']}")
    logger.info(f"Secret Key: {response['AccessKey']['SecretAccessKey']}")


def main():
    create_s3_bucket()
    create_iam_user()
    create_and_attach_policy()
    create_access_keys()
    logger.info("Terraform AWS setup complete!")


if __name__ == "__main__":
    main()
