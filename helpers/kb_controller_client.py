import socket

# import keyboard
import kb_key_hit


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


kb = kb_key_hit.KBHit()


def main():
    server_dns = "bumble.local"  # Replace with your Raspberry Pi's DNS address
    server_port = 5555
    client = UDPClient(server_dns, server_port)

    print("Press arrow keys to control the car. Press 'Esc' to exit.")

    try:
        while True:
            if kb.kbhit():
                c = kb.getarrow()
                print(c)
                if c == 0:  # up
                    client.send_command("UP")
                elif c == 1:  # right
                    client.send_command("RIGHT")
                elif c == 2:  # down
                    client.send_command("DOWN")
                elif c == 3:  # left
                    client.send_command("LEFT")
                elif c == 4:  # space bar
                    client.send_command("STOP")
                print(c)
    except KeyboardInterrupt as e:
        print(e)
        kb.set_normal_term()


if __name__ == "__main__":
    main()
