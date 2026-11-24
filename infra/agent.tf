# ---------- Agent role ----------

data "aws_iam_policy_document" "agent" {
  statement {
    sid     = "InvokeModels"
    actions = ["bedrock:InvokeModel", "bedrock:InvokeModelWithResponseStream", "bedrock:GetInferenceProfile"]
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
}

resource "aws_iam_role" "agent" {
  name               = "AmazonBedrockExecutionRoleForAgents_${local.name}"
  assume_role_policy = data.aws_iam_policy_document.bedrock_trust.json
}

resource "aws_iam_role_policy" "agent" {
  role   = aws_iam_role.agent.id
  policy = data.aws_iam_policy_document.agent.json
}

# ---------- One agent per model ----------

locals {
  agent_instruction = <<-EOT
    You are Campus Assistant, a helpful assistant for students and staff of a university.
    Answer questions about study, enrolment, key dates and campus services using the knowledge base, and always base factual claims on what it returns.
    If the knowledge base does not contain the answer, say you do not know and suggest contacting student services. Never invent dates, fees or policies.
    Use the get_unit_outline tool when the user asks about a specific unit code.
    Use the create_support_request tool only when the user clearly asks to raise a request with a human team, and confirm the category and a one-sentence summary first.
    Keep answers short and plain. Do not write assessable work for students.
  EOT
}

resource "aws_bedrockagent_agent" "this" {
  for_each = var.agent_models

  agent_name                  = "${local.name}-${each.key}"
  description                 = "Campus assistant on ${each.value}"
  agent_resource_role_arn     = aws_iam_role.agent.arn
  foundation_model            = each.value
  instruction                 = local.agent_instruction
  idle_session_ttl_in_seconds = 600
  prepare_agent               = true

  guardrail_configuration = [{
    guardrail_identifier = aws_bedrock_guardrail.main.guardrail_id
    guardrail_version    = aws_bedrock_guardrail_version.v1.version
  }]

  depends_on = [time_sleep.iam_agent]
}

resource "aws_bedrockagent_agent_knowledge_base_association" "this" {
  for_each = var.agent_models

  agent_id             = aws_bedrockagent_agent.this[each.key].agent_id
  agent_version        = "DRAFT"
  knowledge_base_id    = aws_bedrockagent_knowledge_base.main.id
  knowledge_base_state = "ENABLED"
  description          = "Public university web pages: courses, enrolment, key dates, fees, campus services and student support. Search this for any factual question."
}

resource "aws_bedrockagent_agent_action_group" "tools" {
  for_each = var.agent_models

  agent_id          = aws_bedrockagent_agent.this[each.key].agent_id
  agent_version     = "DRAFT"
  action_group_name = "student-tools"
  description       = "Look up a unit outline and raise a support request."
  prepare_agent     = true

  action_group_executor {
    lambda = aws_lambda_function.tools.arn
  }

  function_schema {
    member_functions {
      functions {
        name        = "get_unit_outline"
        description = "Return the outline for one unit: title, credits, study periods, assessments and prerequisites."
        parameters {
          map_block_key = "unit_code"
          type          = "string"
          description   = "Unit code, four letters and four digits, for example DEMO1001"
          required      = true
        }
      }
      functions {
        name        = "create_support_request"
        description = "Raise a support request with a human team and return a reference number."
        parameters {
          map_block_key = "category"
          type          = "string"
          description   = "One of: enrolment, fees, it, accessibility, other"
          required      = true
        }
        parameters {
          map_block_key = "summary"
          type          = "string"
          description   = "One sentence describing what the user needs"
          required      = true
        }
      }
    }
  }

  # Changes to the same agent must not run in parallel, and the last
  # change must be the one that prepares the agent.
  depends_on = [
    aws_bedrockagent_agent_knowledge_base_association.this,
    aws_lambda_permission.bedrock,
  ]
}

# An alias freezes the prepared draft into a numbered version. It must be
# created after the knowledge base and action group are attached.
resource "aws_bedrockagent_agent_alias" "live" {
  for_each = var.agent_models

  agent_id         = aws_bedrockagent_agent.this[each.key].agent_id
  agent_alias_name = "live"
  description      = "Published version used by the demo scripts"

  depends_on = [aws_bedrockagent_agent_action_group.tools]
}
