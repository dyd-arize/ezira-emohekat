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

  tags = merge(
    local.common_tags,
    {
      Application = "EKS"
    }
  )
}
