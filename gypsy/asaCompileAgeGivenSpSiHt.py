import copy
import dataMachete
import numpy
import time

def getColNumbers(completeColNameList=[],readColNameList=[], defaultColNo = 'NA'):
    '''
    '''
    newColNoList = []
    for name in readColNameList:
        if name in completeColNameList:
            newColNo = completeColNameList.index(name)
            newColNoList.append(newColNo)
        else:
            newColNoList.append(defaultColNo)
            print '\n variable name:', name, 'not found in header'
    return newColNoList
            
def convertReadLineToStringList(readLine = '',separator = ','):
    '''
    '''
    newLineList = []
    x = readLine.rstrip()
    if x.startswith('"') and x.endswith('"'):
        x = x[1:-1]
    x = x.split(separator)
    for item in x:
        if item.startswith('"') and item.endswith('"'):
            y = item[1:-1]
        else:
            y = item
        newLineList.append(y)
    return newLineList


def getDataTypeListFromDataDictionary(tableName = '', varNameList=[], dataTypeDict = {}, defaultType = 'string'):
    '''
    '''
    dataTypeList = []
    if not dataTypeDict.has_key(tableName):
        print '\n ldataReadWriteTemplate.getDataTypeListFromDataDictionary()'
        print ' datatypeDict has no table named:', tableName
        print ' empty dataTypeList returned'
    else:
        for varName in varNameList:
            if not dataTypeDict[tableName].has_key(varName):
                print '\n ldataReadWriteTemplate..getDataTypeListFromDataDictionary()'
                print ' datatypeDict table named:', tableName
                print ' has no variable named:', varName
                print ' default variable type:', defaultType, 'added to dataTypeList'
                dataTypeList.append(defaultType)
            else:
                dataTypeList.append(dataTypeDict[tableName][varName]['VARTYPE'])
    return dataTypeList


def convertDataStringListToDataTypeList(dataStringList, listOfDataTypes = [], colNoList = []):
    '''
    '''
    newDataList = []
    end_i = len(listOfDataTypes)
    if not len(colNoList)== end_i:
        print '\n ldataReadWriteTemplate.convertDataStringListLineToDataTypeList()'
        print ' number of COLUMNS:', len(colNoList)
        print ' does not correspond with length of listOfDataTypes:', end_i
        print ' dataStringList not converted to typed data list'
        print ' dataStringList returned as dataStringList'
    else:
        for i in range(0,end_i,1):
            newType = listOfDataTypes[i]
            dataValue = dataStringList[colNoList[i]]
            if newType == 'integer':
                varValue = int(dataValue)
            else:
                if newType == 'float':
                    varValue = float(dataValue)
                else:
                    varValue = dataValue
            newDataList.append(varValue)  
    return newDataList
                  
def idUniqueData(spDict = {},spDataInSiFieldName=''):
    '''
    '''
    uniqueList = []
    for myKey in spDict:
        newValue = spDict[myKey][spDataInSiFieldName]
        if not newValue in uniqueList:
            uniqueList.append(newValue)
    return uniqueList

def append1dListBTo1DListA(listA1D=[],listB1D=[]):
    '''
    '''
    newList = copy.deepcopy(listA1D)
    for item in listB1D:
        newList.append(item)
    return newList

def compileUniqueValueListFromD2List(valuesList=[[]]):
    '''
    '''
    uniqueValueList =[]
    end_i = len(valuesList)
    for i in range(0,end_i,1):
        end_j = len(valuesList[i])
        for j in range(0,end_j,1):
            varValue = valuesList[i][j]
            if not varValue in uniqueValueList:
                uniqueValueList.append(varValue)
    uniqueValueList.sort()
    return uniqueValueList

def get1DParIndexList(d1NameList = [], uniqueIndexNameList= []):
    '''
    '''
    d1IndexList = []
    end_j = len(d1NameList)
    for j in range(0,end_j,1):
        newName = d1NameList[j]
        if not newName in uniqueIndexNameList:
            print 'asaCompileAgeGivenSpSiHt.get1DParIndexList()'
            print 'indexing names in d1NameList'
            print 'could not find name:', newName, 'in uniqueIndexNameList'
            print 'appending index equal to -1'
            d1IndexList.append(-1)
        else:
            newIndex = uniqueIndexNameList.index(newName)
            d1IndexList.append(newIndex)
    return d1IndexList
    

def get2DParIndexList(d2NameList = [[]],uniqueIndexNameList=[]):
    '''
    '''
    end_i = len(d2NameList)
    d2IndexList = []
    for i in range(0,end_i,1):
        newIndexList = get1DParIndexList(d2NameList[i], uniqueIndexNameList)
        d2IndexList.append(copy.deepcopy(newIndexList))
    return d2IndexList

def readLineByLineLookupFunction(dataInFilePath = '', dataInFileName = '', keyVarNameList = [], keyTypeList = [], \
                   readVarNameList = [], readVarTypeList = [], dataInSiNameList = [], dataInSiTypeList = [],
                   spDict = {}, siSpeciesXRefFieldName = 'SISP', spDataInSiFieldName = 'SPSINAME', \
                   ageLookupDict = {}, ageLookupDTreeAgeFieldName = 'AGE', ageLookupSiSigDigits = 0, \
                   ageLookupDHtSigDigits = 2, dataOutPath = ' E:\\Rwd\\', dataOutFileName = 'PREDAGE.csv', \
                   newPredTreeAgeName = 'PHDAGE', attachPredValuesToDataIn = 'NO', \
                   newPredSiName = 'PSPSI', inventoryYear = 2008, newPredOriginName = 'ORIGIN', \
                   largeDatasetWriteLines = 10000, defaultFileExtension = '.csv'):
    '''
    '''
    newFile = open(dataInFilePath + dataInFileName,'r')
    keyColNoList = []
    readColNoList = []
    newAgeList = []
    i = 0
    printLines = largeDatasetWriteLines
    nDigits = max(ageLookupDHtSigDigits,ageLookupSiSigDigits)
    floatFormat = '%0.' + str(nDigits) + 'f'
    for line in newFile:
        newLineList = convertReadLineToStringList(line)
        if i == 0:
            keyColNoList = getColNumbers(newLineList,keyVarNameList)
            readColNoList = getColNumbers(newLineList,readVarNameList)
            siColNoList = getColNumbers(newLineList,dataInSiNameList)
            #print keyColNoList,readColNoList,siColNoList
            headerLength = len(newLineList)
            if attachPredValuesToDataIn=='YES':
                newHeader = copy.deepcopy(newLineList)
            else:
                newHeader = append1dListBTo1DListA(keyVarNameList,readVarNameList)
            newHeader.append(newPredSiName)
            newHeader.append(newPredTreeAgeName)
            newHeader.append(newPredOriginName)
            newAgeList.append(newHeader)
            dataMachete.writeListarrayToCSVFile_v3(newAgeList,dataOutPath,dataOutFileName, \
                               floatFormat,defaultFileExtension,True, \
                               True,[])  
        else:
            if not len(newLineList)==headerLength:
                print '\n readWriteTemplate.readLinebyLine()'
                print ' line length:', len(newLineList), 'not the same as file header:', headerLength
                print ' line number:', i+1
                print ' line not included in unique value identification'
            else:
                keyValueList = convertDataStringListToDataTypeList(newLineList, keyTypeList, keyColNoList)
                readValueList = convertDataStringListToDataTypeList(newLineList, readVarTypeList, readColNoList)
                siValueList = convertDataStringListToDataTypeList(newLineList, dataInSiTypeList, siColNoList)
                #print keyValueList, readValueList, siValueList
                treeSp = readValueList[0]
                siTreeSp = spDict[treeSp][siSpeciesXRefFieldName]
                treeHeight = round(readValueList[1], ageLookupDHtSigDigits)
                if ageLookupDHtSigDigits == 0:
                    treeHeight = int(treeHeight)
                siVarName = spDict[treeSp][spDataInSiFieldName]
                siVarColNo = dataInSiNameList.index(siVarName)
                siValue = round(siValueList[siVarColNo],ageLookupSiSigDigits)
                if ageLookupSiSigDigits == 0:
                    siValue = int(siValue)
                ageValue = ageLookupDict [siTreeSp][siValue][treeHeight][ageLookupDTreeAgeFieldName]
                originValue = inventoryYear - ageValue
                if attachPredValuesToDataIn=='YES':
                    newLine = append1dListBTo1DListA(line,[siValue,ageValue,originValue])
                else:
                    newLine = append1dListBTo1DListA(keyValueList,[treeSp,treeHeight,siValue,ageValue,originValue])
                newAgeList.append(newLine)
                #print keyValueList, treeSp, siValue, treeHeight, ageValue, originValue
                #print newAgeList[i]
                
        i = i + 1
        if i == printLines:
             dataMachete.writeListarrayToCSVFile_v3(newAgeList,dataOutPath,dataOutFileName, \
                               floatFormat, defaultFileExtension, False, \
                               False, [])
             newAgeList = [newHeader]
    if len(newAgeList)>1:
        dataMachete.writeListarrayToCSVFile_v3(newAgeList,dataOutPath,dataOutFileName, \
                               floatFormat, defaultFileExtension, False, \
                               False, [])
    return

def ComputeGypsySiteIndex(species = 'Aw', totalHeight = 1.3, bhage = 0, totalAge = 0):
    '''
    Total age is unknown
    Breast height age is known
    Total height is known
    
    Equations and logic derived from:
    Huang, S., Meng, S.X., and Yang, Y. 2009. A growth and yield projection system (GYPSY) for natural and
    post-harvest stands in Alberta. Technical Report Pb. No.:T/216. Forest Management Branch, Alberta Sustainable
    Resource Development, Edmonton, AB, CAN.  Appendix I. Pp. 21,22.

    Error in white spruce equation discovered Dec 5 2014
    
    '''
    tage = totalAge
    si0 = 0
    iterCount = 0
    if totalHeight > 1.3:
        if bhage > 0 or totalAge > 0:
            if species == 'P' or \
               species == 'Pl' or \
               species == 'Pj' or \
               species == 'Pa' or \
               species == 'Pf':
                b1 = 12.84571
                b2 = -5.73936
                b3 = -0.91312
                b4 = 0.150668
                si0 = 10
                si1 = 0
                while abs(si0-si1)>0.00000001:
                    k1 = numpy.exp(b1+b2*(numpy.log(50+1)**0.5) + b3*numpy.log(si0)+b4*(50**0.5))
                    k2 = si0**b3
                    k3 = ((si0)*(1+k1)/1.3-1)/(numpy.exp(b1)*numpy.exp(b4*(50**0.5))*k2)
                    y2bh = numpy.exp((numpy.log(k3)/b2)**2)-1
                    if bhage > 0 and totalAge == 0:
                        tage = bhage + y2bh
                    else:
                        #bhage = 0 and totalGe > 0
                        #tage = totalAge
                        bhage = tage - y2bh
                    x10 = (1+numpy.exp(b1+b2*(numpy.log(tage+1)**0.5)+b3*numpy.log(si0)+b4*(50**0.5)))
                    x20 = (1+numpy.exp(b1+b2*(numpy.log(50+1)**0.5)+b3*numpy.log(si0)+b4*(50**0.5)))
                    si1 = totalHeight*(x10/float(x20))
                    si0 = (si0+si1)/2
                SI_t=si1
                # estimating Site index BH
                k11=1+numpy.exp(b1+b2*(numpy.log(50+1)**0.5)+b3*numpy.log(SI_t)**1+b4*(50**0.5))
                k21= 1+numpy.exp(b1+b2*(numpy.log(50+y2bh+1)**0.5)+b3*numpy.log(SI_t)+b4*(50**0.5))
                SI_bh=SI_t*k11/k21
                
                    
            if species == 'Sw' or \
               species == 'Se' or \
               species == 'Fd' or \
               species == 'Fb' or \
               species == 'Fa':
                b1 = 12.14943
                b2 = -3.77051
                b3 = -0.28534
                b4 = 0.165483
                si0 = 10
                si1 = 0
                while abs(si0-si1)>0.00000001:
                    k1 = numpy.exp(b1+b2*(numpy.log(50**2+1)**0.5) + b3*(numpy.log(si0)**2)+b4*(50**0.5))
                    k2 = si0**(b3*numpy.log(si0))
                    k3 = ((si0)*(1+k1)/1.3-1)/(numpy.exp(b1)*numpy.exp(b4*(50**0.5))*k2)
                    y2bh = (numpy.exp((numpy.log(k3)/b2)**2)-1)**0.5
                    if bhage > 0 and totalAge == 0:
                        tage = bhage + y2bh
                    else:
                        #bhage = 0 and totalGe > 0
                        #tage = totalAge
                        bhage = tage - y2bh
                    #x10 = (1+numpy.exp(b1+b2*(numpy.log((tage**2)+1)**0.5)+b3*(numpy.log(si0)**2)+b4*(50**0.5)))
                    #x20 = (1+numpy.exp(b1+b2*(numpy.log((50**2)+1)**0.5)+b3*(numpy.log(si0)**2)+b4*(50**0.5)))
                    x10 = (1+numpy.exp(b1+b2*((numpy.log((tage**2)+1))**0.5)+b3*(numpy.log(si0)**2)+b4*(50**0.5)))
                    x20 = (1+numpy.exp(b1+b2*((numpy.log((50**2)+1))**0.5)+b3*(numpy.log(si0)**2)+b4*(50**0.5)))
                    si1 = totalHeight*(x10/float(x20))
                    si0 = (si0+si1)/2
                    iterCount = iterCount + 1
                    if iterCount == 1000:
                        print '\n asaCompileAgeGivenSpHt.ComputeGypsySiteIndex()'
                        print ' species:', species, 'totalHeight:', totalHeight, '\n bhage:', \
                              bhage, 'totalAge', totalAge, 'si0:', si0 
                    SI_bh=0
                SI_t=si1
                # estimating Site index BH
                k11=1+numpy.exp(b1+b2*(((numpy.log(50**2+1)))**0.5)+b3*(numpy.log(SI_t))**2+b4*(50**0.5) )
                k21=1+numpy.exp(b1+b2*(numpy.log(1+(50+y2bh)**2)**0.5)+b3*((numpy.log(SI_t))**2)+b4*(50**0.5) )
                SI_bh=SI_t*k11/k21
                
            if species == 'Sb' or \
               species == 'Lt' or \
               species == 'La' or \
               species == 'Lw' or \
               species == 'L':
                b1 = 14.56236
                b2 = -6.04705
                b3 = -1.53715
                b4 = 0.240174
                si0 = 10
                si1 = 0
                while abs(si0-si1)>0.00000001:
                    k1 = numpy.exp(b1+b2*(numpy.log(50+1)**0.5) + b3*numpy.log(si0)+b4*(50**0.5))
                    k2 = si0**b3
                    k3 = ((si0)*(1+k1)/1.3-1)/(numpy.exp(b1)*numpy.exp(b4*(50**0.5))*k2)
                    y2bh = numpy.exp((numpy.log(k3)/b2)**2)-1
                    if bhage > 0 and totalAge == 0:
                        tage = bhage + y2bh
                    else:
                        #bhage = 0 and totalGe > 0
                        #tage = totalAge
                        bhage = tage - y2bh
                    x10 = (1+numpy.exp(b1+b2*(numpy.log(tage+1)**0.5)+b3*numpy.log(si0)+b4*(50**0.5)))
                    x20 = (1+numpy.exp(b1+b2*(numpy.log(50+1)**0.5)+b3*numpy.log(si0)+b4*(50**0.5)))
                    si1 = totalHeight*(x10/float(x20))
                    si0 = (si0+si1)/2
                    SI_bh=0
                SI_t=si1
                # estimating Site index BH
                k11=1+numpy.exp(b1+b2*(numpy.log(50+1)**0.5)+b3*numpy.log(SI_t)+b4*(50**0.5))
                k21=1+numpy.exp(b1+b2*((numpy.log(50+y2bh+1))**0.5)+b3*numpy.log(SI_t)+b4*(50**0.5))
                SI_bh=SI_t*k11/k21
                    
            if species == 'Aw' or \
               species == 'Bw' or \
               species == 'Pb' or \
               species == 'A' or \
               species == 'H':
                b1 = 9.908888
                b2 = -3.92451
                b3 = -0.32778
                b4 = 0.134376
                si0 = 10
                si1 = 0
                while abs(si0-si1)>0.00000001:
                    k1 = numpy.exp(b1+b2*(numpy.log(50+1)**0.5) + b3*(numpy.log(si0)**2)+b4*(50**0.5))
                    k2 = si0**(b3*numpy.log(si0))
                    k3 = ((si0)*(1+k1)/1.3-1)/(numpy.exp(b1)*numpy.exp(b4*(50**0.5))*k2)
                    y2bh = numpy.exp((numpy.log(k3)/b2)**2)-1
                    if bhage > 0 and totalAge == 0:
                        tage = bhage + y2bh
                    else:
                        #bhage = 0 and totalGe > 0
                        tage = totalAge
                        bhage = tage - y2bh
                    x10 = (1+numpy.exp(b1+b2*(numpy.log(tage+1)**0.5)+b3*(numpy.log(si0)**2)+b4*(50**0.5)))
                    x20 = (1+numpy.exp(b1+b2*(numpy.log(50+1)**0.5)+b3*(numpy.log(si0)**2)+b4*(50**0.5)))
                    si1 = totalHeight*(x10/float(x20))
                    si0 = (si0+si1)/2
                    SI_bh=0
                SI_t=si1
                # estimating Site index BH
                SI_bh=SI_t*(1+numpy.exp(b1+b2*(numpy.log(50+1)**0.5)+b3*(numpy.log(SI_t))**2+b4*(50**0.5)))/(1+numpy.exp(b1+b2*(numpy.log(50+y2bh+1)**0.5)+b3*((numpy.log(SI_t))**2)+b4*(50**0.5)))
        else: 
            SI_t = 0
            SI_bh = 0
            y2bh = None
    else:
        SI_t = 0
        SI_bh = 0
        y2bh = None
            
    return bhage, tage, SI_t, y2bh, SI_bh

def ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge(species = 'Aw', siteIndex = 1.3, totalAge = 0):
    '''
    Equations and logic derived from:
    Huang, S., Meng, S.X., and Yang, Y. 2009. A growth and yield projection system (GYPSY) for natural and
    post-harvest stands in Alberta. Technical Report Pb. No.:T/216. Forest Management Branch, Alberta Sustainable
    Resource Development, Edmonton, AB, CAN.  Appendix I. Pp. 21,22.

    Error in white spruce equation discovered Dec 5 2014
    
    '''
    tage = totalAge
    si0 = siteIndex
    treeHeight = 0
    if siteIndex > 1.3:
        if totalAge > 0:
            if species == 'P' or \
               species == 'Pl' or \
               species == 'Pj' or \
               species == 'Pa' or \
               species == 'Pf':
                b1 = 12.84571
                b2 = -5.73936
                b3 = -0.91312
                b4 = 0.150668
                x10 = (1+numpy.exp(b1+b2*(numpy.log(50+1)**0.5)+b3*numpy.log(si0)+b4*(50**0.5)))
                x20 = (1+numpy.exp(b1+b2*(numpy.log(totalAge+1)**0.5)+b3*numpy.log(si0)+b4*(50**0.5)))
                treeHeight = siteIndex*(x10/float(x20))
            if species == 'Sw' or \
               species == 'Se' or \
               species == 'Fd' or \
               species == 'Fb' or \
               species == 'Fa':
                b1 = 12.14943
                b2 = -3.77051
                b3 = -0.28534
                b4 = 0.165483
                #x10 = (1+numpy.exp(b1+b2*(numpy.log((50**2)+1)**0.5)+b3*((numpy.log(si0))**2)+b4*(50**0.5)))
                #x20 = (1+numpy.exp(b1+b2*(numpy.log((totalAge**2)+1)**0.5)+b3*((numpy.log(si0))**2)+b4*(50**0.5)))
                #treeHeight = siteIndex*(x10/float(x20))
                x10 = (1+numpy.exp(b1+b2*((numpy.log((50**2)+1))**0.5)+b3*((numpy.log(si0))**2)+b4*(50**0.5)))
                x20 = (1+numpy.exp(b1+b2*((numpy.log((totalAge**2)+1))**0.5) +b3*((numpy.log(si0))**2)+b4*(50**0.5)))
                treeHeight = siteIndex*(x10/float(x20))               
                
            if species == 'Sb' or \
               species == 'Lt' or \
               species == 'La' or \
               species == 'Lw' or \
               species == 'L':
                b1 = 14.56236
                b2 = -6.04705
                b3 = -1.53715
                b4 = 0.240174
                x10 = (1+numpy.exp(b1+b2*(numpy.log(50+1)**0.5)+b3*numpy.log(si0)+b4*(50**0.5)))
                x20 = (1+numpy.exp(b1+b2*(numpy.log(totalAge+1)**0.5)+b3*numpy.log(si0)+b4*(50**0.5)))
                treeHeight = siteIndex*(x10/float(x20))
            if species == 'Aw' or \
               species == 'Bw' or \
               species == 'Pb' or \
               species == 'A' or \
               species == 'H':
                b1 = 9.908888
                b2 = -3.92451
                b3 = -0.32778
                b4 = 0.134376
                x10 = (1+numpy.exp(b1+b2*(numpy.log(50+1)**0.5)+b3*(numpy.log(si0)**2)+b4*(50**0.5)))
                x20 = (1+numpy.exp(b1+b2*(numpy.log(totalAge+1)**0.5)+b3*(numpy.log(si0)**2)+b4*(50**0.5)))
                treeHeight = siteIndex*(x10/float(x20))
        else:
            treeHeight = 0
    else:
            treeHeight = 0
            
    return treeHeight

def computeTimberProductivityRatingFromSiteIndex(treeSpecies = '', siteIndex = 0):
    '''
    Timber Productivity Ratings (TPR) extracted from Alberta vegetation inventory interpretation
    standards. Version 2.1.1. Chapter 3 - Vegetation inventory standards and
    data model documents. March 2005. Pp. 64-65
    '''
    tpr = ''
    
    if treeSpecies == 'Aw' or \
       treeSpecies == 'Bw' or \
       treeSpecies == 'Pb' or \
       treeSpecies == 'A':
        if siteIndex <= 10.05:
            tpr = 'U'
        else:
            if siteIndex > 10.05 and siteIndex <= 14.05:
                tpr = 'F'
            else:
                if siteIndex > 14.05 and siteIndex <= 18.05:
                    tpr = 'M'
                else:
                    if siteIndex > 18.05 and siteIndex <= 30:
                        tpr = 'G'
                    else:
                        print 'Species', treeSpecies, 'site index', siteIndex, 'exceeds 30 m height at 50 years breast height age'
                        tpr = 'G'
                        
    if treeSpecies == 'Sw' or \
       treeSpecies == 'Se' or \
       treeSpecies == 'Fd' or \
       treeSpecies == 'Fb' or \
       treeSpecies == 'Fa':
        if siteIndex <= 6.05:
            tpr = 'U'
        else:
            if siteIndex > 6.05 and siteIndex <= 10.05:
                tpr = 'F'
            else:
                if siteIndex > 10.05 and siteIndex <= 15.55:
                    tpr = 'M'
                else:
                    if siteIndex > 15.55 and siteIndex <= 25:
                        tpr = 'G'
                    else:
                        print 'Species', treeSpecies, 'site index', siteIndex, 'exceeds 25 m height at 50 years breast height age'
                        tpr = 'G'

    if treeSpecies == 'P' or \
       treeSpecies == 'Pl' or \
       treeSpecies == 'Pj' or \
       treeSpecies == 'Pa' or \
       treeSpecies == 'Pf':
        if siteIndex <= 7.05:
            tpr = 'U'
        else:
            if siteIndex > 7.05 and siteIndex <= 12.05:
                tpr = 'F'
            else:
                if siteIndex > 12.05 and siteIndex <= 16.05:
                    tpr = 'M'
                else:
                    if siteIndex > 16.05 and siteIndex <= 25:
                        tpr = 'G'
                    else:
                        print 'Species', treeSpecies, 'site index', siteIndex, 'exceeds 25 m height at 50 years breast height age'
                        tpr = 'G'

    if treeSpecies == 'Sb' or \
       treeSpecies == 'Lt':
        if siteIndex <= 6.05:
            tpr = 'U'
        else:
            if siteIndex > 6.05 and siteIndex <= 7.05:
                tpr = 'F'
            else:
                if siteIndex > 7.05 and siteIndex <= 10.05:
                    tpr = 'M'
                else:
                    if siteIndex > 10.05 and siteIndex <= 20:
                        tpr = 'G'
                    else:
                        print 'Species', treeSpecies, 'site index', siteIndex, 'exceeds 20 m height at 50 years breast height age'
                        tpr = 'G'
    return tpr

def removeListItemsFromMyList(remList = [], myList=[]):
    '''
    '''
    newList = []
    end_i = len(myList)
    for i in range(0,end_i,1):
        item = myList[i]
        if not item in remList:
            newList.append(item)
    return newList

def getVariableNamesAndValuesForCompilingSiAge(paramDict={}, paramEqTypeField ='EQTYPE', paramAgeSiEqTypeName='AGESI', \
                                               paramNameField = 'PARNAME', paramValueField = 'PARVALUE', \
                                               paramInterceptName = 'INTERCEPT', paramLnSiParamName = 'LNSI_Gp', \
                                               paramLnDomHtParamName = 'LNPHT1Gp'):
    '''
    Parameter Dictionary = {EQTYPE:{PARNAME:{}}}
    A standard name, paramInterceptName, is given to the intercept term.
    A standard name, paramLnSiParamName, is given to the site index term
    A standard name, paramLnDomHtParamName, is given to the site index term
    
    The intercept, site index and dominant height terms (applied to the ln of site index) are considered separately from the remaining parameters
    The remaining parameters (under the paramNameField) refer to actual variable names in the data file
    #
    Return a list of parameter names and associated parameter values excluding the intercept, site index and dominant height terms
    Retrun the intercept value (PARVALUE) associated with the paramInterceptName
    Return the site index value (PARVALUE) associated with the paramLnSiParamName
    Return the dominant tree height value (PARVALUE) associated with the paramLnDomHtParamName

    '''
    newParNameList = []
    newParValueList = []
    interceptValue = 0
    lnSiValue = 0
    lnDHtValue = 0
    if not paramDict.has_key(paramAgeSiEqTypeName):
        print '\n asaCompileAgeGivenSpSiHt.getVariableNamesAndValuesForCompilingSiAge()'
        print ' parameter dictionary does not have paramAgeSisEqTypeName:', paramAgeSiEqTypeName
        print ' cannot compile site index/age equation parameter values'
    else:
        newParNameList = paramDict[paramAgeSiEqTypeName].keys()
        reserveNameList = [paramInterceptName,paramLnSiParamName,paramLnDomHtParamName]
        newParNameList = removeListItemsFromMyList(reserveNameList, newParNameList)
        end_i = len(newParNameList)
        for i in range(0,end_i):
            parName = newParNameList[i]
            parValue = paramDict[paramAgeSiEqTypeName][parName][paramValueField]
            newParValueList.append(parValue)

        if paramDict[paramAgeSiEqTypeName].has_key(paramInterceptName):
            interceptValue = paramDict[paramAgeSiEqTypeName][paramInterceptName][paramValueField]
        else:
            print '\n asaCompileAgeGivenSpSiHt.getVariableNamesAndValuesForCompilingSiAge()'
            print ' no intercept term:', paramInterceptName, 'interceptValue set to 0'
            
        if paramDict[paramAgeSiEqTypeName].has_key(paramLnSiParamName):
            lnSiValue = paramDict[paramAgeSiEqTypeName][paramLnSiParamName][paramValueField]
        else:
            print '\n asaCompileAgeGivenSpSiHt.getVariableNamesAndValuesForCompilingSiAge()'
            print ' no paramLnSiParamName:', paramLnSiParamName, 'lnSiValue set to 0'

        if paramDict[paramAgeSiEqTypeName].has_key(paramLnDomHtParamName):
            lnDHtValue = paramDict[paramAgeSiEqTypeName][paramLnDomHtParamName][paramValueField]
        else:
            print '\n asaCompileAgeGivenSpSiHt.getVariableNamesAndValuesForCompilingSiAge()'
            print ' no paramLnSiParamName:', paramLnDomHtParamName, 'lnDHtValue set to 0'
                                                                                  
    return [newParNameList, newParValueList], [paramInterceptName,interceptValue], \
           [paramLnSiParamName,lnSiValue], [paramLnDomHtParamName, lnDHtValue]
        


def getVariableNamesAndValuesForCompilingSiAge_v2(paramDict={}, paramEqTypeField ='EQTYPE', \
                                                paramNameField = 'PARNAME', paramValueField = 'PARVALUE', \
                                                paramInterceptName = 'INTERCEPT', paramLnConvFName = 'CF', \
                                                paramEqList=['LHSWP','LHPLP','LHAWP','SIPLP','SISWP','SIAWP']):
    '''
    Parameter Dictionary = {EQTYPE:{PARNAME:{}}}
    A standard name, paramInterceptName, is given to the intercept term.
    A standard name, paramLnConvFName, is given to the log transform correction factor (adjusting for bias)
    The paramEqList contains a list of Equation Types ('EQTYPE') where there is a need to get a separation of variables    
    
    The remaining parameters (under the paramNameField) refer to actual variable names in the data file
    #
    Return a list of parameter names and associated parameter values excluding the intercept, site index and dominant height terms
    Retrun the intercept value (PARVALUE) associated with the paramInterceptName
    Return the site index value (PARVALUE) associated with the paramLnSiParamName
    Return the dominant tree height value (PARVALUE) associated with the paramLnDomHtParamName

    '''
    parNameList = []
    parValueList = []
    interceptValueList = []
    correctionValueList = []
    reserveNameList = [paramInterceptName,paramLnConvFName]
    end_i = len(paramEqList)
    for i in range(0,end_i,1):
        eqType = paramEqList[i]
        newParNameList = []
        newParValueList=[]
        if not paramDict.has_key(eqType):
            print '\n asaCompileAgeGivenSpSiHt.getVariableNamesAndValuesForCompilingSiAge_v2()'
            print ' parameter dictionary does not have equation type:', eqType
            print ' cannot compile equationTypeParameter parameter values'
            parNameList.append([])
            interceptValueList.append(0)
            correctionValueList.append(0)
        else:
            newParNameList = paramDict[eqType].keys()
            newParNameList = removeListItemsFromMyList(reserveNameList, newParNameList)
            parNameList.append(copy.deepcopy(newParNameList))
            end_j = len(newParNameList)
            for j in range(0,end_j):
                parName = newParNameList[j]
                parValue = paramDict[eqType][parName][paramValueField]
                newParValueList.append(parValue)
            parValueList.append(copy.deepcopy(newParValueList))
            if paramDict[eqType].has_key(paramInterceptName):
                interceptValue = paramDict[eqType][paramInterceptName][paramValueField]
            else:
                print '\n asaCompileAgeGivenSpSiHt.getVariableNamesAndValuesForCompilingSiAge()'
                print ' no intercept term:', paramInterceptName, 'interceptValue set to 0'
                interceptValue = 0
            interceptValueList.append(interceptValue)
            if paramDict[eqType].has_key(paramLnConvFName):
                paramLnConvFValue = paramDict[eqType][paramLnConvFName][paramValueField]
            else:
                paramLnConvFValue = 1
            correctionValueList.append(paramLnConvFValue)                        
    return parNameList,parValueList,interceptValueList,correctionValueList

def lookupSiteIndexTreeSpecies(originalTreeSpecies = 'NA', siSpeciesXRefFieldName = 'SISP', spDict = {}, spIdFlag = True):
    '''
    '''
    siSp = 'NA'
    if spDict.has_key(originalTreeSpecies):
        if spDict[originalTreeSpecies].has_key(siSpeciesXRefFieldName):
            siSp = spDict[originalTreeSpecies][siSpeciesXRefFieldName]
        else:
            if spIdFlag == True:
                print '\n asaCompileAgeGivenSpSiHt.lookupSiteIndexTreeSpecies()'
                print ' species dictionary does not have siSpeciesXRefFieldName:', siSpeciesXRefFieldName
                print ' Original tree species assigned as site index species:', originalTreeSpecies
            siSp = originalTreeSpecies
    else:
        if spIdFlag == True:
            print '\n asaCompileAgeGivenSpSiHt.lookupSiteIndexTreeSpecies()'
            print ' species dictionary does not have originalTreeSpecies:', originalTreeSpecies
            print ' Original tree species assigned as site index species'
        siSp = originalTreeSpecies
    return siSp, spIdFlag

def getVarValues(newLineList = [], varColNoReadList = [], varReadTypeList = [], myHeader = []):
    '''
    '''
    newValueList = []
    if not len(varColNoReadList)==len(varReadTypeList):
        print '\n asaCompileAgeGivenSpSiHt.lookupSiteIndexTreeSpecies()'
        print ' varColNoReadList not the same length as the varReadTypeList'
        print ' can not correctly type variables in varColnoReadList'
    end_j = len(varColNoReadList)
    for j in range(0,end_j,1):
        colNo = varColNoReadList[j]
        varType = varReadTypeList[j]
        varValue = newLineList[colNo]
        if varType == 'integer':
            varValue = int(varValue)
        else:
            if varType == 'float':
                varValue = float(varValue)
        newValueList.append(varValue)
    return newValueList
                           
def compileSiteIndicesAndAges(dataInFilePath = '', dataInFileName = '', dataInKeyVarNameList = [], dataInKeyTypeList = [], \
                            paramList = [[]], paramTypeList = [], \
                              interceptList = [], lnSiList = [], lnDHtList = [], dataInLeadingSpFieldName = 'SISP1_Gp', \
                              dataInDomTreeHtFieldName = 'PHT1_Gp', spDict = {}, originalSpXRefFieldName = 'ORIGSP', \
                              siSpeciesXRefFieldName = 'SISP', newPredTreeAgeName = 'PHDAGE', newPredSiName = 'PSPSI', \
                              newTprClassName = 'TPR', inventoryYear = 2008, newPredOriginName = 'ORIGIN', \
                              attachPredValuesToDataIn = 'NO', largeDatasetWriteLines = 10000, \
                              dataOutPath = '', dataOutFileName = '', noSigDigits = 9, defaultFileExtension = '.csv'):
    '''
    Inputs
        dataInFilePath              The file path where the dataInFileName is located e.g. E:\Rwd\
        dataInFileName              The name of the file that is to be processed line by line including file extension
        dataInKeyVarNameList        The list of variable name(s) containing that uniquely identify each row
        paramList                   Output from getVariableNamesAndValuesForCompilingSiAge
                                        contains in a list: [newParNameList, newParValueList]
                                        Excludes items in interceptList, lnSiList and lnDHtList
        paramTypeList               Types assigned variable names in newParNameList;
                                        also contained in the dataIn file header            
        interceptList               Output from getVariableNamesAndValuesForCompilingSiAge
                                        contains in a list: [paramInterceptName,interceptValue]
        lnSiList                    Output from getVariableNamesAndValuesForCompilingSiAge
                                        contains in a list: [paramLnSiParamName,lnSiValue]
                                        Coefficient values are applied to ln(si + 1)
        lnDHtList                   Output from getVariableNamesAndValuesForCompilingSiAge
                                        contains in a list: [paramLnDomHtParamName, lnDHtValue]
                                        Coefficient values are applied to ln(si + 1)
        dataInLeadingSpFieldName    The name of the field containing the leading species
        dataInDomTreeHtFieldName    The name of the field containing (untransformed) dominant tree height
        spDict                      A dictionary contianing the dataIn species codes and the species codes
                                        to which the original dataIn species is asigned for the purpose of
                                        determing dominant tree age and site index given dataInDomTreeHt
        originalSpXRefFieldName     Field name in spDict containing a list of leading tree species in the dataInFileName (primary key)
        siSpeciesXRefFieldName      Field name in spDict containing a list of tree species
                                        associated with originalSpXRefFieldName for the purpose of determining dominant tree
                                        age and site index given dataInDomTreeHt
        newPredTreeAgeName          Field name used to indicate the estimated dominant tree age in the output file
        newPredSiName               Field name used to indicate the estimated site index in the output file
        newTprClassName             Field name used to assign the Alberta Timber Productivity Rating Class
        inventoryYear               The date when the inventory was compiled - equal to the date when ground plots were established
                                    Used to compile the year when a stand was initiated, i.e. date of origin
        newPredOriginName           Field name used to indiocate the date of origin in the output file
        attachPredValuesToDataIn    Used to indicate whether the output is to be appended to the datainFileName data ('YES')
                                        or written to a new file ('NO')
        largeDatasetWriteLines      Used to control how many lines of data are stored in memory before printing to file
        dataOutPath                 The file path (excluding file name) to which the data is to be printed
        dataOutFileName             The file name, including file extension, to which the data is to be printed.
        noSigDigits                 The number of significant digits to be used when print float type variables
        defaultFileExtension        The file extension to be used if dataOutFileName does not already have an extension; e.g. .csv

    Output Header Attributes
        dataInKeyVarNameList
        dataInLeadingSpFieldName
        dataInDomTreeHtFieldName
        siSpeciesXRefFieldName
        newPredTreeAgeName
        newPredSiName
        newTprClassName
        newPredOriginName
        
    '''
    newFile = open(dataInFilePath + dataInFileName,'r')
    floatFormat = '%0.' + str(noSigDigits) + 'f'
    dataOutList = []
    i = 0
    for line in newFile:
        newLineList = convertReadLineToStringList(line)
        if i == 0:
            keyColNoList = getColNumbers(newLineList,dataInKeyVarNameList)
            paramColNoList = getColNumbers(newLineList,paramList[0])
            lspColNoList = getColNumbers(newLineList,[dataInLeadingSpFieldName])
            dhtColNoList = getColNumbers(newLineList,[dataInDomTreeHtFieldName])
            spIdFlag = True
            if attachPredValuesToDataIn == 'YES':   #Create new header for print file
                newHeader = copy.deepcopy(newLineList)
                newHeader = append1dListBTo1DListA(newHeader,[siSpeciesXRefFieldName, \
                                newPredTreeAgeName,newPredSiName,newTprClassName, \
                                                              newPredOriginName])
            else:
                newHeader = copy.deepcopy(dataInKeyVarNameList)
                newHeader = append1dListBTo1DListA(newHeader,[dataInLeadingSpFieldName, \
                                dataInDomTreeHtFieldName, siSpeciesXRefFieldName, \
                                newPredTreeAgeName,newPredSiName,newTprClassName, \
                                                              newPredOriginName])
            print newHeader
            dataMachete.writeListarrayToCSVFile_v2([newHeader], dataOutPath, dataOutFileName, \
                               floatFormat, defaultFileExtension, True, \
                               True)
            nKeys = len(dataInKeyVarNameList)
            nParam = len(paramList[0])
            dataOutList.append(newHeader)               #Initialize dataOutList
            headerLength = len(newLineList)
        else:
            if not len(newLineList)==headerLength:
                print '\n asaCompileAgeGivenSpSiHt.compileSiteIndicesAndAges()'
                print ' line length:', len(newLineList), 'not the same as file header:', headerLength
                print ' line number:', i+1
                print ' line not included in processing'
            else:
                keyValueList = getVarValues(newLineList, keyColNoList, dataInKeyTypeList, newHeader)
                eqVarValueList = getVarValues(newLineList, paramColNoList, paramTypeList, newHeader)
                valueVector = numpy.inner(paramList[1], eqVarValueList)
                treeSpList = getVarValues(newLineList, lspColNoList, ['string'], newHeader)
                treeSp = treeSpList[0]
                siSp, spIdFlag = lookupSiteIndexTreeSpecies(treeSp, siSpeciesXRefFieldName, spDict, spIdFlag) 
                domHtList = getVarValues(newLineList, dhtColNoList, ['float'], newHeader)
                domHt = domHtList[0]
                htDiffFlag = False
                predSi = 15
                while htDiffFlag == False:
                    #print lnDHtList, lnSiList, interceptList
                    predAge = numpy.exp(valueVector + numpy.log(domHt+1)* lnDHtList[1] + numpy.log(predSi+1)* lnSiList[1] + interceptList[1])-1
                    newHt = ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge(siSp, predSi, predAge)
                    #print 'Key',keyValueList[0]
                    #print 'EqVal', eqVarValueList
                    #print 'Param', paramList[1]
                    #print 'Value', valueVector
                    #print treeSp
                    #print siSp
                    if abs(domHt-newHt) < 0.0001:
                        htDiffFlag = True
                        predAge = int(round(predAge,0))
                        predSi = round(predSi,2)
                    else:
                        predSi = ((domHt-newHt)/domHt)*predSi + predSi
                        #print domHt, newHt
                        #print predAge, predSi
                predOrigin = inventoryYear - predAge
                predTpr = computeTimberProductivityRatingFromSiteIndex(siSp, predSi)
                if attachPredValuesToDataIn == 'YES':
                    newList = copy.deepcopy(newLineList)
                    newList = append1dListBTo1DListA(newList,[siSp, \
                                predAge,predSi,predTpr,predOrigin])
                else:
                    newList = copy.deepcopy(keyValueList)
                    newList = append1dListBTo1DListA(newList,[treeSp, \
                                domHt,siSp,predAge,predSi,predTpr,predOrigin])
                print newList
                dataOutList.append(newList)
    
                    
        
                
                                          
        i = i + 1
    return 

def compileSiteIndicesAndAges_v2(dataInFilePath = '', dataInFileName = '', dataInKeyVarNameList = [], dataInKeyTypeList = [], \
                            uniqueParNameList = [], uniqueParNumberList = [[]], uniqueParTypeList = [], parEqList=[], \
                            parNameList = [[]], parValueList=[[]], interceptList = [], correctionValueList = [], \
                            dataInLeadingSpFieldName = 'PSP1', parDict = {}, spDict = {}, originalSpXRefFieldName = 'ORIGSP', \
                            siSpeciesXRefFieldName = 'SISP', newPredSiSpName = 'PSISPP', \
                            newPredTreeHtName = 'PHTP', newPredTreeAgeName = 'PAGEP', newPredSiName = 'PSIP', \
                            newTprClassName = 'TPR', inventoryYear = 2011, newPredOriginName = 'ORIGIN', \
                            attachPredValuesToDataIn = 'NO', largeDatasetWriteLines = 10000, \
                            dataOutPath = '', dataOutFileName = '', noSigDigits = 9, defaultFileExtension = '.csv'):
    '''
    Inputs
        dataInFilePath              The file path where the dataInFileName is located e.g. E:\Rwd\
        dataInFileName              The name of the file that is to be processed line by line including file extension
        dataInKeyVarNameList        The list of variable name(s) containing that uniquely identify each row
        dataInKeyTypeList           A list of variable types associated with each of the variables in the dataInKeyVarNameList
        uniqueParNameList           A unique list of the variables to be read from each line
        uniqueParNumberList         The variable number in the uniqueParName List assigned to each of the variables in the
                                        paramNameList
        uniqueParTypeList           The variable types associated with each parameter name in the uniqueParNameList
        parEqList                   The names of equation types with variable names that need to be extracted from the input data
        parNameList                 The names of parameters associated with each of the equation types listed in the paramEqList
                                        encluding intercepts and natural log correction factors
        parValueList                The parameter values to be multiplied by the variable values wehere the variable names are the
                                        same as those listed in the parNameList
        parTypeList                 Types assigned variable names in newParNameList;
                                        also contained in the dataIn file header            
        interceptList               A list of intercept values associated with each of the equation types in parEqList
        correctionValueList         A list of correction factors to multiply (adjust) by the final calculated value
                                        associated with each of the equation types in the parEqList; note that this
                                        is primarilly for the purpose of correcting for bias following from the natural
                                        log transformation.
        parDict                     The parameter dictionary containing all of the equations, parameter names and parameter
                                        values including those required to make adjustments to lodgepole pine site index,
                                        height and age (these adjustments are hard coded into this routine).
        spDict                      A dictionary contianing the dataIn species codes and the species codes
                                        to which the original dataIn species is asigned for the purpose of
                                        determing dominant tree age and site index given dataInDomTreeHt
        originalSpXRefFieldName     Field name in spDict containing a list of leading tree species in the dataInFileName (primary key)
        siSpeciesXRefFieldName      Field name in spDict containing a list of tree species
                                        associated with originalSpXRefFieldName for the purpose of determining dominant tree
                                        age and site index given dataInDomTreeHt
        newPredSiSpName
        newPredTreeHtName
        newPredTreeAgeName          Field name used to indicate the estimated dominant tree age in the output file
        newPredSiName               Field name used to indicate the estimated site index in the output file
        newTprClassName             Field name used to assign the Alberta Timber Productivity Rating Class
        inventoryYear               The date when the inventory was compiled - equal to the date when ground plots were established
                                    Used to compile the year when a stand was initiated, i.e. date of origin
        newPredOriginName           Field name used to indiocate the date of origin in the output file
        attachPredValuesToDataIn    Used to indicate whether the output is to be appended to the datainFileName data ('YES')
                                        or written to a new file ('NO')
        largeDatasetWriteLines      Used to control how many lines of data are stored in memory before printing to file
        dataOutPath                 The file path (excluding file name) to which the data is to be printed
        dataOutFileName             The file name, including file extension, to which the data is to be printed.
        noSigDigits                 The number of significant digits to be used when print float type variables
        defaultFileExtension        The file extension to be used if dataOutFileName does not already have an extension; e.g. .csv

    Output Header Attributes
        dataInKeyVarNameList
        dataInLeadingSpFieldName
        dataInDomTreeHtFieldName
        siSpeciesXRefFieldName
        newPredTreeAgeName
        newPredSiName
        newTprClassName
        newPredOriginName
        
    '''
    newFile = open(dataInFilePath + dataInFileName,'r')
    floatFormat = '%0.' + str(noSigDigits) + 'f'
    dataOutList = []
    printLines = largeDatasetWriteLines
    i = 0
    for line in newFile:
        newLineList = convertReadLineToStringList(line)
        if i == 0:
            keyColNoList = getColNumbers(newLineList,dataInKeyVarNameList)
            dataColNoList = getColNumbers(newLineList,uniqueParNameList)
            lspColNoList = getColNumbers(newLineList,[dataInLeadingSpFieldName])
            spIdFlag = True
            if attachPredValuesToDataIn == 'YES':   #Create new header for print file
                newHeader = copy.deepcopy(newLineList)
            else:
                newHeader = copy.deepcopy(dataInKeyVarNameList)
            newHeader = append1dListBTo1DListA(newHeader,[newPredSiSpName,newPredOriginName, \
                                newPredTreeHtName,newPredTreeAgeName,newPredSiName,newTprClassName])
            #print newHeader
            dataMachete.writeListarrayToCSVFile_v2([newHeader], dataOutPath, dataOutFileName, \
                               floatFormat, defaultFileExtension, True, \
                               True)
            nKeys = len(dataInKeyVarNameList)
            nParam = len(uniqueParNameList)
            dataOutList.append(newHeader)               #Initialize dataOutList
            headerLength = len(newLineList)
        else:
            if not len(newLineList)==headerLength:
                print '\n asaCompileAgeGivenSpSiHt.compileSiteIndicesAndAges()'
                print ' line length:', len(newLineList), 'not the same as file header:', headerLength
                print ' line number:', i+1
                print ' line not included in processing'
            else:
                keyValueList = getVarValues(newLineList, keyColNoList, dataInKeyTypeList, newHeader)
                uniqueVarValueList = getVarValues(newLineList, dataColNoList, uniqueParTypeList, newHeader)
                treeSpList = getVarValues(newLineList, lspColNoList, ['string'], newHeader)
                treeSp = treeSpList[0]
                siSp, spIdFlag = lookupSiteIndexTreeSpecies(treeSp, siSpeciesXRefFieldName, spDict, spIdFlag)
                maxTreeAge = maxTreeSpeciesAge(siSp)
                #print keyValueList[0]
                treeHt, treeSi, treeAge = computeTreeHeightSiteIndexAndAge(siSp,parEqList,parValueList,uniqueVarValueList,uniqueParNumberList, \
                                                               interceptList, correctionValueList, parDict, maxTreeAge, i)
                
                predOrigin = int(round(inventoryYear - treeAge,0))
                predTpr = computeTimberProductivityRatingFromSiteIndex(siSp, treeSi)
                #print keyValueList[0], siSp, predOrigin, treeHt, treeAge, treeSi, predTpr
                if attachPredValuesToDataIn == 'YES':
                    newList = copy.deepcopy(newLineList)
                else:
                    newList = copy.deepcopy(keyValueList)
                newList = append1dListBTo1DListA(newList,[siSp, \
                                predOrigin,treeHt, treeAge, treeSi, predTpr])
                    
                dataOutList.append(newList)                  
        i = i + 1
        if i == printLines:
            print printLines, time.ctime()
            dataMachete.writeListarrayToCSVFile_v3(dataOutList, dataOutPath, dataOutFileName, \
                               floatFormat, defaultFileExtension, False, \
                               False)
            dataOutList = [newHeader]
            printLines = printLines + largeDatasetWriteLines
            
    if len(dataOutList)>1:
        dataMachete.writeListarrayToCSVFile_v3(dataOutList, dataOutPath, dataOutFileName, \
                               floatFormat, defaultFileExtension, False, \
                               False)
    return 

def getVarValuesGivenColNo(colNoList = [],varValueList = []):
    '''
    '''
    newList = []
    nCols = len(colNoList)
    for x in range(0,nCols):
        colNo = colNoList[x]
        varValue = varValueList[colNo]
        newList.append(varValue)
    return newList

def computeTreeAge(siSp='',treeHt = 20, treeSi=15, maxTreeAge = 450, rowIndex = 0, printWarnings = True):
    '''
    '''
    treeAge = (treeHt/treeSi)*25
    htDiffFlag = False
    iterCount = 0
    acceptableDiff = 0.0001 
    while htDiffFlag == False:
        newHt = ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge(siSp, treeSi, treeAge)
        if abs(treeHt-newHt) < acceptableDiff:
            htDiffFlag = True
        else:
            #print treeHt, newHt, treeAge
            #treeAge = ((treeHt-newHt)/treeHt)*(treeAge/2) + treeAge
            treeAge = ((treeHt-newHt)/treeHt)*(treeAge) + treeAge
        iterCount = iterCount + 1
            
        if iterCount == 150 and printWarnings == True:
            print '\n asaCompileAgeGivenSpSiHt.computeTreeAge()'
            print ' Slow convergence'
            print ' rowIndex:', rowIndex, 'siSp:', siSp, 'treeHt:', treeHt, 'treeSi:', treeSi, 'current treeAge:', treeAge
        if treeAge > 1000:
            htDiffFlag = True
            if printWarnings == True:
                print '\n asaCompileAgeGivenSpSiHt.computeTreeAge()'
                print ' Tree Age Search Routine Terminated; treeAge > 1000'
                print ' rowIndex:', rowIndex, 'siSp:', siSp, 'treeHt:', treeHt, 'treeSi:', treeSi, 'current treeAge:', treeAge
    return treeAge

def adjustSiHtToMeetTreeAge(siSp='Pl',treeAge=90,treeHt=15,treeSi=15,adjHt=1,adjSi=3):
    '''
    '''
    htDiffFlag = False
    refHt = treeHt + (treeHt)*adjHt
    refSi = treeSi + (treeSi)*adjSi
    prevRatio = 0
    #print treeHt, refHt, treeSi, refSi
    while htDiffFlag == False:
        newHt = ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge(siSp, refSi, treeAge)
        htRatio = (newHt)/refHt
        #print treeHt, refHt, newHt, htRatio, treeSi, refSi, treeAge
        if abs(htRatio) < 1.01 and htRatio > 0.99:
            htDiffFlag = True
        else:
            if not prevRatio==0 and abs(prevRatio-htRatio)>0.0000001:
                htDiffFlag = True
            else:
                refSi = treeSi + htRatio*(treeSi)*adjSi
                prevRatio = htRatio
            #refHt = treeHt + htRatio*(treeHt)*adjHt
    treeHt = newHt
    treeSi = refSi
    return treeHt, treeSi



def computeTreeHeightSiteIndexAndAge(siSp='Pl',parEqList=['LHSWP','LHPLP','LHAWP','SIPLP','SISWP','SIAWP'], \
                                parValueList =[[]],uniqueVarValueList=[],uniqueParNumberList=[[]], \
                                interceptList = [], correctionValueList = [], parDict = {}, maxTreeAge = 450, rowIndex = 0):
    '''
    '''
    treeHt = 0
    treeSi = 0
    treeAge = 0
    if siSp == 'Aw' or \
       siSp == 'Bw' or \
       siSp == 'Pb' or \
       siSp == 'A':
        spHtNo = parEqList.index('LHAWP')
        spSiNo = parEqList.index('SIAWP')
    else:
        if siSp == 'P' or \
           siSp == 'Pl' or \
           siSp == 'Pj' or \
           siSp == 'Pa' or \
           siSp == 'Pf':
            spHtNo = parEqList.index('LHPLP')
            spSiNo = parEqList.index('SIPLP')
        else:
            spHtNo = parEqList.index('LHSWP')
            spSiNo = parEqList.index('SISWP')
    #Calculate tree height
    htParValues = parValueList[spHtNo]
    htVarColNos = uniqueParNumberList[spHtNo]
    htVarValues = getVarValuesGivenColNo(htVarColNos,uniqueVarValueList)
    intercept = interceptList[spHtNo]
    correction = correctionValueList[spHtNo]
    treeHt = (numpy.exp(numpy.inner(htParValues,htVarValues)+intercept)-1)*correction
    treeHt = checkMaximumHeight(siSp, treeHt, maxTreeAge)
    #Calculate tree site index
    siParValues = parValueList[spSiNo]
    siVarColNos = uniqueParNumberList[spSiNo]
    siVarValues = getVarValuesGivenColNo(siVarColNos,uniqueVarValueList)
    intercept = interceptList[spSiNo]
    treeSi = numpy.inner(siParValues,siVarValues)+intercept
    #Check for blank
    if treeSi == '':
        print '\n asaCompileAgeGivenSpSiHt.computeTreeHeightSiteIndexAndAge()'
        print ' treeSi blank; rowIndex:', rowIndex
        print '\n siParValues:', siParValues
        print '\n siVarValues:', siVarValues
    #Check minimum and maximum site indices
    treeSi = checkMinimumSiteIndices(siSp, treeSi)
    treeSi = checkInitialMaximumSiteIndices(siSp, treeSi)
    if treeHt <= 1.3:
        treeAge = computeAgesForTreesAtOrBelowBreastHeight(siSp, treeHt)
    else:
        treeAge = computeTreeAge(siSp,treeHt, treeSi, maxTreeAge, rowIndex)
    #If si below max and tree age > max reduce age to max 
    if treeAge > maxTreeAge:
        #site index is assumed to be under-estimated and tree height over-estimated;
        #Use mid point between height given maxTreeAge and site index and original tree height
        #Then recalculate site index accordingly
        oldHt = treeHt
        treeHt = (ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge(siSp, treeSi, maxTreeAge)+oldHt)/float(2)
        bhage, treeAge, treeSi = ComputeGypsySiteIndex(siSp, treeHt, 0, maxTreeAge)
    else:
        #If spSi is PL then some adjustments are required:
        if siSp == 'P' or \
            siSp == 'Pl' or \
            siSp == 'Pj' or \
            siSp == 'Pa' or \
            siSp == 'Pf':
            treeSi = parDict['ESIPL']['INTERCEPT']['PARCOEF']+parDict['ESIPL']['HPLP']['PARCOEF']*treeHt + treeSi
            treeHt = parDict['EHPL']['INTERCEPT']['PARCOEF']+parDict['EHPL']['AGEPL']['PARCOEF']*treeAge + treeHt
            treeHt = checkMaximumHeight(siSp, treeHt, maxTreeAge)
            treeSi = checkMinimumSiteIndices(siSp, treeSi)
            treeSi = checkInitialMaximumSiteIndices(siSp, treeSi)
            treeAge = computeTreeAge(siSp,treeHt, treeSi, rowIndex)
            if treeSi == '':
                print '\n asaCompileAgeGivenSpSiHt.computeTreeHeightSiteIndexAndAge()'
                print ' treeSi blank; rowIndex:', rowIndex
                print ' Failure to apply first correction to treeSi'
            treeSi = checkMinimumSiteIndices(siSp, treeSi)
            #Constrain adjustments to a minimum associated with a maximum tree age of 150 years 
            if treeAge > 150:
                myTreeAge = 150
            else:
                myTreeAge = treeAge
            ageMultiplier = (parDict['EAPL']['INTERCEPT']['PARCOEF']+parDict['EAPL']['AGEPL1']['PARCOEF']*myTreeAge)
            treeAge = treeAge + ageMultiplier*myTreeAge
            treeHtAdj = (parDict['WHTPL']['WHTPL']['PARCOEF']*ageMultiplier)
            treeSiAdj = (parDict['WSIPL']['WSIPL']['PARCOEF']*ageMultiplier)
            if treeHtAdj + treeHt <= 1.3:
                #Tree height is below breast height
                treeAge = computeAgesForTreesAtOrBelowBreastHeight(siSp, treeHt)
                treeSi = checkMinimumSiteIndices(siSp, treeSi)
            else:
                #print parDict['WHTPL']['WHTPL']['PARCOEF'],parDict['WSIPL']['WSIPL']['PARCOEF'], ageMultiplier
                if treeAge > maxTreeAge:
                    #Compute site index from height and maximum tree age
                    bhage, treeAge, treeSi = ComputeGypsySiteIndex(siSp, treeHt, 0, maxTreeAge)
                    print '\n asaCompileAgeGivenSpSiHt.computeTreeHeightSiteIndexAndAge()'
                    print ' Pl site index estimated from height and maximum tree age'
                    print ' rowIndex:', rowIndex, 'treeHt:', treeHt, 'treeAge:', treeAge, 'treeSi:', treeSi
                else:
                    treeHt, treeSi = adjustSiHtToMeetTreeAge(siSp,treeAge,treeHt,treeSi,treeHtAdj,treeSiAdj)
    
    treeSi, treeAge, treeHt = checkMaximumSiteIndices(siSp, treeSi, treeHt, treeAge, rowIndex, maxTreeAge)
    treeAge = int(round(treeAge,0))
    treeSi = round(treeSi,2)
    treeHt = round(treeHt,1)
    return treeHt, treeSi, treeAge

def maxTreeSpeciesAge(mySp = ''):
    '''
    '''
    maxTreeAge = 450
    if mySp == 'Aw' or \
       mySp == 'Bw' or \
       mySp == 'A':
        maxTreeAge = 120
    else:
        if mySp == 'Pb':
            maxTreeAge = 200
        else:
            if mySp == 'P' or \
               mySp == 'Pl' or \
               mySp == 'Pj' or \
               mySp == 'Pa' or \
               mySp == 'Pf' or \
               mySp == 'Lt':
                maxTreeAge = 250
            #else:
                #if mySp == 'Sw' or \
                #   mySp == 'Sb' or \
                #   mySp == 'Se' or \
                #   mySp == 'Fd' or \
                #   mySp == 'Fb' or \
                #   mySp == 'Fa':
                #    maxTreeAge = 450
    return maxTreeAge

def checkMinimumSiteIndices(siSp = '', treeSi = 0):
    '''
    '''
    #Check minimum site indices
    if siSp == 'Aw' or \
       siSp == 'Bw' or \
       siSp == 'Pb' or \
       siSp == 'A':
        if treeSi < 5:
            treeSi = 5
    else:
        if siSp == 'P' or \
           siSp == 'Pl' or \
           siSp == 'Pj' or \
           siSp == 'Pa' or \
           siSp == 'Pf':
            if treeSi < 3:
                treeSi = 3
        else:
            if siSp == 'Sw' or \
               siSp == 'Fd' or \
               siSp == 'Fb' or \
               siSp == 'Fa':
                if treeSi < 3:
                    treeSi = 3
            else:
                if siSp == 'Sb' or \
                   siSp == 'Lt':
                    if treeSi < 1:
                        treeSi = 1
                else:
                    if treeSi < 1:
                        treeSi = 1
    return treeSi

def computeAgesForTreesAtOrBelowBreastHeight(siSp = '', treeHt = 1.3):
    '''
    A linear interpolation of age with years to breast height
    based on Table 3-10 (p. 20) of the following:

    Alberta Sustainable Resource Development. 2005. Alberta
    vegetation inventory interpretation standards. Version 2.1.1
    March 2005. Chapter 3 - Vegetation inventory standards and
    data model documents. Resource Information Management Branch,
    Albrta Sustainable Resource Development, Edmonton, AB.
    
    '''
    if treeHt <= 0:
        age = 0
    else:
        if siSp == 'Aw' or \
           siSp == 'Bw' or \
           siSp == 'Pb' or \
           siSp == 'A':
            age = treeHt/1.3 * 6
        
        else:
            if siSp == 'P' or \
               siSp == 'Pl' or \
               siSp == 'Pj' or \
               siSp == 'Pa' or \
               siSp == 'Pf':
                age = treeHt/1.3 * 10
            
            else:
                if siSp == 'Sw' or \
                   siSp == 'Fd' or \
                   siSp == 'Fb' or \
                   siSp == 'Fa' or \
                   siSp == 'Lt':
                    age = treeHt/1.3 * 15
                else:
                    if siSp == 'Sb':
                        age = treeHt/1.3 * 20
                    else:
                        age = treeHt/1.3 * 15
    return age 

def checkMaximumSiteIndices(siSp = '', treeSi = 15, treeHt = 15, treeAge = 50, rowIndex = 0, maxTreeAge = 450):
    '''
    Timber Productivity Ratings (TPR) extracted from Alberta vegetation inventory interpretation
    standards. Version 2.1.1. Chapter 3 - Vegetation inventory standards and
    data model documents. March 2005. Pp. 64-65
    '''
    if siSp == 'Aw' or \
       siSp == 'Bw' or \
       siSp == 'Pb' or \
       siSp == 'A':
        if treeSi > 30:
            treeSi = 30
            if treeHt > 1.3:
                treeAge = computeTreeAge(siSp,treeHt,treeSi, 450, rowIndex)
                if treeAge > maxTreeAge:
                    treeAge = maxTreeAge
                    treeHt = ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge(siSp, treeSi, treeAge)
    if siSp == 'Sw' or \
       siSp == 'Se' or \
       siSp == 'Fd' or \
       siSp == 'Fb' or \
       siSp == 'Fa':
        if treeSi > 25:
            treeSi = 25
            if treeHt > 1.3:
                treeAge = computeTreeAge(siSp,treeHt,treeSi, 450, rowIndex)
                if treeAge > maxTreeAge:
                    treeAge = maxTreeAge
                    treeHt = ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge(siSp, treeSi, treeAge)

    if siSp == 'P' or \
       siSp == 'Pl' or \
       siSp == 'Pj' or \
       siSp == 'Pa' or \
       siSp == 'Pf':
        if treeSi > 25:
            treeSi = 25
            if treeHt > 1.3:
                treeAge = computeTreeAge(siSp,treeHt,treeSi, 450, rowIndex)
                if treeAge > maxTreeAge:
                    treeAge = maxTreeAge
                    treeHt = ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge(siSp, treeSi, treeAge)

    if siSp == 'Sb' or \
       siSp == 'Lt':
        if treeSi > 20:
            treeSi = 20
            if treeHt > 1.3:
                treeAge = computeTreeAge(siSp,treeHt,treeSi, 450, rowIndex)
                if treeAge > maxTreeAge:
                    treeAge = maxTreeAge
                    treeHt = ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge(siSp, treeSi, treeAge)
    return treeSi, treeAge, treeHt

def checkInitialMaximumSiteIndices(siSp = '', treeSi = 15):
    '''
    Timber Productivity Ratings (TPR) extracted from Alberta vegetation inventory interpretation
    standards. Version 2.1.1. Chapter 3 - Vegetation inventory standards and
    data model documents. March 2005. Pp. 64-65
    '''
    if siSp == 'Aw' or \
       siSp == 'Bw' or \
       siSp == 'Pb' or \
       siSp == 'A':
        if treeSi > 30:
            treeSi = 30
            
    if siSp == 'Sw' or \
       siSp == 'Se' or \
       siSp == 'Fd' or \
       siSp == 'Fb' or \
       siSp == 'Fa':
        if treeSi > 25:
            treeSi = 25
            
    if siSp == 'P' or \
       siSp == 'Pl' or \
       siSp == 'Pj' or \
       siSp == 'Pa' or \
       siSp == 'Pf':
        if treeSi > 25:
            treeSi = 25
            
    if siSp == 'Sb' or \
       siSp == 'Lt':
        if treeSi > 20:
            treeSi = 20
    return treeSi

def checkMaximumHeight(siSp = '', treeHt = 15, maxTreeAge = 450):
    '''
    Timber Productivity Ratings (TPR) extracted from Alberta vegetation inventory interpretation
    standards. Version 2.1.1. Chapter 3 - Vegetation inventory standards and
    data model documents. March 2005. Pp. 64-65
    '''
    maxSi = 30
    if siSp == 'Aw' or \
       siSp == 'Bw' or \
       siSp == 'Pb' or \
       siSp == 'A':
        maxSi = 30                               
    if siSp == 'Sw' or \
       siSp == 'Se' or \
       siSp == 'Fd' or \
       siSp == 'Fb' or \
       siSp == 'Fa':
        maxSi = 25
    if siSp == 'P' or \
       siSp == 'Pl' or \
       siSp == 'Pj' or \
       siSp == 'Pa' or \
       siSp == 'Pf':
        maxSi = 25    
    if siSp == 'Sb' or \
       siSp == 'Lt':
        maxSi = 20
    maxHt = ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge(siSp, maxSi, maxTreeAge)
    if maxHt < treeHt:
        treeHt = maxHt
    return treeHt

def checkCompilationOfHeightSiteIndexAndAge(siSp = '', domHt = 3, domAge = 50, siteIndex = 15, \
                                 minAge = 1, maxAge = 450, minSiteIndex = 3,
                                 maxSiteIndex = 30, minDomTreeHeight = 1.3):
    '''
    A constrained search for compatable height, site index and age
    Note that the site index does not converge properly 
    '''
    oldAge = domAge
    oldHt = domHt
    oldSi = siteIndex
        
    #Get maximum tree height given maximum site index and age
    maxHt = ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge(siSp, maxSiteIndex, maxAge)
    
    maxIterations = 100
    iterInc = maxIterations
    
    diffFlag = False
    ageFlag = False
    htFlag = False
    siFlag = False
    
    i = 0
    
    #Start constrained search
    while diffFlag == False:
        #Ensure tree age is within reasonable limits
        if oldAge > maxAge:
            oldAge = maxAge
        else:
            if oldAge < 1:
                oldAge = 1

        #Ensure dominant tree height within reasonable limits
        if oldHt > maxHt:
            oldHt = maxHt
        else:
            if oldHt < minDomTreeHeight:
                oldHt = minDomHt

        #Ensure that site index is within reasonable limits
        if oldSi < minSiteIndex:
            oldSi = minSiteIndex
        else:
            if oldSi > maxSiteIndex:
                oldSi = maxSiteIndex

        #print oldAge, oldHt, oldSi

        bhage, tage, newSi = ComputeGypsySiteIndex(siSp, oldHt, 0, oldAge)
        if newSi < minSiteIndex:
            newSi = minSiteIndex
        else:
            if newSi > maxSiteIndex:
                newSi = maxSiteIndex

        newAge = computeTreeAge(siSp, oldHt, newSi, maxAge, 0)
        if newAge > maxAge:
            newAge = maxAge
        else:
            if newAge < 1:
                newAge = 1


        newHt = ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge(siSp, newSi, newAge)
        if newHt > maxHt:
            newHt = maxHt
        else:
            if newHt < minDomTreeHeight:
                newHt = minDomHt

        

        #print newAge, newHt, newSi

        #Check for convergence
        #if abs(newAge - oldAge) < 0.25: ageFlag = True 
        #if abs(newHt-oldHt) < 0.01: htFlag = True
        #if abs(newSi-oldSi) < 0.01: siFlag = True
        #if not False in [ageFlag, htFlag, siFlag]:
        #       diffFlag = False
        diffFlag = True      
        #oldAge = (oldAge + newAge)/float(2)
        #oldHt = (oldHt + newHt)/float(2)
        #oldSi = (oldSi + newHt)/float(2)
        #i = i + 1
               
        #Track the number of iterations to converge; report slow convergence
        if i > maxIterations:
               print '\n asaCompileAgeGivenSpSiHt.iterativeCompilationOfHeightSiteIndexAndAge()'
               print ' slow convergence ...', i, 'iterations'
               print ' oldAge:', oldAge, 'newAge:', newAge
               print ' oldHt:', oldHt, 'newHt:', newHt
               print ' oldSi:', oldSi, 'newSi:', newSi
               maxIterations = maxIterations + iterInc
               
    return newAge, newHt, newSi

def checkCompilationOfHeightSiteIndexAndAge_v2(siSp = '', domHt = 3, domAge = 50, siteIndex = 15, \
                                 minAge = 1, maxAge = 450, minSiteIndex = 3,
                                 maxSiteIndex = 30, minDomTreeHeight = 1.3):
    '''
    A constrained search for compatable height, site index and age
    Note that the site index does not converge properly 
    '''
    oldAge = domAge
    oldHt = domHt
    oldSi = siteIndex
        
    #Get maximum tree height given maximum site index and age
    maxHt = ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge(siSp, maxSiteIndex, maxAge)
       
    i = 0
    
    #Ensure dominant tree height within reasonable limits
    if oldHt > maxHt:
        oldHt = maxHt
    else:
        if oldHt < minDomTreeHeight:
            oldHt = minDomHt

    #Ensure that site index is within reasonable limits
    if oldSi < minSiteIndex:
        oldSi = minSiteIndex
    else:
        if oldSi > maxSiteIndex:
            oldSi = maxSiteIndex

    #print oldAge, oldHt, oldSi

    newAge = computeTreeAge(siSp, oldHt, oldSi, maxAge, 0)
    if newAge > maxAge:
        newAge = maxAge
    else:
        if newAge < 1:
            newAge = 1
               
    return newAge, oldHt, oldSi


def computeAviBhageFromTotalAge(species = 'Aw', totalAge = 0, bhage = 0):
    '''
    Breast height age formula's extracted from Alberta vegetation inventory interpretation
    standards. Version 2.1.1. Chapter 3 - Vegetation inventory standards and
    data model documents. March 2005. Pp. 20.
    '''
    if species == 'Aw' or \
       species == 'Bw' or \
       species == 'Pb' or \
       species == 'A' or \
       species == 'H':
        if totalAge > 0 and bhage == 0:
            bhage = totalAge - 6
        else:
            totalAge = bhage + 6
    if species == 'Sw' or \
       species == 'Se' or \
       species == 'Fd' or \
       species == 'Fb' or \
       species == 'Fa' or \
       species == 'Lt' or \
       species == 'La' or \
       species == 'Lw' or \
       species == 'L':
        if totalAge > 0 and bhage == 0:
            bhage = totalAge - 15
        else:
            totalAge = bhage + 15
    if species == 'P' or \
       species == 'Pl' or \
       species == 'Pj' or \
       species == 'Pa' or \
       species == 'Pf':
        if totalAge > 0 and bhage == 0:
            bhage = totalAge - 10
        else:
            totalAge = bhage + 10
    if species == 'Sb':
        if totalAge > 0 and bhage == 0:
            bhage = totalAge - 20
        else:
            totalAge = bhage + 20
    if bhage < 0:
        bhage = 0
    if totalAge < 0:
        totalAge = 0
    return bhage, totalAge


def ComputeAviSiteIndex(species = 'Aw', bhage = 1, treeHeight = 2):
    '''
    Site index formula's extracted from Alberta vegetation inventory interpretation
    standards. Version 2.1.1. Chapter 3 - Vegetation inventory standards and
    data model documents. March 2005. Pp. 64-65
    '''
    siteIndex = 0
    newTreeHeight = treeHeight - 1.3
    if newTreeHeight > 0 and bhage > 0:
        if species == 'Aw' or \
           species == 'Bw' or \
           species == 'Pb' or \
           species == 'A' or \
           species == 'H':
            siteIndex = 1.3 + 17.0100096 \
                            + 0.878406*(newTreeHeight) \
                            + 1.836354*numpy.log(bhage) \
                            - 1.401817*(numpy.log(bhage))**2 \
                            + 0.437430*numpy.log(newTreeHeight)/float(bhage)
        if species == 'Sw' or \
           species == 'Se' or \
           species == 'Fd' or \
           species == 'Fb' or \
           species == 'Fa':
            siteIndex = 1.3 + 10.398053 \
                            + 0.324415*(newTreeHeight) \
                            + 0.00599608*numpy.log(bhage)*bhage \
                            - 0.838036*(numpy.log(bhage))**2 \
                            + 27.487397*(newTreeHeight)/float(bhage) \
                            + 1.191405*(numpy.log(newTreeHeight))
        if species == 'P' or \
           species == 'Pl' or \
           species == 'Pj' or \
           species == 'Pa' or \
           species == 'Pf':
            siteIndex = 1.3 + 10.940796 \
                            + 1.675298 *(newTreeHeight) \
                            - 0.932222*(numpy.log(bhage))**2 \
                            + 0.005439671*numpy.log(bhage)*bhage \
                            + 8.228059*(newTreeHeight)/float(bhage) \
                            - 0.256865*(newTreeHeight)*numpy.log(newTreeHeight)
        if species == 'Sb' or \
           species == 'Lt' or \
           species == 'La' or \
           species == 'Lw' or \
           species == 'L':
            siteIndex = 1.3 + 4.903774 \
                            + 0.811817 * (newTreeHeight) \
                            - 0.363756*(numpy.log(bhage))**2 \
                            + 24.030758*(newTreeHeight)/float(bhage) \
                            - 0.102076*(newTreeHeight)*numpy.log(newTreeHeight)
    return siteIndex

