'''Query ADS for citation counts of the bibcodes in the `bibcodes` table.'''

import create_db
import ads

conn, cur = create_db.init()

cur.execute('SELECT bibcode FROM bibcodes WHERE num_citations IS NULL AND bibcode <> \'2018ascl.soft02005K\' AND bibcode <> \'2019ascl.soft07008S\'')
bibcodes = cur.fetchall()

for bibcode_tuple in bibcodes:
	bibcode = bibcode_tuple[0]
	print(bibcode)
	article = list(ads.SearchQuery(bibcode=bibcode, fl=['citation_count', 'bibcode']))
	if not article:
		article = list(ads.SearchQuery(alternate_bibcode=bibcode, fl=['citation_count', 'bibcode']))
	article = article[0]
	cur.execute('UPDATE bibcodes SET num_citations = ?, resolved_bibcode = ? WHERE bibcode = ?', (article.citation_count, article.bibcode, bibcode))
	conn.commit()

conn.close()