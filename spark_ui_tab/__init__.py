def _jupyter_server_extension_paths():
    """Used by "jupyter serverextension" command to install web server extension'"""
    return [{
        "module": "spark_ui_tab"
    }]








import json
from notebook.base.handlers import IPythonHandler
import requests
import tornado.web
from tornado import httpclient
import socket
import re
import os
import logging
from bs4 import BeautifulSoup

proxy_root = "/sparkuitab"

class SparkSummary(IPythonHandler):
    async def get(self):
        try:
            uri = self.request.uri[(self.request.uri.index(proxy_root) + len(proxy_root) + 3):].split(":")
            host=None
            port=None
            if len(uri)==1:
                host = uri[0]
            elif len(uri)==2:
                host, port = uri

            self.sparkExtention(host=host, port=port)
            logger.info("GET: SparkSummary PASS")
        except:
            logger.info("GET: SparkSummary FAILED")
            self.handle_bad_response()

        pass

    def handle_bad_response():
        self.write("No Active Spark Cluster Found (ports <4040:4049>)")

    def getInfo(self, url = "http://0.0.0.0:4040"):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s1=url.split(":")
        port = int(s1[-1])
        host = s1[1][2:]
        result = sock.connect_ex((host,port))
        if result==0:
    #         print("Port is open")
            info = []
            dic={}
            r = requests.get(url+"/environment")
            con = str(r.content)
            spark_app_name = re.findall(r"<td>spark.app.name</td><td>[a-zA-Z0-9 -.\[\]<>]*</td>", con)[0]
            spark_app_name = spark_app_name.split("<td>")[2][:-5]
            spark_appId = spark_appId = re.findall(r"<td>spark.app.id</td><td>[a-zA-Z0-9 -.\[\]<>]*</td>", con)[0]
            spark_appId = spark_appId.split("<td>")[2][:-5]
            spark_driver_host = re.findall(r"<td>spark.driver.host</td><td>[a-zA-Z0-9 -.\[\]<>]*</td>", con)[0]
            spark_driver_host = spark_driver_host.split("<td>")[2][:-5]
            spark_driver_port = re.findall(r"<td>spark.driver.port</td><td>[a-zA-Z0-9 -.\[\]<>]*</td>", con)[0]
            spark_driver_port = spark_driver_port.split("<td>")[2][:-5]
            spark_master = re.findall(r"<td>spark.master</td><td>[a-zA-Z0-9 -.\[\]<>]*</td>", con)[0]
            spark_master = spark_master.split("<td>")[2][:-5]
            dic["spark_app_name"] = spark_app_name
            dic["spark_appId"] = spark_appId   
            dic["spark_driver_host"] = spark_driver_host   
            dic["spark_driver_port"] = spark_driver_port   
            dic["spark_master"] = spark_master   
            return dic             
                                 
        else:
    #         print("Port is not open")
            return 0
        sock.close()
        
    def summary(self, host=None, port=None):
        url_pre = "http://"
        port_list = ["404"+str(i) for i in range(10)]
        if host == None:
            host = "0.0.0.0"
        if port != None:
            port_list = [port]
        url_list = [url_pre+host+":"+port for port in port_list]    
        # url_list => ['http://0.0.0.0:4040', 'http://0.0.0.0:4041', 'http://0.0.0.0:4042', 'http://0.0.0.0:4043', 'http://0.0.0.0:4044', 'http://0.0.0.0:4045', 'http://0.0.0.0:4046', 'http://0.0.0.0:4047', 'http://0.0.0.0:4048', 'http://0.0.0.0:4049']
    #     print(url_list)    
        spark_dict = {}
        ## pulling applications summary into dictionary
        for url in url_list:
            res = self.getInfo(url)
            if res!=0:
                spark_dict[url] = res
    #     print(spark_dict)
        return spark_dict
        
            
    def sparkExtention(self, host=None, port=None):
        result = "<html><body><pre>"
        spark_dict = self.summary(host=host, port=port)

        Clusters = {}
        for key, value in sorted(spark_dict.items()):
            Clusters.setdefault(value['spark_master'], []).append(key)
        # print(Clusters)

        Number_of_Clusters = len(Clusters)
    #     print('Number_of_Clusters: ', Number_of_Clusters)
    #     print()
        result +='Number of Clusters Found: '+str(Number_of_Clusters) + '\n'
        Cluster_cnt=1
        for mater_node, apps in Clusters.items():
    #         print("Cluster",Cluster_cnt,": ", mater_node)
            result += "Cluster"+str(Cluster_cnt)+": "+ str(mater_node) +'\n'
            Number_of_Apps = len(apps)
    #         print('Number_of_Apps:', Number_of_Apps)
            result += 'Number of Apps:' + str(Number_of_Apps) +'\n'
            app_cnt=1
            for app in apps:
                info = spark_dict[app]
    #             print("  Application",app_cnt,": ", info["spark_app_name"])
                result += "  Application"+ str(app_cnt) + ": " + str(info["spark_app_name"]) +'\n'
                for key, value in info.items():
    #                 print("      ",key," : ", value)
                    result += "      "+key+" : "+ value +'\n'

                app_cnt+=1
    #             print()
                result += '\n'
            Cluster_cnt+=1
        result += "</pre></body></html>"
        #     print('\n')
        self.write(result)
            



class SparkMonitorHandler(IPythonHandler):
    async def get(self):

        http = httpclient.AsyncHTTPClient()
        baseurl = os.environ.get("SPARKMONITOR_UI_HOST", "127.0.0.1")
        port = os.environ.get("SPARKMONITOR_UI_PORT", "4040")
        url = "http://" + baseurl + ":" + port
        
        request_uri = self.request.uri[(self.request.uri.index(proxy_root) + len(proxy_root) + 3):]

        self.replace_path = self.request.uri[:self.request.uri.index(proxy_root) + len(proxy_root)]
        
        url = "http://" + request_uri
        request_path = ""
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
            # with open(os.path.join(os.path.dirname(__file__), "spark_not_found.html"), 'r') as f:
            #     content = f.read()
            self.set_header("Content-Type", content_type)
            self.write("<html><body><center></BR><h3>SPARK UI NOT FOUND</h3></center></body></html>")
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

    print("SPARKEXTENTION_SERVER: Loading Server Extension")

    global logger
    logger = logging.getLogger("sparkmonitorserver")
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    fh = logging.FileHandler("sparkmonitor_serverextension.log", mode="w")
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(levelname)s:  %(asctime)s - %(name)s - %(process)d - %(processName)s - \
        %(thread)d - %(threadName)s\n %(message)s \n")
    fh.setFormatter(formatter)
    logger.addHandler(fh) 

    web_app = nb_server_app.web_app
    host_pattern = ".*$"
    route_pattern1 = url_path_join(
        web_app.settings["base_url"], proxy_root + "dns.*")
    route_pattern2 = url_path_join(
        web_app.settings["base_url"], proxy_root + "url.*")
    web_app.add_handlers(host_pattern, [(route_pattern1, SparkSummary),
        (route_pattern2 , SparkMonitorHandler)
        ])





def replace(content, root_url):
    try:
        import lxml
    except ImportError:
        BEAUTIFULSOUP_BUILDER = "html.parser"
    else:
        BEAUTIFULSOUP_BUILDER = "lxml"
    PROXY_PATH_RE = re.compile(r"\/proxy\/application_\d+_\d+\/(.*)")
    PROXY_ATTRIBUTES = (
        (("a", "link"), "href"),
        (("img", "script"), "src"),
    )
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
