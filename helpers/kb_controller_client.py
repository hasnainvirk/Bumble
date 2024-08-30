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
                elif c == 5:  # a
                    client.send_command("ROTATE_CAMERA_LEFT")
                elif c == 6:  # d
                    client.send_command("ROTATE_CAMERA_RIGHT")
                elif c == 7:  # w
                    client.send_command("CAMERA_UP")
                elif c == 8:  # s
                    client.send_command("ROTATE_CAMERA_STRAIGHT")
                elif c == 9:  # x
                    client.send_command("CAMERA_DOWN")
                elif c == 10:  # q
                    client.send_command("ROTATE_CAMERA_LEFT_INCREMENTLY")
                elif c == 11:  # e
                    client.send_command("ROTATE_CAMERA_RIGHT_INCREMENTLY")
                elif c == 12:  # z
                    client.send_command("OPEN_CAMERA")
                elif c == 13:  # c
                    client.send_command("CLOSE_CAMERA")
    except KeyboardInterrupt as e:
        print(e)
        kb.set_normal_term()


if __name__ == "__main__":
    main()
