import csv, re

def find_bibcodes(str):
	str = str.replace('%26','&')
	res = re.findall(r"\d{4}[A-Za-z\.\&]{5}[\w\.]{4}[ACELPQ-Za-l0-9\.][\d\.]{4}[A-Z]", str)
	if len(res) > 0:
		return res
	else:
		return []

def get_num_authors(str):
	return str.count(',')

with open('codes_with_described_in_or_citation_method.tsv', encoding='utf-8') as tsvfile:
	with open('bibcodes.tsv','w') as out:
		out.write("ascl_id\tnum_commas\tnum_semicolons\tbibcode\ttype\n")

		reader = csv.DictReader(tsvfile, delimiter="\t", dialect='excel-tab')
		for row in reader:
			ascl_id = row['ascl_id']
			num_commas = row['credit'].count(',')
			num_semicolons = row['credit'].count(';')
			di_bibcodes = find_bibcodes(row['described_in'])
			cm_bibcodes = find_bibcodes(row['citation_method'])

			if di_bibcodes is not None:
				for di in di_bibcodes:
					out.write("{}\t{}\t{}\t{}\tdescribed_in\n".format(ascl_id, num_commas, num_semicolons, di))

			if cm_bibcodes is not None:
				for cm in cm_bibcodes:
					out.write("{}\t{}\t{}\t{}\tcitation_method\n".format(ascl_id, num_commas, num_semicolons, cm))