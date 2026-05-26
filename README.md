# FastBox Delivery System

A logistics simulator for a fictional delivery company.
Simulates one day of operations across warehouses, agents, and packages.

## How to Run

```bash
# Run with default base_case.json
python main.py

# Run with a specific test case
python main.py test_cases/test_case_1.json
```

## Output Files
- `report.json` — delivery summary with best agent
- `top_performer.csv` — detailed route of the best agent

## Features
- Nearest-agent package assignment using Euclidean distance
- Two-leg delivery simulation (agent → warehouse → destination)
- Efficiency scoring per agent
- Random delivery delays
- ASCII route map
- CSV export of top performer