# 🚦 Fuzzy Logic-Based Traffic Light Control System

An intelligent traffic light control system using **Fuzzy Logic** and **Mamdani Inference** to optimize traffic flow at a 4-way intersection. This project demonstrates how adaptive control can significantly outperform traditional fixed-time controllers.

## 📊 Live Demo

**[View Live Dashboard](https://kinhluan.github.io/fuzzy-traffic-system/)**

## ✨ Key Features

- **🎯 28 Advanced Fuzzy Rules** per direction (112 total rules)
- **🚗 Realistic Queue-Based Simulation** using Poisson arrival distribution
- **📈 14-47% Performance Improvement** over fixed-time controllers (average +27.3%)
- **⚖️ Fairness-Aware Optimization** preventing vehicle starvation
- **🌐 Interactive Web Dashboard** with real-time visualizations
- **📊 Comprehensive Metrics** (waiting time, queue length, throughput, fairness index)

## 🏗️ System Architecture

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌────────────────┐
│   Input     │───▶│Fuzzification │───▶│   Fuzzy     │───▶│Defuzzification │
│   Layer     │    │              │    │   Rules     │    │                │
│             │    │              │    │  (Mamdani)  │    │                │
│ • Density   │    │ Low/Med/High │    │  28 Rules   │    │ Green Duration │
│ • Wait Time │    │              │    │             │    │   10-90 sec    │
└─────────────┘    └──────────────┘    └─────────────┘    └────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Poetry (for dependency management)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/kinhluan/fuzzy-traffic-system.git
cd fuzzy-traffic-system
```

2. Install dependencies using Poetry:

```bash
poetry install
```

3. Activate the virtual environment:

```bash
poetry shell
```

### Running the Simulation

**Option 1: Using Shell Scripts (Recommended)**

```bash
# Run full simulation (5-10 minutes, all 9 scenarios)
./scripts/run.sh

# Or quick demo (2 minutes, 1 scenario)
./scripts/demo.sh
```

**Option 2: Direct Python Execution**

```bash
# Full simulation
poetry run python src/main.py

# Individual scenario test
poetry run python examples/simple_comparison.py
```

This will:
- Run simulations for all 9 traffic scenarios
- Compare Fuzzy vs Fixed-Time controllers (30 min simulation each)
- Generate comprehensive performance metrics
- Export results to `web/data/comparison_results.json`

### View the Dashboard

Start the local web server:

```bash
# Using script
./scripts/serve.sh

# Or manually
cd web && python3 -m http.server 8000
```

Then open **http://localhost:8000** in your browser.

**Dashboard Features:**
- 📊 Performance comparison charts (waiting time, queue length, throughput)
- 📈 Detailed metrics tables for all scenarios
- 🎯 Scenario selector to compare different traffic patterns
- 🏗️ System architecture overview

### Testing Individual Components

```bash
# Test all components
./scripts/test.sh

# Or test individually
poetry run python src/fuzzy_controller/controller.py
poetry run python src/simulation/traffic_model.py
poetry run python src/fuzzy_controller/membership_functions.py
```

## 📁 Project Structure

```
fuzzy-traffic-system/
├── src/
│   ├── fuzzy_controller/
│   │   ├── membership_functions.py  # Fuzzy membership functions
│   │   ├── fuzzy_rules.py          # 28 advanced fuzzy rules
│   │   └── controller.py           # Main fuzzy controller
│   ├── simulation/
│   │   ├── traffic_model.py        # Queue-based traffic simulator
│   │   ├── fixed_controller.py     # Fixed-time baseline controller
│   │   └── scenarios.py            # Traffic scenarios (9 scenarios)
│   ├── utils/
│   │   └── metrics.py              # Performance metrics calculator
│   └── main.py                     # Main comparison script
├── web/
│   ├── index.html                  # Dashboard homepage
│   ├── css/style.css               # Styling
│   ├── js/
│   │   └── main.js                 # Dashboard visualizations
│   └── data/
│       └── comparison_results.json # Generated simulation results
├── scripts/
│   ├── setup.sh                    # Install dependencies
│   ├── run.sh                      # Run full simulation
│   ├── demo.sh                     # Quick demo
│   ├── test.sh                     # Run tests
│   ├── serve.sh                    # Start web server
│   ├── visualize.sh                # Generate visualizations
│   └── clean.sh                    # Clean caches
├── docs/                           # Documentation & visualizations
├── examples/                       # Example scripts
├── pyproject.toml                  # Poetry dependencies
├── test_system.py                  # System integration tests
└── README.md
```

## 🧠 Fuzzy Logic Implementation

### Input Variables

- **Vehicle Density** (0-100 vehicles): Low, Medium, High
- **Waiting Time** (0-300 seconds): Short, Medium, Long, Very Long

### Output Variable

- **Green Light Duration** (10-90 seconds): Short, Medium, Long, Very Long

### Fuzzy Rules Categories

#### 1. Primary Density-Based Rules (12 rules)

```
IF current_density HIGH AND opposite_density LOW
THEN green_time VERY_LONG
```

#### 2. Waiting Time Priority Rules (8 rules)

```
IF waiting_time VERY_LONG
THEN green_time LONG (prevent starvation)
```

#### 3. Fairness & Balance Rules (8 rules)

```
IF all_directions HIGH_DENSITY
THEN green_time MEDIUM (rotate fairly)
```

**Total: 28 rules per direction × 4 directions = 112 fuzzy rules**

## 📊 Performance Results

**Real simulation data from 30-minute runs (1800s) for each scenario.**

### Summary Across All Scenarios

| Scenario | Fuzzy Waiting Time | Fixed Waiting Time | Improvement |
|----------|-------------------|-------------------|-------------|
| **Normal Traffic** | 9.81s | 15.69s | **+37.5%** ⭐ |
| **Rush Hour (N-S)** | 13.64s | 17.89s | **+23.7%** |
| **Rush Hour (E-W)** | 12.65s | 19.46s | **+35.0%** |
| **Light Traffic** | 8.27s | 15.68s | **+47.2%** 🏆 |
| **Asymmetric (Heavy North)** | 13.48s | 19.39s | **+30.5%** |
| **Peak Congestion** | 20.37s | 19.80s | -2.9%* |
| **Morning Commute** | 14.75s | 17.12s | **+13.9%** |
| **Evening Commute** | 14.31s | 17.64s | **+18.9%** |
| **Weekend Leisure** | 10.52s | 15.56s | **+32.4%** |

**Average Improvement: +27.3%** (excluding peak congestion)

*Peak Congestion: Fixed-time performs slightly better under extreme congestion when all directions are saturated.

### Detailed Metrics - Normal Traffic

| Metric | Fuzzy Controller | Fixed-Time | Improvement |
|--------|-----------------|------------|-------------|
| Avg Waiting Time | 9.81s | 15.69s | **+37.5%** |
| Max Waiting Time | 35.0s | 50.0s | **+30.0%** |
| Avg Queue Length | 7.62 vehicles | 12.26 vehicles | **+37.8%** |
| Max Queue Length | 21 vehicles | 33 vehicles | **+36.4%** |
| Throughput | 2784 veh/h | 2752 veh/h | **+1.2%** |
| Fairness Index | 1.000 | 0.998 | **+0.002** |

### Detailed Metrics - Rush Hour (N-S)

| Metric | Fuzzy Controller | Fixed-Time | Improvement |
|--------|-----------------|------------|-------------|
| Avg Waiting Time | 13.64s | 17.89s | **+23.7%** |
| Max Waiting Time | 53.0s | 51.0s | -3.9% |
| Avg Queue Length | 19.70 vehicles | 26.00 vehicles | **+24.2%** |
| Max Queue Length | 58 vehicles | 75 vehicles | **+22.7%** |
| Throughput | 5184 veh/h | 5128 veh/h | **+1.1%** |
| Fairness Index | 0.956 | 0.986 | -0.030 |

### Key Findings

✅ **Best Performance**: Light traffic scenarios (+47.2% improvement)
✅ **Consistent Gains**: 14-37% improvement in most scenarios
✅ **Queue Reduction**: 24-47% shorter queues on average
✅ **Adaptive Advantage**: Handles asymmetric patterns 30% better
⚠️ **Peak Limitation**: Slight disadvantage under extreme saturation

## 🎨 Web Dashboard

### Main Dashboard (`index.html`)

The interactive web dashboard provides:

- **📊 Scenario Selector**: Choose from 9 traffic scenarios
- **📈 Performance Charts**: Comparative visualizations using Chart.js
  - Average waiting time comparison
  - Queue length comparison
  - Throughput analysis
  - Improvement percentage bars
- **📋 Metrics Table**: Detailed performance comparison with all metrics
- **🏗️ Architecture Diagram**: System overview and data flow
- **📜 Fuzzy Rules Explorer**: View rule categories and examples

## 🔬 Traffic Scenarios

1. **Normal Traffic**: Balanced 12 veh/min on all directions
2. **Rush Hour (N-S)**: Heavy N-S (35 veh/min), light E-W (10 veh/min)
3. **Rush Hour (E-W)**: Heavy E-W (35 veh/min), light N-S (10 veh/min)
4. **Light Traffic**: Late night, 5 veh/min all directions
5. **Asymmetric (Heavy North)**: 45 veh/min North, 8 veh/min others
6. **Peak Congestion**: 40 veh/min all directions (stress test)
7. **Morning Commute**: Inbound heavy (N:30, E:25), outbound light
8. **Evening Commute**: Outbound heavy (S:30, W:25), inbound light
9. **Weekend Leisure**: Moderate balanced flow

## 🧪 Testing

Run comprehensive system tests:

```bash
# Using script
./scripts/test.sh

# Or directly
poetry run python test_system.py
```

This tests all 6 core components:
1. ✅ Membership Functions creation
2. ✅ Fuzzy Rules generation (112 rules)
3. ✅ Fuzzy Controller inference
4. ✅ Traffic Simulator logic
5. ✅ Fixed-Time Controller
6. ✅ Traffic Scenarios definitions

## 📖 Documentation

- **[Quick Start Guide](QUICKSTART.md)**: 5-minute setup guide
- **[Deployment Guide](DEPLOYMENT_GUIDE.md)**: Deploy to GitHub Pages
- **[Project Summary](PROJECT_SUMMARY.md)**: Complete project overview
- **[SUMO Integration Guide](docs/SUMO_INTEGRATION.md)**: How to integrate SUMO (Simulation of Urban MObility)
- **[Scripts Documentation](scripts/README.md)**: All available shell scripts
- **[Membership Functions Analysis](docs/README.md)**: Detailed fuzzy logic analysis
- **Membership Functions Visualization**: `docs/membership_functions.png`

## 🛠️ Technologies Used

- **Python 3.11+**: Core programming language
- **scikit-fuzzy**: Fuzzy logic implementation (Mamdani inference)
- **NumPy & Pandas**: Data processing and analysis
- **Matplotlib**: Visualization and plotting
- **Poetry**: Dependency management
- **Chart.js**: Interactive web visualizations
- **HTML/CSS/JavaScript**: Web dashboard

## 📚 References

1. **Research Papers**:
   - Adaptive Fuzzy Traffic Controllers (IEEE Xplore)
   - Mamdani Inference for Traffic Optimization

2. **Fuzzy Logic**:
   - [scikit-fuzzy Documentation](https://pythonhosted.org/scikit-fuzzy/)
   - Fuzzy Logic Toolbox (MATLAB equivalent in Python)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍🎓 Author

- **Luân B**

- Project for: Fuzzy Logic and Applications Course

## 🙏 Acknowledgments

- Thanks to the scikit-fuzzy team for the excellent fuzzy logic library
- Inspired by research in adaptive traffic control systems
- SUMO (Simulation of Urban MObility) team for traffic simulation concepts

---

**⭐ If you find this project useful, please consider giving it a star!**

## 📧 Contact

For questions or feedback, please open an issue on GitHub.
