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
}

locals {
  common_tags = {
    Contract    = var.tag_contract
    Application = var.tag_application
    Environment = var.tag_environment
  }
}
