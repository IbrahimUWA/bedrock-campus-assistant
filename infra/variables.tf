variable "region" {
  description = "AWS region. Sydney keeps data in Australia."
  type        = string
  default     = "ap-southeast-2"
}

variable "project" {
  type    = string
  default = "campus-assistant"
}

variable "embedding_model_id" {
  description = "Embedding model used by the Knowledge Base."
  type        = string
  default     = "amazon.titan-embed-text-v2:0"
}

variable "embedding_dimensions" {
  type    = number
  default = 1024
}

variable "agent_models" {
  description = "The agent can run on any entry, so the same questions can be compared across models. Values are model IDs or inference profile IDs available in the region (check with scripts/00_preflight.py)."
  type        = map(string)
  default = {
    nova  = "apac.amazon.nova-lite-v1:0"
    haiku = "au.anthropic.claude-haiku-4-5-20251001-v1:0"
  }
}

variable "enable_invocation_logging" {
  description = "Model invocation logging is one setting per account and region. Set false if the account already has it configured."
  type        = bool
  default     = true
}

variable "log_prompt_text" {
  description = "Store prompt and response text in the invocation log. Token counts and latency are logged either way."
  type        = bool
  default     = true
}

variable "log_retention_days" {
  type    = number
  default = 7
}
