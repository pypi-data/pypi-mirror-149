# Podcast-Scraper

Ce script permet de récupérer les url de téléchargements de podcasts. Vous pouvez dès lors les recupérer avec votre outil favoris; par exemple wget.

Ceci est motivé par le fait que les podcast de france culture sont hebergés par apple et que tout comme les flux RSS ne
permettent de telécharger uniquement quelques épisodes.

Le monde diplomatique fournit aux adhérents des podcasts de certains ses articles lus. Tout comme le précédent, le flux
rss ne permet pas de récuperer l'historique. Podcast-scraper permet d'y remédier, à condition bien sûr d'avoir un abonement.

# Sources Gérées

- france culture
- le monde diplomatique
- c'est tout pour l'instant

# Dependencies

This needs **docker** to run.

# Install

``` bash
pip install podcast-scraper
```

# Usage

```
podcast-scraper --help
Usage: podcast-scraper [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  csv             Download or tag the podcast defined in a csv
  france-culture  Get podcast url for France Culture
  monde-diplo     Get podcast url for Monde Diplo

```

# Exemples

```
podcast-scraper france-culture --url https://www.franceculture.fr/emissions/carbone-14-le-magazine-de-larcheologie > export.csv
podcast-scraper csv --csv-path export.csv --podcast-path /tmp/  --download --tag

USER=email PASSWORD=your-password podcast-scraper monde-diplo
```
