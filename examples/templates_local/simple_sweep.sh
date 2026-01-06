#!/bin/bash
# =============================================================================
# シンプルなSweepテンプレート（ローカル実行用）
# =============================================================================
#
# 使用方法:
#   lifter sweep start examples/sweeps/sweep_simple.yaml \
#     --local \
#     --template examples/templates_local/simple_sweep.sh \
#     --max-runs 5
#
# テンプレート変数:
#   {{SWEEP_ID}}    - W&B Sweep ID（自動注入）
#   {{RUN_NUMBER}}  - 実行番号（自動注入）
#   {{VAR}}         - .envファイルの変数
#
# =============================================================================

set -euo pipefail

echo "=== Sweep Job Information (Local) ==="
echo "Date: $(date)"
echo "Hostname: $(hostname)"
echo "Sweep ID: {{SWEEP_ID}}"
echo "Run Number: {{RUN_NUMBER}}"
echo ""

# W&B設定
export WANDB_API_KEY={{WANDB_API_KEY}}
export WANDB_PROJECT={{WANDB_PROJECT}}
export WANDB_ENTITY={{WANDB_ENTITY}}

echo "=== Starting W&B Agent ==="

# W&B Agentを実行（1回だけ実行）
wandb agent --count 1 "{{WANDB_ENTITY}}/{{WANDB_PROJECT}}/{{SWEEP_ID}}"

echo ""
echo "=== Job Completed ==="
echo "End time: $(date)"
