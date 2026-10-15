"""Expose only the host model relay to an otherwise offline network namespace."""
import http.client
import http.server
import socket
import sys
import threading


class UnixConnection(http.client.HTTPConnection):
    def connect(self):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.settimeout(240)
        self.sock.connect("/run/model.sock")


class Bridge(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *_):
        pass

    def do_POST(self):
        if self.path != "/v1/chat/completions":
            self.send_error(404)
            return
        body = self.rfile.read(int(self.headers["Content-Length"]))
        conn = UnixConnection("relay", timeout=240)
        try:
            conn.request("POST", "/" + sys.argv[1] + self.path, body, {"Content-Type": "application/json"})
            response = conn.getresponse()
            self.send_response(response.status)
            self.send_header("Content-Type", response.getheader("Content-Type", "application/json"))
            self.send_header("Connection", "close")
            self.end_headers()
            while data := response.read1(65536):
                self.wfile.write(data)
                self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError):
            pass
        finally:
            conn.close()
            self.close_connection = True


if __name__ == "__main__":
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 18761), Bridge)
    server.serve_forever()
