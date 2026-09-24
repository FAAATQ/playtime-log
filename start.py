# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

"""Start the Week 4 genre interaction locally.

    uv run start.py

Open http://127.0.0.1:8000/site/ in a browser, then choose a genre.
Press Ctrl+C here when you are finished.
"""

from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import os
import webbrowser

HERE = Path(__file__).parent
URL = "http://127.0.0.1:8000/site/"


def main():
    os.chdir(HERE)
    server = ThreadingHTTPServer(("127.0.0.1", 8000), SimpleHTTPRequestHandler)
    print(f"Serving {HERE}")
    print(f"Open {URL}")
    webbrowser.open(URL)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
