import unittest
from unittest.mock import patch
from src.main import XL9535

class TestXL9535(unittest.TestCase):
    def setUp(self):
        patcher = patch('smbus2.SMBus')
        self.addCleanup(patcher.stop)
        self.MockSMBus = patcher.start()
        self.mock_bus = self.MockSMBus.return_value
        self.xl9535 = XL9535()

    def test_initialization(self):
        """Test that initialization writes correct values to the device."""
        self.mock_bus.write_byte_data.assert_any_call(0x20, 0x06, 0x00)
        self.mock_bus.write_byte_data.assert_any_call(0x20, 0x07, 0x00)
        self.mock_bus.write_byte_data.assert_any_call(0x20, 0x02, 0x00)
        self.mock_bus.write_byte_data.assert_any_call(0x20, 0x03, 0x00)

    def test_validate_port_and_relay_num(self):
        """Test validation of port and relay number raises ValueError on invalid input."""
        with self.assertRaises(ValueError):
            self.xl9535.validate_port_and_relay_num(2, 0)
        with self.assertRaises(ValueError):
            self.xl9535.validate_port_and_relay_num(0, 8)
        with self.assertRaises(ValueError):
            self.xl9535.validate_port_and_relay_num(0, -1)

    def test_set_relay(self):
        """Test setting relay ON and OFF writes correct values."""
        self.mock_bus.read_byte_data.return_value = 0x00
        self.xl9535.set_relay(0, 0, 1)
        self.mock_bus.write_byte_data.assert_called_with(0x20, 0x02, 0x01)

        self.mock_bus.read_byte_data.return_value = 0x01
        self.xl9535.set_relay(0, 0, 0)
        self.mock_bus.write_byte_data.assert_called_with(0x20, 0x02, 0x00)

    def test_get_relay_state(self):
        """Test getting relay state returns correct value."""
        self.mock_bus.read_byte_data.return_value = 0x01
        state = self.xl9535.get_relay_state(0, 0)
        self.assertEqual(state, 1)

        self.mock_bus.read_byte_data.return_value = 0x00
        state = self.xl9535.get_relay_state(0, 0)
        self.assertEqual(state, 0)

    def test_set_relay_ioerror(self):
        """Test set_relay raises IOError on I2C error."""
        self.mock_bus.read_byte_data.side_effect = IOError("I2C read error")
        with self.assertRaises(IOError):
            self.xl9535.set_relay(0, 0, 1)

    def test_get_relay_state_ioerror(self):
        """Test get_relay_state returns None on I2C error."""
        self.mock_bus.read_byte_data.side_effect = IOError("I2C read error")
        state = self.xl9535.get_relay_state(0, 0)
        self.assertIsNone(state)

if __name__ == '__main__':
    unittest.main()
