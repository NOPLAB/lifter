#!/bin/bash
# =============================================================================
# シンプルなPythonジョブ
# =============================================================================
#
# 使用方法:
#   lifter submit examples/jobs/simple_python.sh
#
# =============================================================================

#SBATCH --job-name=simple_python
#SBATCH --partition={{SLURM_PARTITION}}
#SBATCH --nodes=1
#SBATCH --gpus=1
#SBATCH --time=00:30:00
#SBATCH --output=logs/simple_python_%j.out
#SBATCH --error=logs/simple_python_%j.err

set -euo pipefail

echo "=== Environment ==="
echo "Date: $(date)"
echo "Hostname: $(hostname)"
echo "Python: $(python3 --version)"

# GPUが使える場合は表示
nvidia-smi 2>/dev/null || echo "No GPU available"

echo ""
echo "=== Running Python Script ==="

python3 << 'EOF'
import sys
import os

print(f"Python version: {sys.version}")
print(f"Working directory: {os.getcwd()}")

# PyTorchが使える場合
try:
    import torch
    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(0)}")
except ImportError:
    print("PyTorch not installed")

print("\nDone!")
EOF

echo ""
echo "=== Job Completed ==="
