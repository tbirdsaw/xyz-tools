#!/usr/bin/python

file = "testfiles/first10236bytes.txt"
file2 = "testfiles/secondbytes.txt"

ckfile = open(file, 'r')
ck2file = open(file2, 'r')
#checksum function
def checksum(st):
#    return reduce(lambda x,y:x+y, map(ord, st))
	return sum(ord(c) for c in st)

print checksum(ckfile.read())
print checksum(ck2file.read())
