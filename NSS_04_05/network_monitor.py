import random
import time
import csv
from datetime import datetime

# Simulation parameters
HOSTS = 50
MAX_CONNECTIONS = 10        # Normal max outbound connections
ANOMALY_THRESHOLD = 15      # Flag hosts exceeding this

def simulate_network_activity():
    """
    Returns a dictionary of host_id -> number of outbound connections.
    """
    activity = {}
    for host_id in range(HOSTS):
        normal_activity = random.randint(1, MAX_CONNECTIONS)
        # Simulate occasional anomaly
        if random.random() < 0.1:
            normal_activity += random.randint(5, 10)
        activity[host_id] = normal_activity
    return activity

def monitor_network(steps=20):
    """
    Simulates monitoring network activity over time.
    Logs anomalies to 'network_alerts.csv'.
    """
    with open("network_alerts.csv", mode="w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Timestamp", "Host", "Connections", "Alert"])

        for step in range(steps):
            activity = simulate_network_activity()
            for host, connections in activity.items():
                if connections > ANOMALY_THRESHOLD:
                    alert = "EXCESSIVE CONNECTIONS"
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"[ALERT] {timestamp} - Host {host} has {connections} outbound connections!")
                    # Record the alert for later review
                    writer.writerow([timestamp, host, connections, alert])
            time.sleep(0.3)

if __name__ == "__main__":
    print("Starting simulated network monitoring...")
    monitor_network()
    print("Monitoring complete. Alerts logged to 'network_alerts.csv'.")
