#!/bin/bash
# =============================================================================
# シンプルなSweepテンプレート（Slurm用）
# =============================================================================
#
# 使用方法:
#   lifter sweep start examples/sweeps/sweep_simple.yaml \
#     --template examples/templates_remote/simple_sweep.sh \
#     --max-runs 5
#
# テンプレート変数:
#   {{SWEEP_ID}}    - W&B Sweep ID（自動注入）
#   {{RUN_NUMBER}}  - 実行番号（自動注入）
#   {{VAR}}         - .envファイルの変数
#
# =============================================================================

#SBATCH --job-name=sweep_{{SWEEP_ID}}_{{RUN_NUMBER}}
#SBATCH --partition={{SLURM_PARTITION}}
#SBATCH --nodes=1
#SBATCH --gpus=1
#SBATCH --time=01:00:00
#SBATCH --output=logs/sweep_%j.out
#SBATCH --error=logs/sweep_%j.err

set -euo pipefail

echo "=== Sweep Job Information ==="
echo "Date: $(date)"
echo "Hostname: $(hostname)"
echo "Sweep ID: {{SWEEP_ID}}"
echo "Run Number: {{RUN_NUMBER}}"
echo ""

# W&B設定
export WANDB_API_KEY={{WANDB_API_KEY}}
export WANDB_PROJECT={{WANDB_PROJECT}}
export WANDB_ENTITY={{WANDB_ENTITY}}

# ログディレクトリを作成
mkdir -p logs

echo "=== Starting W&B Agent ==="

# W&B Agentを実行（1回だけ実行）
wandb agent --count 1 "{{WANDB_ENTITY}}/{{WANDB_PROJECT}}/{{SWEEP_ID}}"

echo ""
echo "=== Job Completed ==="
echo "End time: $(date)"
