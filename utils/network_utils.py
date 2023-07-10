import socket

class NetworkUtils:
    @staticmethod
    def is_port_in_use(port: int, ip: str = '127.0.0.1'):
        try:
            # Tạo một socket và kết nối đến cổng được chỉ định
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((ip, port))
            sock.close()

            if result == 0:
                # Cổng đã được sử dụng
                return True
            else:
                # Cổng không được sử dụng
                return False
        except socket.error as e:
            return False

