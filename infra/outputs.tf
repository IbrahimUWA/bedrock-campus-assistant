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

output "agents" {
  description = "Per model key: the model, agent id and alias id."
  value = {
    for k, v in var.agent_models : k => {
      model    = v
      agent_id = aws_bedrockagent_agent.this[k].agent_id
      alias_id = aws_bedrockagent_agent_alias.live[k].agent_alias_id
    }
  }
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
