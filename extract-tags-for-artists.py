#!/usr/bin/python
# -!- coding: utf-8 -!-
# usage: create-tag-db.py music-db tag-db title artist

import os, sys, codecs, sqlite3

usage = 'usage: create-tag-db.py music-db tag-db'

def GetData(table, row, cursor):
	cursor.execute('select %s from %s' % (row, table))
	items = [item[0] for item in cursor.fetchall()]
	return items

if(__name__ == '__main__'):
	if len(sys.argv) < 3:
		print (usage)
		sys.exit()

	tagdb = sqlite3.connect(sys.argv[2])
	tagdb_cursor = tagdb.cursor()

	musicdb = sqlite3.connect(sys.argv[1])
	musicdb_cursor = musicdb.cursor()

	musicdb_cursor.execute('select distinct artist_id, artist_name from songs')
	for row in musicdb_cursor.fetchall():
		artistid, artistname = row
		tagdb_cursor.execute('select term from artist_term where artist_id=?', (artistid,))
		print ('%s\t%s' % (artistname, '\t'.join(item[0] for item in tagdb_cursor.fetchall()))).encode('utf-8')