from pprint import pprint
from collections import defaultdict
from lxml import etree
from prettytable import PrettyTable, ALL
from textwrap import fill
from math import log, floor
import sys
import os

def getDict(Fname):
	valuelist = []
	newDict = {}
	capture = 0
	try:
		with open(Fname) as fHandle:
			NewLst = fHandle.readlines()
	except:
		print("Incorrect File name sufficed, please check for correct file name")
		exit()	
	newlist1 = [s.replace("\n", "") for s in NewLst]
	for items in newlist1:
		if "Destination" in items:
			itemKey = "DEST FPC-PFE "+items.split(" ")[3].split(",")[0]+":"+items.split(" ")[7].split(",")[0]+" Source FPC-PFE "+items.split(" ")[11].split(",")[0]+":"+items.split(" ")[15].split(",")[0]
			key = itemKey
		else:
			if "Drop statistics" in items:
				capture = 1
			elif "Qdepth" in items:
				newDict[key]=valuelist
				capture = 0
				valuelist = []
			if capture:
				valuelist.append(items)
	Nlist = []
	for val,itm in newDict.items():
		for i in itm:
			i = " ".join(i.split())
			Nlist.append(i)
		newDict[val]=Nlist
		Nlist = []
	return newDict

def getDictStat(Fname):
	valueliststat = []
	newDictstat = {}
	capturestat = 0
	try:
		with open(Fname) as fHandle:
			NewLst = fHandle.readlines()
	except:
		print("Incorrect File name sufficed, please check for correct file name")
		exit()	
	newlist1 = [s.replace("\n", "") for s in NewLst]
	for items in newlist1:
		if "Destination" in items:
			itemKey = "DEST FPC-PFE "+items.split(" ")[3].split(",")[0]+":"+items.split(" ")[7].split(",")[0]+" ** Source FPC-PFE "+items.split(" ")[11].split(",")[0]+":"+items.split(" ")[15].split(",")[0]
			key = itemKey
		else:
			if "Total statistics:   High priority" in items:
				capturestat = 1
			elif "Tx statistics:      High priority " in items:
				newDictstat[key]=valueliststat
				capturestat = 0
				valueliststat = []
			if capturestat:
				valueliststat.append(items)
	Nlist = []
	for val,itm in newDictstat.items():
		for i in itm:
			i = " ".join(i.split())
			Nlist.append(i)
		newDictstat[val]=Nlist
		Nlist = []
	return newDictstat

def IntConv(number):
    units = ['', 'K', 'M', 'G', 'T', 'P']
    k = 1000.0
    if number != 0:
    	magnitude = int(floor(log(number, k)))
    	return '%.2f%s' % (number / k**magnitude, units[magnitude])
    else:
    	return number

#MAIN METHOD
#=====================
if len(sys.argv) < 3:
	print("Enter files for comparision")
	exit()

nDict1 = getDict(sys.argv[1])
nDict2 = getDict(sys.argv[2])
nDictStat1 = getDictStat(sys.argv[1])
nDictStat2 = getDictStat(sys.argv[2])

print("=============================================================")
print("=                 Class of Service Stats Diff               =")
print("=============================================================")
ActLssStat = {}
os.system('clear')
RtTbl = PrettyTable(['Source PFE','Destination PFE','LowPri Pkt Diff','LowPri Byt Diff','HighPri Pkt Diff','HighPri Byt Diff'])
newKey = list(nDictStat1.keys())[0].split(" ** ")[1]
for key1,val1 in nDictStat1.items():
	if newKey == key1.split(" ** ")[1]:
		val2 = nDictStat2[key1]
		if val1[1] != val2[1] or val1[2] != val2[2]:
			#packet
			lvlA1 = val1[1].split(" ")[-1]
			lvlA2 = val2[1].split(" ")[-1]
			#byte
			lvlB1 = val1[2].split(" ")[-1]
			lvlB2 = val2[2].split(" ")[-1]
			#packet
			hvlA1 = val1[1].split(" ")[-2]
			hvlA2 = val2[1].split(" ")[-2]
			#byte
			hvlB1 = val1[2].split(" ")[-2]
			hvlB2 = val2[2].split(" ")[-2]
			lpkt = IntConv(int(lvlA1) - int(lvlA2))
			lbyt = IntConv(int(lvlB1) - int(lvlB2))
			hpkt = IntConv(int(hvlA1) - int(hvlA2))
			hbyt = IntConv(int(hvlB1) - int(hvlB2))
			RtTbl.add_row([key1.split(" ** ")[1],key1.split(" ** ")[0],lpkt,lbyt,hpkt,hbyt])
	else:
		pprint(RtTbl)
		a = input("")
		os.system('clear')
		newKey = key1.split(" ** ")[1]
		RtTbl = PrettyTable(['Source PFE','Destination PFE','LowPri Pkt Diff','LowPri Byt Diff','HighPri Pkt Diff','HighPri Byt Diff'])
		val2 = nDictStat2[key1]
		if val1[1] != val2[1] or val1[2] != val2[2]:
			#packet
			lvlA1 = val1[1].split(" ")[-1]
			lvlA2 = val2[1].split(" ")[-1]
			#byte
			lvlB1 = val1[2].split(" ")[-1]
			lvlB2 = val2[2].split(" ")[-1]
			#packet
			hvlA1 = val1[1].split(" ")[-2]
			hvlA2 = val2[1].split(" ")[-2]
			#byte
			hvlB1 = val1[2].split(" ")[-2]
			hvlB2 = val2[2].split(" ")[-2]
			lpkt = IntConv(int(lvlA1) - int(lvlA2))
			lbyt = IntConv(int(lvlB1) - int(lvlB2))
			hpkt = IntConv(int(hvlA1) - int(hvlA2))
			hbyt = IntConv(int(hvlB1) - int(hvlB2))
			RtTbl.add_row([key1.split(" ** ")[1],key1.split(" ** ")[0],lpkt,lbyt,hpkt,hbyt])
pprint(RtTbl)
a=input("")
ActLss = {}
os.system('clear')
print("======================")
print("    Drop statistics   ")
print("======================")
for key1,val1 in nDict1.items():
	val2 = nDict2[key1]
	if val1[1] != val2[1] or val1[2] != val2[2]:
		#packet
		lvlA1 = val1[1].split(" ")[-1]
		lvlA2 = val2[1].split(" ")[-1]
		#byte
		lvlB1 = val1[2].split(" ")[-1]
		lvlB2 = val2[2].split(" ")[-1]
		#packet
		hvlA1 = val1[1].split(" ")[-2]
		hvlA2 = val2[1].split(" ")[-2]
		#byte
		hvlB1 = val1[2].split(" ")[-2]
		hvlB2 = val2[2].split(" ")[-2]
		lpkt = int(lvlA1) - int(lvlA2)
		lbyt = int(lvlB1) - int(lvlB2)
		hpkt = int(hvlA1) - int(hvlA2)
		hbyt = int(hvlB1) - int(hvlB2)
		if lpkt != 0:
			print("Drop record for : \t ",key1)
			print("Low priority Packet Drop Diff:\t",lpkt,"\n Low priority Bytes Drop Diff: \t",lbyt)
		if hpkt != 0:
			print("Drop record for : \t ",key1)
			print("High priority Packet Drop Diff:\t",hpkt,"\n High priority Bytes Drop Diff: \t",hbyt)
	if int(val1[3].split(" ")[-1]) != 0 or int(val1[3].split(" ")[-2]) != 0:
		KeyA = key1 + "  New Record"
		ActLss[KeyA] = val1[3].split(" ")[-1] + " " + val1[3].split(" ")[-2]
	if int(val2[3].split(" ")[-1]) != 0 or int(val2[3].split(" ")[-2]) != 0:
		KeyA = key1 + "  Old Record"
		ActLss[KeyA] = val2[3].split(" ")[-1] + " " + val2[3].split(" ")[-2]
NoActDrp = True
print("======================")
print("Active Drop statistics")
print("======================")
for k,v in ActLss.items():
	if v != '0':
		NoActDrp = False
		print("[",k,"]  =>",v," pps")
if NoActDrp:
	print("No Active drops between this comparision")
print("======================")
