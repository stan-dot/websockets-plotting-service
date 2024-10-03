[![CI](https://github.com/stan-dot/websockets-plotting-blue/actions/workflows/ci.yml/badge.svg)](https://github.com/stan-dot/websockets-plotting-blue/actions/workflows/ci.yml)
[![Coverage](https://codecov.io/gh/stan-dot/websockets-plotting-blue/branch/main/graph/badge.svg)](https://codecov.io/gh/stan-dot/websockets-plotting-blue)
[![PyPI](https://img.shields.io/pypi/v/websockets-plotting-blue.svg)](https://pypi.org/project/websockets-plotting-blue)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

# websockets_plotting_blue

plotting bluesky scans with websockets for frontend consumption

This is where you should write a short paragraph that describes what your module does,
how it does it, and why people should use it.

|  Source  |     <https://github.com/stan-dot/websockets-plotting-blue>      |
| :------: | :-------------------------------------------------------------: |
|   PyPI   |             `pip install websockets-plotting-blue`              |
|  Docker  |  `docker run ghcr.io/stan-dot/websockets-plotting-blue:latest`  |
| Releases | <https://github.com/stan-dot/websockets-plotting-blue/releases> |

This is where you should put some images or code snippets that illustrate
some relevant examples. If it is a library then you might put some
introductory code here:

```python
from websockets_plotting_blue import __version__

print(f"Hello websockets_plotting_blue {__version__}")
```

Or if it is a commandline tool then you might put some example commands here:

```
python -m websockets_plotting_blue --version
```

# use

- [ ] the parsing should rely on processing based on the start-document ID, defined in the plan
- [ ] specific raster scan processing reconstruction logic gets StreamResource and a bunch of file system images
- [ ] from the images the data representation is constructed - ? what is the data format here?

need to go through the tutorials
need windowing to collect the data - a set of images
<https://docs.bytewax.io/stable/guide/getting-started/collecting-windowing-example.html>

```mermaid
flowchart TD
    A[Global Listener] -->|Receives Messages| B[Message Queue]
    B -->|Pulls Message| C[Process Message]

    C -->|Parse Message| D[Identify Document Type]
    D -->|Check Listeners| E{Is Start Document?}

    E -->|Yes| F[Start Run Processing]
    F -->|Track Message| G[Save to PostgreSQL]
    F -->|Maintain WebSocket State| H[WebSocket State Management]
    H -->|Stream Data| I[WebSocket Streamer]
    I -->|Send to Clients| J[WebSocket Clients]

    E -->|No| K[IO Manager]
    K -->|Read File| L[Return Result]
    L -->|Stream Data| M[WebSocket Streamer]
    M -->|Send to Clients| J

    style A fill:#f9f,stroke:#333,stroke-width:2px
    style B fill:#bbf,stroke:#333,stroke-width:2px
    style C fill:#ffb,stroke:#333,stroke-width:2px
    style D fill:#fff,stroke:#333,stroke-width:2px
    style E fill:#fbf,stroke:#333,stroke-width:2px
    style F fill:#bfb,stroke:#333,stroke-width:2px
    style G fill:#bfb,stroke:#333,stroke-width:2px
    style H fill:#ffb,stroke:#333,stroke-width:2px
    style I fill:#bfb,stroke:#333,stroke-width:2px
    style J fill:#ffb,stroke:#333,stroke-width:2px
    style K fill:#fbf,stroke:#333,stroke-width:2px
    style L fill:#fbf,stroke:#333,stroke-width:2px
    style M fill:#bfb,stroke:#333,stroke-width:2px

```
