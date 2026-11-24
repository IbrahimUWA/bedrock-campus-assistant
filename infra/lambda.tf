data "archive_file" "tools" {
  type        = "zip"
  source_dir  = "${path.module}/../lambda"
  output_path = "${path.module}/.build/tools.zip"
}

data "aws_iam_policy_document" "lambda_trust" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "tools" {
  name               = "${local.name}-tools"
  assume_role_policy = data.aws_iam_policy_document.lambda_trust.json
}

resource "aws_iam_role_policy_attachment" "tools_logs" {
  role       = aws_iam_role.tools.name
  policy_arn = "arn:${data.aws_partition.now.partition}:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_cloudwatch_log_group" "tools" {
  name              = "/aws/lambda/${local.name}-tools"
  retention_in_days = var.log_retention_days
}

resource "aws_lambda_function" "tools" {
  function_name    = "${local.name}-tools"
  role             = aws_iam_role.tools.arn
  runtime          = "python3.12"
  handler          = "handler.lambda_handler"
  filename         = data.archive_file.tools.output_path
  source_code_hash = data.archive_file.tools.output_base64sha256
  timeout          = 10
  depends_on       = [aws_cloudwatch_log_group.tools]
}

# Only this account's Bedrock agents may invoke the function.
resource "aws_lambda_permission" "bedrock" {
  statement_id   = "AllowBedrockAgents"
  action         = "lambda:InvokeFunction"
  function_name  = aws_lambda_function.tools.function_name
  principal      = "bedrock.amazonaws.com"
  source_account = local.account
  source_arn     = "arn:${data.aws_partition.now.partition}:bedrock:${var.region}:${local.account}:agent/*"
}
