Param(
  [string]$In = "docs/diagrams/architecture.mmd",
  [string]$Out = "docs/diagrams/architecture.png"
)

if (-not (Get-Command npx -ErrorAction SilentlyContinue)) {
  Write-Error "npx não encontrado. Instale Node.js (https://nodejs.org)."; exit 1
}

npx -y @mermaid-js/mermaid-cli -i $In -o $Out

Write-Host "Gerado: $Out"

