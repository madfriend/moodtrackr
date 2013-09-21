#!/bin/python
#coding:utf-8

import sys,json,codecs

tagfile = codecs.open('artists-tags.uniq.txt','r').readlines()

tags = []
for i in tagfile:
	res = i.split('\t')
	tags.append(res)


words = []
wordsfile = codecs.open('words.txt','r').readlines()
for i in wordsfile:
	res = i.strip()
	words.append(res)

for i in sys.stdin:
	res = i.split('\t')
	if len(res) == 3:
		(artist,track,date) = res
	else:
		print "error!"
		continue
	for a in tags:
		#print artist, a[1]
		if a[0].strip() == artist.strip():
			mood = [w for w in a[1:] if w.strip() in words]
			if len(mood) > 0:
			    print date.strip(),'\t',','.join(mood)

