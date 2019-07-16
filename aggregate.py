import create_db
import csv

conn, cur = create_db.init()

# https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.row_factory
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
conn.row_factory = dict_factory
cur = conn.cursor() # have to reassign this

class Entry():
	def __init__(self, ascl_id=None, bibcode=None, credit=None, num_citations=None):
		self.ascl_id = ascl_id
		self.credit = credit
		self.bibcodes = set([bibcode])
		self.num_citations = int(num_citations)

	def add_bibcode(self, bibcode, citation_count):
		if bibcode not in self.bibcodes:
			self.bibcodes.add(bibcode)
			self.num_citations += int(citation_count)


entries = {}

def process(item):
	if item['ascl_id'] not in entries:
		entries[item['ascl_id']] = Entry(ascl_id=item['ascl_id'], bibcode=item['resolved_bibcode'], credit=item['credit'], num_citations=item['num_citations'])
	else:
		print(item)
		if item['resolved_bibcode'] not in entries[item['ascl_id']].bibcodes:
			entries[item['ascl_id']].add_bibcode(item['resolved_bibcode'], item['num_citations'])


cur.execute("SELECT * FROM bibcodes WHERE bibcode <> \'2018ascl.soft02005K\' AND bibcode <> \'2019ascl.soft07008S\'")
for item in cur.fetchall():
	process(item)

with open('ascl_entry_citations.tsv', encoding='utf-8') as f:
	reader = csv.DictReader(f, delimiter="\t", dialect='excel-tab')
	for row in reader:
		# lame workaround
		row['resolved_bibcode'] = row['bibcode']
		process(row)

with open('res.tsv','w',encoding='utf-8') as out:
	out.write("ascl_id\tcredit\tnum_commas\tnum_semicolons\tnum_citations\n")
	for k in entries.keys():
		entry = entries[k]
		out.write("{}\t{}\t{}\t{}\t{}\n".format(entry.ascl_id, entry.credit, entry.credit.count(','), entry.credit.count(';'), entry.num_citations))