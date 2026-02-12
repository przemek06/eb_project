# reproducibility card — final project

run date: 2026-02-12
track: c — egfr
authors: Przemysław Świat, Paweł Mańczak, Adam Cherek

## environment

- python: 3.x
- packages: requests

## data sources and versions

- uniprot rest: https://rest.uniprot.org/uniprotkb/P00533.json — fetched 2026-02-12
- ncbi e-utilities (gene): esummary, db=gene, id=1956 — fetched 2026-02-12
- ncbi e-utilities (protein fasta): efetch, db=protein, id=NP_005219.2 — fetched 2026-02-12
- ncbi e-utilities (mrna fasta): efetch, db=nucleotide, id=NM_005228.4 — fetched 2026-02-12
- ncbi e-utilities (clinvar search): esearch, db=clinvar, term=EGFR[gene], retmax=500 — fetched 2026-02-12
- ncbi e-utilities (clinvar details): esummary, db=clinvar, 500 variant ids in batches of 100 — fetched 2026-02-12

## key queries

- uniprot: GET https://rest.uniprot.org/uniprotkb/P00533.json
- ncbi gene: GET esummary.fcgi?db=gene&id=1956&retmode=json
- ncbi protein fasta: GET efetch.fcgi?db=protein&id=NP_005219.2&rettype=fasta&retmode=text
- ncbi mrna fasta: GET efetch.fcgi?db=nucleotide&id=NM_005228.4&rettype=fasta&retmode=text
- clinvar search: GET esearch.fcgi?db=clinvar&term=EGFR[gene]&retmax=500&retmode=json
- clinvar details: GET esummary.fcgi?db=clinvar&id=[batch of ids]&retmode=json

## cache

- location: cache/
- offline mode: yes

## ai (if used)

- used for: code suggestions, text formatting, help with interpretation of biological data
