import requests
import re
import json
import sys
from bs4 import BeautifulSoup
from bs4.element import Tag
from dataclasses import dataclass
from typing import Optional, List


GRAPH_PATTERN = re.compile(r"{#([^}]+)}")
TEXT_TAGS = ("p", "li")


# TODO:  config_id;title;subtitle;duiding;credits_id;update_datum;group;order
@dataclass
class Graph:
    description: Optional[str] = None
    title: Optional[str] = None


def main(path: str):
    urls = open(path).read().splitlines()
    graphs = []

    for url in urls:
        res = requests.get(url)
        res.raise_for_status()
        dom = BeautifulSoup(res.text, "html.parser")
        ids = []

        for text_node in dom.find_all(string=GRAPH_PATTERN):
            match = GRAPH_PATTERN.search(text_node)
            if not match:
                continue

            token = match.group(0)
            html_id = match.group(1)
            ids.append(html_id)

        for id in ids:
            anchor = dom.find(id=id)

            if not anchor:
                continue

            parent = anchor.find_parent("div", class_="card")

            if not parent:
                continue

            title = parent.find("h3", class_="card-header")

            if not title:
                continue

            content = parent.find("div", class_="card-content")

            if not isinstance(content, Tag):
                continue

            blocks = []

            for elem in content.find_all(TEXT_TAGS, recursive=True):
                text = elem.get_text(separator=" ", strip=True)
                if not text:
                    continue

                text = re.sub(r"\s+", " ", text)
                if elem.name == "li":
                    blocks.append(f"- {text}")
                else:
                    blocks.append(text)

            formatted_text = "\n\n".join(blocks)
            graphs.append(Graph(formatted_text, title.text))

        print(graphs)


if __name__ == "__main__":
    txtSource = sys.argv[1]
    main(txtSource)
