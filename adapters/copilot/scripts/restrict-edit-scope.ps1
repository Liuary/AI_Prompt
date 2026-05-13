# restrict-edit-scope.ps1
# PreToolUse hook for GitHub Copilot custom agents.
# Restricts file write/edit operations to allowed path prefixes.
#
# Usage:
#   powershell -File restrict-edit-scope.ps1 -AllowedPrefix ".ai/"
#   powershell -File restrict-edit-scope.ps1 -AllowedPrefix ".ai/code_review/"

param(
    [string]$AllowedPrefix
)

$input_json = $input | Out-String
try {
    $data = $input_json | ConvertFrom-Json
} catch {
    $reason = "Failed to parse hook input JSON"
    $result = @{
        hookSpecificOutput = @{
            hookEventName = "PreToolUse"
            permissionDecision = "ask"
            permissionDecisionReason = $reason
        }
    }
    Write-Output ($result | ConvertTo-Json -Depth 4)
    exit 0
}

# 仅拦截编辑类工具
$tool_name = $data.tool_name
if ($tool_name -notin @("edit", "write", "Write", "Edit")) {
    $result = @{
        hookSpecificOutput = @{
            hookEventName = "PreToolUse"
            permissionDecision = "allow"
            permissionDecisionReason = "Tool $tool_name does not require path restriction"
        }
    }
    Write-Output ($result | ConvertTo-Json -Depth 4)
    exit 0
}

# 提取目标路径
$target_paths = @()
if ($data.tool_input) {
    $input_obj = $data.tool_input
    if ($input_obj.filePath) { $target_paths += $input_obj.filePath }
    if ($input_obj.file_path) { $target_paths += $input_obj.file_path }
    if ($input_obj.path) { $target_paths += $input_obj.path }
    if ($input_obj.files) {
        if ($input_obj.files -is [array]) { $target_paths += $input_obj.files }
        else { $target_paths += $input_obj.files -split ',' }
    }
    if ($input_obj.oldString -and $input_obj.filePath) {
        $target_paths += $input_obj.filePath
    }
}

if ($target_paths.Count -eq 0) {
    # 无法确定目标路径，默认询问
    $result = @{
        hookSpecificOutput = @{
            hookEventName = "PreToolUse"
            permissionDecision = "ask"
            permissionDecisionReason = "Unable to determine the target file path from tool input. Please confirm before continuing."
        }
    }
    Write-Output ($result | ConvertTo-Json -Depth 4)
    exit 0
}

# 检查路径是否在允许范围内
$blocked = @()
foreach ($p in $target_paths) {
    $normalized = $p -replace '\\', '/' -replace '^/+', ''
    if ($normalized -notlike "$AllowedPrefix*") {
        $blocked += $normalized
    }
}

if ($blocked.Count -gt 0) {
    $result = @{
        hookSpecificOutput = @{
            hookEventName = "PreToolUse"
            permissionDecision = "deny"
            permissionDecisionReason = "This agent may only edit these paths: $AllowedPrefix. Blocked target paths: $($blocked -join ', ')."
        }
    }
} else {
    $result = @{
        hookSpecificOutput = @{
            hookEventName = "PreToolUse"
            permissionDecision = "allow"
            permissionDecisionReason = "All target paths within allowed prefix: $AllowedPrefix"
        }
    }
}

Write-Output ($result | ConvertTo-Json -Depth 4)
