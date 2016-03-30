##Implementation of Algorithm to find out frequent itemsets based on negative border analysis
import sys
import random
from itertools import combinations
"""Function for Toivonen Algorithm"""
def toivonen(record,z,finalstep):
    """Adjusting the support threshold according to the size of sampled input"""
    z=z*0.44
    record.seek(0,0)
    FinalChkArrNew=[]
    CompareToFullFileFreq=[]
    CompareToFullFileNeg=[]
    di={}
    numline=len(record.readlines())
    """Taking a sample of input file"""
    numline*=11
    getline=numline/20
    record.seek(0,0)
    lines=random.sample(record.readlines(),getline)
    for line in lines:
        for t in line.replace(',',''):
            if t !=('\n'):
                if t not in di.keys():
                    di[t]=1
                elif t in di.keys():
                    di[t]+=1
    freq1=sorted([[v] for v in di.keys() if di[v]>=z])
    """Appending the frequent and infrequent itemsets to lists for comparison against the entire file"""
    if len(freq1)!=0:
        for each in freq1:
            CompareToFullFileFreq.append(each)
    """Constructing negative border for frequent items"""
    neg1=sorted([[v] for v in di.keys() if di[v]<z])
    if len(neg1)!=0:
        for each in neg1:
            CompareToFullFileNeg.append(each)

    FrqCan=[]
    for m in range(len(freq1)):
        for n in freq1[m+1:]:
            FrqCan.append([freq1[m][0],n[0]])
    for re in FrqCan:
        counter=0
        a=0
        for line in lines:
            for r in re:
                a=0
                if r in line:
                    a=1
                elif r not in line:
                    break
            if a==1:
                counter+=1
        re.append(counter)
    FrqAct=[]
    FreqNeg=[]
    for re in FrqCan:
        Supp=re[-1]
        if Supp>=z:
            FrqAct.append(re[:-1])
        elif Supp<z:
            FreqNeg.append(re[:-1])
    if len(FrqAct)!=0:
        for each in FrqAct:
            CompareToFullFileFreq.append(each)
    if len(FreqNeg)!=0:
        for each in FreqNeg:
            CompareToFullFileNeg.append(each)
    if len(FrqAct)!=0:
        apriori(FrqAct,lines,3,z,CompareToFullFileFreq,CompareToFullFileNeg,freq1)

    z=(z/0.44)
    record.seek(0,0)
    for re in CompareToFullFileNeg:
        record.seek(0,0)
        counter=0
        a=0
        for line in record:
            for r in re:
                a=0
                if r in line:
                    a=1
                elif r not in line:
                    break
            if a==1:
                counter+=1
        re.append(counter)
    ResultNeg=[]
    for re in CompareToFullFileNeg:
        Supp=re[-1]
        if Supp>=z:
            ResultNeg.append(re[:-1])

    if len(ResultNeg)!=0:
        return 0
    elif len(ResultNeg)==0:
        record.seek(0,0)
        for re in CompareToFullFileFreq:
            record.seek(0,0)
            counter=0
            a=0
            for line in record:
                for r in re:
                    a=0
                    if r in line:
                        a=1
                    elif r not in line:
                        break
                if a==1:
                    counter+=1
            re.append(counter)
        ResultFreq=[]
        for re in CompareToFullFileFreq:
            Supp=re[-1]
            if Supp>=z:
                ResultFreq.append(re[:-1])
        print ('FINAL RESULT')
        if len(ResultFreq)==0:
            print (finalstep)
            print ('0.55')
            print ('No Frequent Items')
        elif len(ResultFreq)!=0:
            lastlength=len(ResultFreq[len(ResultFreq)-1])
            print (finalstep)
            """Print the sample size"""
            print ('0.55')
            for i in range(lastlength):
                h=[j for j in ResultFreq if len(j)==(i+1)]
                print (h)
        return 1
def apriori(FrqAct,lines,k,z,TotFrqAct,TotFrqNeg,freq1):
    Freq=[]
    FreqNew=[]
    FinalChkArr=[]
    for t in FrqAct:
        lastelement=t[-1]
        ind=freq1.index([lastelement])
        for i in freq1[ind+1:]:
            templist=[v for v in t]
            templist.append(i[0])
            for combi in combinations(templist,k-1):
                newcombi=[g for g in combi]
                if  newcombi not in FrqAct:
                    e=0
                    break
                elif newcombi in FrqAct:
                    e=1
            if (e==1):
                Freq.append(sorted(templist))

    for re in Freq:
        counter=0
        a=0
        for line in lines:
            for r in re:
                a=0
                if r in line:
                    a=1
                elif r not in line:
                    break
            if a==1:
                counter+=1
        re.append(counter)
    FrqNewAct=[]
    FrqNewNeg=[]
    for re in Freq:
        Supp=re[-1]
        if Supp>=z:
            FrqNewAct.append(re[:-1])
        elif Supp<z:
            FrqNewNeg.append(re[:-1])
    if len(FrqNewAct)!=0:
        for each in sorted(FrqNewAct):
            TotFrqAct.append(each)

    if len(FrqNewNeg)!=0:
        for each in sorted(FrqNewNeg):
            TotFrqNeg.append(each)

    if len(FrqNewAct)!=0:
        apriori(FrqNewAct,lines,k+1,z,TotFrqAct,TotFrqNeg,freq1)

if __name__=='__main__':
    retcounter=0
    inputdata=open("toivonen_test.txt")
    supp=int(20)
    counter=0
    while (retcounter!=1):
        counter+=1
        retcounter=toivonen(inputdata,supp,counter)


