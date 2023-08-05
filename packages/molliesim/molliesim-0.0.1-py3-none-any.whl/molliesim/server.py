import json

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer, _get_best_family

from molliesim.api import ParseException
from molliesim.router import Router


class MollieRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

    def _write_response(self, status, dict_data):
        self.send_response(status)
        self.send_header("content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(dict_data).encode("utf-8"))

    def _handle_request(self, method):
        content_len = int(self.headers.get("Content-Length") or "0")
        try:
            return Router.handle_route(
                method,
                self.path,
                self.headers,
                json.loads(self.rfile.read(content_len).decode("utf-8") or "{}"),
            )
        except ParseException as err:
            return err.error, err.error["status"]

    def do_GET(self):
        rv, status = self._handle_request("GET")
        self._write_response(status, rv)

    def do_POST(self):
        rv, status = self._handle_request("POST")
        self._write_response(status, rv)

    def do_DELETE(self):
        rv, status = self._handle_request("DELETE")
        self._write_response(status, rv)

    def do_PUT(self):
        rv, status = self._handle_request("PUT")
        self._write_response(status, rv)


def run_server(ServerClass, protocol="HTTP/1.0", port=8000, bind=None):
    ServerClass.address_family, addr = _get_best_family(bind, port)
    MollieRequestHandler.protocol_version = protocol
    with ServerClass(addr, MollieRequestHandler) as httpd:
        host, port = httpd.socket.getsockname()[:2]
        url_host = f"[{host}]" if ":" in host else host
        print(f"Serving HTTP on {host} port {port} " f"(http://{url_host}:{port}/) ...")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received, exiting.")
            sys.exit(0)


if __name__ == "__main__":
    import argparse
    import contextlib

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--bind",
        "-b",
        metavar="ADDRESS",
        help="specify alternate bind address " "(default: all interfaces)",
    )
    parser.add_argument(
        "port",
        action="store",
        default=8000,
        type=int,
        nargs="?",
        help="specify alternate port (default: 8000)",
    )
    args = parser.parse_args()

    # ensure dual-stack is not disabled; ref #38907
    class DualStackServer(ThreadingHTTPServer):
        def server_bind(self):
            # suppress exception when protocol is IPv4
            with contextlib.suppress(Exception):
                self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
            return super().server_bind()

        def finish_request(self, request, client_address):
            MollieRequestHandler(request, client_address, self)

    run_server(
        ServerClass=DualStackServer,
        port=args.port,
        bind=args.bind,
    )
