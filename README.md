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

Deze code is nog een concept. De huidige versie van Regiobeeld heeft nog geen anchors met custom attributen gerelateerd aan de grafieken. Daarom maken we nu gebruik van een hardcoded html gerelateerd aan de pagina van [Ouderen met een kwetsbare gezondheid
](https://www.regiobeeld.nl/regiobeelden-IZA/ouderen-met-kwetsbare-gezondheid)

## Libs:

- [BeautifulSoup](https://beautiful-soup-4.readthedocs.io/en/latest/index.html?highlight=find_parent#): Beautiful Soup is een Python-bibliotheek om gegevens uit HTML- en XML-bestanden te halen. Het werkt samen met je favoriete parser om natuurlijke manieren te bieden om door de parseboom te navigeren, te zoeken en deze aan te passen.

## Output example

- **Pagina**: https://www.regiobeeld.nl/regiobeelden-IZA/ouderen-met-kwetsbare-gezondheid
- **Grafiek**: `{#IZA_ouderen_lasa_indicatoren}`

```txt
In 2021/2022 hebben LASA-deelnemers antwoord gegeven op de vragen:

- Hoe zou u over het algemeen uw gezondheid noemen? (990 deelnemers)

- Hoe zou u de kwaliteit van uw leven inschatten? (1.000 deelnemers)

- Bent u, alles bij elkaar genomen, de laatste tijd tevreden over uw leven? (1.000 deelnemers)

Hieronder laten we de resultaten zien van deze drie indicatoren uitgesplitst naar doelgroep zoals weergegeven bovenaan deze pagina. De verschillende indicatoren zijn te selecteren via het keuzemenu boven het figuur.
```
