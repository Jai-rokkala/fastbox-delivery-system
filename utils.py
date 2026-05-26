import json
import math
import random
import csv


def load_data(filepath):
    with open(filepath, "r") as f:
        raw = json.loads(f.read())

    warehouses = {}
    if isinstance(raw["warehouses"], list):
        for w in raw["warehouses"]:
            warehouses[w["id"]] = w["location"]
    else:
        warehouses = raw["warehouses"]


    agents = {}
    if isinstance(raw["agents"], list):
        for a in raw["agents"]:
            agents[a["id"]] = a["location"]
    else:
        agents = raw["agents"]


    packages = []
    for p in raw["packages"]:
        packages.append({
            "id": p["id"],
            "warehouse": p.get("warehouse") or p.get("warehouse_id"),
            "destination": p["destination"]
        })

    return {"warehouses": warehouses, "agents": agents, "packages": packages}


def euclidean(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def assign_packages(packages, agents, warehouses):

     # Keeping track of where each delivery agent is right now.
    agent_positions = {aid: list(pos) for aid, pos in agents.items()}

    # Creating an empty delivery list for every agent.
    assignments = {aid: [] for aid in agents}

    for pkg in packages:

        # Get the coordinates of the warehouse this package belongs to.
        warehouse_pos = warehouses[pkg["warehouse"]]

        # Find the nearest agent to this warehouse.
        nearest = min(agents, key=lambda aid: euclidean(agent_positions[aid], warehouse_pos))
        assignments[nearest].append(pkg)

        # After delivering the package, the agent's new position
        # becomes the package destination.
        agent_positions[nearest] = pkg["destination"]

    return assignments


def simulate_deliveries(assignments, agents, warehouses):
    results = {}

    for agent_id, pkgs in assignments.items():
        # Each agent begins from their original starting location.
        current_pos = list(agents[agent_id])

        # Tracking the total distance traveled by this agent.
        total_distance = 0.0

        # Store details about every completed delivery.
        delivered = []

        for pkg in pkgs:
            warehouse_pos = warehouses[pkg["warehouse"]]
            destination = pkg["destination"]

            # First, the agent travels from their current location
            # to the package's warehouse.
            leg1 = euclidean(current_pos, warehouse_pos)

            # Then, the package is delivered from the warehouse
            # to its final destination.
            leg2 = euclidean(warehouse_pos, destination)

            # Add both parts of the trip to the running total.
            total_distance += leg1 + leg2

            # Save a summary of this delivery.
            delay = random.randint(0, 15)
            delivered.append({
            "package_id": pkg["id"],
            "warehouse": pkg["warehouse"],
            "destination": destination,
            "distance": round(leg1 + leg2, 2),
            "delay_minutes": delay
        })

            # After delivery, the agent's new location
            # becomes the destination point.
            current_pos = destination

        # Count how many packages this agent handled.
        packages_delivered = len(delivered)

        # Efficiency is measured as average distance travelled
        # per package delivered.
        efficiency = round(total_distance / packages_delivered, 2) if packages_delivered else 0.0

        # Store the final performance summary for this agent.
        results[agent_id] = {
            "packages_delivered": packages_delivered,
            "total_distance": round(total_distance, 2),
            "efficiency": efficiency,
            "deliveries": delivered
        }

    return results


def generate_report(results):
    report = {}

    for agent_id, data in results.items():
        report[agent_id] = {
            "packages_delivered": data["packages_delivered"],
            "total_distance": data["total_distance"],
            "efficiency": data["efficiency"]
        }

    active = {aid: v for aid, v in report.items() if v["packages_delivered"] > 0}

     # Best agent = lowest efficiency score (least distance per package)
    best_agent = min(active, key=lambda aid: active[aid]["efficiency"])
    report["best_agent"] = best_agent

    return report


def save_report(report, filepath="report.json"):
    with open(filepath, "w") as f:
        json.dump(report, f, indent=2)
    print(f"Report saved to {filepath}")

#Bonus = Export top performer details to CSV
def export_top_performer(report, results, filepath="top_performer.csv"):
    best = report["best_agent"]
    deliveries = results[best]["deliveries"]

    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Agent", "Package", "Warehouse", "Destination", "Distance", "Delay (min)"])
        for d in deliveries:
            writer.writerow([
                best,
                d["package_id"],
                d["warehouse"],
                d["destination"],
                d["distance"],
                d["delay_minutes"]
            ])
    print(f"Top performer CSV saved to {filepath}")

# Bonus = Simple ASCII map visualization of the scenario
def ascii_map(warehouses, agents, packages, grid_size=12, scale=10):
    grid = [["." for _ in range(grid_size + 1)] for _ in range(grid_size + 1)]

    def place(pos, symbol):
        gx = min(int(pos[0] / scale), grid_size)
        gy = min(int(pos[1] / scale), grid_size)
        grid[grid_size - gy][gx] = symbol

    for pos in warehouses.values():
        place(pos, "W")
    for pos in agents.values():
        place(pos, "A")
    for pkg in packages:
        place(pkg["destination"], "D")

    print("\n[ ASCII Map ]")
    print("  +" + "-" * (grid_size * 2 + 1) + "+")
    for row in grid:
        print("  | " + " ".join(row) + " |")
    print("  +" + "-" * (grid_size * 2 + 1) + "+")
    print("  W=Warehouse  A=Agent  D=Destination\n")