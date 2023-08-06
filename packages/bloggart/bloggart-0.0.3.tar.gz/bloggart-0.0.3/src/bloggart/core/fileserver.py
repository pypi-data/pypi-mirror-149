import tornado.web
import os

FILESERVER_BASEURI = 'html'

# class MainHandler(tornado.web.RequestHandler):
#     def get(self):
#         self.write("Hello, world")

def Handle(config):
    if not os.path.isdir(config['static']):
        raise Exception('static is not directory: {}'.format(config['static']))
    # utils.simplifyPath(config['static'])
    uri = os.path.join(r"/", config['base_uri'], FILESERVER_BASEURI, r'(.*)$')
    print(config, uri)
    # return [(r'/(.*)$', tornado.web.StaticFileHandler, {'path': 'html/', 'default_filename': 'index.html'})]
    return [(uri, tornado.web.StaticFileHandler, {'path': config['static'], 'default_filename': 'index.html'})]