import requests
import re
import sys
import csv
from os import path
from bs4 import BeautifulSoup
from bs4.element import Tag
from dataclasses import dataclass, asdict
from typing import Optional, List, cast
from dataclasses import asdict

GRAPH_PATTERN = re.compile(r"{#([^}]+)}")
TEXT_TAGS = ("p", "ul")


@dataclass
class Graph:
    config_id: Optional[str] = None
    title: Optional[str] = None
    duiding: Optional[str] = None
    html: Optional[str] = None


def ascii_title() -> str:
    return """
▄▄▄▄  ▄▄▄▄▄  ▄▄▄▄ ▄▄  ▄▄▄     ▄▄▄▄ ▄▄▄▄   ▄▄▄  ▄▄   ▄▄ ▄▄    ▄▄▄▄▄ ▄▄▄▄  
██▄█▄ ██▄▄  ██ ▄▄ ██ ██▀██   ██▀▀▀ ██▄█▄ ██▀██ ██ ▄ ██ ██    ██▄▄  ██▄█▄ 
██ ██ ██▄▄▄ ▀███▀ ██ ▀███▀   ▀████ ██ ██ ██▀██  ▀█▀█▀  ██▄▄▄ ██▄▄▄ ██ ██ 
        """


def clean_html(tag: Tag) -> str:
    """
    Verwijdert ongewenste inline tags zoals <span>, <a>, <button>,
    en elementen met role="button", maar behoudt structuur en tekst.
    """
    for unwanted in tag.find_all(["span", "a", "button"]):
        unwanted.unwrap()

    for button_like in tag.find_all(attrs={"role": "button"}):
        button_like.decompose()

    return str(tag)


def main(path: str) -> List[Graph]:
    urls: List[str] = open(path).read().splitlines()
    graphs: List[Graph] = []

    for url in urls:
        res = requests.get(url)
        res.raise_for_status()
        dom = BeautifulSoup(res.text, "html.parser")

        print(f"processing: {url}")

        ids = []

        for text_node in dom.find_all(string=GRAPH_PATTERN):
            for match in GRAPH_PATTERN.finditer(text_node):
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

            blocks_text: List[str] = []
            blocks_html: List[str] = []

            elements = cast(List[Tag], content.find_all(TEXT_TAGS, recursive=True))

            for elem in elements:

                if elem.name == "ul":  # <ul></ul>
                    items_html = []

                    for li in elem.find_all("li", recursive=True):
                        for unwanted in li.find_all(["span", "a"]):
                            unwanted.unwrap()

                        items_html.append(f"<li>{li.decode_contents().strip()}</li>")

                    ul_html = "<ul>" + "".join(items_html) + "</ul>"
                    blocks_html.append(ul_html)

                    text = elem.get_text(separator=" ", strip=True)
                    blocks_text.append(f"- {text}")

                else:  # <p></p>
                    cleaned_html = clean_html(elem)
                    blocks_html.append(cleaned_html)

                    text = elem.get_text(separator=" ", strip=True)
                    blocks_text.append(text)

            formatted_text = "\n".join(blocks_text)
            formatted_html = "\n".join(blocks_html)

            graphs.append(
                Graph(
                    config_id=graph_id,
                    title=title,
                    duiding=formatted_text,
                    html=formatted_html,
                )
            )

    return graphs


if __name__ == "__main__":
    urls = sys.argv[1]
    print(ascii_title())

    if path.exists(urls) and path.getsize(urls) == 0:
        print("Input file is empty. Exiting.")
        sys.exit(1)

    resp = main(urls)

    if not resp:
        print("No data returned. Nothing to write.")
        sys.exit(0)

    with open("output/config.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=asdict(resp[0]).keys(), delimiter=";")
        writer.writeheader()

        for graph in resp:
            writer.writerow(asdict(graph))
