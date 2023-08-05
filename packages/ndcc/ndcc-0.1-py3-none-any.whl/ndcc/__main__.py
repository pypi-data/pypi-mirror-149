from rich.console import Console

import compare


def main():
    console = Console()
    tables = compare.get_tables()
    for table in tables:
        console.print(table)


if __name__ == "__main__":
    main()
