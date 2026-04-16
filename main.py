from bs4 import BeautifulSoup
from pathlib import Path
import re

# import requests

# url = 'https://www.regiobeeld.nl/regiobeelden-IZA/ouderen-met-kwetsbare-gezondheid'
# response = requests.get(url)
# if response.status_code == 200:
#     html = response.text
#     dom = BeautifulSoup(html, 'html.parser')
#     print(dom);
# else:
#     print("Failed to fetch page:", response.status_code)

# Nu hardcoded. TIBCO API gaat uiteindelijk vervanger hiervoor zijn
page = "ouderen-met-kwetsbare-gezondheid"

# Nu hardcoded. TIBCO API gaat uiteindelijk vervanger hiervoor zijn
ids = [
    "IZA_ouderen_lasa_omvangdoelgroep",
    "ouderen_zorgtreden",
    "ouderen_zorgtreden_uitsplitsing",
    "ouderen_seh_nl",
    "ouderen_seh",
    "ouderen_seh_gebruik",
    "ouderen_ongepl_zkh",
    "IZA_prem",
    "IZA_prem_NPS",
    "mantelzorgPotentieel_IZA",
    "IZA_ouderen_lasa_indicatoren",
    "IZA_ouderen_MKVL",
    "IZA_ouderen_profhulp",
]

textual_elements = [
    "p",
    "span",
    "b",
    "i",
    "strong",
    "em",
    "small",
    "mark",
    "del",
    "ins",
    "sub",
    "sup",
    "blockquote",
    "q",
    "pre",
    "code",
    "samp",
    "kbd",
    "var",
    "cite",
    "dfn",
    "abbr",
    "address",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "li",
    "dt",
    "dd",
    "caption",
    "legend",
]

ids_set = set(ids)

with open(f"static/{page}.html", encoding="utf-8") as html:
    dom = BeautifulSoup(html, "html.parser")

for anchor in dom.select("a[data-graph-id]"):
    graph_id = anchor.get("data-graph-id")

    if graph_id not in ids_set:
        continue

    parent_div = anchor.find_parent("div")
    if not parent_div:
        continue

    blocks = []
    for elem in parent_div.find_all(
        ["p", "h1", "h2", "h3", "h4", "h5", "h6", "li", "div"], recursive=True
    ):
        text = elem.get_text(separator=" ", strip=True)
        # Collapse multiple spaces/newlines inside the text
        text = re.sub(r"\s+", " ", text)
        if text:
            if elem.name == "li":
                blocks.append(f"- {text}")
            else:
                blocks.append(text)

    clean_text = "\n\n".join(blocks)

    output_path = Path("output") / f"{graph_id}.txt"
    output_path.write_text(clean_text, encoding="utf-8")
    print(f"Exported text related to: {graph_id}")
