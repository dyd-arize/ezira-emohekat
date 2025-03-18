module "ecr_registry" {
  source = "terraform-aws-modules/ecr/aws"

  repository_name = "arize-${var.tag_environment}/webapp"

  ## TODO
  # repository_read_write_access_arns = ["arn:aws:iam::012345678901:role/terraform"]

  # mutable just for dev environment
  repository_image_tag_mutability = var.tag_environment == "dev" ? "MUTABLE" : "IMMUTABLE"

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

  tags = local.common_tags
}
