# SPDX-License-Identifier: MIT
# Copyright 2025 nop
"""Sweep実行エンジン.

W&B Sweepを作成し、Slurmジョブとして実行するエンジン。

新しいアーキテクチャでは、パラメータの取得とRunの作成は
Slurmジョブ内のwandb.agent()が行います。これにより、
RunがSweepに正しく関連付けられます。
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from lifter.clients import SlurmClient
from lifter.config import Settings
from lifter.sweep.base import BaseSweepEngine
from lifter.sweep.template import JobGenerator
from lifter.sweep.wandb_client import WandbSweepClient


class SweepEngine(BaseSweepEngine):
    """Slurm Sweep実行エンジン.

    新しいアーキテクチャでは、パラメータの取得とRunの作成は
    Slurmジョブ内のwandb.agent()が行います。
    エンジンはSweepの作成とジョブの投下・監視のみを担当します。
    """

    def __init__(
        self,
        slurm: SlurmClient,
        wandb: WandbSweepClient,
        settings: Settings,
        job_generator: JobGenerator | None = None,
    ):
        """エンジンを初期化.

        Args:
            slurm: Slurmクライアント
            wandb: W&B Sweepクライアント
            settings: 設定
            job_generator: ジョブスクリプト生成関数 (省略時はデフォルト生成)
        """
        super().__init__(wandb, job_generator)
        self.slurm = slurm
        self.settings = settings

    def _get_mode_name(self) -> str:
        """実行モード名を取得."""
        return "Slurm"

    def _default_job_generator(self, sweep_id: str, run_number: int) -> str:
        """デフォルトのジョブスクリプト生成.

        Note: 実際の使用ではテンプレートベースのジェネレータを使用することを推奨。

        Args:
            sweep_id: W&B Sweep ID
            run_number: このSweep内での実行番号

        Returns:
            ジョブスクリプトの内容

        Raises:
            NotImplementedError: テンプレートが指定されていない場合
        """
        raise NotImplementedError(
            "デフォルトのジョブ生成は実装されていません。"
            "テンプレートベースのジェネレータを使用してください。"
        )

    def _submit_job(self, script_content: str, script_name: str) -> str:
        """Slurmジョブを投下.

        Args:
            script_content: ジョブスクリプトの内容
            script_name: スクリプト名

        Returns:
            ジョブID

        Raises:
            SlurmError: ジョブ投下に失敗した場合
        """
        return self.slurm.submit_script_content(script_content, script_name)

    def _wait_for_job(
        self,
        job_id: str,
        poll_interval: int,
        log_poll_interval: int,
    ) -> str:
        """Slurmジョブ完了を待機.

        Args:
            job_id: 待機するジョブID
            poll_interval: 状態ポーリング間隔 (秒)
            log_poll_interval: ログポーリング間隔 (秒)

        Returns:
            最終状態 (COMPLETED, FAILED, etc.)
        """
        return self.slurm.wait_for_completion(
            job_id,
            poll_interval=poll_interval,
            log_poll_interval=log_poll_interval,
        )

    def _get_job_state(self, job_id: str) -> str | None:
        """Slurmジョブ状態を取得.

        Args:
            job_id: ジョブID

        Returns:
            ジョブの状態、見つからない場合はNone
        """
        return self.slurm.get_job_state(job_id)

    def _is_job_running(self, state: str | None) -> bool:
        """ジョブが実行中かどうかを判定.

        Args:
            state: ジョブの状態

        Returns:
            実行中の場合True
        """
        return state in ("RUNNING", "PENDING", "R", "PD")


# 後方互換性のためのエイリアス
from lifter.sweep.template import create_custom_job_generator  # noqa: E402, F401

if TYPE_CHECKING:
    from lifter.config import LocalSettings
    from lifter.sweep.backends.local import LocalExecutionBackend


class LocalSweepEngine(BaseSweepEngine):
    """ローカルSweep実行エンジン.

    SSH/Slurmを使わずにローカルでSweepを実行する。
    並列実行（max_concurrent_jobs > 1）もサポート。

    Note: この実装は後方互換性のため engine.py に残しています。
    実際のLocalExecutionBackendは sweep/backends/local.py にあります。
    """

    def __init__(
        self,
        backend: LocalExecutionBackend,
        wandb: WandbSweepClient,
        settings: LocalSettings,
        job_generator: JobGenerator | None = None,
    ):
        """エンジンを初期化.

        Args:
            backend: ローカル実行バックエンド
            wandb: W&B Sweepクライアント
            settings: ローカル設定
            job_generator: ジョブスクリプト生成関数 (必須)
        """
        super().__init__(wandb, job_generator)
        self.backend = backend
        self.settings = settings

    def _get_mode_name(self) -> str:
        """実行モード名を取得."""
        return "ローカル"

    def _default_job_generator(self, sweep_id: str, run_number: int) -> str:
        """デフォルトのジョブスクリプト生成.

        Note: ローカル実行ではテンプレートベースのジェネレータを使用することを推奨。

        Args:
            sweep_id: W&B Sweep ID
            run_number: このSweep内での実行番号

        Returns:
            ジョブスクリプトの内容

        Raises:
            NotImplementedError: テンプレートが指定されていない場合
        """
        raise NotImplementedError(
            "デフォルトのジョブ生成は実装されていません。"
            "テンプレートベースのジェネレータを使用してください。"
        )

    def _submit_job(self, script_content: str, script_name: str) -> str:
        """ローカルジョブを投下.

        Args:
            script_content: ジョブスクリプトの内容
            script_name: スクリプト名

        Returns:
            ジョブID
        """
        return self.backend.submit_job(script_content, script_name)

    def _wait_for_job(
        self,
        job_id: str,
        poll_interval: int,
        log_poll_interval: int,
    ) -> str:
        """ローカルジョブ完了を待機.

        Args:
            job_id: 待機するジョブID
            poll_interval: 状態ポーリング間隔 (秒)
            log_poll_interval: ログポーリング間隔 (秒)

        Returns:
            最終状態 (COMPLETED, FAILED, etc.)
        """
        return self.backend.wait_for_completion(
            job_id,
            poll_interval=poll_interval,
            log_poll_interval=log_poll_interval,
        )

    def _get_job_state(self, job_id: str) -> str | None:
        """ローカルジョブ状態を取得.

        Args:
            job_id: ジョブID

        Returns:
            ジョブの状態、見つからない場合はNone
        """
        return self.backend.get_job_state(job_id)

    def _is_job_running(self, state: str | None) -> bool:
        """ジョブが実行中かどうかを判定.

        Args:
            state: ジョブの状態

        Returns:
            実行中の場合True
        """
        return state in ("RUNNING", None)
