# ---------- Model invocation logging ----------

resource "aws_cloudwatch_log_group" "invocations" {
  name              = "/bedrock/${local.name}/invocations"
  retention_in_days = var.log_retention_days
}

data "aws_iam_policy_document" "logging" {
  statement {
    actions   = ["logs:CreateLogStream", "logs:PutLogEvents"]
    resources = ["${aws_cloudwatch_log_group.invocations.arn}:log-stream:aws/bedrock/modelinvocations"]
  }
}

resource "aws_iam_role" "logging" {
  name               = "${local.name}-bedrock-logging"
  assume_role_policy = data.aws_iam_policy_document.bedrock_trust.json
}

resource "aws_iam_role_policy" "logging" {
  role   = aws_iam_role.logging.id
  policy = data.aws_iam_policy_document.logging.json
}

resource "aws_bedrock_model_invocation_logging_configuration" "this" {
  count = var.enable_invocation_logging ? 1 : 0

  logging_config {
    text_data_delivery_enabled      = var.log_prompt_text
    embedding_data_delivery_enabled = false
    image_data_delivery_enabled     = false
    cloudwatch_config {
      log_group_name = aws_cloudwatch_log_group.invocations.name
      role_arn       = aws_iam_role.logging.arn
    }
  }

  depends_on = [time_sleep.iam]
}

# ---------- Dashboard ----------

locals {
  metric_widgets = [
    { title = "Invocations per model", metric = "Invocations", stat = "Sum" },
    { title = "Latency per model (ms, average)", metric = "InvocationLatency", stat = "Average" },
    { title = "Input tokens per model", metric = "InputTokenCount", stat = "Sum" },
    { title = "Output tokens per model", metric = "OutputTokenCount", stat = "Sum" },
  ]
}

resource "aws_cloudwatch_dashboard" "main" {
  dashboard_name = local.name
  dashboard_body = jsonencode({
    widgets = concat(
      [for i, w in local.metric_widgets : {
        type   = "metric"
        x      = (i % 2) * 12
        y      = floor(i / 2) * 6
        width  = 12
        height = 6
        properties = {
          title   = w.title
          region  = var.region
          view    = "timeSeries"
          period  = 300
          metrics = [[{ expression = "SEARCH('{AWS/Bedrock,ModelId} MetricName=\"${w.metric}\"', '${w.stat}', 300)", id = "e${i}" }]]
        }
      }],
      [
        {
          type   = "metric"
          x      = 0
          y      = 12
          width  = 12
          height = 6
          properties = {
            title   = "Demo comparison: cost per question (USD)"
            region  = var.region
            view    = "timeSeries"
            period  = 300
            metrics = [[{ expression = "SEARCH('{CampusAssistant,Model} MetricName=\"CostUSD\"', 'Average', 300)", id = "c1" }]]
          }
        },
        {
          type   = "metric"
          x      = 12
          y      = 12
          width  = 12
          height = 6
          properties = {
            title   = "Guardrail interventions"
            region  = var.region
            view    = "timeSeries"
            period  = 300
            metrics = [[{ expression = "SEARCH('{AWS/Bedrock/Guardrails,GuardrailArn,GuardrailVersion} MetricName=\"InvocationsIntervened\"', 'Sum', 300)", id = "g1" }]]
          }
        },
        {
          type   = "log"
          x      = 0
          y      = 18
          width  = 24
          height = 7
          properties = {
            title  = "Tokens per model from the invocation log"
            region = var.region
            view   = "table"
            query  = "SOURCE '${aws_cloudwatch_log_group.invocations.name}' | stats count(*) as calls, sum(input.inputTokenCount) as input_tokens, sum(output.outputTokenCount) as output_tokens by modelId"
          }
        },
      ]
    )
  })
}
