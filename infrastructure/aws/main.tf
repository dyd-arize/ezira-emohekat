terraform {
  required_version = ">= 1.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket       = "drewyangdev-arize-state"
    key          = "terraform/state.tfstate"
    use_lockfile = true
  }
}

provider "aws" {
  region  = var.aws_region
  profile = var.aws_profile
  alias   = "default"
}

provider "aws" {
  region  = "us-east-1"
  profile = var.aws_profile
  alias   = "east"
}

locals {
  common_tags = {
    Contract    = var.tag_contract
    Environment = var.tag_environment
  }
}
