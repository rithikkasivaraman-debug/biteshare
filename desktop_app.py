import os
import sys
import time
import subprocess
import threading
import urllib.request
import webbrowser

PORT = 8088

def start_server():
    import server
    server.run_server()

def get_edge_path():
    candidates = [
        os.path.expandvars(r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"),
        os.path.expandvars(r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"),
        os.path.expandvars(r"%LocalAppData%\Microsoft\Edge\Application\msedge.exe")
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return None

def main():
    # Start server in background thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    app_url = f"http://localhost:{PORT}"
    
    # Wait for server to respond
    for _ in range(30):
        try:
            with urllib.request.urlopen(f"{app_url}/api/state", timeout=1) as resp:
                if resp.status == 200:
                    break
        except Exception:
            time.sleep(0.2)

    edge = get_edge_path()
    if edge:
        # Launch Microsoft Edge in native standalone application mode
        cmd = [
            edge,
            f"--app={app_url}",
            "--window-size=1360,900",
            "--window-position=100,60"
        ]
        proc = subprocess.Popen(cmd)
        proc.wait()
    else:
        webbrowser.open(app_url)
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass

if __name__ == '__main__':
    main()
