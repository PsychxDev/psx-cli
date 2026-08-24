from psx.utils.display import header, sep

def run(commands) :
    length = header("Commands")

    for name, data in commands.items() :
        print(f"{name:10}: {data['description']}")

    sep(length)