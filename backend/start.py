import os
import subprocess
import sys

port = os.getenv("PORT", "10000")
subprocess.run([
    sys.executable,
    "-m",
    "gunicorn",
    "--bind",
    f"0.0.0.0:{port}",
    "--workers",
    "2",
    "backend.app:app",
], check=True)
