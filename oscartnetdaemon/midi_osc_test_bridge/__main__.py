import time

from oscartnetdaemon.midi_osc_test_bridge.domain.service import Domain


motb = Domain()
motb.start()

try:
    while True:
        time.sleep(0.01)

except KeyboardInterrupt:
    pass
