"""
run_all.py
==========
Convenience script that runs all simulations in this project with their
default settings and saves every plot into the results/ directory.

Usage:
    python run_all.py
"""

import subprocess
import sys

SCRIPTS = [
    "src/backoff_simulation.py",
    "src/energy_consumption.py",
    "src/scheduling_simulation.py",
]


def main():
    for script in SCRIPTS:
        print(f"\n{'=' * 60}")
        print(f"Running {script}")
        print("=" * 60)
        subprocess.run([sys.executable, script], check=True)

    print("\nAll simulations complete. See the results/ directory for plots.")


if __name__ == "__main__":
    main()
