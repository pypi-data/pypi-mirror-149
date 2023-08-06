from typing import Dict


def reduce_dictionary(dictionary: Dict) -> Dict:
    """
    Removes none properties from dictionary
    """
    reduced_dictionary = {k: v for k, v in dictionary.items() if v is not None}
    return reduced_dictionary
