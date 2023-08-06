# API wrapper for the Political ML API

## About Political ML

Political ML is a set of API that can perform multiple NLP related tasks. Currently three things are supported:
1. extracting entities
2. categorising texts
3. extracting meaningful content from a webpage or html

These tasks currently work best for Dutch texts. Political ML is developed by [Wepublic](https://wepublic.nl). It only has a private API available, that's not meant for public use.

### How to use

These clients are available: `NerClient`, `CategoriseClient`, `ArticleExtractionClient`. Below are some examples:

```python
from political_ml import NerClient

client = NerClient(endpoint, token)
texts = [
    {
        "id": 1,
        "text": "Mark Rutte eet wel bitterballen."
    },
    {
        "id": 2,
        "text": "Jesse Klaver eet geen bitterballen."
    }
]
entities = client.ner(texts)

```

```python
from political_ml import CategoriseClient

client = CategoriseClient(endpoint, token)
texts = [
    {
        "id": 1,
        "text": "In Assendelft (gemeente Zaanstad, provincie Noord-Holland) is bij legkippen op een kleinschalige houderij vogelgriep (H5) vastgesteld. Het gaat waarschijnlijk om een hoogpathogene variant van de vogelgriep. Om verspreiding van het virus te voorkomen worden de circa 140 legkippen en 50 loopeenden van de besmette locatie geruimd. De ruiming wordt uitgevoerd door de Nederlandse Voedsel- en Warenautoriteit (NVWA)."
    },
]
categories = client.categorise(texts)
```

```python
from political_ml import ArticleExtractionClient

client = ArticleExtractionClient(endpoint, token)
meaningful_data = client.by_url("https://news.website/article/1")
other_meaningful_data = client.by_html("<html><body><h1>this is a title</h1><p>this is body text</p></body></html>")
```


## For development

### Requirements

- Python 3.8+
- Make

### Setup for development

- Create a virtual env: `python -m virtualenv venv`
- Install development dependencies: `python -m pip install -e ".[dev]"`
- Run `make unit-test` to run unit tests or run `tox` to run unit tests for all support python versions.
- If you have an instance of the API's available, you can run integration tests with `make integration-test`.

New PRs are opened against `develop`.

### Publishing a new version

1. Bump version numbers in [__meta__.py](/src/source_aggregation/__meta__.py)
2. Publish a [new release](https://github.com/wepublic-nl/sas-package/releases/new) and create a git tag equal to the version number set in step 1.

A Github Action workflow takes care of building and publishing to [PyPi](https://pypi.org/project/source-aggregation/#description).

## Contact / maintainers

Jonathan (stakeholderintel@wepublic.nl) is the maintainer of this package.
