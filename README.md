<div align="center">
  <a href="#">
    <img src="images/logo2.png" alt="Logo" height="120" style="border-radius: 1.75rem;">
  </a>
  <p align="center">
    Python crawlertje voor Regiobeeld grafiekjes en tekstjes
  </p>
</div>

## 📦 Libs:

| Library                            | Doel                                                   |
| ---------------------------------- | ------------------------------------------------------ |
| `requests`                         | HTTP-verzoeken uitvoeren naar websites en API's        |
| `re`                               | Werken met reguliere expressies voor patroonherkenning |
| `sys`                              | Toegang tot systeem- en runtime-informatie             |
| `csv`                              | Lezen en schrijven van CSV-bestanden                   |
| `os.path`                          | Bestands- en padbeheer                                 |
| `beautifulsoup4` (`BeautifulSoup`) | HTML/XML parser voor web scraping                      |
| `dataclasses`                      | Eenvoudig definiëren van data-objecten                 |
| `typing`                           | Type hints voor betere codekwaliteit                   |
| `copy` (`deepcopy`)                | Diepe kopieën van objecten maken                       |

## 🔧 Configuratie:

Als parameter geef je nu het pad naar een tekst bestand met daarin alle urls.
Voorbeeld:

```sh
python main.py /Users/myname/documents/pages.txt /Users/myname/documents/output.csv
```

Voorbeeld van `pages.txt`:

```txt
https://www.regiobeeld.nl/onderwerpen/zorggebruik
https://www.regiobeeld.nl/onderwerpen/zorgaanbod-en-arbeidsmarkt
https://www.regiobeeld.nl/onderwerpen/gezondheid-en-leefstijl
...
...
```
