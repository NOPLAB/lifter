# CLAUDE.md

このファイルはClaude Code (claude.ai/code) がこのリポジトリで作業する際のガイダンスを提供します。

## プロジェクト概要

**lifter** はSSH経由でSlurmクラスターにジョブを投下するCLIツール。W&B Sweep統合によるハイパーパラメータ探索をサポート。リモート（Slurm）とローカル両方の実行モードに対応。

## よく使うコマンド

```bash
# 開発モードでインストール
pip install -e .

# 開発用依存関係も含めてインストール
pip install -e ".[dev]"

# リント実行
ruff check src/

# 型チェック
mypy src/

# テスト実行
pytest

# 単一テストの実行
pytest tests/test_config.py::test_load_settings -v
```

## CLI使用方法

```bash
# ジョブスクリプトを投下
lifter submit jobs/train.sh

# ジョブ状態を確認
lifter status [job_id]

# ジョブをキャンセル
lifter cancel <job_id>

# ジョブ完了を待機（ログ表示あり）
lifter wait <job_id>

# W&B Sweepを開始（リモートSlurm）
lifter sweep start sweeps/config.yaml --template templates/sweep.sh --max-runs 10

# W&B Sweepを開始（ローカル実行）
lifter sweep start sweeps/config.yaml --local --template templates_local/sweep.sh --max-runs 5

# 既存Sweepを再開
lifter sweep resume <sweep_id> --template templates/sweep.sh

# Sweep状態を確認
lifter sweep status <sweep_id>
```

## アーキテクチャ

### パッケージ構成

- `src/lifter/cli.py` - Typerを使用したメインCLIエントリーポイント。トップレベルコマンド（submit, status, cancel, wait）を定義
- `src/lifter/config.py` - Pydanticによる設定管理。リモート用の`Settings`、ローカル用の`LocalSettings`
- `src/lifter/clients/` - paramikoを使用したSSH/Slurmクライアントラッパー
- `src/lifter/sweep/` - W&B Sweep統合
- `src/lifter/core/` - 共有ユーティリティ（console, exceptions, CLIヘルパー）
- `src/lifter/ui/` - Richベースのステータステーブルとジョブ監視UI

### Sweep実行フロー

1. `sweep/cli.py` がCLIコマンドを処理し、`WandbSweepClient`経由でW&B Sweepを作成
2. `sweep/engine.py` に`SweepEngine`（Slurm用）と`LocalSweepEngine`クラスがある
3. 両方とも`sweep/base.py::BaseSweepEngine`を継承し、逐次/並列実行ロジックを共有
4. ジョブスクリプトは`sweep/template.py`でJinja2テンプレートから生成
5. テンプレートは`{{ VAR }}`プレースホルダを使用、`.env`とランタイム値（SWEEP_ID, RUN_NUMBER）で置換

### 設定

`.env`ファイルから以下のプレフィックスで設定を読み込む：

- `SLURM_SSH_*` - SSH接続設定（host, user, port, 認証方式）
- `SLURM_*` - Slurm設定（partition, gpus, time, remote_workdir）
- `WANDB_*` - W&B設定（api_key, entity, project）
- `LOCAL_*` - ローカル実行設定（ポーリング間隔）

### ジョブテンプレート

`examples/templates_remote/`と`examples/templates_local/`のテンプレートはJinja2を使用：

- `{{ SWEEP_ID }}`と`{{ RUN_NUMBER }}`は自動注入される
- すべての`.env`変数がテンプレート変数として利用可能
- 条件分岐: `{% if VAR %}...{% endif %}`
- デフォルト値: `{{ VAR | default('value') }}`

## コードスタイル

- Python 3.10+、型ヒント使用
- ruffでリント（line-length: 100）
- mypy strictモードで型チェック
- 日本語のコメントとdocstringを使用
