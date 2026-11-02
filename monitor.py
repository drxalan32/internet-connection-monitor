
import csv
import socket
import time
from datetime import datetime
from pathlib import Path

HOST = "1.1.1.1"
PORT = 443
INTERVAL = 5
TIMEOUT = 3

LOG_FILE = Path("connection_log.csv")


def check_connection():
    start = time.perf_counter()

    try:
        with socket.create_connection((HOST, PORT), timeout=TIMEOUT):
            latency = (time.perf_counter() - start) * 1000
            return True, round(latency, 2)

    except (socket.timeout, OSError):
        return False, None


def initialize_log():
    if not LOG_FILE.exists():
        with LOG_FILE.open("w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["timestamp", "status", "latency_ms"])


def save_result(timestamp, status, latency):
    with LOG_FILE.open("a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, status, latency or ""])


def main():
    initialize_log()

    print("StreamNexa - Internet Connection Monitor")
    print("Press Ctrl+C to stop monitoring.\n")

    try:
        while True:
            timestamp = datetime.now().astimezone().isoformat(
                timespec="seconds"
            )

            connected, latency = check_connection()

            if connected:
                status = "ONLINE"
                print(f"[{timestamp}] ONLINE | {latency} ms")
            else:
                status = "OFFLINE"
                print(f"[{timestamp}] OFFLINE | Connection failed")

            save_result(timestamp, status, latency)
            time.sleep(INTERVAL)

    except KeyboardInterrupt:
        print("\nMonitoring stopped.")
        print(f"Results saved to: {LOG_FILE.resolve()}")


if __name__ == "__main__":
    main()
