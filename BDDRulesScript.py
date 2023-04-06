file2tag = {}
import os
files = set()
trueFiles = set()

with open('MixupOutput/TestingFAMILY_HIST.txt','r') as f:
    for line in f:
        lineInfo = line.strip().split(' ')
        if len(lineInfo) > 1:
            fileName = lineInfo[1]
            if fileName in file2tag: file2tag[fileName].append(lineInfo[2:])
            else: file2tag[fileName] = [lineInfo[2:]]
"""
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
                if typeOfTag == 'familyhistory' or typeOfTag == 'fhdiseases':
                    files.add(fileName.split('-')[0])
                    histKnown = True
            if not histKnown:
                fw.write("\t<FAMILY_HIST id=\"DOC"+str(doccount)+"\" indicator=\"not present\"/>\n")
                doccount += 1
            else:
                fw.write("\t<FAMILY_HIST id=\"DOC"+str(doccount)+"\" indicator=\"present\"/>\n")
                doccount += 1
            fw.write('\t</TAGS>\n')
            fw.write('</root>')
            sentences = fileString.split('.')
            for tag in tagsList:
                if '<FAMILY_HIST' in tag and 'indicator="present"/>' in tag:
                    print(fileName)
                    print('FAMILY HISTORY' in fileString.upper())
"""



def famHist(sent):
    familymembs = {"FATHER ","MOTHER ","SISTER ","BROTHER ","FATHER,","MOTHER,","SISTER,","BROTHER,","FATHER.","MOTHER.","SISTER.","BROTHER."}
    risks = {"MI ","MI,", "MYOCARDIAL INFARCTION", "CAD", "CORONARY ARTERY DISEASE"}
    sentUp = sent.upper()
    memb, risk = False, False
    for r in risks:
        if r in sentUp: risk = True
    for m in familymembs:
        if m in sentUp : memb = True
    if risk and memb: return True
    return False

count = 0


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
                """
                if typeOfTag == 'familyhistory' or typeOfTag == 'fhdiseases':
                    files.add(fileName.split('-')[0])
                    histKnown = True
                """
            sentences0 = fileString.split('\t')
            sentences = [sent for senty in sentences0 for sent in senty.split(".")]
            for sentence in sentences:
                if famHist(sentence):
                    histKnown = True
            if not histKnown:
                fw.write("\t<FAMILY_HIST id=\"DOC"+str(doccount)+"\" indicator=\"not present\"/>\n")
                doccount += 1
            if histKnown:
                fw.write("\t<FAMILY_HIST id=\"DOC"+str(doccount)+"\" indicator=\"present\"/>\n")
                doccount += 1
            fw.write('\t</TAGS>\n')
            fw.write('</root>')

"""
                    count += 1
                    print(fileName)
                    #print(sentence)
            for tag in tagsList:
                if '<FAMILY_HIST' in tag and 'indicator="present" ' in tag:
                    trueFiles.add(fileName)
"""
