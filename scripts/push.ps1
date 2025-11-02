Param(
  [string]$RemoteRepo = "https://github.com/caiorcastro/FIAP-Enterprise-Challenge-Sprint-1-YOUVISA",
  [string]$Branch = "main"
)

# Requer: $env:GITHUB_TOKEN com escopo 'repo'
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
  Write-Error "git não encontrado no PATH."; exit 1
}

$isRepo = Test-Path .git
if (-not $isRepo) {
  git init
}

git add .
try { git commit -m "docs: planejamento sprint 1 (YOUVISA)" } catch { }

# Configurar remote origin
if (-not (git remote | Select-String -Quiet "origin")) {
  git remote add origin $RemoteRepo
}

# Push usando token (sem salvar o token permanentemente)
if (-not $env:GITHUB_TOKEN) {
  Write-Warning "Defina $env:GITHUB_TOKEN para push via HTTPS autenticado. Ex.: `$env:GITHUB_TOKEN='xxxxx'`";
  Write-Host "Tentando push sem token (se SSH estiver configurado, funcionará)."
  git branch -M $Branch
  git push -u origin $Branch
  exit $LASTEXITCODE
}

$remoteWithToken = $RemoteRepo -replace "https://","https://$env:GITHUB_TOKEN@"
git remote set-url origin $remoteWithToken
git branch -M $Branch
git push -u origin $Branch

# Restaurar URL limpa
git remote set-url origin $RemoteRepo

Write-Host "Push concluído. Para congelar versão, crie a tag: git tag v1.0-sprint1 && git push origin v1.0-sprint1"

