from psx.utils.display import header, sep


def run(commands):
    length = header("Commands")

    print("PSX CLI")
    print("Command overview")
    print()

    preferred_order = ["System", "Network", "Utility", "General"]
    grouped = {}

    for name, data in commands.items():
        group = data.get("group", "General")
        grouped.setdefault(group, [])
        grouped[group].append((name, data.get("description", "No description.")))

    group_names = []
    for group_name in preferred_order:
        if group_name in grouped:
            group_names.append(group_name)

    for group_name in sorted(grouped):
        if group_name not in preferred_order:
            group_names.append(group_name)

    for index, group_name in enumerate(group_names):
        print(f"[{group_name}]")
        for name, description in grouped[group_name]:
            print(f"  {name:<12} {description}")

        if index != len(group_names) - 1:
            print()

    sep(length)