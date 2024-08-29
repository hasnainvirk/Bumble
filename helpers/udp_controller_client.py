import socket


class UDPClient:
    def __init__(self, server_dns, server_port):
        self.server_ip = socket.gethostbyname(server_dns)
        self.server_port = server_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_command(self, command):
        try:
            self.sock.sendto(
                command.encode("utf-8"), (self.server_ip, self.server_port)
            )
            print(f"Sent command: {command}")
        except Exception as e:
            print(f"Error: {e}")

    def close(self):
        self.sock.close()
        print("Socket closed")
