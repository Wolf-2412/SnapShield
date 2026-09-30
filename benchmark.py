import time
import statistics
import psutil

from ai_engine import predict
from network_monitor import collect_network_snapshot
from network_ai import analyze_network


def benchmark_event_ai(runs=100):
    events = [
        "normal interactive login",
        "port scan detected",
        "powershell encoded command observed",
        "unusual outbound connection detected",
    ]

    times = []

    for i in range(runs):
        event = events[i % len(events)]

        start = time.perf_counter()
        predict(event)
        end = time.perf_counter()

        times.append((end - start) * 1000)

    return {
        "runs": runs,
        "average_ms": statistics.mean(times),
        "median_ms": statistics.median(times),
        "min_ms": min(times),
        "max_ms": max(times),
    }


def benchmark_network_ai(runs=50):
    times = []

    for _ in range(runs):
        snapshot = collect_network_snapshot()

        start = time.perf_counter()
        analyze_network(snapshot)
        end = time.perf_counter()

        times.append((end - start) * 1000)

    return {
        "runs": runs,
        "average_ms": statistics.mean(times),
        "median_ms": statistics.median(times),
        "min_ms": min(times),
        "max_ms": max(times),
    }


def main():
    print("=" * 60)
    print("SNAPSHIELD PERFORMANCE BENCHMARK")
    print("=" * 60)

    print("\nSystem")
    print("-" * 60)
    print("CPU:", psutil.cpu_count(logical=False), "physical cores")
    print("Logical CPUs:", psutil.cpu_count(logical=True))
    print("RAM:", round(psutil.virtual_memory().total / (1024**3), 2), "GB")

    print("\nEvent AI Inference")
    print("-" * 60)

    event_result = benchmark_event_ai()

    for key, value in event_result.items():
        if key == "runs":
            print(f"{key}: {value}")
        else:
            print(f"{key}: {value:.4f} ms")

    print("\nNetwork AI Inference")
    print("-" * 60)

    network_result = benchmark_network_ai()

    for key, value in network_result.items():
        if key == "runs":
            print(f"{key}: {value}")
        else:
            print(f"{key}: {value:.4f} ms")

    print("\n" + "=" * 60)
    print("Benchmark complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()