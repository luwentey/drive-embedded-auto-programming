# 本地初始化 Git 并推送到 GitHub（令牌仅通过环境变量传入，勿写入脚本）
# 用法:
#   $env:GH_TOKEN = "ghp_xxxx"   # 在 PowerShell 中临时设置
#   .\scripts\setup-repo.ps1

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root

if (-not $env:GH_TOKEN) {
    Write-Error "请先设置环境变量 GH_TOKEN（GitHub Personal Access Token）"
}

if (-not (Test-Path .git)) {
    git init
    git add -A
    git commit -m "Initial commit: drive embedded auto-programming codegen tool"
}

$desc = "驱动器嵌入式软件自动编程 - 参数化生成电机驱动固件代码"
$names = @(
    "drive-embedded-auto-programming",
    "drive-embedded-auto-programming-wenlu"
)

$created = $false
foreach ($name in $names) {
    gh repo create $name --public --source=. --remote=origin --description $desc --push 2>$null
    if ($LASTEXITCODE -eq 0) { $created = $true; break }
    git remote remove origin 2>$null
}

if (-not $created) {
    $user = gh api user -q .login
    $fallback = "$user-drive-embedded-codegen"
    gh repo create $fallback --public --source=. --remote=origin --description $desc --push
}

Write-Host "`n--- 完成 ---"
git log -1 --oneline
git remote get-url origin
