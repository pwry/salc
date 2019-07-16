import sqlite3

schema = ['bibcodes (id INTEGER PRIMARY KEY, ascl_id VARCHAR(255) NOT NULL,\
		  bibcode VARCHAR(255) NOT NULL, resolved_bibcode VARCHAR(255), num_citations INTEGER,\
          credit TEXT NOT NULL, num_commas INTEGER, num_semicolons INTEGER NOT NULL,\
          type VARCHAR(255) NOT NULL)', 
          'ascl_entries (id INTEGER PRIMARY KEY, ascl_id VARCHAR(255) NOT NULL,\
           num_citations INTEGER NOT NULL)']

def init():
	DBPATH = './data.sqlite'
	conn = sqlite3.connect(DBPATH)
	cur = conn.cursor()
	for t in schema:
		cur.execute(f'CREATE TABLE IF NOT EXISTS {t}')
	return (conn, cur)

if __name__ == '__main__':
	conn, cur = init()
	conn.commit()
	conn.close() 