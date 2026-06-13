"""
scheduling_simulation.py
=========================
Compares First-Come-First-Served (FCFS) and Round Robin scheduling for
allocating channel access time among nodes in a disaster communication
network, evaluating per-node waiting time and overall network throughput.

Outputs:
  - results/waiting_time_comparison.png
  - results/throughput_comparison.png
  - Printed summary of average waiting times and throughput.
"""

import argparse
import os
import random

import numpy as np
import matplotlib.pyplot as plt


def fcfs_waiting_time(burst_times):
    """Compute per-node waiting times under First-Come-First-Served scheduling."""
    num_nodes = len(burst_times)
    waiting_times = [0]
    for i in range(1, num_nodes):
        waiting_times.append(waiting_times[i - 1] + burst_times[i - 1])
    return waiting_times


def round_robin_waiting_time(burst_times, time_quantum):
    """Compute per-node waiting times under Round Robin scheduling."""
    num_nodes = len(burst_times)
    remaining_times = burst_times.copy()
    waiting_times = [0] * num_nodes
    current_time = 0

    while True:
        all_finished = True
        for i in range(num_nodes):
            if remaining_times[i] > 0:
                all_finished = False
                if remaining_times[i] > time_quantum:
                    current_time += time_quantum
                    remaining_times[i] -= time_quantum
                else:
                    current_time += remaining_times[i]
                    waiting_times[i] = current_time - burst_times[i]
                    remaining_times[i] = 0
        if all_finished:
            break

    return waiting_times


def calculate_throughput(burst_times, waiting_times,
                          data_packet_size=100, sifs=1, ack_transmission_time=2):
    """Estimate network throughput given burst and waiting times.

    Args:
        burst_times: List of per-node transmission burst durations (ms).
        waiting_times: List of per-node waiting times (ms).
        data_packet_size: Size of a data packet in bytes.
        sifs: Short interframe spacing duration (ms).
        ack_transmission_time: ACK transmission duration (ms).

    Returns:
        Throughput in bytes/ms.
    """
    channel_busy_time = sum(burst_times) + np.mean(waiting_times)
    return data_packet_size / (channel_busy_time + sifs + ack_transmission_time)


def plot_waiting_times(burst_times, waiting_fcfs, waiting_rr, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    node_labels = [f"Node {i + 1}" for i in range(len(burst_times))]

    plt.figure(figsize=(10, 5))
    plt.plot(node_labels, waiting_fcfs, linestyle="-", label="FCFS (Traditional)")
    plt.plot(node_labels, waiting_rr, linestyle="--", label="Round Robin")
    plt.xlabel("Nodes")
    plt.ylabel("Waiting Time (ms)")
    plt.title("Per-Node Waiting Time: FCFS vs. Round Robin")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    path = os.path.join(output_dir, "waiting_time_comparison.png")
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"Saved plot to: {path}")


def plot_throughput(throughput_fcfs, throughput_rr, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    plt.figure(figsize=(6, 5))
    plt.bar(["FCFS (Traditional)", "Round Robin"],
            [throughput_fcfs, throughput_rr],
            color=["#050234", "#E310BD"])
    plt.ylabel("Throughput (bytes/ms)")
    plt.title("Throughput Comparison")
    plt.tight_layout()

    path = os.path.join(output_dir, "throughput_comparison.png")
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"Saved plot to: {path}")


def main():
    parser = argparse.ArgumentParser(
        description="Compare FCFS and Round Robin scheduling for channel access."
    )
    parser.add_argument("--num-nodes", type=int, default=8,
                         help="Number of nodes in the network (default: 8)")
    parser.add_argument("--time-quantum", type=int, default=5,
                         help="Round Robin time quantum in milliseconds (default: 5)")
    parser.add_argument("--burst-times", type=int, nargs="+", default=None,
                         help="Optional explicit burst times per node, e.g. --burst-times 4 8 2 6. "
                              "If omitted, random burst times are generated.")
    parser.add_argument("--seed", type=int, default=42,
                         help="Random seed for reproducible burst-time generation (default: 42)")
    parser.add_argument("--output-dir", type=str, default="results",
                         help="Directory to save plots (default: results/)")
    args = parser.parse_args()

    if args.burst_times:
        burst_times = args.burst_times
        num_nodes = len(burst_times)
    else:
        random.seed(args.seed)
        num_nodes = args.num_nodes
        burst_times = [random.randint(2, 12) for _ in range(num_nodes)]

    waiting_fcfs = fcfs_waiting_time(burst_times)
    waiting_rr = round_robin_waiting_time(burst_times, args.time_quantum)

    throughput_fcfs = calculate_throughput(burst_times, waiting_fcfs)
    throughput_rr = calculate_throughput(burst_times, waiting_rr)

    print(f"Burst times: {burst_times}")
    print(f"Time quantum: {args.time_quantum} ms\n")

    print("Per-node waiting times:")
    for i in range(num_nodes):
        print(f"  Node {i + 1}: FCFS = {waiting_fcfs[i]} ms, "
              f"Round Robin = {waiting_rr[i]} ms")

    print(f"\nAverage Waiting Time (FCFS):        {np.mean(waiting_fcfs):.2f} ms")
    print(f"Average Waiting Time (Round Robin):  {np.mean(waiting_rr):.2f} ms")

    print(f"\nThroughput (FCFS):       {throughput_fcfs:.4f} bytes/ms")
    print(f"Throughput (Round Robin): {throughput_rr:.4f} bytes/ms")

    plot_waiting_times(burst_times, waiting_fcfs, waiting_rr, args.output_dir)
    plot_throughput(throughput_fcfs, throughput_rr, args.output_dir)


if __name__ == "__main__":
    main()
