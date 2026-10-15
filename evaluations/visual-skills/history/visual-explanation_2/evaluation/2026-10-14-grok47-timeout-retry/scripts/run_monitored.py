"""Record host resource pressure without changing generation behavior."""
import datetime
import json
import os
from pathlib import Path
import threading
import run

stop = threading.Event()


def monitor():
    with (run.ROOT / 'preflight/resource-history.jsonl').open('a') as stream:
        while True:
            memory = {}
            for line in Path('/proc/meminfo').read_text().splitlines():
                key, value = line.split(':', 1)
                if key in ('MemTotal', 'MemAvailable', 'SwapTotal', 'SwapFree'):
                    memory[key + '_kB'] = int(value.strip().split()[0])
            stream.write(json.dumps({
                'time': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                'load_average': os.getloadavg(),
                **memory,
            }) + '\n')
            stream.flush()
            if stop.wait(20):
                return


if __name__ == '__main__':
    worker = threading.Thread(target=monitor, daemon=True)
    worker.start()
    try:
        run.main()
    finally:
        stop.set()
        worker.join()
