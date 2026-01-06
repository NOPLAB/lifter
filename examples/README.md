# Examples

lifterの使用例集です。

## ディレクトリ構成

```
examples/
├── jobs/                    # シンプルなジョブスクリプト
│   ├── hello.sh             # Hello Worldジョブ
│   └── simple_python.sh     # Pythonスクリプト実行
├── sweeps/                  # W&B Sweep設定
│   ├── sweep_simple.yaml    # 入門用シンプル設定
│   └── sweep_openvla.yaml   # OpenVLA用設定
├── sweeps_remote/           # Slurmリモート実行用テンプレート
│   ├── simple_sweep.sh      # シンプルなSweepテンプレート
│   └── openvla_sweep.sh     # OpenVLA用テンプレート
└── sweeps_local/            # ローカル実行用テンプレート
    ├── simple_sweep.sh      # シンプルなSweepテンプレート
    └── openvla_sweep.sh     # OpenVLA用テンプレート
```

## クイックスタート

### 1. シンプルなジョブ投下

```bash
# Hello Worldジョブを投下
lifter submit examples/jobs/hello.sh

# ジョブ状態を確認
lifter status

# ジョブ完了を待機
lifter wait <job_id>
```

### 2. Pythonジョブの投下

```bash
lifter submit examples/jobs/simple_python.sh
```

### 3. シンプルなW&B Sweep

```bash
# リモート（Slurm）で実行
lifter sweep start examples/sweeps/sweep_simple.yaml \
  --template examples/sweeps_remote/simple_sweep.sh \
  --max-runs 5

# ローカルで実行
lifter sweep start examples/sweeps/sweep_simple.yaml \
  --local \
  --template examples/sweeps_local/simple_sweep.sh \
  --max-runs 5
```

## テンプレート変数

テンプレートでは以下の変数が使用できます：

| 変数                  | 説明                     |
| --------------------- | ------------------------ |
| `{{SWEEP_ID}}`        | W&B Sweep ID（自動注入） |
| `{{RUN_NUMBER}}`      | 実行番号（自動注入）     |
| `{{SLURM_PARTITION}}` | Slurmパーティション名    |
| `{{WANDB_API_KEY}}`   | W&B APIキー              |
| `{{WANDB_PROJECT}}`   | W&Bプロジェクト名        |
| `{{WANDB_ENTITY}}`    | W&Bエンティティ名        |

すべての`.env`変数がテンプレート変数として利用可能です。

## 必要な設定

`.env`ファイルに以下を設定：

```bash
# SSH接続設定
SLURM_SSH_HOST=your-cluster.example.com
SLURM_SSH_USER=your-username

# Slurm設定
SLURM_PARTITION=gpu

# W&B設定（Sweep使用時）
WANDB_API_KEY=your-api-key
WANDB_ENTITY=your-entity
WANDB_PROJECT=your-project
```
