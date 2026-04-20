<div align="center">
  <a href="#">
    <img src="images/logo.png" alt="Logo" width="120" height="120" style="border-radius: 1.75rem;">
  </a>

  <h1 align="center">Regio Crawler</h1>

  <p align="center">
    Python crawlertje voor Regiobeeld grafiekjes en tekstjes
  </p>
</div>

## Notitie:

Deze code (`new.py`) is nog een concept. De huidige versie van Regiobeeld heeft nog geen anchors met custom attributen gerelateerd aan de grafieken. Om het alsnog te kunnen testen hebben we in Regiobeeld een [concept pagina](https://www.regiobeeld.nl/hefys5j47zs1n0cwy866d25p31cbgzvz268dnqk1id7mvzo8bt) aangemaakt om de functionaliteit te testen.

## Libs:

- [BeautifulSoup](https://beautiful-soup-4.readthedocs.io/en/latest/index.html?highlight=find_parent#): Beautiful Soup is een Python-bibliotheek om gegevens uit HTML- en XML-bestanden te halen. Het werkt samen met je favoriete parser om natuurlijke manieren te bieden om door de parseboom te navigeren, te zoeken en deze aan te passen.

## Configuratie:

Als parameter geef je nu het paad naar een tekst bestand met daarin alle urls.
Voorbeeld:

```sh
python new.py /Users/myname/documents/pages.txt
```

Voorbeeld van `pages.txt`:

```txt
https://www.regiobeeld.nl/onderwerpen/zorggebruik
https://www.regiobeeld.nl/onderwerpen/zorgaanbod-en-arbeidsmarkt
https://www.regiobeeld.nl/onderwerpen/gezondheid-en-leefstijl
...
...
```
