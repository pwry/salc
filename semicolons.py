import csv

with open('semicolons.tsv','w') as out:
	def munge(row):
		ascl_id = row['ascl_id']
		num_commas = row['credit'].count(',')
		num_semicolons = row['credit'].count(';')

		if num_semicolons < 3 and (num_semicolons > 0 or num_commas > 0) and num_semicolons != num_commas - 1:
			out.write("{}\t{}\t{}\t{}\n".format(ascl_id, num_commas, num_semicolons, num_semicolons - num_commas))


	with open('codes_with_described_in_or_citation_method.tsv', encoding='utf-8') as tsvfile:
		out.write("ascl_id\tcommas\tsemicolons\tdiff\n")
		reader = csv.DictReader(tsvfile, delimiter="\t", dialect='excel-tab')
		for row in reader:
			munge(row)

	with open('ascl_entry_citations.tsv', encoding='utf-8') as tsvfile:
		reader = csv.DictReader(tsvfile, delimiter="\t", dialect='excel-tab')
		for row in reader:
			munge(row)