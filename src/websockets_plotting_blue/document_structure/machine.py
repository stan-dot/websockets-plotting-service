import asyncio
from contextlib import contextmanager
from enum import Enum
from typing import Any, Dict, List

import psycopg2  # PostgreSQL driver
from pydantic import ValidationError


# Define the document types you expect
class DocumentType(str, Enum):
    RUN_START = "Run Start"
    EVENT = "Event"
    EVENT_DESCRIPTOR = "Event Descriptor"
    RUN_STOP = "Run Stop"


# Define the expected sequence of document types
class RunState(Enum):
    IDLE = 0
    RUNNING = 1
    STOPPED = 2


# Database connection context manager
@contextmanager
def get_db_connection():
    conn = psycopg2.connect(
        dbname="your_db",
        user="your_user",
        password="your_password",
        host="your_host",
        port="5432",
    )
    try:
        yield conn
    finally:
        conn.close()


class RunStateManager:
    def __init__(self):
        self.current_run_state = RunState.IDLE
        self.last_received_document: Union[None, DocumentType] = None
        self.cache: List[Dict[str, Any]] = []  # Cache to store messages during the run

    def validate_document_sequence(self, document_type: DocumentType):
        """
        Validates the sequence of received documents.
        Ensures that documents are processed in the correct order.
        """
        if document_type == DocumentType.RUN_START:
            if self.current_run_state != RunState.IDLE:
                raise ValueError(
                    "Cannot receive 'Run Start' after another run has started."
                )
            self.current_run_state = RunState.RUNNING

        elif document_type in [DocumentType.EVENT, DocumentType.EVENT_DESCRIPTOR]:
            if self.current_run_state != RunState.RUNNING:
                raise ValueError(
                    f"Cannot receive '{document_type}' unless a run is active."
                )

        elif document_type == DocumentType.RUN_STOP:
            if self.current_run_state != RunState.RUNNING:
                raise ValueError("Cannot receive 'Run Stop' unless a run is active.")
            self.current_run_state = RunState.STOPPED

        self.last_received_document = document_type

    def cache_message(self, message: Dict[str, Any]):
        """Cache the received message."""
        self.cache.append(message)

    def close_run(self):
        """Close the current run and write cached data to the database."""
        if self.current_run_state != RunState.STOPPED:
            raise ValueError("Cannot close a run unless it has been stopped.")

        # Write cached data to the PostgreSQL database
        self.write_to_db()

        # Reset the state for the next run
        self.reset()

    def write_to_db(self):
        """Write the cached data to the PostgreSQL database."""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            for message in self.cache:
                # Example SQL statement for inserting data (adjust for your schema)
                cursor.execute(
                    """
                    INSERT INTO experiment_data (run_uid, data, document_type, timestamp)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (
                        message.get("uid"),  # Assuming each message has a UID
                        str(
                            message.get("data")
                        ),  # Convert the data to a string (modify as needed)
                        message.get("type"),  # Document type
                        message.get("time"),  # Timestamp
                    ),
                )
            conn.commit()
            cursor.close()

    def reset(self):
        """Resets the state to IDLE and clears the cache."""
        self.current_run_state = RunState.IDLE
        self.last_received_document = None
        self.cache.clear()


# Initialize the state manager
run_state_manager = RunStateManager()


def on_message(message: str, context: MessageContext) -> None:
    """
    This function is called when a new message arrives from the broker.
    It parses the message and checks document sequence.
    """
    try:
        parsed_data = parse_message(message)
        document_type = identify_document_type(
            parsed_data
        )  # Function to identify document type

        # Validate that the document follows the correct sequence using the state manager
        run_state_manager.validate_document_sequence(document_type)

        # Cache the message
        run_state_manager.cache_message(parsed_data)

        # If it's a Run Stop document, close the run and write to the DB
        if document_type == DocumentType.RUN_STOP:
            run_state_manager.close_run()

        # Process the parsed data further
        asyncio.run(queue.put(parsed_data))  # Put the parsed data into the queue
    except ValueError as e:
        print(f"Sequence Error: {e}")
    except ValidationError as e:
        print(f"Parsing Error: {e}")


def identify_document_type(data: dict) -> DocumentType:
    """
    Identify the type of the document based on its content.
    For example, you can check for specific fields that distinguish Run Start, Event, etc.
    """
    if "run_start" in data:
        return DocumentType.RUN_START
    elif "run_stop" in data:
        return DocumentType.RUN_STOP
    elif "descriptor" in data:
        return DocumentType.EVENT_DESCRIPTOR
    else:
        return DocumentType.EVENT
