import mimetypes
import pathlib
from http.server import BaseHTTPRequestHandler
import urllib.parse
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from app.storage import DataStorage
from app.utils.format_timestamp import format_timestamp


class HttpHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.data_storage = DataStorage()
        self.env = Environment(loader=FileSystemLoader("."))
        self.env.filters["format_timestamp"] = format_timestamp
        super().__init__(*args, **kwargs)

    def do_POST(self):
        # timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        timestamp = f"{datetime.now()}"  #
        data = self.rfile.read(int(self.headers["Content-Length"]))
        data_parse = urllib.parse.unquote_plus(data.decode())
        data_dict = {
            key: value for key, value in [el.split("=") for el in data_parse.split("&")]
        }

        new_msg = {
            timestamp: {
                "username": data_dict.get("username", "anonymous"),
                "message": data_dict.get("message", ""),
            }
        }

        self.data_storage.write_data(new_msg)

        self.send_response(302)
        self.send_header("Location", "/")
        self.end_headers()

    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == "/":
            self.render_template("templates/index.html")
        elif pr_url.path == "/message":
            self.render_template("templates/message.html")
        elif pr_url.path == "/read":
            messages = self.data_storage.read_data()
            self.render_template(
                "templates/messages.html", context={"messages": messages}
            )

        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.render_template("templates/error.html", None, 404)

    def render_template(self, template_name, context=None, status=200):
        if context is None:
            context = {}

        template = self.env.get_template(template_name)
        html_content = template.render(**context)
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html_content.encode("utf-8"))

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        with open(filename, "rb") as fd:
            self.wfile.write(fd.read())

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", "text/plain")
        self.end_headers()
        with open(f".{self.path}", "rb") as file:
            self.wfile.write(file.read())
