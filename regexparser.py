import re

import requests


def _get_items_list() -> requests.Response:
    """ Sends a GET request to TBOIR wiki and returns the response. """
    return requests.get("http://bindingofisaacrebirth.fandom.com/wiki/Items?action=render&format=json")


def dict_items() -> dict:
    """ Returns a dict of {link_name: human_name} pairs of items. """
    items_dict = dict()
    pattern = re.compile(
        r"value=\"(.+)\">(\<.*?\>\s)?<a\shref=\"https://bindingofisaacrebirth\.fandom\.com/wiki/(.+)\"\stitle=\".+\">(.+)</a"
    )
    response = _get_items_list()
    for line in response.iter_lines():
        match = re.search(pattern, str(line))
        if match:
            item_tuple = match.group(1, 2, 3, 4)
            if item_tuple[3] == "&lt;3":
                items_dict.update({"<3": item_tuple[2]})
            else:
                items_dict.update({item_tuple[3].replace("\\'", "'"): item_tuple[2]})
    return items_dict


if __name__ == "__main__":
    items_dct = dict_items()
    for k, v in items_dct.items():
        print(k, ": ", v, sep="")
