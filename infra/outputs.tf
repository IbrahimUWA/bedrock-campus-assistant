output "region" {
  value = var.region
}

output "docs_bucket" {
  value = aws_s3_bucket.docs.bucket
}

output "knowledge_base_id" {
  value = aws_bedrockagent_knowledge_base.main.id
}

output "data_source_id" {
  value = aws_bedrockagent_data_source.pages.data_source_id
}

output "guardrail_id" {
  value = aws_bedrock_guardrail.main.guardrail_id
}

output "guardrail_version" {
  value = aws_bedrock_guardrail_version.v1.version
}

output "models" {
  description = "Model key to model ID, one per model being compared."
  value       = var.agent_models
}

output "agent_runtime_policy_arn" {
  value = aws_iam_policy.agent_runtime.arn
}

output "invocation_log_group" {
  value = aws_cloudwatch_log_group.invocations.name
}

output "tools_function" {
  value = aws_lambda_function.tools.function_name
}

output "dashboard_url" {
  value = "https://${var.region}.console.aws.amazon.com/cloudwatch/home?region=${var.region}#dashboards:name=${aws_cloudwatch_dashboard.main.dashboard_name}"
}
