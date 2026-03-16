"""
launcher.py — Desktop entry point for Site to DOCX.
Starts the Flask app in a background thread, then opens the browser.
"""

import sys
import os
import threading
import webbrowser
import time

# When bundled by PyInstaller, fix the working directory and path
if getattr(sys, "frozen", False):
    # Running as .exe — set base dir to the temp extraction folder
    BASE_DIR = sys._MEIPASS
    # Also add it to PATH so ChromeDriver can be found
    os.environ["PATH"] = BASE_DIR + os.pathsep + os.environ.get("PATH", "")
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

os.chdir(BASE_DIR)

# Must be set before importing app so Flask finds the templates folder
os.environ.setdefault("FLASK_ENV", "production")

def find_free_port():
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]

PORT = find_free_port()
URL = f"http://localhost:{PORT}"


def start_flask():
    from app import app
    app.run(host="127.0.0.1", port=PORT, debug=False, use_reloader=False)


def open_browser():
    # Give Flask a moment to start before opening the browser
    time.sleep(1.5)
    webbrowser.open(URL)


def show_stop_window():
    try:
        import tkinter as tk
        root = tk.Tk()
        root.title("Site to DOCX")
        root.resizable(False, False)
        root.geometry("300x120")

        # Keep window on top so it's easy to find
        root.attributes("-topmost", True)

        label = tk.Label(
            root,
            text=f"Site to DOCX is running.\n{URL}",
            pady=16,
            font=("Helvetica", 12),
        )
        label.pack()

        btn = tk.Button(
            root,
            text="Stop App",
            command=lambda: sys.exit(0),
            bg="#e53e3e",
            fg="white",
            font=("Helvetica", 12, "bold"),
            padx=20,
            pady=6,
            relief="flat",
            cursor="hand2",
        )
        btn.pack()

        root.protocol("WM_DELETE_WINDOW", lambda: sys.exit(0))
        root.mainloop()
    except Exception:
        # tkinter unavailable — fall back to blocking loop
        print(f"App is running at {URL}. Press Ctrl+C to stop.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            sys.exit(0)


if __name__ == "__main__":
    print(f"Starting Site to DOCX at {URL} ...")

    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()

    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()

    show_stop_window()
