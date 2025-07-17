# XL9535

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE.md)
[![Build Status](https://github.com/Aina261/XL9535/actions/workflows/ci.yml/badge.svg)](https://github.com/Aina261/XL9535/actions)

A Python library for controlling the XL9535 I2C GPIO expander. This library provides an easy-to-use interface for managing relays or GPIOs via the XL9535 chip over I2C, suitable for Raspberry Pi and other Linux-based systems.

## Features
- Simple API to control relays or GPIOs via XL9535
- Set and get relay states
- Input validation and error handling
- Designed for extensibility and integration
- Includes unit tests with mocking for I2C

## Requirements
- Python 3.7+
- [smbus2](https://pypi.org/project/smbus2/)
- Linux-based system with I2C support (e.g., Raspberry Pi)

## Installation

Install the library and its dependencies:

```bash
pip install smbus2
# If using as a package:
pip install .
```

## Usage

### Basic Example

```python
from src.main import XL9535
import time

# Initialize the XL9535 (default I2C bus 1, address 0x20)
xl9535 = XL9535()

# Turn ON relay 0 on port 0
xl9535.set_relay(port=0, relay_num=0, state=1)

# Check relay state
state = xl9535.get_relay_state(port=0, relay_num=0)
print(f"Relay 0 state: {state}")

# Turn OFF relay 0 on port 0
xl9535.set_relay(port=0, relay_num=0, state=0)
```

### Error Handling

The library raises `ValueError` for invalid arguments and propagates `IOError` for I2C communication errors. Use try/except blocks as needed:

```python
try:
    xl9535.set_relay(port=2, relay_num=0, state=1)  # Invalid port
except ValueError as e:
    print(f"Argument error: {e}")
```

## API Reference

### `XL9535(bus_number: int = 1, address: int = 0x20)`
- Initialize the XL9535 device.
- `bus_number`: I2C bus number (default: 1)
- `address`: I2C address (default: 0x20)

### `set_relay(port: int, relay_num: int, state: int) -> None`
- Set the state of a relay (0 = OFF, 1 = ON).
- Raises `ValueError` for invalid arguments, `IOError` for I2C errors.

### `get_relay_state(port: int, relay_num: int) -> Optional[int]`
- Get the state of a relay (0 = OFF, 1 = ON).
- Returns `None` if an I2C error occurs.

## Running Tests

Unit tests are provided in the `tests/` directory. To run tests:

```bash
python -m unittest discover tests
```

## Example: Cycling All Relays

```python
from src.main import XL9535
import time

xl9535 = XL9535()

def set_relays(state, start, end, step):
    for relay_num in range(start, end, step):
        for port in [0, 1]:
            xl9535.set_relay(port=port, relay_num=relay_num, state=state)
            time.sleep(0.1)

for _ in range(10):
    set_relays(state=1, start=0, end=8, step=1)   # Turn relays ON
    set_relays(state=0, start=7, end=-1, step=-1) # Turn relays OFF
```

## License

MIT License. See [LICENSE.md](LICENSE.md) for details.

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Code of Conduct

This project adheres to a [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Contact

For questions or support, contact Aina261 on Github. 