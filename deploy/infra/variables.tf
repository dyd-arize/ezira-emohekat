variable "aws_region" {
  description = "The AWS region to deploy to"
  default     = "us-west-1"
}

variable "aws_profile" {
  description = "Created by pre_init_infra/run.py, but need to manually config aws profileThe AWS profile to use"
  default     = "terraformer"
}

variable "ecr_max_image_count" {
  description = "The maximum number of images to keep in the ECR repository"
  default     = 5
}


variable "tag_contract" {
  description = "Tag for contract"
  type        = string
}

variable "tag_application" {
  description = "Tag for application"
  type        = string
}

variable "tag_environment" {
  description = "Tag for environment"
  type        = string
}
