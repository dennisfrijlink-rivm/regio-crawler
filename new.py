import requests
import re
import json
import sys
from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import Optional, List


GRAPH_PATTERN = re.compile(r"{#([^}]+)}")
TEXT_TAGS = ("p", "h1", "h2", "h3", "h4", "h5", "h6", "li", "div")


@dataclass
class Graph:
    token: str
    html_id: str
    description: Optional[str] = None


def getGraphs(dom: BeautifulSoup) -> List[Graph]:
    graphs = []

    for text_node in dom.find_all(string=GRAPH_PATTERN):
        match = GRAPH_PATTERN.search(text_node)
        if match:
            token = match.group(0)
            html_id = match.group(1)
            graphs.append(Graph(token, html_id))

    return graphs


def getText(parent) -> str:
    blocks = []

    for elem in parent.find_all(TEXT_TAGS, recursive=True):
        text = elem.get_text(separator=" ", strip=True)
        if not text:
            continue

        text = re.sub(r"\s+", " ", text)

        if elem.name == "li":
            blocks.append(f"- {text}")
        else:
            blocks.append(text)

    return " ".join(blocks)


def addText(dom: BeautifulSoup, graphs: List[Graph]) -> List[Graph]:
    for graph in graphs:
        anchor = dom.find(id=graph.html_id)
        if not anchor:
            continue

        parent = anchor.find_parent("div")
        if not parent:
            continue

        graph.description = getText(parent)

    return graphs


def findGraphs(url: str) -> List[Graph]:
    res = requests.get(url)
    res.raise_for_status()

    dom = BeautifulSoup(res.text, "html.parser")

    graphs = getGraphs(dom)
    graphs = addText(dom, graphs)

    return graphs


def getUrls(path: str):
    with open(path, "r") as f:
        urls = f.read().splitlines()

    return urls


def exportData(url: str):
    graphs = findGraphs(url)
    for g in graphs:
        if g.description:
            print(
                json.dumps(
                    {"grafiek": g.html_id, "description": g.description},
                    ensure_ascii=False,
                    indent=2,
                )
            )
            print()


def main(path: str):
    urls = getUrls(path)
    for url in urls:
        exportData(url)


if __name__ == "__main__":
    txtSource = sys.argv[1]
    main(txtSource)
