import sys
def calculatePDF(x):
   name=x[0]
   num=x[1]
   pD=x[2]
   findings=x[3]
   pFD=x[4]
   pFnotD=x[5]
   pF=list()
   pDF=list()
   pDnotF=list()
   pnotFD=list()
   for i in range(len(findings)):
      pF.append(pFD[i]*pD+(1-pD)*pFnotD[i])
      pDF.append(pFD[i]*pD/pF[i])
      pnotF=1-pF[i]
      pDnotF.append((pD-pDF[i]*pF[i])/pnotF)
      pnotFD.append(1-pFD[i])
   ml=list()
   ml.append(name)
   #ml.append(num)
   ml.append(pD)
   #ml.append(pDF)
   ml.append(pFD)
   ml.append(pFnotD)
   ml.append(findings)
   return ml
def calculateP(x,y,z):
   p1=z
   p2=1-z
   for j in range(y):
      p1*= x[2*j]
   for j in range(y):
      p2*= x[2*j+1]
   p=1/(p1+p2)*z
   for j in range(y):
      p*= x[2*j]
   return p
def calculateUP(x,y,z):
   minmax=list()
   if len(y)==0:
      minmax.append('{0:.4f}'.format(calculateP(x,(len(x)+1)/2,z)))
      minmax.append('{0:.4f}'.format(calculateP(x,(len(x)+1)/2,z)))
   else:
      temp=list()
      l=pow(2,len(y))
      for i in range(l):
         for j in range(len(y)):
            flag=i/pow(2,j)
            if flag%2==0:
               flag=0
            else:
               flag=1
            x.append(y[j][flag*2])
            x.append(y[j][flag*2+1])
         temp.append(calculateP(x,len(x)/2,z))
         for j in range(2*len(y)):
            del x[-1]
      minmax.append('{0:.4f}'.format(min(temp)))
      minmax.append('{0:.4f}'.format(max(temp)))
   return minmax
def calculateq3(x,y,z,findings):
   #print y
   q3=list()
   q1=calculateP(x,len(x)/2,z)
   if len(y)==0:
      temp=list()
      q3.append("none")
      q3.append("N")
      q3.append("none")
      q3.append("N")
      return q3
   else:
      temp=list()
      for i in range(2*len(y)):
         index=i/2
         if i%2==0:
            x.append(y[index][0])
            x.append(y[index][1])
         else:
            x.append(y[index][2])
            x.append(y[index][3])
         temp.append(calculateP(x,len(x)/2,z))
         del x[-1]
         del x[-1]
      temp2=list()
      for i in range(len(temp)):
         temp3=list()
         temp3.append(temp[i])
         temp3.append(findings[i/2])
         if i%2==0:
            temp3.append('T')
         else:
            temp3.append('F')
         temp2.append(temp3)
      temp2.sort(key=lambda x: x[1])
      
      if max(temp2)[0]<=q1:
         q3.append('none')
         q3.append('N')
      else:
         q3.append(max(temp2)[1])
         q3.append(max(temp2)[2])
      #print min(temp2)
      if min(temp2)[0]>=q1:
         q3.append('none')
         q3.append('N')
      else:
         q3.append(min(temp2)[1])
         q3.append(min(temp2)[2])
   
   return q3
def calculateq1(x,y,z):
   fileName=z[:-4]+'_inference.txt'
   outputFile=open(fileName,'w')
   probOfDisease=dict()
   minmaxDisease=dict()
   nextFinding=dict()
   for i in range(len(y)):
      for j in range(len(y[i])):
         counter=0
         uCounter=0
         findings=list()
         uFindings=list()
         uFindingNames=list()
         for k in range(len(y[i][j])):
            if y[i][j][k]!='U':
               counter+=1
            if y[i][j][k]=='T':
               findings.append(x[j][2][k])
               findings.append(x[j][3][k])
            if y[i][j][k]=='F':
               findings.append(1-x[j][2][k])
               findings.append(1-x[j][3][k])
            if y[i][j][k]=='U':
               temp=list()
               temp.append(x[j][2][k])
               temp.append(x[j][3][k])
               temp.append(1-x[j][2][k])
               temp.append(1-x[j][3][k])
               uFindings.append(temp)
               uFindingNames.append(x[j][4][k])
         #print uFindingNames
         p=calculateP(findings,counter,x[j][1])
         p2=calculateUP(findings,uFindings,x[j][1])
         p3=calculateq3(findings,uFindings,x[j][1],uFindingNames)
         probOfDisease[x[j][0]]='{0:.4f}'.format(p)
         minmaxDisease[x[j][0]]=p2
         nextFinding[x[j][0]]=p3
         #print(p2)
      outputFile.write('Patient-' + str(i+1)+':\n')
      outputFile.write(str(probOfDisease)+'\n')
      outputFile.write(str(minmaxDisease)+'\n')
      outputFile.write(str(nextFinding)+'\n')
   outputFile.close()
""" READ THE INPUT FILE """
inputFile = open(sys.argv[2])
fileName=str(sys.argv[2])
a1=dict();
firstline = inputFile.readline()
numOfDiseases= int(firstline.split(' ')[0])
numOfPatients= int(firstline.split(' ')[1])
ml=list()
for x in range(numOfDiseases):
   nextline = inputFile.readline()
   nameOfDisease= str(nextline.split(' ')[0])
   numOfFindings = int(nextline.split(' ')[1])
   pOfDisease= float(nextline.split(' ')[2])
   nextline = inputFile.readline()
   findingList = eval(nextline)
   nextline = inputFile.readline()
   pFD= eval(nextline)
   nextline=inputFile.readline()
   pFnotD= eval(nextline)
   ml.append(nameOfDisease)
   ml.append(numOfFindings)
   ml.append(pOfDisease)
   ml.append(findingList)
   ml.append(pFD)
   ml.append(pFnotD)
findings=list()
patientsFindings=list()
for x in range(numOfPatients):
   for i in range(numOfDiseases):
      nextline=inputFile.readline()
      findings.append(eval(nextline))
   patientsFindings.append(findings)
   findings=list()
inputFile.close()
ml2=list()
disease=list()
for i in range(numOfDiseases):
   ml2.append(ml[i*6])
   ml2.append(ml[i*6+1])
   ml2.append(ml[i*6+2])
   ml2.append(ml[i*6+3])
   ml2.append(ml[i*6+4])
   ml2.append(ml[i*6+5])
   #print(ml2)
   disease.append(calculatePDF(ml2))
   ml2=list()
calculateq1(disease,patientsFindings,fileName)
      
