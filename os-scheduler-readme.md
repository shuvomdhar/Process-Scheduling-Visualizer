# Process Scheduler Visualizer

A comprehensive Python-based GUI application for visualizing and comparing CPU process scheduling algorithms commonly used in Operating Systems.

## Overview

This tool provides an interactive way to understand how different scheduling algorithms work by allowing you to add processes dynamically and visualize their execution through Gantt charts. It's particularly useful for students learning OS concepts and educators demonstrating scheduling behavior.

## Features

- **Interactive GUI**: Built with Tkinter for a clean, single-window interface
- **Dynamic Process Management**: Add processes on-the-fly with custom arrival times, burst times, and priorities
- **Multiple Scheduling Algorithms**:
  - First Come First Serve (FCFS)
  - Shortest Job First (SJF) - Non-preemptive
  - Priority Scheduling - Non-preemptive (lower number = higher priority)
  - Round Robin (with configurable time quantum)
- **Visual Gantt Charts**: Real-time Matplotlib popup charts showing process execution timeline
- **Comprehensive Reports**: Export detailed PDF reports containing:
  - Color-coded Gantt chart with process labels
  - Process table showing arrival, burst, waiting, and turnaround times
  - Average Waiting Time (WT) and Turnaround Time (TAT) metrics
- **Test Examples**: Pre-generated sample outputs in the `test/` folder for reference

## Project Structure

```
process_scheduler/
├── __pycache__/          # Python cache files
├── .venv/                # Virtual environment (recommended)
├── .gitignore           # Git ignore configuration
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── test/               # Sample output PDFs and test cases
├── main_gui.py         # Main application entry point
├── fcfs.py             # FCFS algorithm implementation
├── sjf.py              # SJF algorithm implementation
├── priority.py         # Priority scheduling implementation
├── round_robin.py      # Round Robin implementation
└── viz_utils.py        # Visualization and PDF export utilities
```

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Setup Steps

1. **Clone or download the repository**:
   ```bash
   cd process_scheduler
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**:
   - **Windows**:
     ```bash
     .venv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     source .venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Application

```bash
python main_gui.py
```

### Using the Interface

1. **Add Processes**: 
   - Enter process details in the input grid (Arrival Time, Burst Time, Priority for priority scheduling)
   - Click "Add Process" to add each process to the queue
   - The process list updates dynamically

2. **Select Algorithm**:
   - Choose from the dropdown menu: FCFS, SJF, Priority, or Round Robin
   - For Round Robin, specify the time quantum

3. **Visualize**:
   - Click "Generate Gantt Chart" to see the execution visualization
   - A Matplotlib window will popup showing the color-coded Gantt chart

4. **Export Results**:
   - Click "Export to PDF" to save a comprehensive report
   - The PDF includes the Gantt chart, process table, and performance metrics

### Example Process Sets

Sample test cases are available in the `test/` folder, demonstrating outputs for all four algorithms with various process configurations.

## Understanding the Metrics

- **Waiting Time (WT)**: Time a process spends waiting in the ready queue
- **Turnaround Time (TAT)**: Total time from arrival to completion (WT + Burst Time)
- **Average WT**: Mean waiting time across all processes
- **Average TAT**: Mean turnaround time across all processes

Lower average WT and TAT generally indicate better scheduling performance.

## Scheduling Algorithms Explained

### FCFS (First Come First Serve)
Processes are executed in the order they arrive. Simple but can suffer from the "convoy effect" where short processes wait behind long ones.

**Example:**

| PID | Arrival Time | Burst Time |
| --- | ------------ | ---------- |
| P1  | 0            | 5          |
| P2  | 1            | 3          |
| P3  | 2            | 8          |
| P4  | 3            | 6          |

![FCFS Gantt Chart](test/fcfs_example.png)

*Average WT: 5.75, Average TAT: 11.25*

---

### SJF (Shortest Job First)
Non-preemptive algorithm that selects the process with the shortest burst time. Optimal for minimizing average waiting time but requires knowing burst times in advance.

**Example:**

| PID | Arrival | Burst |
| --- | ------- | ----- |
| P1  | 0       | 7     |
| P2  | 2       | 4     |
| P3  | 4       | 1     |
| P4  | 5       | 4     |

![SJF Gantt Chart](test/sjf_example.png)

*Average WT: 4.00, Average TAT: 8.00*

---

### Priority Scheduling
Processes are executed based on priority values (lower number = higher priority in this implementation). Can lead to starvation of low-priority processes.

**Example:**

| PID | Arrival | Burst | Priority |
| --- | ------- | ----- | -------- |
| P1  | 1       | 4     | 2        |
| P2  | 2       | 3     | 1        |
| P3  | 3       | 1     | 4        |
| P4  | 4       | 2     | 3        |

![Priority Scheduling Gantt Chart](test/priority_example.png)

*Average WT: 3.50, Average TAT: 6.00*

---

### Round Robin
Each process gets a fixed time quantum in a circular queue. Provides fair CPU allocation and good response time for interactive systems.

**Example (Time Quantum = 2):**

| PID | Arrival | Burst |
| --- | ------- | ----- |
| P1  | 0       | 5     |
| P2  | 1       | 4     |
| P3  | 2       | 2     |

![Round Robin Gantt Chart](test/round_robin_example.png)

*Average WT: 4.33, Average TAT: 8.00*

## Dependencies

Key libraries used (see `requirements.txt` for versions):
- `tkinter`: GUI framework (usually included with Python)
- `matplotlib`: Gantt chart visualization
- `reportlab`: PDF generation

## Contributing

Contributions are welcome! Areas for enhancement:
- Additional scheduling algorithms (SRTF, Multilevel Queue, etc.)
- Preemptive versions of existing algorithms
- Real-time algorithm comparison
- Enhanced visualization options

## License

This project is intended for educational purposes. Feel free to use and modify for learning and teaching Operating Systems concepts.

## Troubleshooting

**Issue**: Tkinter not found  
**Solution**: Tkinter usually comes with Python. On Linux, install with `sudo apt-get install python3-tk`

**Issue**: Virtual environment activation fails  
**Solution**: Ensure you're using the correct command for your OS and shell

**Issue**: PDF export fails  
**Solution**: Verify reportlab is installed correctly with `pip list | grep reportlab`

## Acknowledgments

This tool was created to help visualize fundamental OS scheduling concepts. The Gantt chart examples in the `test/` folder demonstrate typical behavior of each algorithm.

---

**Author**: Process Scheduler Visualizer Team  
**Version**: 1.0  
**Last Updated**: 2025
