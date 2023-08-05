from typing import Any, List, Callable, Optional


def find(any_list: List[Any], x_filter: Callable) -> Optional[object]:
    """
    Find item in provided list according filter
    @param any_list: List of any values
    @param x_filter: Filter to apply the search
    @return: element that filter return true otherwise None
    """
    for x in any_list:
        if x_filter(x):
            return x
    return None
