terraform {
  required_version = ">= 1.6"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.20"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.4"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
    time = {
      source  = "hashicorp/time"
      version = "~> 0.12"
    }
  }
}

provider "aws" {
  region = var.region
  default_tags {
    tags = {
      Project = var.project
      Purpose = "interview-demo"
    }
  }
}

data "aws_caller_identity" "me" {}
data "aws_partition" "now" {}

resource "random_id" "suffix" {
  byte_length = 3
}

locals {
  account = data.aws_caller_identity.me.account_id
  name    = "${var.project}-${random_id.suffix.hex}"
}
