from prompt_toolkit.shortcuts import checkboxlist_dialog, input_dialog

from ndcc import validate


def get_selected_charts() -> list[str]:
    selected_charts: list[str] = checkboxlist_dialog(
        text="Select value charts to use",
        values=[("Jimmy Johnson", "Jimmy Johnson"),
                ("Rich Hill", "Rich Hill"),
                ("Fitzgerald/Spielberger", "Fitzgerald/Spielberger"),
                ("Kevin Meers", "Kevin Meers"),
                ("PFF", "PFF"),
                ("Michael Lopez", "Michael Lopez")]
    ).run()
    return selected_charts


def get_collection_count() -> int:
    selected_number_of_pick_collections: int = int(input_dialog(
        text="Enter the number of pick collections to compare: ",
        validator=validate.get_collection_count_validator()
    ).run())
    return selected_number_of_pick_collections


def get_collection_name(collection_number: int) -> str:
    collection_name: str = input_dialog(
        text=f"Enter a name/identifier for collection {collection_number}, e.g. 'Vikings receive': ",
        validator=validate.get_collection_name_validator()
    ).run()
    return collection_name


def get_picks(collection_number: int) -> list[int]:
    picks_raw: list[str] = input_dialog(
        text=f"Enter the picks in collection {collection_number}, separated by spaces: ",
        validator=validate.get_pick_validator()
    ).run().split()
    picks: list[int] = [int(i) for i in picks_raw]
    return picks
