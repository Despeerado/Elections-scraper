# Election sscraper

## Popis projektu

Program slouží k extrahování výsledků parlamentních voleb v roce 2017. Odkaz [zde](https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7102).

## Instalace knihoven
Knihovny použité v kódu jsou uloženy v souboru requirements.txt.

Instalace knihoven:
```
pip3 --version
pip3 install -r requirements.txt

```
## Spuštění projektu
Spuštění souboru main.py v rámci přík. řádku vyžaduje 2 argumenty.

```
python main.py <vysledny-soubor> <odkaz-uzemniho-celku>

```

Následně se vám stáhnou výsledky jako soubor s příponou .csv.

## Ukázka projektu

Výsledky hlasování pro okres Olomouc:

1. argument: election_results.csv
2. argument: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7102

spuštění programu:
```
python main.py election_results.csv https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7102

```

průběh programu:
```
Downloading data from the selected url
Scraping elections to election_results.csv
Program finished.
```

částečný výstup:
```
code,location,registered,envelopes,valid,...
552356,Babice,370,256,254,13,0,0,10,...
500526,Bělkovice-Lašťany,1801,1079,1069,...
...
```
