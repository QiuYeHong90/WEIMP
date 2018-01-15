# coding=utf-8

import tornado.ioloop
import tornado.web
import shutil
import os
import hashlib
import time
import tornado.httpserver
import tornado.options


# 上传图片
class UploadFileHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('''
<html>
  <head><title>Upload File</title></head>
  <body>
    <form action='file' enctype="multipart/form-data" method='post'>
    <input type='file' name='file'/><br/>
    水电费了就撒旦法
    <input type='submit' value='submit'/>
    </form>
  </body>
</html>
''')

    def post(self):
        file_metas = self.request.files['file']  # 提取表单中‘name’为‘file’的文件元数据
        userID = self.get_body_argument('userID')
        for meta in file_metas:
            m5 = hashlib.md5()
            fileTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            print fileTime
            m5.update(userID + fileTime)
            filename = m5.hexdigest()
            filepath = '/file/' + filename + '.jpg'
            print filepath
            with open('./file/' + filename + '.jpg', 'wb') as up:  # 有些文件需要已二进制的形式存储，实际中可以更改
                up.write(meta['body'])
            self.finish('http://192.168.1.107:8000' + filepath)


class UploadBgImgHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('''
    <html>
      <head><title>Upload File</title></head>
      <body>
        <form action='file' enctype="multipart/form-data" method='post'>
        <input type='file' name='file'/><br/>
        水电费了就撒旦法
        <input type='submit' value='submit'/>
        </form>
      </body>
    </html>
    ''')

    def post(self):
        file_metas = self.request.files['file']  # 提取表单中‘name’为‘file’的文件元数据
        userID = self.get_body_argument('userID')
        for meta in file_metas:
            m5 = hashlib.md5()
            fileTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            print fileTime
            m5.update(userID + fileTime)
            filename = m5.hexdigest()
            filepath = '/system/' + filename + '.jpg'
            print filepath
            with open('./system/' + filename + '.jpg', 'wb') as up:  # 有些文件需要已二进制的形式存储，实际中可以更改
                up.write(meta['body'])
            self.finish('http://192.168.1.107:8000' + filepath)

            # 读取图片

# 读取上传的系统背景图
class SystemHandler(tornado.web.RequestHandler):
    def get(self, input):
        pic = open('./system/' + input[:], 'r')
        pics = pic.read()
        self.write(pics)


# 读取图片
class ReverseHandler(tornado.web.RequestHandler):
    def get(self, input):
        pic = open('./file/' + input[:], 'r')
        pics = pic.read()
        self.write(pics)


# 读取bg图片
class kpBgImgHandler(tornado.web.RequestHandler):
    def get(self, input):
        pic = open('./kpBgImg/' + input[:], 'r')
        pics = pic.read()
        self.write(pics)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r'/file', UploadFileHandler),
                    (r"/file/(\w+\.+\w+)", ReverseHandler),
                    (r"/kpBgImg/(\w+\.+\w+)", kpBgImgHandler),
                    (r"/upBgImg", UploadBgImgHandler),
                    (r"/system/(\w+\.+\w+)", SystemHandler),
                    ]
        tornado.web.Application.__init__(self, handlers, debug=True)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen('8000')
    tornado.ioloop.IOLoop.instance().start()
