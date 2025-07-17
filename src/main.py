import smbus2
import time
import logging
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class XL9535:
    """
    A class to control the XL9535 I2C GPIO expander.
    """

    INPUT_PORT_0 = 0x00
    INPUT_PORT_1 = 0x01
    OUTPUT_PORT_0 = 0x02
    OUTPUT_PORT_1 = 0x03
    POLARITY_INVERSION_PORT_0 = 0x04
    POLARITY_INVERSION_PORT_1 = 0x05
    CONFIGURATION_PORT_0 = 0x06
    CONFIGURATION_PORT_1 = 0x07

    def __init__(self, bus_number: int = 1, address: int = 0x20):
        """
        Initialize the XL9535 device.
        :param bus_number: I2C bus number
        :param address: I2C address of the device
        """
        self.bus = smbus2.SMBus(bus_number)
        self.address = address

        # Configure all ports as output (0x00) initially
        self.bus.write_byte_data(self.address, self.CONFIGURATION_PORT_0, 0x00)
        self.bus.write_byte_data(self.address, self.CONFIGURATION_PORT_1, 0x00)

        # Initialize output ports to 0x00 (all off)
        self.bus.write_byte_data(self.address, self.OUTPUT_PORT_0, 0x00)
        self.bus.write_byte_data(self.address, self.OUTPUT_PORT_1, 0x00)

    def validate_port_and_relay_num(self, port: int, relay_num: int) -> None:
        """
        Validate port and relay number.
        :param port: Port number (0 or 1)
        :param relay_num: Relay number (0-7)
        :raises ValueError: If port or relay_num is out of range
        """
        if port not in [0, 1]:
            raise ValueError("Port must be 0 or 1")
        if relay_num < 0 or relay_num > 7:
            raise ValueError("Relay number must be between 0 and 7")

    def set_relay(self, port: int, relay_num: int, state: int) -> None:
        """
        Set the state of a relay.
        :param port: Port number (0 or 1)
        :param relay_num: Relay number (0-7)
        :param state: 0 (OFF) or 1 (ON)
        :raises ValueError: If arguments are invalid
        :raises IOError: If I2C communication fails
        """
        self.validate_port_and_relay_num(port, relay_num)
        if state not in [0, 1]:
            raise ValueError("State must be 0 (OFF) or 1 (ON)")
        logger.info(f"Set relay {relay_num} on port {port} to state {state}")

        output_port = self.OUTPUT_PORT_0 if port == 0 else self.OUTPUT_PORT_1
        try:
            current_state = self.bus.read_byte_data(self.address, output_port)
        except IOError as e:
            logger.error(f"Error reading from I2C: {e}")
            raise

        if state == 1:
            new_state = current_state | (1 << relay_num)
        else:
            new_state = current_state & ~(1 << relay_num)

        try:
            self.bus.write_byte_data(self.address, output_port, new_state)
        except IOError as e:
            logger.error(f"Error writing to I2C: {e}")
            raise

    def get_relay_state(self, port: int, relay_num: int) -> Optional[int]:
        """
        Get the state of a relay.
        :param port: Port number (0 or 1)
        :param relay_num: Relay number (0-7)
        :return: State (0 or 1) or None if error
        """
        self.validate_port_and_relay_num(port, relay_num)
        output_port = self.OUTPUT_PORT_0 if port == 0 else self.OUTPUT_PORT_1
        try:
            current_state = self.bus.read_byte_data(self.address, output_port)
        except IOError as e:
            logger.error(f"Error reading from I2C: {e}")
            return None
        relay_state = (current_state >> relay_num) & 1
        return relay_state


# Example usage (move to a separate script for real use)
"""
if __name__ == "__main__":
    xl9535 = XL9535()
    def set_relays(state, start, end, step):
        for relay_num in range(start, end, step):
            for port in [0, 1]:
                logger.info(f"Setup relay {relay_num} from port {port} to state {state}")
                xl9535.set_relay(port=port, relay_num=relay_num, state=state)
                time.sleep(0.1)
    for _ in range(10):
        set_relays(state=1, start=0, end=8, step=1)
        set_relays(state=0, start=7, end=-1, step=-1)
"""
