# 🚦 Fuzzy Logic-Based Traffic Light Control System

An intelligent traffic light control system using **Fuzzy Logic** and **Mamdani Inference** to optimize traffic flow at a 4-way intersection. This project demonstrates how adaptive control can significantly outperform traditional fixed-time controllers.

## 📊 Live Demo

**[View Live Dashboard](https://kinhluan.github.io/fuzzy-traffic-system/)**

## ✨ Key Features

- **🎯 28 Advanced Fuzzy Rules** per direction (112 total rules)
- **🚗 Realistic Queue-Based Simulation** using Poisson arrival distribution
- **📈 20-40% Performance Improvement** over fixed-time controllers
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

Run the main comparison script:

```bash
python src/main.py
```

This will:

- Run simulations for all predefined scenarios
- Compare Fuzzy vs Fixed-Time controllers
- Generate performance metrics
- Export results to `web/data/comparison_results.json`

### Testing Individual Components

Test fuzzy controller:

```bash
python src/fuzzy_controller/controller.py
```

Test traffic simulator:

```bash
python src/simulation/traffic_model.py
```

Test membership functions:

```bash
python src/fuzzy_controller/membership_functions.py
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
│   │   ├── metrics.py              # Performance metrics calculator
│   │   └── visualization.py        # Data visualization utilities
│   └── main.py                     # Main comparison script
├── web/
│   ├── index.html                  # Dashboard homepage
│   ├── css/style.css               # Styling
│   ├── js/main.js                  # Interactive visualizations
│   └── data/                       # Generated comparison results
├── tests/                          # Unit tests
├── docs/                           # Documentation
├── pyproject.toml                  # Poetry dependencies
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

### Normal Traffic Scenario

| Metric | Fuzzy Controller | Fixed-Time | Improvement |
|--------|-----------------|------------|-------------|
| Avg Waiting Time | 45.2s | 62.4s | **+27.6%** |
| Avg Queue Length | 8.5 vehicles | 12.3 vehicles | **+30.9%** |
| Throughput | 576 veh/h | 528 veh/h | **+9.1%** |
| Fairness Index | 0.892 | 0.834 | **+6.9%** |

### Rush Hour Scenario (N-S Heavy)

| Metric | Fuzzy Controller | Fixed-Time | Improvement |
|--------|-----------------|------------|-------------|
| Avg Waiting Time | 58.7s | 89.3s | **+34.3%** |
| Avg Queue Length | 15.2 vehicles | 24.8 vehicles | **+38.7%** |
| Throughput | 1080 veh/h | 972 veh/h | **+11.1%** |

## 🎨 Web Dashboard

The interactive web dashboard provides:

- **Scenario Selector**: Choose from 9 traffic scenarios
- **Performance Charts**: Comparative visualizations (Chart.js)
- **Metrics Table**: Detailed performance comparison
- **Architecture Diagram**: System overview
- **Fuzzy Rules Explorer**: View rule categories and examples

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

Run tests using pytest:

```bash
poetry run pytest tests/
```

## 📖 Documentation

- **[Design Document](docs/design.md)**: System architecture and design decisions
- **[User Guide](docs/user_guide.md)**: Detailed usage instructions
- **[API Reference](docs/api_reference.md)**: Code documentation

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
