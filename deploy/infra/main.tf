terraform {
  required_version = ">= 1.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket       = "arize-terraform-state"
    key          = "terraform/state.tfstate"
    region       = var.aws_region
    use_lockfile = true
  }
}

provider "aws" {
  region = var.aws_region
}
