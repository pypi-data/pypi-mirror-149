import tornado.ioloop
import tornado.web
from bloggart.core import config
from bloggart.core import database
from bloggart.core import fileserver
from bloggart.core import service
# import socket
# g_server_ip = socket.gethostbyname(socket.gethostname())
import argparse

def get_args_parser():
    parser = argparse.ArgumentParser(description="bloggart command line interface.")
    parser.add_argument("-c", "--config", default='config.ini', help="配置文件路径")
    parser.add_argument("-p", "--port", default='config.ini', help="配置文件路径")
    return parser.parse_args()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

def Run():
    args = get_args_parser()
    config.Parse(args.config)

    handler = []
    handler.extend(database.Handle(config.Get_database()))
    handler.extend(fileserver.Handle(config.Get_fileserver()))
    service.Serving(args.port, handler)
    
    print(config.CONFIG)
    exit()
    
if __name__ == "__main__":
    Run()
