# -*- coding: utf-8 -*-

from genericpath import getatime
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from os import path, walk
import json
import os
import cgi
import io
import math
from urllib.parse import unquote

from iconFinder import IconFinder

hostName = "0.0.0.0"
hostPort = 8000

class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        if (self.path == "/"):
            self.sendFile("/index.html")
        elif (self.path == "/sheet.css"):
            self.sendFile("/sheet.css", "text/css")
        elif (self.path.endswith("Icon.png")):
            self.sendIcon(self.path)

        elif (self.path == "/getFiles"):
            self.getFiles()
        
        elif (self.path.startswith("/delete")):
            self.getDelete(self.path) 

        else:
            self.sendFile(self.path)

    def do_POST(self):        
        r, info = self.deal_post_data()
        print(r, info, "by: ", self.client_address)
        f = io.BytesIO()
        if r:
            f.write(b"Success\n")
        else:
            f.write(b"Failed\n")
        length = f.tell()
        f.seek(0)
        self.sendFile("/reconnect.html")
        if f:
            f.close()      

    def deal_post_data(self):
        ctype, pdict = cgi.parse_header(self.headers['Content-Type'])
        pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
        pdict['CONTENT-LENGTH'] = int(self.headers['Content-Length'])
        if ctype == 'multipart/form-data':
            form = cgi.FieldStorage( fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD':'POST', 'CONTENT_TYPE':self.headers['Content-Type'], })
            print (type(form))
            try:
                if isinstance(form["file"], list):
                    for record in form["file"]:
                        open(f"{os.path.dirname(__file__)}/" + "web/files/%s"%record.filename, "wb").write(record.file.read())
                else:
                    open(f"{os.path.dirname(__file__)}/" + "web/files/%s"%form["file"].filename, "wb").write(form["file"].file.read())
            except IOError:
                    return (False, "Can't create file to write, do you have permission to write?")
        return (True, "Files uploaded")

    #return file
    def sendFile(self, file, header = "text/html"):
        file = unquote(file)
        
        if (not path.exists(f"{os.path.dirname(__file__)}/web{file}")):
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"Soubor nebyl nalezen :( " + bytes(file, "utf-8"))
            return

        self.send_response(200)
        self.send_header("Content-type", header)
        self.end_headers()

        with open(f"{os.path.dirname(__file__)}/web{file}", "rb") as f:
            self.wfile.write(f.read())

    def sendIcon(self, icon):
        icon = unquote(icon)

        if (not path.exists(f"{os.path.dirname(__file__)}/web{icon}")):
            self.sendFile("/images/unknownIcon.png")
        else:
            self.sendFile(icon)

    #return array of files on server
    def getFiles(self):
        data = []
        for (dirpath, dirnames, filenames) in walk(f"{os.path.dirname(__file__)}/web/files"):
            iconFinder = IconFinder()
            for f in filenames:
                data.append(
                    {
                        "filename": f,
                        "size": self.convertBytes(os.path.getsize(f"{os.path.dirname(__file__)}/web/files/{f}")),
                        "type": iconFinder.find(f),
                        "date": os.path.getatime(f"{os.path.dirname(__file__)}/web/files/{f}")
                    }
                )


        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(json.dumps(data), "utf-8"))
    
    #delete file
    def getDelete(self, file):
        file = unquote(file)
        file = file.replace("/delete", "")
        
        if (not path.exists(f"{os.path.dirname(__file__)}/web{file}")):
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            return

        os.remove(f"{os.path.dirname(__file__)}/web{file}")
        self.sendFile("/reconnect.html")

    def convertBytes(self, bytes):
        if bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(bytes, 1024)))
        p = math.pow(1024, i)
        s = round(bytes / p, 2)
        return "%s %s" % (s, size_name[i])


if __name__ == "__main__":
    if not os.path.exists(f"{os.path.dirname(__file__)}/web/files"):
        os.makedirs(f"{os.path.dirname(__file__)}/web/files")


    myServer = HTTPServer((hostName, hostPort), Server)
    print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

    try:
        myServer.serve_forever()
    except KeyboardInterrupt:
        pass

    myServer.server_close()
    print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))