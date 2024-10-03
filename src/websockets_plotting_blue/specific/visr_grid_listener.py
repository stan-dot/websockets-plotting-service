# NOTE the plan in ViSR repo must be without arguments and running again and again
# and inside the metadata - for the start document, it will reference for this kind of processing

from event_model import StreamDatum, StreamResource
from event_model.documents import DocumentType

from websockets_plotting_blue.document_structure.machine import (
    DocumentType,
    RunStateManager,
)
from websockets_plotting_blue.fsio.reader import IOManager

# todo union DocumentType is read incorrectly as a variable atm
AnyEvent = StreamDatum | StreamResource


def grid_listener(
    run_manager: RunStateManager, document: dict[str, AnyEvent], io_manager: IOManager
) -> None:
    """
    Listener function that processes Event Descriptor documents.

    Args:
        run_manager (RunStateManager): The run state manager instance.
        document (dict[str, Any]): The document to process.
        io_manager (IOManager): The IO manager for reading files.
    """
    if document.get("type") == DocumentType.EVENT_DESCRIPTOR:
        path = document.get("path")  # Look for the 'path' field
        if path:
            image_data = io_manager.read_image(path)  # Read the image using IOManager
            if image_data is not None:
                # Cache the image data (you can extend this as needed)
                print(f"Cached image from {path} for Run UID: {run_manager.run_uid}")
