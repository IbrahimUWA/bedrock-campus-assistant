# ---------- Documents and vector store ----------

resource "aws_s3_bucket" "docs" {
  bucket        = "${local.name}-docs"
  force_destroy = true
}

resource "aws_s3_bucket_public_access_block" "docs" {
  bucket                  = aws_s3_bucket.docs.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# S3 Vectors: pay per GB stored and per query. No always-on cluster,
# unlike OpenSearch Serverless.
resource "aws_s3vectors_vector_bucket" "kb" {
  vector_bucket_name = "${local.name}-vectors"
  force_destroy      = true
}

resource "aws_s3vectors_index" "kb" {
  vector_bucket_name = aws_s3vectors_vector_bucket.kb.vector_bucket_name
  index_name         = "kb-index"
  data_type          = "float32"
  dimension          = var.embedding_dimensions
  distance_metric    = "cosine"

  # Bedrock stores the chunk text as metadata. Filterable metadata is
  # capped at 2 KB per vector, so the text must be non-filterable.
  metadata_configuration {
    non_filterable_metadata_keys = ["AMAZON_BEDROCK_TEXT", "AMAZON_BEDROCK_METADATA"]
  }
}

# ---------- Knowledge Base role ----------

data "aws_iam_policy_document" "bedrock_trust" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["bedrock.amazonaws.com"]
    }
    condition {
      test     = "StringEquals"
      variable = "aws:SourceAccount"
      values   = [local.account]
    }
  }
}

locals {
  embedding_model_arn = "arn:${data.aws_partition.now.partition}:bedrock:${var.region}::foundation-model/${var.embedding_model_id}"
}

data "aws_iam_policy_document" "kb" {
  statement {
    sid       = "Embed"
    actions   = ["bedrock:InvokeModel"]
    resources = [local.embedding_model_arn]
  }
  statement {
    sid       = "ReadDocs"
    actions   = ["s3:GetObject", "s3:ListBucket"]
    resources = [aws_s3_bucket.docs.arn, "${aws_s3_bucket.docs.arn}/*"]
  }
  statement {
    sid = "Vectors"
    actions = [
      "s3vectors:PutVectors",
      "s3vectors:GetVectors",
      "s3vectors:DeleteVectors",
      "s3vectors:QueryVectors",
      "s3vectors:GetIndex",
    ]
    resources = [aws_s3vectors_index.kb.index_arn]
  }
}

resource "aws_iam_role" "kb" {
  name               = "${local.name}-kb"
  assume_role_policy = data.aws_iam_policy_document.bedrock_trust.json
}

resource "aws_iam_role_policy" "kb" {
  role   = aws_iam_role.kb.id
  policy = data.aws_iam_policy_document.kb.json
}

# New IAM roles take a few seconds to become assumable by Bedrock.
resource "time_sleep" "iam" {
  create_duration = "20s"
  depends_on = [
    aws_iam_role_policy.kb,
    aws_iam_role_policy.logging,
  ]
}

# The agent policy refers to the knowledge base, so it gets its own wait.
resource "time_sleep" "iam_agent" {
  create_duration = "20s"
  depends_on      = [aws_iam_role_policy.agent]
}

# ---------- Knowledge Base ----------

resource "aws_bedrockagent_knowledge_base" "main" {
  name        = "${local.name}-kb"
  description = "Public university web pages for the campus assistant demo."
  role_arn    = aws_iam_role.kb.arn

  knowledge_base_configuration {
    type = "VECTOR"
    vector_knowledge_base_configuration {
      embedding_model_arn = local.embedding_model_arn
      embedding_model_configuration {
        bedrock_embedding_model_configuration {
          dimensions          = var.embedding_dimensions
          embedding_data_type = "FLOAT32"
        }
      }
    }
  }

  storage_configuration {
    type = "S3_VECTORS"
    s3_vectors_configuration {
      index_arn = aws_s3vectors_index.kb.index_arn
    }
  }

  depends_on = [time_sleep.iam]
}

resource "aws_bedrockagent_data_source" "pages" {
  knowledge_base_id    = aws_bedrockagent_knowledge_base.main.id
  name                 = "public-pages"
  data_deletion_policy = "DELETE"

  data_source_configuration {
    type = "S3"
    s3_configuration {
      bucket_arn         = aws_s3_bucket.docs.arn
      inclusion_prefixes = ["pages/"]
    }
  }

  vector_ingestion_configuration {
    chunking_configuration {
      chunking_strategy = "FIXED_SIZE"
      fixed_size_chunking_configuration {
        max_tokens         = 300
        overlap_percentage = 20
      }
    }
  }
}
