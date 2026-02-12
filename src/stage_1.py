import json, time, pathlib, requests

cache = pathlib.Path("cache")
cache.mkdir(exist_ok=True)
out = pathlib.Path("out")
out.mkdir(exist_ok=True)

def get_json(url, params=None, cache_name=None):
    if cache_name:
        p = cache / cache_name
        if p.exists():
            return json.loads(p.read_text(encoding="utf-8"))
    r = requests.get(url, params=params)
    data = r.json()
    if cache_name:
        (cache / cache_name).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    time.sleep(0.34)
    return data


def main():
    data = get_json("https://rest.uniprot.org/uniprotkb/P00533.json", cache_name="uniprot_p00533.json")

    name = data["proteinDescription"]["recommendedName"]["fullName"]["value"]
    gene = data["genes"][0]["geneName"]["value"]
    length = data["sequence"]["length"]

    function_text = ""
    for c in data["comments"]:
        if c["commentType"] == "FUNCTION" and "texts" in c:
            function_text = c["texts"][0]["value"]
            break

    domains = []
    for f in data["features"]:
        if f["type"] == "Domain":
            domains.append(f"{f['description']} ({f['location']['start']['value']}-{f['location']['end']['value']})")

    geneid = ""
    for xref in data["uniProtKBCrossReferences"]:
        if xref["database"] == "GeneID":
            geneid = xref["id"]
            break

    print(f"name: {name}")
    print(f"gene: {gene}")
    print(f"sequence length: {length}")
    print(f"function: {function_text[:200]}")
    print(f"domains: {', '.join(domains)}")
    print(f"geneid: {geneid}")

    ncbi_gene = get_json(
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi",
        params={"db": "gene", "id": geneid, "retmode": "json"},
        cache_name="ncbi_gene_egfr.json"
    )

    refseq_protein = ""
    refseq_mrna = ""
    for xref in data["uniProtKBCrossReferences"]:
        if xref["database"] == "RefSeq" and xref.get("isoformId") == "P00533-1":
            refseq_protein = xref["id"]
            for prop in xref["properties"]:
                if prop["key"] == "NucleotideSequenceId":
                    refseq_mrna = prop["value"]
            break

    protein_out = out / "sequence_protein.faa"
    if not protein_out.exists():
        r = requests.get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi", params={"db": "protein", "id": refseq_protein, "rettype": "fasta", "retmode": "text"})
        protein_out.write_text(r.text, encoding="utf-8")
        time.sleep(0.34)
    protein_fasta = protein_out.read_text(encoding="utf-8")

    mrna_out = out / "sequence_mrna.fna"
    if not mrna_out.exists():
        r = requests.get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi", params={"db": "nucleotide", "id": refseq_mrna, "rettype": "fasta", "retmode": "text"})
        mrna_out.write_text(r.text, encoding="utf-8")
        time.sleep(0.34)

    ncbi_protein_length = 0
    for line in protein_fasta.splitlines():
        if not line.startswith(">"):
            ncbi_protein_length += len(line.strip())

    if length == ncbi_protein_length:
        print("sequence lengths match")
    else:
        print("sequence lengths dont match")

if __name__ == '__main__':
    main()