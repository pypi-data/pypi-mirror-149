from prompt_toolkit.validation import Validator


def _validate_collection_count(text: str) -> bool:
    return text.isdigit() and 1 < int(text) < 32


def _validate_picks(text: str) -> bool:
    for pick in text.split():
        if not pick.isdigit() or not 0 < int(pick) < 271:
            return False
    return True


def _validate_collection_name(text: str) -> bool:
    return bool(text)


def get_collection_count_validator() -> Validator:
    collection_count_validator: Validator = Validator.from_callable(
        _validate_collection_count,
        "Number of collections must be between 2 and 32",
        move_cursor_to_end=True
    )
    return collection_count_validator


def get_pick_validator() -> Validator:
    pick_validator: Validator = Validator.from_callable(
        _validate_picks,
        "One or more picks is invalid. Picks must be ints between 1 and 270.",
        move_cursor_to_end=True
    )
    return pick_validator


def get_collection_name_validator() -> Validator:
    collection_name_validator: Validator = Validator.from_callable(
        _validate_collection_name,
        "Collection name/identifier cannot be empty",
        move_cursor_to_end=True
    )
    return collection_name_validator
