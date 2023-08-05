import pandas

from rich.table import Table

import input


def get_tables() -> list[Table]:
    selected_charts: list[str] = input.get_selected_charts()
    index_and_selected_charts: list[str] = ["Pick #"] + selected_charts
    charts: pandas.DataFrame = pandas.read_csv("../charts.csv", usecols=index_and_selected_charts, index_col=0)

    collection_count: int = input.get_collection_count()

    collection_rows: list[tuple] = []

    tables: list[Table] = []

    for collection_number in range(1, collection_count + 1):

        collection_name: str = input.get_collection_name(collection_number)
        picks: list[int] = input.get_picks(collection_number)

        filtered_df: pandas.DataFrame = charts[charts.index.isin(picks)]
        collection_row: tuple = (collection_name,)
        for chart in filtered_df.columns:
            collection_row += (str(filtered_df[chart].sum()),)

        collection_rows.append(collection_row)
        tables.append(_get_pick_table(collection_name, filtered_df))

    comparison_table: Table = Table(title="Comparison")
    comparison_table.add_column("Collection")
    for chart in charts.columns:
        comparison_table.add_column(chart)
    for row in collection_rows:
        comparison_table.add_row(*row)

    tables.insert(0, comparison_table)

    return tables


def _get_pick_table(collection_name: str, filtered_df: pandas.DataFrame) -> Table:
    
    pick_table: Table = Table(title=collection_name)
    pick_table.add_column("Pick", style="cyan")

    pick_rows: list[tuple] = []

    for tup in filtered_df.itertuples(name=None):
        new_tup = tuple()
        for i in tup:
            new_tup += (str(i),)
        pick_rows.append(new_tup)

    for chart in filtered_df.columns:
        pick_table.add_column(chart)

    for row in pick_rows:
        pick_table.add_row(*row)

    return pick_table
