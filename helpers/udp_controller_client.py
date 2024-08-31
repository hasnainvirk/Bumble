"""
This module is responsible for sending commands to the UDP controller server.
"""

import socket


class UDPClient:
    """
    Class to send commands to the UDP controller server
    """

    def __init__(self, server_dns, server_port):
        self.server_ip = socket.gethostbyname(server_dns)
        self.server_port = server_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_command(self, command):
        """
        Send command to the UDP controller server
        """

        try:
            self.sock.sendto(
                command.encode("utf-8"), (self.server_ip, self.server_port)
            )
            print(f"Sent command: {command}")
        except Exception as e:
            print(f"Error: {e}")

    def close(self):
        """
        Close the socket
        """

        self.sock.close()
        print("Socket closed")
