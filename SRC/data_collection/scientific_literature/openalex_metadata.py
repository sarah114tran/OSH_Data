# %%
# %%
import os
import json
import time
import pandas as pd
from urllib.parse import urlparse
from typing import Dict, List, Any, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
import requests
from datetime import datetime
import logging
from typing import Union, Dict, Any, List
import re
import time
import json 
import csv

# %%
print("👉 Current working directory:", os.getcwd())

# %%
def process_doi(doi: str):
    """Process unstandardized DOIs"""
    doi = doi.lower()

    # Remove https
    if "https://doi.org/" in doi:
        doi = doi.replace("https://doi.org/", "")

    return doi

def fetch_paper_metadata(doi: str, mailto: str) -> dict: 
    """Fetch metadata from OpenAlex"""
    url = f"https://api.openalex.org/works/doi:{doi}"
    
    params = {
        'mailto' : mailto,
    }

    response = requests.get(url, params=params)
    time.sleep(0.5) 

    if response.status_code == 200: 
        return response.json()
    else: 
        raise Exception(f"Failed to fetch paper:{doi}")

def relevant_metadata(paper: dict) -> dict:
    # Extract authors
    authors = [a.get("author", {}).get("display_name") 
               for a in paper.get("authorships", [])]

    # Extract affiliations
    affiliations = []
    for a in paper.get("authorships", []):
        for inst in a.get("institutions", []):
            affiliations.append(inst.get("display_name"))

    return {
        "id": paper.get("id"),
        "doi": paper.get("doi"),
        "title": paper.get("title"),
        "display_name": paper.get("display_name"),
        "authors": "; ".join(authors) if authors else None,
        "author_affiliations": "; ".join(affiliations) if affiliations else None,
        "publication_year": paper.get("publication_year"),
        "publication_date": paper.get("publication_date"),
        "language": paper.get("language"),
        "type": paper.get("type"),
        "cited_by_count": paper.get("cited_by_count"),
        "fwci": paper.get("fwci"),
        "versions": paper.get("versions"),
        "is_retracted": paper.get("is_retracted"),
        "open_access_status": paper.get("open_access", {}).get("oa_status"),
        "updated_date": paper.get("updated_date"),
        "created_date": paper.get("created_date"),
        "primary_topic": paper.get("primary_topic", {}).get("display_name"),
        "primary_topic_field": paper.get("primary_topic", {}).get("field", {}).get("display_name"),
        "primary_topic_subfield": paper.get("primary_topic", {}).get("subfield", {}).get("display_name"),
        "primary_topic_domain": paper.get("primary_topic", {}).get("domain", {}).get("display_name"),
        "paper_license": paper.get("primary_location", {}).get("license"),
        "grants_funder": paper.get("primary_location", {}).get("funder", {}).get("display_name"),
        "grants_funder": paper.get("primary_location", {}).get("award_id"),
    }

def main():
    CSV_PATH = "./included_osh_sci_lit.csv"
    mailto = 'saraht45@uw.edu'

    try:
        if not os.path.exists(CSV_PATH):
            print(f"❌ Error: File '{CSV_PATH}' not found.")
            return
        df = pd.read_csv(CSV_PATH)
    except Exception as e:
        print(f"❌ Error reading CSV file: {e}")
        return

    df['doi'] = df['doi'].astype(str).str.strip().str.lower()
    df = df[df['doi'].notna() & (df['doi'] != '')]

    raw_metadata = []
    flat_metadata = []

    for i, doi in enumerate(df['doi']):
        try:
            print(f"[{i+1}] Looping over: {doi}")
            processed_doi = process_doi(doi)
            paper_metadata = fetch_paper_metadata(processed_doi, mailto)

            if not isinstance(paper_metadata, dict):
                print(f"⚠️ Skipping invalid metadata for {processed_doi}")
                continue

            raw_metadata.append(paper_metadata)
            flat_metadata.append(relevant_metadata(paper_metadata))

            print(f" ✓ Collected: {processed_doi} (total {len(raw_metadata)})")

        except Exception as e:
            print(f"❌ Error analyzing DOI {doi}: {e}\n")

    print(f"✅ Finished! Total papers collected: {len(raw_metadata)}")

    # Save raw JSON
    with open('openalex_metadata.json', 'w', encoding='utf-8') as f:
        json.dump(raw_metadata, f, indent=2, ensure_ascii=False)

    # Save raw metadata as CSV (flattened automatically by pandas)
    pd.json_normalize(raw_metadata).to_csv('openalex_metadata.csv', index=False)

    # Save flattened metadata (your relevant fields only)
    if flat_metadata:
        with open('openalex_metadata_clean.csv', 'w', newline='', encoding='utf-8') as file:
            fieldnames = flat_metadata[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(flat_metadata)


if __name__ == "__main__":
    main()


