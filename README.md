# Steps

1) Download the appropriate reports from ASCL.
- codes_with_described_in_or_citation_method.tsv: ascl_id, credit, described_in (serialized array), citation_method (string)
- ascl_entry_citations.tsv: ascl_id, credit, num_citations

2) Build the database.
- populate_db.py loads codes_with_etc.tsv into a sqlite db, building the bibcodes table
- TODO: handle ascl_entry_citations

3) Query ADS for bibcode citations.
- query_ads.py

4) Aggregate described_in/citation_method citations (in data.sqlite) with ASCL entry citations (in ascl_entry_citations.tsv).
- aggregate.py