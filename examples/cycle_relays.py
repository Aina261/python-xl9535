from src.main import XL9535
import time

xl9535 = XL9535()


def set_relays(state, start, end, step):
    for relay_num in range(start, end, step):
        for port in [0, 1]:
            xl9535.set_relay(port=port, relay_num=relay_num, state=state)
            time.sleep(0.1)


for _ in range(10):
    set_relays(state=1, start=0, end=8, step=1)  # Turn relays ON
    set_relays(state=0, start=7, end=-1, step=-1)  # Turn relays OFF
