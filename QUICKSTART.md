# 🚀 Quick Start Guide

Get up and running with the Fuzzy Traffic Light Control System in 5 minutes!

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/kinhluan/fuzzy-traffic-system.git
cd fuzzy-traffic-system
```

2. **Install dependencies with Poetry:**
```bash
poetry install
```

3. **Activate the virtual environment:**
```bash
poetry shell
```

## Quick Tests

### Test All Components
Run the comprehensive system test:
```bash
python test_system.py
```

Expected output:
```
ALL TESTS PASSED! ✓
✓ Created 8 input variables and 1 output variable
✓ Created 112 fuzzy rules across 4 directions
✓ Fuzzy controller working
✓ Traffic simulator working
✓ Fixed-time controller working
✓ Loaded 9 traffic scenarios
```

### Test Individual Components

**Membership Functions:**
```bash
python src/fuzzy_controller/membership_functions.py
```
Generates `membership_functions.png` visualization.

**Fuzzy Rules:**
```bash
python src/fuzzy_controller/fuzzy_rules.py
```
Shows summary of all 112 rules.

**Traffic Scenarios:**
```bash
python src/simulation/scenarios.py
```
Lists all 9 predefined scenarios.

## Running Simulations

### Simple 2-Minute Demo
```bash
python examples/simple_comparison.py
```

This runs a quick comparison between Fuzzy and Fixed-Time controllers.

### Full Comparison (All Scenarios)
```bash
python src/main.py
```

This will:
- Run simulations for all 9 scenarios
- Compare Fuzzy vs Fixed-Time performance
- Generate `web/data/comparison_results.json`
- Display comprehensive metrics

Expected runtime: 5-10 minutes

## Viewing Results

### Web Dashboard

1. **Option A: Open locally**
   - Open `web/index.html` in your browser
   - Note: Charts will use mock data until you run `python src/main.py`

2. **Option B: Deploy to GitHub Pages**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```
   - Go to repo **Settings** → **Pages**
   - Source: `main` branch, `/web` folder
   - Save and wait for deployment
   - Access at: `https://kinhluan.github.io/fuzzy-traffic-system/`

### Command Line Results

After running `python src/main.py`, you'll see output like:

```
======================================================================
Scenario: Normal Traffic
======================================================================
FUZZY CONTROLLER RESULTS:
  Avg Waiting Time:     45.2s
  Avg Queue Length:     8.5
  Throughput:           576 veh/h
  Fairness Index:       0.892

FIXED-TIME CONTROLLER RESULTS:
  Avg Waiting Time:     62.4s
  Avg Queue Length:     12.3
  Throughput:           528 veh/h
  Fairness Index:       0.834

IMPROVEMENT (Fuzzy vs Fixed):
  Waiting Time:    +27.6%
  Queue Length:    +30.9%
  Throughput:      +9.1%
```

## Project Structure

```
fuzzy-traffic-system/
├── src/
│   ├── fuzzy_controller/    # Fuzzy logic implementation
│   ├── simulation/           # Traffic simulation
│   └── utils/                # Metrics and utilities
├── web/                      # Web dashboard (GitHub Pages)
├── examples/                 # Example scripts
├── test_system.py            # Quick system test
└── README.md                 # Full documentation
```

## Next Steps

1. **Experiment with Scenarios:**
   - Edit `src/simulation/scenarios.py` to create custom scenarios
   - Modify arrival rates to simulate different traffic patterns

2. **Tune Fuzzy Rules:**
   - Edit `src/fuzzy_controller/fuzzy_rules.py` to adjust rules
   - Modify membership functions in `membership_functions.py`

3. **Analyze Results:**
   - View detailed metrics in the web dashboard
   - Export data from `web/data/comparison_results.json`

4. **Contribute:**
   - Add SUMO integration (optional advanced feature)
   - Implement additional scenarios
   - Improve web visualizations

## Troubleshooting

### Import Errors
If you see `ModuleNotFoundError`:
```bash
poetry install  # Reinstall dependencies
poetry shell    # Make sure you're in the virtual environment
```

### Missing scipy/networkx
These should be installed automatically, but if not:
```bash
poetry add scipy networkx
```

### Web Dashboard Shows Mock Data
Run the simulation to generate real data:
```bash
python src/main.py
```

### Port Already in Use (if using local server)
```bash
# Use a different port
python -m http.server 8001 --directory web
```

## Help & Support

- **Full Documentation:** See `README.md`
- **Issues:** Open an issue on GitHub
- **Examples:** Check the `examples/` directory

---

**Ready to optimize traffic! 🚦**
