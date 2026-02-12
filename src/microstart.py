import json, time, pathlib, requests

CACHE = pathlib.Path("cache")
CACHE.mkdir(exist_ok=True)

def get_json(url, params=None, cache_name=None, sleep_s=0.34):
    if cache_name:
        p = CACHE / cache_name
        if p.exists():
            return json.loads(p.read_text(encoding="utf-8"))
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()
    if cache_name:
        (CACHE / cache_name).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    time.sleep(sleep_s)  # respect limits (especially NCBI)
    return data

uniprot = get_json("https://rest.uniprot.org/uniprotkb/P00533.json", cache_name="check_uniprot.json")

ncbi_gene = get_json(
    "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",
    params={"db": "gene", "term": "EGFR[gene] AND Homo sapiens[orgn]", "retmode": "json"},
    cache_name="check_ncbi_gene.json"
)
gene_ids = ncbi_gene["esearchresult"]["idlist"]

clinvar = get_json(
    "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",
    params={"db": "clinvar", "term": "EGFR[gene]", "retmode": "json"},
    cache_name="check_clinvar.json"
)