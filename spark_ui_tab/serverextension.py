

from notebook.base.handlers import IPythonHandler
import tornado.web
from tornado import httpclient
import re
import os
import logging
from bs4 import BeautifulSoup

proxy_root = "/sparkuitab"


class SparkMonitorHandler(IPythonHandler):

    async def get(self):
       

        http = httpclient.AsyncHTTPClient()
        baseurl = os.environ.get("SPARKMONITOR_UI_HOST", "127.0.0.1")
        port = os.environ.get("SPARKMONITOR_UI_PORT", "4040")
        url = "http://" + baseurl + ":" + port
        request_path = self.request.uri[(
                                                self.request.uri.index(proxy_root) + len(proxy_root) + 1):]
        self.replace_path = self.request.uri[:self.request.uri.index(
            proxy_root) + len(proxy_root)]
        # print("SPARKMONITOR_SERVER: Request_path " + request_path + " \n Replace_path:" + self.replace_path)
        backendurl = url_path_join(url, request_path)
        self.debug_url = url
        self.backendurl = backendurl
        logger.info("GET: \n Request uri:%s \n Port: %s \n Host: %s \n request_path: %s ", self.request.uri,
                    os.environ.get(
                        "SPARKMONITOR_UI_PORT", "4040"), os.environ.get("SPARKMONITOR_UI_HOST", "127.0.0.1"),
                    request_path)
        try:
            x = await http.fetch(backendurl)
            self.handle_response(x)
        except:
            self.handle_bad_response()

    def handle_bad_response(self):
        content_type = "text/html"

        try:
            with open(os.path.join(os.path.dirname(__file__), "spark_not_found.html"), 'r') as f:
                content = f.read()
                self.set_header("Content-Type", content_type)
                self.write(content)
                self.finish()
            print("SPARKMONITOR_SERVER: Spark UI not running")
        except FileNotFoundError:
            logger.info("default html file was not found")

    def handle_response(self, response):
        try:
            content_type = response.headers["Content-Type"]
            if "text/html" in content_type:
                content = replace(response.body, self.replace_path)
            elif "javascript" in content_type:
                body = "location.origin +'" + self.replace_path + "' "
                content = response.body.replace(b"location.origin", body.encode())
            else:
                # Probably binary response, send it directly.
                content = response.body
            self.set_header("Content-Type", content_type)
            self.write(content)
            self.finish()
        except Exception as e:
            logger.error(str(e))
            raise e


def load_jupyter_server_extension(nb_server_app):
    
    print("SPARKMONITOR_SERVER: Loading Server Extension")
    # Configuring logging for the extension
    # This is necessary because in some versions of jupyter, print statements are not output to console.

    global logger
    logger = logging.getLogger("sparkmonitorserver")
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    # For debugging this module - Writes logs to a file
    #TODO: find a more k8s way to do so
    fh = logging.FileHandler("sparkmonitor_serverextension.log", mode="w")
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(levelname)s:  %(asctime)s - %(name)s - %(process)d - %(processName)s - \
        %(thread)d - %(threadName)s\n %(message)s \n")
    fh.setFormatter(formatter)
    logger.addHandler(fh)  ## Comment this line to disable logging to a file.

    web_app = nb_server_app.web_app
    host_pattern = ".*$"
    route_pattern = url_path_join(
        web_app.settings["base_url"], proxy_root + ".*")
    web_app.add_handlers(host_pattern, [(route_pattern, SparkMonitorHandler)])


try:
    import lxml
except ImportError:
    BEAUTIFULSOUP_BUILDER = "html.parser"
else:
    BEAUTIFULSOUP_BUILDER = "lxml"
# a regular expression to match paths against the Spark on EMR proxy paths
PROXY_PATH_RE = re.compile(r"\/proxy\/application_\d+_\d+\/(.*)")
# a tuple of tuples with tag names and their attribute to automatically fix
PROXY_ATTRIBUTES = (
    (("a", "link"), "href"),
    (("img", "script"), "src"),
)


def replace(content, root_url):

    soup = BeautifulSoup(content, BEAUTIFULSOUP_BUILDER)
    for tags, attribute in PROXY_ATTRIBUTES:
        for tag in soup.find_all(tags, **{attribute: True}):
            value = tag[attribute]
            match = PROXY_PATH_RE.match(value)
            if match is not None:
                value = match.groups()[0]
            tag[attribute] = url_path_join(root_url, value)
    return str(soup)


def url_path_join(*pieces):
    initial = pieces[0].startswith("/")
    final = pieces[-1].endswith("/")
    stripped = [s.strip("/") for s in pieces]
    result = "/".join(s for s in stripped if s)
    if initial:
        result = "/" + result
    if final:
        result = result + "/"
    if result == "//":
        result = "/"
    return result
