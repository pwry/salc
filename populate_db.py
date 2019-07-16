import create_db
import csv
from build_bibcodes_tsv import find_bibcodes
from collections import OrderedDict

conn, cur = create_db.init()

def insert(table, props, cur = cur):
    s = 'INSERT INTO {} ({}) VALUES ({})'.format(table, ','.join(props.keys()), ','.join([f':{val}' for val in props.keys()]))
    cur.execute(s, props)

with open('codes_with_described_in_or_citation_method.tsv', encoding='utf-8') as tsvfile:
	reader = csv.DictReader(tsvfile, delimiter="\t", dialect='excel-tab')
	for row in reader:
		ascl_id = row['ascl_id']
		credit = row['credit']
		di_bibcodes = find_bibcodes(row['described_in'])
		cm_bibcodes = find_bibcodes(row['citation_method'])

		num_commas = row['credit'].count(',')
		num_semicolons = row['credit'].count(';')

		props = OrderedDict([
			('ascl_id', ascl_id),
			('credit', credit),
			('num_commas', num_commas),
			('num_semicolons', num_semicolons)
		])

		if di_bibcodes:
			for b in di_bibcodes:
				p = props.copy()
				p['type'] = 'described_in'
				p['bibcode'] = b
				insert('bibcodes', p)

		if cm_bibcodes:
			for b in cm_bibcodes:
				p = props.copy()
				p['type'] = 'citation_method'
				p['bibcode'] = b
				insert('bibcodes', p)

conn.commit()
conn.close()