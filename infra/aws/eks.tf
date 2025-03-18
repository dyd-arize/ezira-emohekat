module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.31"

  cluster_name    = "arize-${var.tag_environment}"
  cluster_version = "1.31"

  cluster_endpoint_public_access           = true
  enable_cluster_creator_admin_permissions = true


  cluster_compute_config = {
    enabled    = true
    node_pools = ["system", "general-purpose"]
  }

  vpc_id     = module.vpc.vpc_id
  subnet_ids = [for subnet_id in module.vpc.public_subnets : subnet_id]

  cluster_security_group_additional_rules = {
    egress_all = {
      description = "Allow all outbound traffic"
      protocol    = "-1"
      from_port   = 0
      to_port     = 0
      type        = "egress"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }

  tags = merge(
    local.common_tags,
    {
      Application = "EKS"
    }
  )
}
