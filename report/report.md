# EGFR Bioinformatics Pipeline Report

Track C - EGFR (Epidermal Growth Factor Receptor)
UniProt accession: P00533 | NCBI Gene ID: 1956

## Introduction

This report documents the results of a bioinformatics pipeline built for Track C. The focus is the Epidermal Growth Factor Receptor, EGFR.
EGFR (UniProt P00533, NCBI Gene 1956) is located on chromosome 7p11.2 and encodes a 1210-amino acid transmembrane protein that binds EGF-family ligands to activate downstream signaling cascades including RAS-RAF-MEK-ERK and PI3K-AKT.
Somatic variants in the EGFR kinase domain drive non small cell lung cancer. Tyrosine kinase inhibitors target common driver variants, for example erlotinib, gefitinib, and osimertinib.
The pipeline retrieves data from two API sources (UniProt REST and NCBI E-utilities including ClinVar), maps identifiers across databases, and examines clinical variant classifications and their conflicts.
The goal is to demonstrate reproducible, API-first data retrieval with caching, provenance tracking, and critical assessment of data quality.
Data was retrieved programmatically and cached for offline reproducibility.

## Methods

The pipeline consists of three Python scripts:

- `src/microstart.py` - Verifies API connectivity for UniProt REST, NCBI Gene ESearch, and ClinVar ESearch.
- `src/stage_1.py` - Fetches UniProt record for P00533, extracts protein profile fields, fetches NCBI Gene record (ESummary, Gene ID 1956), retrieves protein (NP_005219.2) and mRNA (NM_005228.4) FASTA sequences via NCBI EFetch, and performs sequence length sanity check.
- `src/stage_2.py` - Searches ClinVar for EGFR variants (ESearch, term "EGFR[gene]", retmax 500), fetches variant details in batches (ESummary), selects 5 representative variants, and outputs CSV.

All API responses are cached in `cache/` as JSON. The pipeline can run offline from cache.
NCBI requests include a 0.34s sleep between calls to respect rate limits.
UniProt REST endpoint: `https://rest.uniprot.org/uniprotkb/P00533.json`.
NCBI E-utilities base: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/`.

## Results

### 1. Protein profile

| Field | Value | Source |
|-|-|-|
| Protein name | Epidermal growth factor receptor | UniProt P00533 |
| Gene | EGFR | UniProt P00533 |
| Organism | Homo sapiens | UniProt P00533 |
| Sequence length | 1210 amino acids | UniProt P00533, NCBI NP_005219.2 (match confirmed) |
| Function | Receptor tyrosine kinase binding EGF-family ligands, activating RAS-RAF-MEK-ERK, PI3K-AKT, PLCgamma-PKC, and STATs signaling cascades | UniProt P00533 (function comment) |
| Domain | Protein kinase (712-979) | UniProt P00533 (feature type "Domain") |
| Chromosome | 7p11.2 | NCBI Gene 1956 |
| Genomic coordinates | NC_000007.14:55019016-55211627 (GRCh38), 32 exons | NCBI Gene 1956 |
| NCBI Gene ID | 1956 | UniProt cross-reference (GeneID) |
| RefSeq protein | NP_005219.2 | UniProt cross-reference (RefSeq) |
| RefSeq mRNA | NM_005228.4 | UniProt cross-reference (RefSeq) |

Sanity check: UniProt sequence length (1210) matches NCBI protein sequence length (1210). This confirms correct identifier mapping between UniProt P00533 and NCBI RefSeq NP_005219.2 (isoform a, canonical).

### Protein card

EGFR (Epidermal Growth Factor Receptor) is a receptor tyrosine kinase encoded by the EGFR gene on chromosome 7p11.2 in humans (NCBI Gene ID 1956, UniProt P00533).
The protein is 1210 amino acids long and belongs to the ErbB/HER family, functioning as a receptor for EGF-family ligands that triggers dimerization and autophosphorylation to activate downstream signaling cascades including RAS-RAF-MEK-ERK, PI3K-AKT, PLCgamma-PKC, and STATs.
Its key structural feature is the protein kinase domain (residues 712-979), and the extracellular region contains receptor L domains and furin-like cysteine-rich domains responsible for ligand binding.
Somatic mutations in EGFR, particularly in the kinase domain, are strongly associated with non-small cell lung cancer and are targets for tyrosine kinase inhibitors such as erlotinib and gefitinib.
EGFR is one of the most studied oncogenes with extensive clinical variant data in ClinVar, making it a central target in precision oncology.

### 2. ClinVar variants

ClinVar search for "EGFR[gene]" returned 3835 total variants, we fetched and examined 500 of them.
Classification breakdown of the 500 fetched variants: 292 Uncertain significance, 127 Likely benign, 15 Benign, 4 Benign/Likely benign, 2 Pathogenic, 1 Likely pathogenic, 49 with no germline classification, 10 with oncogenicity classification.

#### Selected variants (5)

| Variant ID | HGVS | Clinical significance | Review status | Condition | Source |
|-|-|-|-|-|-|
| VCV004277604 | NM_005228.5(EGFR):c.2816_2819dup (p.Ile941fs) | Likely pathogenic | criteria provided, single submitter | Lung cancer | SCV006551916 |
| VCV003729655 | NM_005228.5(EGFR):c.1150_1160del (p.Thr384fs) | Pathogenic | criteria provided, single submitter | EGFR-related lung cancer | SCV005844279 |
| VCV003765034 | NM_005228.5(EGFR):c.2310_2311insGGT (p.Asp770_Asn771insGly) | Oncogenicity: Likely oncogenic | criteria provided, single submitter | Neoplasm | SCV005872090 |
| VCV004640069 | NM_005228.5(EGFR):c.2157C>A (p.Gly719=) | Likely benign | criteria provided, single submitter | Hereditary cancer-predisposing syndrome | SCV007256826 |
| VCV004685791 | NM_005228.5(EGFR):c.1912A>G (p.Thr638Ala) | Uncertain significance | criteria provided, single submitter | Not provided | SCV007331535 |

### 3. Conflicts and interpretation

Across 500 EGFR variants, ClinVar did not assign the explicit label "Conflicting interpretations of pathogenicity". EGFR acts mainly as a somatic driver gene, so germline conflict labels appear less often.

However, a subtler form of conflict exists: 10 variants have an oncogenicity classification alongside or instead of a germline classification, meaning the same variant can be "Uncertain significance" in a germline context but "Likely oncogenic" in a somatic context.
This dual-classification pattern is characteristic of EGFR because most clinically actionable mutations (e.g. L858R, exon 19 deletions, T790M) are somatic driver mutations in lung cancer, not inherited germline variants, so the germline framework often assigns them VUS or does not apply.

Review status across these variants is predominantly "criteria provided, single submitter" (only 1 star), meaning most classifications lack independent confirmation and should be interpreted with caution. No EGFR variants in this batch reached expert panel or practice guideline status.

## Discussion

The pipeline successfully mapped identifiers from UniProt (P00533) to NCBI Gene (1956) to RefSeq sequences (NP_005219.2, NM_005228.4) and ClinVar variants. Sequence length sanity check confirmed consistency between UniProt and NCBI (both 1210 aa).

The ClinVar data shows that 58.4 percent of the 500 EGFR variants fall into the "Uncertain significance" category. This pattern is common for genes like EGFR. Doctors care most about EGFR mutations in tumors, not inherited ones.
No variants carry the "Conflicting interpretations" label. Labs mostly agree when they classify EGFR variants in the inherited disease context. The real disagreement happens between two different systems. One system evaluates inherited risk. The other system evaluates cancer driver mutations. The same variant gets different labels depending on which lens you use.

Bias observations: 
1. ClinVar submissions for EGFR are biased toward germline testing contexts (hereditary cancer panels), while the gene's primary clinical relevance is in somatic tumor testing, which may not always feed into ClinVar.
2. Popular genes like EGFR attract more submissions, but submission volume does not equal evidence quality - nearly all variants here are single-submitter with no expert panel review. This means the data appears comprehensive but the confidence level per variant is low.

## References

- UniProt P00533: https://www.uniprot.org/uniprotkb/P00533
- NCBI Gene 1956: https://www.ncbi.nlm.nih.gov/gene/1956
- NCBI RefSeq NP_005219.2 (protein): https://www.ncbi.nlm.nih.gov/protein/NP_005219.2
- NCBI RefSeq NM_005228.4 (mRNA): https://www.ncbi.nlm.nih.gov/nuccore/NM_005228.4
- ClinVar EGFR variants: https://www.ncbi.nlm.nih.gov/clinvar/?term=EGFR%5Bgene%5D
- ClinVar VCV004277604: https://www.ncbi.nlm.nih.gov/clinvar/variation/4277604/
- ClinVar VCV003729655: https://www.ncbi.nlm.nih.gov/clinvar/variation/3729655/
- ClinVar VCV003765034: https://www.ncbi.nlm.nih.gov/clinvar/variation/3765034/
- ClinVar VCV004640069: https://www.ncbi.nlm.nih.gov/clinvar/variation/4640069/
- ClinVar VCV004685791: https://www.ncbi.nlm.nih.gov/clinvar/variation/4685791/
