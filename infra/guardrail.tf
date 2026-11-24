resource "aws_bedrock_guardrail" "main" {
  name                      = "${local.name}-guardrail"
  description               = "Content filtering, PII masking and prompt-attack detection for the campus assistant."
  blocked_input_messaging   = "Sorry, I can't help with that request. I can answer questions about study, enrolment and campus services."
  blocked_outputs_messaging = "Sorry, I can't share that response. Please rephrase your question or contact student services."

  # 1. Harmful content, plus prompt-attack detection on the input side.
  content_policy_config {
    dynamic "filters_config" {
      for_each = toset(["HATE", "INSULTS", "SEXUAL", "VIOLENCE", "MISCONDUCT"])
      content {
        type            = filters_config.value
        input_strength  = "HIGH"
        output_strength = "HIGH"
      }
    }
    filters_config {
      type            = "PROMPT_ATTACK"
      input_strength  = "HIGH"
      output_strength = "NONE" # prompt-attack filtering applies to inputs only
    }
  }

  # 2. PII: mask contact details, block card numbers outright.
  sensitive_information_policy_config {
    pii_entities_config {
      type   = "EMAIL"
      action = "ANONYMIZE"
    }
    pii_entities_config {
      type   = "PHONE"
      action = "ANONYMIZE"
    }
    pii_entities_config {
      type   = "CREDIT_DEBIT_CARD_NUMBER"
      action = "BLOCK"
    }
    regexes_config {
      name        = "student-id"
      description = "Eight-digit student ID"
      pattern     = "\\b\\d{8}\\b"
      action      = "ANONYMIZE"
    }
  }

  # 3. A denied topic that matters to a university: academic integrity.
  topic_policy_config {
    topics_config {
      name       = "assessment-ghostwriting"
      type       = "DENY"
      definition = "Requests to write, complete or rewrite an assessable assignment, essay, exam answer or thesis for a student to submit as their own work."
      examples = [
        "Write my 2000 word essay on climate policy so I can submit it tomorrow.",
        "Complete this assignment for me and make it pass the plagiarism check.",
        "Give me the answers to my take-home exam.",
      ]
    }
  }
}

# Agents attach a numbered, immutable guardrail version rather than the draft.
resource "aws_bedrock_guardrail_version" "v1" {
  guardrail_arn = aws_bedrock_guardrail.main.guardrail_arn
  description   = "Initial version"
  skip_destroy  = false
}
