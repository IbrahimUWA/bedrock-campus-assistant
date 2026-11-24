# Deploys the whole demo: checks the account, builds the infrastructure,
# downloads the pages and indexes them. Safe to run again.
#   .\deploy.ps1            deploy
#   .\deploy.ps1 -Destroy   remove everything
param([switch]$Destroy)
$ErrorActionPreference = "Stop"
$root = $PSScriptRoot

if ($Destroy) {
    terraform -chdir="$root\infra" destroy -auto-approve
    Remove-Item "$root\infra\outputs.json" -ErrorAction SilentlyContinue
    exit $LASTEXITCODE
}

python "$root\scripts\00_preflight.py"
if ($LASTEXITCODE -ne 0) { exit 1 }

terraform -chdir="$root\infra" init -input=false
terraform -chdir="$root\infra" apply -auto-approve -input=false
if ($LASTEXITCODE -ne 0) { exit 1 }
terraform -chdir="$root\infra" output -json | Set-Content -Encoding utf8 "$root\infra\outputs.json"

python "$root\scripts\01_fetch_pages.py"
python "$root\scripts\02_ingest.py"
if ($LASTEXITCODE -ne 0) { exit 1 }

Write-Host "`nDeployed. Try:  python scripts\03_ask.py `"When are exam results released?`""
