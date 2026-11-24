# The agent itself is code (agent/core.py), not a Bedrock Agents resource.
#
# Amazon Bedrock Agents became "Agents Classic" and closed to new accounts on
# 30 July 2026: CreateAgent returns 403 for an account with no prior usage.
# AWS's recommended replacement is a code-defined agent, hosted on Amazon
# Bedrock AgentCore Runtime. Knowledge Bases and Guardrails are unaffected,
# so the agent uses the ones this stack builds.
#
# This file holds the one thing the agent needs from IAM: a least-privilege
# policy, attached to whatever identity runs the agent loop (the AgentCore
# Runtime execution role in the cloud, or your own user when run locally).

data "aws_iam_policy_document" "agent_runtime" {
  statement {
    sid     = "InvokeModels"
    actions = ["bedrock:InvokeModel", "bedrock:InvokeModelWithResponseStream"]
    # Inference profiles route to the model in more than one region, so
    # the foundation-model ARN cannot be pinned to a single region.
    resources = [
      "arn:${data.aws_partition.now.partition}:bedrock:*::foundation-model/*",
      "arn:${data.aws_partition.now.partition}:bedrock:*:${local.account}:inference-profile/*",
    ]
  }
  statement {
    sid       = "SearchKnowledgeBase"
    actions   = ["bedrock:Retrieve"]
    resources = [aws_bedrockagent_knowledge_base.main.arn]
  }
  statement {
    sid       = "ApplyGuardrail"
    actions   = ["bedrock:ApplyGuardrail"]
    resources = [aws_bedrock_guardrail.main.guardrail_arn]
  }
  statement {
    sid       = "CallTools"
    actions   = ["lambda:InvokeFunction"]
    resources = [aws_lambda_function.tools.arn]
  }
}

resource "aws_iam_policy" "agent_runtime" {
  name        = "${local.name}-agent-runtime"
  description = "What the campus assistant agent may do: call models, search its knowledge base, apply its guardrail, call its tools."
  policy      = data.aws_iam_policy_document.agent_runtime.json
}
