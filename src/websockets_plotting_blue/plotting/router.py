import io

import matplotlib.pyplot as plt
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.get("/plot/")
async def get_plot():
    # Generate a Matplotlib plot
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [1, 4, 9])
    ax.set_title("Sample Plot")

    # Save the plot to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")
