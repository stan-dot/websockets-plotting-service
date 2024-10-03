import subprocess
import sys

from websockets_plotting_blue import __version__


def test_cli_version():
    cmd = [sys.executable, "-m", "websockets_plotting_blue", "--version"]
    assert subprocess.check_output(cmd).decode().strip() == __version__
