import json, time, pathlib, requests, csv

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

def get_sig(v):
    germ = v.get("germline_classification", {})
    onco = v.get("oncogenicity_classification", {})
    parts = []
    if germ.get("description"):
        parts.append(germ["description"])
    if onco.get("description"):
        parts.append(f"oncogenicity: {onco['description']}")
    return "; ".join(parts) if parts else ""

def get_review(v):
    germ = v.get("germline_classification", {})
    onco = v.get("oncogenicity_classification", {})
    parts = []
    if germ.get("review_status"):
        parts.append(germ["review_status"])
    if onco.get("review_status"):
        parts.append(onco["review_status"])
    return "; ".join(parts) if parts else ""

def get_condition(v):
    germ = v.get("germline_classification", {})
    onco = v.get("oncogenicity_classification", {})
    traits = germ.get("trait_set", [])
    if not traits:
        traits = onco.get("trait_set", [])
    if traits:
        return traits[0].get("trait_name", "")
    return ""

def get_source(v):
    scvs = v.get("supporting_submissions", {}).get("scv", [])
    return ", ".join(scvs[:3])

def main():
    search = get_json(
    "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",
    params={"db": "clinvar", "term": "EGFR[gene]", "retmax": "500", "retmode": "json"},
    cache_name="clinvar_search_egfr.json"
    )

    ids = search["esearchresult"]["idlist"]
    print(f"clinvar search: {search['esearchresult']['count']} total, fetched {len(ids)} ids")

    details_path = cache / "clinvar_details_egfr.json"
    if details_path.exists():
        combined = json.loads(details_path.read_text(encoding="utf-8"))
        all_variants = combined["variants"]
    else:
        all_variants = {}
        for i in range(0, len(ids), 100):
            batch = ids[i:i+100]
            r = requests.get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi", params={"db": "clinvar", "id": ",".join(batch), "retmode": "json"})
            details = r.json()
            for uid in details["result"].get("uids", []):
                all_variants[uid] = details["result"][uid]
            time.sleep(0.34)
        combined = {"count": len(all_variants), "variants": all_variants}
        details_path.write_text(json.dumps(combined, ensure_ascii=False, indent=2), encoding="utf-8")

    pathogenic = []
    oncogenic = []
    benign_likely = []
    vus = []
    for uid, v in all_variants.items():
        germ = v.get("germline_classification", {})
        onco = v.get("oncogenicity_classification", {})
        sig = germ.get("description", "")
        onco_sig = onco.get("description", "")
        if "pathogenic" in sig.lower() and "uncertain" not in sig.lower() and "likely" not in sig.lower() and "conflicting" not in sig.lower():
            pathogenic.append(v)
        elif "likely pathogenic" in sig.lower():
            pathogenic.append(v)
        elif "benign" in sig.lower() and "likely" in sig.lower():
            benign_likely.append(v)
        elif "uncertain" in sig.lower() and "oncogenic" not in onco_sig.lower():
            vus.append(v)
        if "oncogenic" in onco_sig.lower() and "uncertain" not in onco_sig.lower():
            oncogenic.append(v)

    selected = []
    for v in pathogenic[:2]:
        selected.append(v)
    for v in oncogenic[:1]:
        if v not in selected:
            selected.append(v)
    for v in benign_likely[:1]:
        selected.append(v)
    for v in vus[:1]:
        selected.append(v)

    with open(out / "variants_top.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["variant_id", "hgvs", "clinical_significance", "review_status", "condition", "source"])
        for v in selected:
            w.writerow([
                v["accession"],
                v["title"],
                get_sig(v),
                get_review(v),
                get_condition(v),
                get_source(v)
            ])

if __name__ == '__main__':
    main()