#!/usr/bin/python
# -!- coding: utf-8 -!-
# usage: create-tag-db.py music-db tag-db

import os, sys, codecs, sqlite3

usage = 'usage: create-tag-db.py music-db tag-db'

if(__name__ == '__main__'):
	if len(sys.argv) < 3:
		print (usage)
		sys.exit()

	musicdb = sqlite3.connect(sys.argv[1])
	musicdb_cursor = musicdb.cursor()

	track = "TRMMMCH128F425532C"

	musicdb_cursor.execute('select title, artist_name from songs where track_id=?', (track,))
	for row in musicdb_cursor.fetchall():
		print row
