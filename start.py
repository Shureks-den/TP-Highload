from server import HTTPWebServer

HOST = '0.0.0.0'
PORT = 80
DEFAULT_THREADS = 256
DEFAULT_ROOT_DIR = '/var/www/html'

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