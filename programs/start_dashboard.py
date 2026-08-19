import http.server
import socketserver
import webbrowser
import threading
import time

PORT = 8000
URL = f"http://localhost:{PORT}/dashboard.html"

class MyHandler(http.server.SimpleHTTPRequestHandler):
    # Log requests quietly to avoid cluttering the terminal
    def log_message(self, format, *args):
        pass

def open_browser():
    # Wait a moment for the server to start up
    time.sleep(1.0)
    print(f"Opening browser to {URL}...")
    webbrowser.open(URL)

def run_server():
    handler = MyHandler
    # Allow socket reuse to avoid "address already in use" errors if restarted quickly
    socketserver.TCPServer.allow_reuse_address = True
    
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"Local dashboard server running at http://localhost:{PORT}/")
        print("Press Ctrl+C in this terminal to stop the server.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopping dashboard server. Goodbye!")

if __name__ == "__main__":
    import os
    # Change working directory to the parent/project root directory so we serve files from the root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))
    os.chdir(project_root)
    
    # Start the browser-opening thread
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Run server on the main thread
    run_server()
