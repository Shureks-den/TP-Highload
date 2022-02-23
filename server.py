from datetime import datetime
import mimetypes
import threading
import os
import queue
import socket
import signal
from httpHelper import HTTPRequest, HTTPResponse


DEFAULT_THREADS = 256
DEFAULT_ROOT_DIR = '/var/www/html'
HOST = '0.0.0.0'
PORT = 80

class HTTPWebServer():
        def __init__(self, host, port, threads, dir):
            print('start')
            self._cpuNum = os.cpu_count()
            self._host = host
            self._port = port
            self._threads = threads
            self._dir = dir
            self._cpuPool = []
            self._requestQueue = queue.SimpleQueue()
            print('done')

        def listenAndServe(self):
            sock = socket.socket()
            try:
                sock.bind((self._host, self._port))
                sock.listen()
                pid = 0
                for _ in range(self._cpuNum):
                    pid = os.fork()
                    if pid == 0:
                        return
                    for _ in range(self._threads):
                        t = threading.Thread(target = self.threadWork, daemon=True)
                        t.start()
                    self._cpuPool.append(pid)
                    print(pid)
                print('ready to serve')
                while True:
                    conn, _ = sock.accept()
                    self._requestQueue.put(conn)
            except KeyboardInterrupt:
                sock.close()
                for pid in self._cpuPool:
                    os.kill(pid, signal.SIGTERM)


        def threadWork(self):
            while True:
                conn = self._requestQueue.get()
                if conn:
                    self.handle(conn)
                    conn.close()


        def fileLookUp(self, conn, filePath):
            type, _ = mimetypes.guess_type(filePath, strict=True)
            headers = [('Content-Type', type), ('Content-Length', os.path.getsize(filePath)),
                ('Server', 'Highload-python'), ('Date', datetime.now()), ('Connection', 'keep-alive')]
            res = HTTPResponse(200, 'OK', headers)
            self.response(conn, res)

        def handle(self, conn):
            request = self.parseRequest(conn)
            if (type(request) != HTTPRequest):
                self.response(conn, request) # отправляем ошибкой, если произошла ошибка парсинга
                return
            if request._path.find('/../') != -1:
                self.response(HTTPResponse(
                    405, 'Method Not Allowed'), [('Content-length', 0)])
                return
    
            indexFile = False
            if request._path[-1] == '/':
                filePath = self._dir + request._path + 'index.html'
                indexFile = True
            try:
                file = open(filePath, 'r')
            except:
                headers = [('Content-Length', 0), ('Server', 'Highload-python'),
                    ('Date', datetime.now()), ('Connection', 'close')]
                if indexFile:
                    resp = HTTPResponse(403, 'Forbidden', headers=headers)
                else:
                    resp = HTTPResponse(404, 'Not Found', headers=headers)
                self.response(conn, resp)
                return

            self.fileLookUp(conn, filePath)
            if request._method == 'GET':
                conn.sendfile(file)
            file.close()     


        def response(self, conn, res):
            answer = conn.makefile('w')
            answer.write(f'HTTP/1.1 {res._code} {res._status}\r\n')

            if res._headers:
                for (key, value) in res._headers:
                    answer.write(f'{key}: {value}\r\n')
            answer.write('\r\n')

            if res._body:
                answer.write(res.body)
            answer.close()


        def parseRequest(self, conn):
            rawFile = conn.makefile('r')
            method, path, ver = rawFile.readline().split()
            if method != 'GET' and method != 'HEAD':
                return HTTPResponse(405, 'Method Not Allowed', [('Content-length', 0)])
            if ver != 'HTTP/1.1' and ver != 'HTTP/1.0':
                return HTTPResponse(505, 'HTTP Version Not Supported', [('Content-length', 0)])
            headers = {}
            while True:
                line = rawFile.readline()
                if line in ('\r\n', '\n', ''):
                    break
                headerName, headerValue = line.split(':')
                headers[headerName] = headerValue
            if 'Content-length' in headers:
                req = HTTPRequest(method, path, ver, headers, rawFile.read(int(headers['Content-length'])))
                rawFile.close()
                return req
            else:
                rawFile.close()
                return HTTPRequest(method, path, ver, headers, None)
        


def parseConf():
    threads = DEFAULT_THREADS
    root = DEFAULT_ROOT_DIR
    try:
        f = open('./httpd.conf', 'r')
        # f = open('/etc/httpd.conf', 'r')
        parsedFile = f.read().split('\n')
        for text in parsedFile:
            if text.find('thread_limit') > -1:
                threads = int(text.split(' ')[1])
            if text.find('document_root') > -1:
                root = text.split(' ')[1]
    finally:
        f.close()
        return threads, root

if __name__ == '__main__':
    numThreads, rootFolder = parseConf()
    server = HTTPWebServer(HOST, PORT, numThreads, rootFolder)
    server.listenAndServe()
