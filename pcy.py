##Park-Chen-Yu Algorithm
from itertools import combinations
import sys

##Definition of PCY Function
def PCY(record,y,z):
    """to store the bucket counts"""
    hashbuc={}
    """to store counts of singletons"""
    di={}
    lstest=[]
    s=1
    Sum=0
    HashNew=[]
    """Moving to the starting of file"""
    record.seek(0,0)
    """Finding out frequent singletons in a file"""
    for line in record:
        for t in line.replace(',',''):
            if t !=('\n'):
                """Adding singletons to a dictionary"""
                if t not in di.keys():
                    """s assigns a numeric value to each input record for later calculation of Hash Function"""
                    di[t]=[1,s]
                    s+=1
                elif t in di.keys():
                    di[t][0]+=1
    print ('Memory for item counts:'+str(len(di)*8))

    """Freq1 contains all the frequent singletons whose count is greater than minimum threshold"""
    freq1=sorted([v for v in di.keys() if di[v][0]>=z])
    if len(freq1)!=0:
        print ('Memory for frequent items of size 1 :'+str(len(freq1)*8))
        print (freq1)
    elif len(freq1)==0:
        print ('No Frequent Singletons')
    record.seek(0,0)
    """Storing the counts of pairs in buckets in the first pass itself"""
    for pairline in record:
        pairlinenew=pairline.replace(',','')
        for j in range(len(pairlinenew)):
            if j!=('\n'):
                for k in pairlinenew[j+1:]:
                    if k !=('\n'):
                        """Getting the bucket number for the pair from a hash function"""
                        r=Hash_It(di[pairlinenew[j]][1],di[k][1],y)
                        """Adding to bucket counts for the pairs that hash to a particular bucket"""
                        if r not in hashbuc.keys():
                            hashbuc[r]=1
                        elif r in hashbuc.keys():
                            hashbuc[r]+=1
                        for b in range(y):
                            if b not in hashbuc.keys():
                                hashbuc[b]=0
    print (hashbuc)
    print ('Memory for buckets:'+str(y*4))
    """Creating a bit vector for the frequent buckets"""
    Bit_Vect=Bit_Vec_Form(hashbuc,z)

    HashNew=Cand_Gen(freq1,Bit_Vect,2,y,di)
    print ('Memory for candidate pairs:'+str(len(HashNew)*12))

    for re in HashNew:
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
    Frq2=[]
    for re in HashNew:
        Supp=re[-1]
        if Supp>=z:
            Frq2.append(re[:-1])
    if len(hashbuc)!=0 and len(freq1)!=0 and len(Frq2)!=0:
        print (hashbuc)
    if len(Frq2)!=0:
        print ('Memory for frequent pairs'+str(len(Frq2)*12))
        print (Frq2)
    elif len(Frq2)==0 and len(freq1)!=0:
        print ('No frequent Doubletons')

    pcygeneric(3,record,Frq2,freq1,y,di,z)

def Cand_Gen(freq1,bitarray,k,o,di):
    CandGen=[]
    HashActFreq={}
    if k==2:
        for m in range(len(freq1)):
            for n in freq1[m+1:]:
                a=Hash_It(di[freq1[m]][1],di[n][1],o)
                if bitarray[a]==1:
                    CandGen.append([freq1[m],n])

    return CandGen

def pcygeneric(k,record,freqlessk,freq1,o,di,z):
    Fre=[]
    record.seek(0,0)
    buck={}
    for line in record:
        Arrline=[]
        newline=line.replace(',','')
        for t in newline:
            if t !=('\n'):
                Arrline.append(t)
        """Creating higher itemsets from pairs through combinations"""
        for i in combinations(Arrline,k):
            """Judging the bucket number through hash function"""
            Buckno=Hash_It_New(i,o,di)
            if Buckno not in buck:
                buck[Buckno]=1
            elif Buckno in buck:
                buck[Buckno]+=1
            for b in range(o):
                if b not in buck.keys():
                    buck[b]=0
    if len(buck)!=0 and len(freq1)!=0 and len(freqlessk)!=0:
        print (buck)
    Bit_Vec_Generic=Bit_Vec_Form(buck,z)
    """Carrying out the procedure not only for pairs but for higher frequent sets"""
    for t in freqlessk:
        lastelement=t[-1]
        ind=freq1.index(lastelement)
        for i in freq1[ind+1:]:
            templist=[v for v in t]
            templist.append(i)
            for combi in combinations(templist,k-1):
                newcombi=[g for g in combi]
                if  newcombi not in freqlessk:
                    e=0
                    break
                elif newcombi in freqlessk:
                    e=1
            if (e==1):
                Fre.append(sorted(templist))
    NewCand=[]
    if len(Fre)!=0:
        for eachfre in Fre:
            BitReturn=Hash_It_New(eachfre,o,di)
            if Bit_Vec_Generic[BitReturn]==1:
                NewCand.append(eachfre)

    if 'NewCand' in locals() and len(NewCand)!=0:
        print ('Memory for Candidate itemsets:'+(str(len(NewCand)*(k+1)*4)))
        for re in NewCand:
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
    FrqNew=[]
    if 'NewCand' in locals() and len(NewCand)!=0:
        for re in NewCand:
            Supp=re[-1]
            if Supp>=z:
                FrqNew.append(re[:-1])
    if len(FrqNew)!=0:
        print ('Memory for frequent itemsets: '+ str(len(FrqNew)*(k+1)*4))
        print (FrqNew)
    if len(FrqNew)!=0:
        k+=1
        pcygeneric(k,record,FrqNew,freq1,o,di,z)
"""Hash Function for itemsets to judge the bucket number"""
def Hash_It_New(i,o,di):
    Prod=1
    for m in i:
        Prod*=di[m][1]
    return Prod%o

def Hash_It(m,n,o):
    return (m*n)%o
"""Setting of bits in bit vector array"""
def Bit_Vec_Form(buc,z_support):
    Bit_Arr=[]
    for k in range(len(buc)):
        Bit_Arr.append(0)
    for v in buc.keys():
        if buc[v]>=z_support:
            Bit_Arr[v]=1
        elif buc[v]<z_support:
            Bit_Arr[v]=0
    return Bit_Arr

if __name__=='__main__':
    inputdata=open(sys.argv[1])
    n_bucsize=int(sys.argv[3])
    z_supp=int(sys.argv[2])
    PCY(inputdata,n_bucsize,z_supp)
