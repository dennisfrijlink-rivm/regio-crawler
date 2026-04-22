import requests
import re
import sys
import csv
from bs4 import BeautifulSoup
from bs4.element import Tag
from dataclasses import dataclass, asdict
from typing import Optional, List, cast
from dataclasses import asdict


GRAPH_PATTERN = re.compile(r"{#([^}]+)}")
TEXT_TAGS = ("p", "li")


@dataclass
class Graph:
    config_id: Optional[str] = None
    title: Optional[str] = None
    duiding: Optional[str] = None


def main(path: str) -> List[Graph]:
    urls: List[str] = open(path).read().splitlines()
    graphs: List[Graph] = []

    for url in urls:
        res: requests.Response = requests.get(url)
        res.raise_for_status()
        dom = BeautifulSoup(res.text, "html.parser")
        ids = []

        for text_node in dom.find_all(string=GRAPH_PATTERN):
            for match in GRAPH_PATTERN.finditer(text_node):
                # match.group(0) = volledige match van de regex r"{#([^}]+)}"
                #   bv: "{#abc123}"
                #
                # match.group(1) = eerste capture group uit de regex.
                # Een capture group is een gedeelte tussen haakjes. In dit geval dus alles behalve de '{', '#' en '}'
                #   alles binnen de haakjes ( ... )
                #   in dit geval: de ID zonder "{#" en "}"
                #   bv: "abc123"
                graph_id = match.group(1)
                ids.append(graph_id)

        for graph_id in ids:
            anchor = dom.find(id=graph_id)

            if not isinstance(anchor, Tag):
                continue

            parent: Optional[Tag] = anchor.find_parent("div", class_="card")
            if parent is None:
                continue

            title_tag = parent.find("h3", class_="card-header")
            if not isinstance(title_tag, Tag):
                continue

            title: str = title_tag.get_text(strip=True)

            content = parent.find("div", class_="card-content")
            if not isinstance(content, Tag):
                continue

            blocks = []
            elements = cast(List[Tag], content.find_all(TEXT_TAGS, recursive=True))

            for elem in elements:
                text = elem.get_text(separator=" ", strip=True)
                if not text:
                    continue

                text = re.sub(r"\s+", " ", text)
                if elem.name == "li":
                    blocks.append(f"- {text}")
                else:
                    blocks.append(text)

            formatted_text = "\\n".join(blocks)
            graphs.append(
                Graph(config_id=graph_id, title=title, duiding=formatted_text)
            )

    return graphs


if __name__ == "__main__":
    urls = sys.argv[1]
    resp = main(urls)
    with open("output/config.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=asdict(resp[0]).keys(), delimiter=";")
        writer.writeheader()

        for graph in resp:
            writer.writerow(asdict(graph))
