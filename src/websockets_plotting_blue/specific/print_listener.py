from collections.abc import Callable
from typing import Any, TypeVar

from websockets_plotting_blue.document_structure.machine import RunStateManager

RunStateManagerType = TypeVar("RunStateManagerType", bound="RunStateManager")
ListenerType = Callable[[RunStateManagerType, dict[str, Any]], None]


# Define the print_listener function
def print_listener(run_manager: RunStateManager, document: dict[str, Any]) -> None:
    """
    Process a document, printing the Run Start and Run Stop documents.

    Args:
        run_manager (RunStateManager): The run state manager instance.
        document (dict[str, Any]): The document to process.
    """
    doc_type = document.get("type")
    if doc_type == "Run Start":
        print(
            f"Run Start Document: UID: {document.get('uid')}, Timestamp: {document.get('time')}"
        )
    elif doc_type == "Run Stop":
        print(
            f"Run Stop Document: UID: {document.get('uid')}, Timestamp: {document.get('time')}"
        )
