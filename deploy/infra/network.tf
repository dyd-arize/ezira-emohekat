module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = "arize-${var.tag_environment}"
  cidr = "10.0.1.0/24"

  azs = ["us-west-1a", "us-west-1b"]
  private_subnets = [
    "10.0.1.224/27", "10.0.1.192/27",
    "10.0.1.160/27", "10.0.1.128/27",
  ]
  private_subnet_names = [
    "arize-${var.tag_environment}-worker-us-west-1a",
    "arize-${var.tag_environment}-worker-us-west-1b",
    "arize-${var.tag_environment}-cluster-us-west-1a",
    "arize-${var.tag_environment}-cluster-us-west-1b",
  ]
  public_subnets = ["10.0.1.0/27", "10.0.1.32/27"]
  public_subnet_names = [
    "arize-${var.tag_environment}-public-us-west-1a",
    "arize-${var.tag_environment}-public-us-west-1b",
  ]

  create_igw = true

  tags = local.common_tags
}
