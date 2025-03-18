module "ecr_public" {
  source = "terraform-aws-modules/ecr/aws"
  providers = {
    aws = aws.east
  }

  repository_name = "arize-${var.tag_environment}/webapp"
  repository_type = "public"

  # mutable just for dev environment
  repository_image_tag_mutability = var.tag_environment == "dev" ? "MUTABLE" : "IMMUTABLE"

  public_repository_catalog_data = {
    operating_systems = ["Linux"]
    architectures     = ["x86-64", "ARM 64"]
  }

  repository_lifecycle_policy = jsonencode({
    rules = [
      {
        rulePriority = 1,
        description  = "Keep last ${var.ecr_max_image_count} images",
        selection = {
          tagStatus     = "tagged",
          tagPrefixList = ["v"],
          countType     = "imageCountMoreThan",
          countNumber   = var.ecr_max_image_count
        },
        action = {
          type = "expire"
        }
      }
    ]
  })

  tags = merge(
    local.common_tags,
    {
      Application = "ECR"
    }
  )
}
