from network.getter import get_wiki_data
from utils.testutils import dump_any_to_file
from praser.bs4 import prase_main_card
import json

def main():
    raw_resp = get_wiki_data()
    dump_any_to_file("json", json.dumps(raw_resp, indent=4))
    html_data = raw_resp["parse"]["text"]["*"]
    dump_any_to_file("html", html_data)
    prase_main_card(html_data)

if __name__ == "__main__":
    main()
