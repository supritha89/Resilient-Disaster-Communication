"""
energy_consumption.py
======================
Estimates relative energy consumption of nodes in a disaster communication
network under a traditional CSMA/CA backoff scheme versus a proposed
dynamic backoff scheme. Energy consumption is approximated as proportional
to the total time nodes spend in backoff (idle-listening) states.

Outputs:
  - results/energy_consumption.png
  - Printed summary table.
"""

import argparse
import os
import random

import pandas as pd
import matplotlib.pyplot as plt


def csma_ca_backoff(slot_time: int, contention_window_exp: int = 5) -> float:
    """Compute a CSMA/CA backoff time based on a contention window.

    Args:
        slot_time: Duration of a single time slot, in milliseconds.
        contention_window_exp: Exponent (m) defining contention window size 2^m.

    Returns:
        Backoff time in milliseconds.
    """
    random_slots = random.randint(0, (2 ** contention_window_exp) - 1)
    return random_slots * slot_time


def run_simulation(num_test_cases: int, max_nodes: int, slot_time: int = 10):
    """Run the energy consumption simulation across a range of node counts.

    Returns:
        A pandas DataFrame with traditional, proposed, and average energy
        consumption per network size.
    """
    records = []

    for num_nodes in range(1, max_nodes + 1):
        total_energy_old = 0.0
        total_energy_new = 0.0

        for _ in range(num_test_cases):
            backoff_times_old = []
            backoff_times_new = []

            for i in range(num_nodes):
                bt_old = csma_ca_backoff(slot_time)
                backoff_times_old.append(bt_old)

                if i == 0:
                    bt_new = bt_old
                else:
                    # Proposed dynamic adjustment scales backoff by node index
                    bt_new = bt_old * (i + 10) / (i + 5)
                backoff_times_new.append(bt_new)

            total_energy_old += sum(backoff_times_old)
            total_energy_new += sum(backoff_times_new)

        avg_energy_old = total_energy_old / num_test_cases
        avg_energy_new = total_energy_new / num_test_cases

        records.append({
            "Nodes": num_nodes,
            "Energy - Traditional": avg_energy_old,
            "Energy - Proposed": avg_energy_new,
        })

    df = pd.DataFrame(records)
    df["Average Energy"] = (df["Energy - Traditional"] + df["Energy - Proposed"]) / 2
    return df


def plot_results(df: pd.DataFrame, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)

    plt.figure(figsize=(10, 5))
    plt.plot(df["Nodes"], df["Energy - Traditional"], "b-", label="Traditional algorithm")
    plt.plot(df["Nodes"], df["Energy - Proposed"], "r-", label="Proposed algorithm")
    plt.plot(df["Nodes"], df["Average Energy"], "g--", label="Average")
    plt.xlabel("Number of Nodes")
    plt.ylabel("Relative Energy Consumption")
    plt.title("Energy Consumption vs. Number of Nodes")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    path = os.path.join(output_dir, "energy_consumption.png")
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"Saved plot to: {path}")


def main():
    parser = argparse.ArgumentParser(
        description="Compare relative energy consumption of traditional vs. proposed backoff schemes."
    )
    parser.add_argument("--test-cases", type=int, default=100,
                         help="Number of randomized trials per node count (default: 100)")
    parser.add_argument("--max-nodes", type=int, default=20,
                         help="Maximum number of nodes to simulate (default: 20)")
    parser.add_argument("--slot-time", type=int, default=10,
                         help="Slot duration in milliseconds (default: 10)")
    parser.add_argument("--output-dir", type=str, default="results",
                         help="Directory to save plots (default: results/)")
    args = parser.parse_args()

    df = run_simulation(args.test_cases, args.max_nodes, args.slot_time)

    print("\nEnergy Consumption Comparison:")
    print(df.to_string(index=False))

    plot_results(df, args.output_dir)


if __name__ == "__main__":
    main()
