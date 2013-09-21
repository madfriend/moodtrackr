#!/usr/bin/python
# -!- coding: utf-8 -!-
# usage: build-db.py tags adjectives

import os, sys, codecs, sqlite3

usage = 'usage: build-db.py tags adjectives output.sqlite'

def CreateDB(filename):
	conn = sqlite3.connect(filename)
	cur = conn.cursor()

	cur.execute('drop table if exists artists')
	cur.execute('drop table if exists albums')
	cur.execute('drop table if exists tracks')
	
	cur.execute('create table artists(id int, name text)')
	cur.execute('create table albums(id int, name text)')
	cur.execute('create table tracks(id int, name text)')

	cur.execute('drop table if exists artists_values')
	cur.execute('drop table if exists albums_values')
	cur.execute('drop table if exists tracks_values')
	
	cur.execute('create table artists_values(artist_id int, value_row text)')
	cur.execute('create table albums_values(album_id int, artist_id int, value_row text)')
	cur.execute('create table tracks_values(track_id int, artist_id int, value_row text)')

	return conn

def ReadCoeffs(filename):
	result = {}
	inpFile = codecs.open(filename, encoding = 'utf-8')
#inpFile.readline()
	for line in (line_raw.strip('\r\n') for line_raw in inpFile):
		if not '\t' in line:
			continue
		adj, coeffs = line.strip(' \t').split('\t', 1)
		coeffs = [float(item) for item in coeffs.split('\t')]
		result[adj] = coeffs

	return result

def CountCoefficients(coeffs, items):
	result = [0.0] * 12
	for item in items:
		if not item in coeffs:
			continue
		for i in range(len(result)):
			result[i] += coeffs[item][i]

	return result


def ReadList(filename):
	l = []
	inpFile = codecs.open(filename, encoding = 'utf-8')
	for line in (line_raw.strip('\r\n') for line_raw in inpFile):
		l.append(line)
	return l

if(__name__ == '__main__'):
	if len(sys.argv) < 4:
		print (usage)
		sys.exit()

	conn = CreateDB(sys.argv[3])
	cur = conn.cursor()
	adjectives = set(ReadList(sys.argv[2]))
	adjectives_coeffs = ReadCoeffs(sys.argv[4])

	inpFile = codecs.open(sys.argv[1], encoding = 'utf-8')
	artistID = 1
	for line in (line_raw.strip('\r\n') for line_raw in inpFile):
		if not '\t' in line:
			continue	
		artist, tags = line.split('\t', 1)
		tags = tags.split('\t')
		if len(set(tags) & adjectives) > 0:
			values = CountCoefficients(adjectives_coeffs, set(tags) & adjectives)
			print ('%s\t%s' % (artist, '\t'.join(set(tags) & adjectives))).encode('utf-8')
			cur.execute('insert into artists(id, name) values (?, ?)', (artistID, artist))
			cur.execute('insert into artists_values (artist_id, value_row) values (?, ?)', (artistID, ' '.join(str(item) for item in values)))
			artistID += 1

	conn.commit()
