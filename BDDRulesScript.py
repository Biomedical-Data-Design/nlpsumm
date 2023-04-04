#!/usr/bin/env python
# coding: utf-8

# In[2]:


file2tag = {}
import os

with open('MixupOutput/TestingFAMILY_HIST.txt','r') as f:
    for line in f:
        lineInfo = line.strip().split(' ')
        if len(lineInfo) > 1:
            fileName = lineInfo[1]
            if fileName in file2tag: file2tag[fileName].append(lineInfo[2:])
            else: file2tag[fileName] = [lineInfo[2:]]

for fileName in os.listdir('BDDDataset/testing-RiskFactors-Gold/'): #Input EHRs
    with open('BDDDataset/testing-RiskFactors-Gold/'+fileName,'r') as f:
        with open('RulesTesting/'+fileName,'w') as fw: #Can change this to any folder name you want (this is where it puts the outputs)
            f.readline()
            f.readline()
            fileString = ''
            tags = False
            tagsList = []
            doccount = 0
            fw.write("<?xml version='1.0' encoding='UTF-8'?>\n")
            fw.write("<root>\n")
            for line in f.readlines():
                fileString += line
                if tags: tagsList.append(line)
                else: fw.write(line)
                if '<TAGS>' in line: tags = True
            histKnown = False
            for tag in file2tag[fileName]:
                typeOfTag = tag[-1].strip().replace('\n','').replace('\t','')
                if typeOfTag == 'familyhistory':
                    histKnown = True
            if not histKnown:
                fw.write("\t<FAMILY_HIST id=\"DOC"+str(doccount)+"\" indicator=\"not present\"/>\n")
                doccount += 1
            else:
                fw.write("\t<FAMILY_HIST id=\"DOC"+str(doccount)+"\" indicator=\"present\"/>\n")
                doccount += 1
            fw.write('\t</TAGS>\n')
            fw.write('</root>')

