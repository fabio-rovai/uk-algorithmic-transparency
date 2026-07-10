# UK Algorithmic Transparency Corpus

Every published record under the UK's Algorithmic Transparency Recording
Standard (ATRS), structured as an open corpus: which public bodies have
disclosed which algorithmic and AI tools, and when.

| | |
|---|---|
| ATRS records | **136** |
| Distinct publishing bodies | **73** |
| Source | GOV.UK ATRS records |
| Licence | Open Government Licence v3.0 |

## Why

The ATRS is the UK government's standard for publishing how the public sector
uses algorithmic tools in decisions that affect people. It is the closest thing
to a public register of government AI, and it is growing. But it is published as
a set of individual records, not as a dataset you can analyse. This assembles
the full set into one structured corpus: publishing body, tool name, description
and date per record.

## The picture

136 records span **73 distinct public bodies**, led by DSIT, DWP, the Money and
Pensions Service, DfE, DESNZ and DBT. The corpus is the base for asking the
questions the individual records cannot: which parts of government are most
transparent about their AI, what kinds of tools recur, and how disclosure is
growing over time.

## Files

- `data/atrs_records.json` / `.csv` — structured records
- `scripts/harvest.py` — reproducible harvest from the GOV.UK Search API

## Reproduce

```bash
python3 scripts/harvest.py
```

Contains public sector information licensed under the Open Government Licence
v3.0. Independent, self-initiated open research by
[Tesseract Academy](https://gov.tesseract.academy).
