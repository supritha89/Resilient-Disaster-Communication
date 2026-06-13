"""
backoff_simulation.py
======================
Simulates and compares a traditional CSMA/CA exponential backoff scheme
against a proposed dynamic backoff scheme for contention-based medium
access in ad-hoc disaster communication networks.

For each network size (number of contending nodes), the script:
  - Computes the average backoff time under the traditional algorithm.
  - Computes the average backoff time under the proposed (dynamic) algorithm.
  - Estimates the collision rate as a function of network density.

Outputs:
  - results/backoff_comparison.png   (backoff time vs. number of nodes)
  - results/collision_rate.png       (collision rate vs. number of nodes)
  - Printed summary tables.
"""

import argparse
import os
import random

import pandas as pd
import matplotlib.pyplot as plt


def csma_ca_backoff(retry_count: int, max_backoff_time: int = 1024) -> int:
    """Compute a traditional CSMA/CA exponential backoff time.

    Args:
        retry_count: Current retransmission attempt number (n).
        max_backoff_time: Upper bound on the backoff window, in slots.

    Returns:
        Backoff time in milliseconds.
    """
    backoff_time = random.randint(0, 2 ** retry_count - 1)
    backoff_time = min(backoff_time, max_backoff_time)
    return backoff_time * 10  # convert slots to milliseconds


def run_simulation(num_test_cases: int, max_nodes: int):
    """Run the backoff/collision simulation across a range of node counts.

    Returns:
        Tuple of (backoff_df, collision_df, comparison_df) pandas DataFrames.
    """
    backoff_results = []
    collision_results = []
    comparison_results = []

    for num_nodes in range(1, max_nodes + 1):
        total_backoff_time = 0
        total_collisions = 0
        total_comparison_collisions = 0

        for _ in range(num_test_cases):
            backoff_times = []
            collisions = 0
            comparison_collisions = 0

            for i in range(num_nodes):
                bt = csma_ca_backoff(i)
                backoff_times.append(bt)

                if bt == 0:
                    collisions += 1
                if i > 0 and backoff_times[i] == backoff_times[i - 1]:
                    comparison_collisions += 1

            total_backoff_time += sum(backoff_times)
            total_collisions += collisions
            total_comparison_collisions += comparison_collisions

        avg_backoff_time = total_backoff_time / (num_test_cases * num_nodes)
        # Proposed dynamic backoff: scales the average by network density
        new_backoff_time = avg_backoff_time * (num_nodes + 1) / num_nodes
        collision_rate = total_collisions / (num_test_cases * num_nodes)

        backoff_results.append({
            "Nodes": num_nodes,
            "Traditional Backoff Time (ms)": avg_backoff_time,
            "Proposed Backoff Time (ms)": new_backoff_time,
        })
        collision_results.append({
            "Nodes": num_nodes,
            "Collision Rate": collision_rate,
        })

        if num_nodes > 1:
            comparison_rate = total_comparison_collisions / (num_test_cases * (num_nodes - 1))
        else:
            comparison_rate = 0
        comparison_results.append({
            "Nodes": num_nodes,
            "Consecutive Backoff Match Rate": comparison_rate,
        })

    return (
        pd.DataFrame(backoff_results),
        pd.DataFrame(collision_results),
        pd.DataFrame(comparison_results),
    )


def plot_results(backoff_df: pd.DataFrame, collision_df: pd.DataFrame, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)

    # Backoff time comparison
    plt.figure(figsize=(10, 5))
    plt.plot(backoff_df["Nodes"], backoff_df["Traditional Backoff Time (ms)"],
             "b-", linewidth=1.5, label="Traditional exponential backoff")
    plt.plot(backoff_df["Nodes"], backoff_df["Proposed Backoff Time (ms)"],
             "r-", linewidth=1.5, label="Proposed dynamic backoff")
    plt.xlabel("Number of Nodes")
    plt.ylabel("Average Backoff Time (ms)")
    plt.title("Backoff Time vs. Number of Contending Nodes")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    backoff_path = os.path.join(output_dir, "backoff_comparison.png")
    plt.savefig(backoff_path, dpi=150)
    plt.close()

    # Collision rate
    plt.figure(figsize=(10, 5))
    plt.plot(collision_df["Nodes"], collision_df["Collision Rate"],
             "g-", linewidth=1.5, label="Collision rate")
    plt.scatter(collision_df["Nodes"], collision_df["Collision Rate"], color="g", s=40)
    plt.xlabel("Number of Nodes")
    plt.ylabel("Collision Rate")
    plt.title("Collision Rate vs. Number of Contending Nodes")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    collision_path = os.path.join(output_dir, "collision_rate.png")
    plt.savefig(collision_path, dpi=150)
    plt.close()

    print(f"Saved plots to: {backoff_path}, {collision_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Compare traditional vs. proposed CSMA/CA backoff algorithms."
    )
    parser.add_argument("--test-cases", type=int, default=100,
                         help="Number of randomized trials per node count (default: 100)")
    parser.add_argument("--max-nodes", type=int, default=20,
                         help="Maximum number of contending nodes to simulate (default: 20)")
    parser.add_argument("--output-dir", type=str, default="results",
                         help="Directory to save plots (default: results/)")
    args = parser.parse_args()

    backoff_df, collision_df, comparison_df = run_simulation(args.test_cases, args.max_nodes)

    print("\nBackoff Time Comparison:")
    print(backoff_df.to_string(index=False))
    print("\nCollision Rate by Network Size:")
    print(collision_df.to_string(index=False))

    plot_results(backoff_df, collision_df, args.output_dir)


if __name__ == "__main__":
    main()
