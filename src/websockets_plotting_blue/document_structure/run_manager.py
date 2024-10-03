from typing import Any

from websockets_plotting_blue.document_structure.run_state_manager import (
    RunStateManager,
)


class RunManager:
    def __init__(self):
        self.active_runs: dict[str, RunStateManager] = {}

    async def start_run(self, run_start_doc: dict[str, Any]):
        run_uid = run_start_doc["uid"]
        if run_uid not in self.active_runs:
            manager = RunStateManager(run_uid, run_start_doc)
            self.active_runs[run_uid] = manager

    async def stop_run(self, run_stop_doc: dict[str, Any]):
        run_uid = run_stop_doc["run_uid"]
        if run_uid in self.active_runs:
            manager = self.active_runs.pop(run_uid)
            await manager.close()

    async def handle_event(self, event_doc: dict[str, Any]):
        run_uid = event_doc["descriptor"]
        if run_uid in self.active_runs:
            await self.active_runs[run_uid].handle_event(event_doc)
        else:
            # Optionally, log or raise an error about an unexpected event
            pass
