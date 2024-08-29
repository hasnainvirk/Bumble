from kb_key_controller import KeyboardKeyController as kb_key_controller
from udp_controller_client import UDPClient as udp_controller_client

kb = kb_key_controller()


def main():
    server_dns = "bumble.local"
    server_port = 5555
    client = udp_controller_client(server_dns, server_port)

    print("Press arrow keys to control the car. Press 'Esc' to exit.")

    try:
        while True:
            if kb.block_until_key_pressed():
                c = kb.get_command()
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
    except KeyboardInterrupt as e:
        print(e)
        kb.set_normal_term()


if __name__ == "__main__":
    main()
