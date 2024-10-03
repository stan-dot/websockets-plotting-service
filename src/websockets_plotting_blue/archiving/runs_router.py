import asyncpg
import msgpack
import numpy as np
from fastapi import APIRouter, HTTPException

# Create a router instance for run-related endpoints
router = APIRouter()


async def get_db_connection():
    return await asyncpg.connect(dsn="postgres://user:password@localhost/dbname")


@router.get("/runs")
async def get_all_runs():
    conn = await get_db_connection()
    try:
        query = """
            SELECT run_uid, timestamp, start_document
            FROM run_metadata
        """
        runs = await conn.fetch(query)
        return [
            {
                "run_uid": run["run_uid"],
                "timestamp": run["timestamp"],
                "start_document": run["start_document"],
            }
            for run in runs
        ]
    finally:
        await conn.close()


@router.get("/runs/{run_uid}/data")
async def get_run_data(run_uid: str):
    conn = await get_db_connection()
    try:
        query = """
            SELECT event_data
            FROM event_data
            WHERE run_uid = $1
            ORDER BY timestamp ASC
        """
        events = await conn.fetch(query, run_uid)

        if not events:
            raise HTTPException(
                status_code=404, detail="Run not found or no data available."
            )

        # Convert the event data to a numpy array
        event_list = [event["event_data"]["data"] for event in events]
        event_array = np.array(event_list)

        # Serialize the numpy array using msgpack
        packed_data = msgpack.packb(event_array.tolist())

        return packed_data
    finally:
        await conn.close()
