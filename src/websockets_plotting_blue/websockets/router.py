import asyncio
import random
import time

import numpy as np
from fastapi import APIRouter, WebSocket

from websockets_plotting_blue.shared.queue import main_queue

# Create a new router
router = APIRouter()


async def _send_message_at_hertz(socket: WebSocket, message: dict, hertz: float):
    interval = 1 / hertz
    while True:
        await socket.send_json(message)
        await asyncio.sleep(interval)


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Simulating data generation
            now = time.time()
            data = {"time": now, "value": random.random()}
            await websocket.send_json(data)
            await asyncio.sleep(0.01)  # 100 Hz rate
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await websocket.close()


# Generate 10,000 random integers between 0 and 255
def generate_rgb_array(size=10000):
    return np.random.randint(0, 256, size=size, dtype=np.uint8)


# Initialize RGB arrays
r_array = generate_rgb_array()
g_array = generate_rgb_array()
b_array = generate_rgb_array()


interval = 0.6
# 0.1 to Emit every 100 ms (10 Hz)


@router.websocket("/ws/colors")
async def colors_websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    zipped_arrays = zip(r_array, g_array, b_array, strict=False)
    try:
        while True:
            for r, g, b in zipped_arrays:
                total = r + g + b
                # Convert NumPy integers to standard Python integers
                r = int(r)
                g = int(g)
                b = int(b)
                total = int(total)
                # todo total will be histagrammed
                # print(r,g,b)

                # Create JSON data format
                red_data = {"c": "r", "i": r}
                green_data = {"c": "g", "i": g}
                blue_data = {"c": "b", "i": b}
                total_data = {"c": "t", "i": total}

                for data in [red_data, green_data, blue_data, total_data]:
                    # Send JSON data
                    await websocket.send_json(data)
                await asyncio.sleep(interval)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await websocket.close()


@router.websocket("/ws/experiment")
async def experiment_websocket_endpoint(websocket: WebSocket):
    """
    This websocket endpoint brings a stream of data from RMQ
    that could be generated by a scientific experiment.
    sends numpy arrays in order to be unpacked with ndarray npm package
    """
    await websocket.accept()
    try:
        while True:
            # Simulating data generation
            # Wait for a message to be available in the queue (from the broker)
            message = await main_queue.get()

            now = time.time()
            data = {"time": now, "value": np.random.rand(10, 3), "message": message}
            await websocket.send_json(data)
            await asyncio.sleep(0.01)  # 100 Hz rate
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await websocket.close()
