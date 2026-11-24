# Step by step

Every command is run from the repository folder in PowerShell. Each step says what it does, what you should see, and
what it teaches about Bedrock.

## 0. One-time setup

1. Create an AWS account at <https://aws.amazon.com> if you do not have one.
2. In the AWS console open **IAM > Users > Create user**, attach `AdministratorAccess` (fine for a short-lived
   personal demo account; never for a shared one), then **Security credentials > Create access key > CLI**.
3. Install the tools and sign in:

   ```powershell
   winget install Hashicorp.Terraform
   winget install Amazon.AWSCLI
   pip install -r requirements.txt
   aws configure          # paste the key and secret; region: ap-southeast-2; output: json
   ```

4. Check the account can run the demo:

   ```powershell
   python scripts\00_preflight.py
   ```

   Every line should start with `ok`. If a model line says `FAIL`, the script lists the inference profiles your region
   does offer; put one in `infra\terraform.tfvars`, for example:

   ```hcl
   agent_models = {
     nova  = "apac.amazon.nova-lite-v1:0"
     haiku = "global.anthropic.claude-haiku-4-5-20251001-v1:0"
   }
   ```

   The first time an account uses an Anthropic model, AWS asks for a short use-case form in the Bedrock console
   (**Model catalog**, pick the model).

### If model calls are refused on a new account

A new account can fail the preflight with `ThrottlingException: Too many tokens per day` on every model. Check
**Service Quotas > Amazon Bedrock**: if the applied values are 0 while the AWS defaults are not, the account is
restricted. What I did: upgraded from the Free plan to the Paid plan (credits are kept), submitted the Anthropic
use-case form, and opened an **Account and billing** support case asking for the default Bedrock quotas. Everything
except model calls still deploys, and step 3 onwards can run with `$env:CAMPUS_BACKEND = "local"` (see the README).

### Cost control

Create a budget in **Billing and Cost Management > Budgets** (for example 10 USD with an email alert) before you
deploy. Nothing in this stack bills while idle apart from a few cents of storage.

## 1. Build the infrastructure

```powershell
cd infra
terraform init
terraform plan            # read this: about 20 resources
terraform apply
terraform output -json | Set-Content -Encoding utf8 outputs.json
cd ..
```

What gets built, in dependency order:

1. S3 bucket for documents; S3 Vectors bucket and index (1024 dimensions, cosine).
2. IAM roles: one for the Knowledge Base, one for the agents, one for logging, one for the Lambda.
3. The Knowledge Base and its S3 data source.
4. The Lambda function with the two tools.
5. The guardrail and version 1 of it.
6. A least-privilege IAM policy for the agent loop. The agent itself is code, `agent/core.py`: Bedrock Agents is
   closed to new accounts (see the README).
7. The invocation log group, logging configuration and dashboard.

`.\deploy.ps1` runs steps 0 to 3 in one go.

## 2. Load the documents

```powershell
python scripts\01_fetch_pages.py
python scripts\02_ingest.py
```

The first script saves each page as text plus a `.metadata.json` file holding its URL. The second uploads them and
starts an **ingestion job**: Bedrock chunks each page, embeds the chunks with Titan Text Embeddings v2 and writes the
vectors to the index. It ends with a **retrieval check** that searches the Knowledge Base directly, with no LLM. Check
retrieval before you look at answers: if the right chunk is not retrieved, no model can answer correctly.

## 3. Ask questions

```powershell
python scripts\03_ask.py "When are results released after the mid-year exams?"
python scripts\03_ask.py "What are the assessments for unit DEMO2002?"
python scripts\03_ask.py "How much does parking cost per hour at Bentley?"
python scripts\03_ask.py --model haiku "When is the November exam period?"
```

Read the lines above each answer:

* `[search]` means the model chose to query the Knowledge Base, and shows the query it wrote.
* `[tool]` means it called a Lambda function, and shows the parameters it extracted.
* The numbered links are the citations.
* The last line is the model, total latency, tokens across every model call in the loop, and cost.

The third question is not in the pages. A good answer says so instead of guessing.

## 4. Test the guardrail

```powershell
python scripts\04_guardrail_tests.py
```

This calls `ApplyGuardrail`, which runs the policy on text without any model, so each rule is tested on its own. It
then sends three of the cases through the agent. Results land in `results\guardrail_tests.md`. Watch the
`model calls` column for blocked inputs: when the guardrail blocks the input, the model should never be called.

## 5. Compare the two models

```powershell
python scripts\05_compare_models.py --repeats 3
```

Ten questions go through the agent on each model: seven answered from the pages, two that need a tool, one that cannot be
answered. The script records latency, tokens and cost, checks each answer for the expected facts, writes
`results\comparison.md`, and publishes the numbers to CloudWatch under the `CampusAssistant` namespace.

## 6. Look at CloudWatch

```powershell
terraform -chdir=infra output dashboard_url
```

Open the link. The top four charts are Bedrock's own metrics per model (invocations, latency, input and output
tokens). Below are the comparison's cost per question, guardrail interventions, and a Logs Insights table of tokens
per model read from the invocation log. Metrics take a few minutes to appear.

To see one raw log record: **CloudWatch > Log groups > /bedrock/campus-assistant-…/invocations**. Each record has the
model id, token counts and, because `log_prompt_text` is on, the prompt and response. In production, decide
deliberately whether prompt text should be logged.

## 7. Chat interface

```powershell
streamlit run scripts\app.py
```

## 8. Change something and rerun

Edit the system prompt or a tool description in `agent\core.py` and rerun step 5: the question set is your regression
test. Edit a guardrail rule in `infra\guardrail.tf` and run `terraform apply`; the agent keeps using the numbered
version until you publish a new one.

## 9. Tear down

```powershell
.\deploy.ps1 -Destroy
```

Then check **Billing > Bills** the next day to confirm nothing is still running.
