from components.remote_control.modules.infrared_recvr import (
    InfraRedRecvr as infra_red_recvr,
)
from components.remote_control.modules.buttons import (
    ButtonControls as button_controls,
    button_key_codes,
)
from components.remote_control.modules.buttons import (
    ButtonActionConfig as button_action_config,
)

import logging


class RemoteControlTest:
    def __init__(self):
        self.ir = infra_red_recvr()
        self.button_controls = button_controls()
        self.action_config = button_action_config()
        self.log = logging.getLogger("bumble")

    def execute_command(self):
        output = lambda msg: self.log.info(msg)
        for key in button_key_codes:
            self.action_config[key] = {
                "key": button_key_codes[key],
                "action": output(f"Button {key} pressed"),
            }
            self.button_controls[key] = self.action_config[key]

        self.ir.listen_and_process(self.button_controls)
