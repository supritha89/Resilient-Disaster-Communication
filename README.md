# Resilient Disaster Communication: MAC-Layer Protocol Simulations

A collection of Python simulations evaluating medium access control (MAC)
strategies for ad-hoc wireless networks deployed in disaster-recovery
scenarios — situations where conventional infrastructure (cell towers, Wi-Fi
access points) is unavailable and nodes (rescue devices, sensors, radios)
must coordinate channel access among themselves.

The project compares **traditional** scheduling/backoff algorithms against
**proposed alternatives**, measuring the metrics that matter most for
emergency networks: collision rate, channel access delay, throughput, and
energy consumption.

## Why this matters

In a disaster scenario, network nodes are often battery-powered, deployed in
large numbers, and competing for a shared, congested wireless channel.
Standard protocols designed for everyday networks can perform poorly under
these conditions — leading to excessive collisions, wasted energy, and
unfair access delays. This project simulates and visualizes how alternative
backoff and scheduling strategies affect network performance as the number
of nodes grows, to explore whether simple algorithmic changes can improve
resilience.

## What's included

| Module | What it does |
|---|---|
| `src/backoff_simulation.py` | Compares a traditional CSMA/CA exponential backoff scheme against a proposed dynamic backoff scheme. Measures average backoff time and collision rate as network density increases. |
| `src/energy_consumption.py` | Estimates relative energy consumption (proportional to time spent in backoff/idle-listening) for both backoff schemes across varying node counts. |
| `src/scheduling_simulation.py` | Compares First-Come-First-Served (FCFS) and Round Robin channel-access scheduling, measuring per-node waiting time and overall throughput. |

Each module can be run independently, or all together via `run_all.py`.

## Algorithms compared

**Backoff schemes**
- *Traditional*: Standard binary exponential backoff, where the contention
  window doubles with each retransmission attempt.
- *Proposed (dynamic)*: Adjusts the backoff window based on the current
  network density, aiming to reduce collisions as more nodes join.

**Scheduling schemes**
- *FCFS*: Nodes are served strictly in arrival order; a node waits for all
  previously queued nodes to fully complete their transmission.
- *Round Robin*: Each node is given a fixed time slice (quantum); nodes
  cycle through the queue until all transmissions complete.

## How to run

```bash
# Install dependencies
pip install -r requirements.txt

# Run everything with default settings
python run_all.py

# Or run an individual simulation with custom parameters
python src/backoff_simulation.py --max-nodes 30 --test-cases 200
python src/energy_consumption.py --max-nodes 30 --slot-time 10
python src/scheduling_simulation.py --num-nodes 10 --time-quantum 4
```

All plots are saved to the `results/` directory.

## Project structure

```
.
├── src/
│   ├── backoff_simulation.py
│   ├── energy_consumption.py
│   └── scheduling_simulation.py
├── results/                 # Generated plots (created on first run)
├── run_all.py
├── requirements.txt
└── README.md
```

## Sample results

After running `run_all.py`, the `results/` folder will contain:

- `backoff_comparison.png` — average backoff time vs. number of nodes for
  both algorithms.
- `collision_rate.png` — collision rate vs. number of nodes.
- `energy_consumption.png` — relative energy consumption vs. number of
  nodes.
- `waiting_time_comparison.png` — per-node waiting time under FCFS vs.
  Round Robin.
- `throughput_comparison.png` — overall throughput under FCFS vs. Round
  Robin.

*(Add a sentence or two here summarizing your actual findings once you've
run the simulations — e.g. "At 20 nodes, the proposed dynamic backoff
reduced the collision rate by X% compared to traditional exponential
backoff.")*

## Possible extensions

- Replace the simplified analytical models with a packet-level discrete
  event simulation (e.g. using SimPy).
- Add a mobility model to simulate nodes moving in/out of range, as would
  happen with rescue personnel.
- Extend the energy model to account for transmit/receive/idle power
  states separately, using realistic radio hardware values.

## License

This project is for educational and research purposes.
