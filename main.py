import sys
from utils import load_data, assign_packages, simulate_deliveries, generate_report, save_report

def main():
    # Step 1: Loading data
    filepath = sys.argv[1] if len(sys.argv) > 1 else "base_case.json"
    data = load_data(filepath)

    warehouses = data["warehouses"]
    agents     = data["agents"]
    packages   = data["packages"]

    print(f"Loaded {len(packages)} packages, {len(agents)} agents, {len(warehouses)} warehouses")

    # Step 2: Assiging packages to nearest agents
    assignments = assign_packages(packages, agents, warehouses)

    print("\n--- Assignments ---")
    for agent_id, pkgs in assignments.items():
        pkg_ids = [p["id"] for p in pkgs]
        print(f"  {agent_id} → {pkg_ids}")

    # Step 3: Simulating deliveries
    results = simulate_deliveries(assignments, agents, warehouses)

    print("\n--- Results ---")
    for agent_id, res in results.items():
        print(f"  {agent_id}: {res['packages_delivered']} pkg(s) | distance={res['total_distance']} | efficiency={res['efficiency']}")

    # Step 4: Generating and saving report
    report = generate_report(results)
    save_report(report)

    print(f"\nBest agent: {report['best_agent']}")
    print(f"Total packages delivered: {sum(r['packages_delivered'] for r in results.values())} / {len(packages)}")


if __name__ == "__main__":
    main()