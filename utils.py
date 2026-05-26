import json
import math

def load_data(filepath):
    with open(filepath, "r") as f:
        raw = json.loads(f.read())

    warehouse = {}
        for w in raw["warehouse"]:
            warehouse[w["id"]] = w["location"]

    agents = {}
        for a in raw["agents"]:
            agents[a["id"]] = a["location"]

    packages = []
        for p in raw["packages"]:
            packages.append({
                "id" = p["id"]
                "warehouse" = p["warehouse_id"]
                "destination": p["destination"]
            })
    return {"warehouses": warehouses, "agents": agents, "packages": packages}

def euclidean(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def assign_packages(packages, agents, warehouses):
    # Keep track of where each delivery agent is right now.
    # Initially, everyone starts at their assigned starting location.
    agent_positions = {aid: list(pos) for aid, pos in agents.items()}
    
    # Creating an empty delivery list for every agent.
    assignments = {aid: [] for aid in agents}

    for pkg in packages:
        # Get the coordinates of the warehouse this package belongs to.
        warehouse_pos = warehouses[pkg["warehouse"]]

        # Picking the agent who is currently closest to the warehouse.
        nearest = min(
            agents,
            key=lambda aid: euclidean(agent_positions[aid], warehouse_pos)
        )

        # Assigning the package to the selected agent.
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
            delivered.append({
                "package_id": pkg["id"],
                "warehouse": pkg["warehouse"],
                "destination": destination,
                "distance": round(leg1 + leg2, 2)
            })

            # After delivery, the agent's new location
            # becomes the destination point.
            current_pos = destination

        # Count how many packages this agent handled.
        packages_delivered = len(delivered)

        # Efficiency is measured as average distance travelled
        # per package delivered.
        efficiency = (
            round(total_distance / packages_delivered, 2)
            if packages_delivered else 0.0
        )

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

    # Best agent = lowest efficiency score (least distance per package)
    best_agent = min(report, key=lambda aid: report[aid]["efficiency"])
    report["best_agent"] = best_agent

    return report


def save_report(report, filepath="report.json"):
    with open(filepath, "w") as f:
        json.dump(report, f, indent=2)
    print(f"Report saved to {filepath}")