import time
import csv
import os
import psutil  # OS Kernel Telemetry Interfacing Library

print("🔌 Real-time Hardware Kernel Telemetry Stream Initialized...")

CSV_FILE = "server_metrics.csv"
SAMPLE_INTERVAL = 1.5

# Check if file exists to write headers
if not os.path.isfile(CSV_FILE):
    with open(CSV_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "CPU_Usage", "RAM_Usage", "Response_Time", "Status"])

# Prime cpu_percent so the first value is based on a valid interval
psutil.cpu_percent(interval=None)
loop_counter = 0

try:
    while True:
        loop_counter += 1
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

        try:
            cpu_usage = psutil.cpu_percent(interval=None)
            ram_usage = psutil.virtual_memory().percent
        except Exception as exc:
            print(f"[ERROR] Metric collection failed: {exc}")
            time.sleep(SAMPLE_INTERVAL)
            continue

        if cpu_usage > 80 or ram_usage > 85:
            response_time = round(1500 + (cpu_usage * 15), 2)
            status = 1
            mode = "STRESS"
        else:
            response_time = round(20 + (cpu_usage * 4), 2)
            status = 0
            mode = "HEALTHY"

        print(
            f"[{mode}] Loop: {loop_counter} | CPU: {cpu_usage}% | RAM: {ram_usage}% | "
            f"Latency: {response_time}ms"
        )

        try:
            with open(CSV_FILE, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([timestamp, cpu_usage, ram_usage, response_time, status])
        except OSError as exc:
            print(f"[ERROR] CSV write failed: {exc}")

        time.sleep(SAMPLE_INTERVAL)

except KeyboardInterrupt:
    print("\n🛑 Telemetry ingestion stream suspended safely by operator.")