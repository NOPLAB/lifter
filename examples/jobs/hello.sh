#!/bin/bash
# =============================================================================
# Hello World ジョブ - 最もシンプルな例
# =============================================================================
#
# 使用方法:
#   lifter submit examples/jobs/hello.sh
#
# =============================================================================

#SBATCH --job-name=hello_world
#SBATCH --partition={{SLURM_PARTITION}}
#SBATCH --nodes=1
#SBATCH --time=00:05:00
#SBATCH --output=logs/hello_%j.out
#SBATCH --error=logs/hello_%j.err

echo "Hello from Slurm!"
echo "Date: $(date)"
echo "Hostname: $(hostname)"
echo "Job ID: ${SLURM_JOB_ID:-N/A}"
echo "Done!"
