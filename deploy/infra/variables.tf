variable "aws_region" {
  description = "The AWS region to deploy to"
  default     = "us-west-1"
}

variable "aws_profile" {
  description = "The AWS profile to use"
  # created by pre_init_infra/run.py, but need to manually config aws profile
  default = "terraformer"
}
