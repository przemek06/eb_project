# EGFR bioinformatics pipeline — track c

Pipeline for retrieving and analyzing EGFR (P00533) data from uniprot and ncbi (gene + clinvar).

## Setup

```
pip install -r requirements.txt
```

## Usage

Run in order from the project root:

```
python src/microstart.py
python src/stage_1.py
python src/stage_2.py
```

All api responses are cached in `cache/`. Next runs use cached data.
