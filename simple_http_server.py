#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单HTTP文件服务器，用于临时提供docx文件访问
"""

import http.server
import socketserver
import os
import threading
import time

def start_server(directory, port=8000):
    """启动HTTP服务器"""
    os.chdir(directory)
    handler = http.server.SimpleHTTPRequestHandler
    
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"服务器启动在端口 {port}")
        print(f"访问地址: http://localhost:{port}/")
        httpd.serve_forever()

if __name__ == "__main__":
    # 在当前目录启动服务器
    start_server(".", 8000)
