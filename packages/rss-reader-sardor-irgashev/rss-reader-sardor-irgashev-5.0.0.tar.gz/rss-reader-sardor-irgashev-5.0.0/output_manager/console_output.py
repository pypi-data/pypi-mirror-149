"""The module provides implementation for outputting news to console"""

import json
from typing import List


class Colors:
    """Represents output colors"""

    BLACK_ON_CYAN = ""
    BLACK_ON_YELLOW = ""
    PURPLE = ""
    GREEN = ""
    OKCYAN = ""

    END = ""
    BOLD = ""

    def enable_colors(self) -> None:
        """Enables colorization

        Returns:
            None
        """
        self.BLACK_ON_CYAN = '\033[37;44m'
        self.BLACK_ON_YELLOW = '\033[30;43m'
        self.PURPLE = '\033[35m'
        self.GREEN = '\033[32m'
        self.OKCYAN = '\033[96m'

        self.END = '\033[0m'
        self.BOLD = '\033[1m'


def to_json(content: List[tuple]) -> str:
    """Converts list containing news items into JSON string

    Args:
        content: List containing the news items

    Returns:
        JSON formatted string of serialized (converted) objects
    """
    json_list = []
    for item in content:
        json_item = {
            'Feed Title': item[1],
            'Feed Source': item[0],
            'News Item': {
                'News Title': item[2],
                'Publication Date': item[3],
                'Description': item[4],
                'Link': item[5],
                'Image Link': item[6]
            }
        }
        json_list.append(json_item)
    return json.dumps(json_list, indent=4)


def to_console(content: List[tuple], colorize: bool = False) -> None:
    """Outputs the contents of the parsed feed-containing XML

    Args:
        content: List containing the news items
        colorize: Colorization option

    Returns:
        None
    """
    colors = Colors()
    if colorize:
        colors.enable_colors()

    for item in content:
        print(f"\n{colors.OKCYAN}{colors.BOLD}Feed Title: {item[1]}{colors.END}\n")
        print(f"{colors.GREEN}{colors.BOLD}News Title: {item[2]}{colors.END}")
        print(f"{colors.BLACK_ON_YELLOW}Date Published: {item[3]}{colors.END}")
        print(f"{colors.PURPLE}Description: {item[4]}{colors.END}")
        print(f"{colors.BLACK_ON_CYAN}Link:{colors.END} {item[5]}")
        print(f"{colors.BLACK_ON_CYAN}Image:{colors.END} {item[6]}")
        print('\n====================================================================================\n')
