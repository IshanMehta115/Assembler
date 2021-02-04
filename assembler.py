import random
def addLabel(labelName,locationCounter,symbol_table,opcode_table):
    label_table=symbol_table['label_table']
    variable_table=symbol_table['variable_table']
    lineNumber = str(locationCounter)
    if(labelName in variable_table):
        return ('Error in line '+lineNumber+': label name cant be equal to variable name',locationCounter)
    if(labelName in opcode_table):
        return ('Error in line '+lineNumber+': invalid label name',locationCounter)
    if(labelName in label_table):
        return ('Error in line '+lineNumber+': label name already defined',locationCounter)
    else:
        label_table[labelName]='{:08b}'.format(locationCounter)
def addVariable(variableName,symbol_table,opcode_table,lineNumber,addressCounter):
    label_table=symbol_table['label_table']
    variable_table=symbol_table['variable_table']
    if(variableName in label_table):
        return ('Error in line '+str(lineNumber)+': variable name cant be equal to label name',lineNumber)
    if(variableName in opcode_table):
        return('Error in line '+str(lineNumber)+': invalid variable name',lineNumber)
    if(variableName in variable_table):
        return('Error in line '+str(lineNumber)+': variable name already defined',lineNumber)
    else:
        variable_table[variableName]='{:08b}'.format(addressCounter)
def addVariable1(variableName, locationCounter,symbol_table,opcode_table) :
    label_table=symbol_table['label_table']
    variable_table=symbol_table['variable_table']
    lineNumber = str(locationCounter)
    if(variableName in label_table):
        return ('Error in line '+str(lineNumber)+': variable name cant be equal to label name',lineNumber)
    if(variableName in opcode_table):
        return('Error in line '+str(lineNumber)+': invalid variable name',lineNumber)
    if(variableName in variable_table):
        return('Error in line '+str(lineNumber)+': variable name already defined',lineNumber)
    else:
        variable_table[variableName]='{:08b}'.format(locationCounter)
def firstPass(instructions,symbol_table,opcode_table,addressCounter):
    foundEnd = False
    foundError = False
    errorFirstPass=''# to store the error message
    for i in range (len(instructions)):
        line = instructions[i]
        if(line.find(',')!=-1):#checks if label is present
            if(foundError==False):
                errorFirstPass = addVariable1(line[:line.find(',')],i,symbol_table,opcode_table)#puts label in label table , returns error if any
                if(errorFirstPass!=None):
                    foundError=True
            else:
                addVariable(line[:line.find(',')],i,symbol_table,opcode_table)
            continue
        if(line.find(':')!=-1):#checks if label is present
            if(foundError==False):
                errorFirstPass = addLabel(line[:line.find(':')],i,symbol_table,opcode_table)#puts label in label table , returns error if any
                if(errorFirstPass!=None):
                    foundError=True
            else:
                addLabel(line[:line.find(':')],i,symbol_table,opcode_table)
            line = line[line.find(':')+1:]
        line=line.split()

        if((line[0] in ('CLA','STP')) and len(line)!=1):
            if(foundError==False):
                foundError=True
                errorFirstPass='Error in line '+str(i)+': invalid number of parameters',i
        if((line[0] in ('MUL','DIV')) and len(line)!=2):
            if(foundError==False):
                foundError=True
                errorFirstPass='Error in line '+str(i)+': invalid number of parameters',i
        if(line[0] in opcode_table and ((line[0] in ('CLA','STP','MUL','DIV'))==False) and len(line)!=2):
            if(foundError==False):
                foundError=True
                errorFirstPass='Error in line '+str(i)+': invalid number of parameters',i





        

        if(line[0]=='INP'):
            if(foundError==False):
                errorFirstPass = addVariable(line[1],symbol_table,opcode_table,i,addressCounter)
                addressCounter+=1
                if(errorFirstPass!=None):
                    foundError=True
            else:
                addVariable(line[1],symbol_table,opcode_table,i,addressCounter)
                addressCounter+=1
        if(line[0]=='STP'):
            foundEnd = True
        if(line[0] in ('BRP','BRZ','BRN')):
            if(line[1] in variable_table):
                if(foundError==False):
                    foundError=True
                    errorFirstPass='Error in line '+str(i)+': variable cant be used as a label',i
        if(line[0] in ('ADD','SUB','DIV','MUL','LAC')):
            for j in range(1,len(line)):
                if(line[j] in label_table):
                    if(foundError==False):
                        foundError=True
                        errorFirstPass='Error in line '+str(i)+': label cant be used as a variable',i
        if((line[0] in opcode_table) == False):
            if(foundError==False):
                foundError=True
                errorFirstPass='Error in line '+str(i)+': invalid opcode',i



        if (line[0] in ['LAC', 'SAC', 'ADD', 'SUB', 'BRZ', 'BRN', 'BRP', 'INP', 'DSP', 'MUL', 'DIV']) and (line[1].isdigit()) :
            if(foundError==False):
                foundError=True
                errorFirstPass='Error in line '+str(i)+': ' + line[0] + ' cant have number as parameter',i




    if(foundEnd == False):
        if(foundError==False):
            foundError=True
            errorFirstPass='End of program not found',len(instructions)-1
    return errorFirstPass
def setOpcodes(opcodes):# takes a list of opcodes whose each element is of the form -> opcodeName-opcodeBinaryCode
    opcode_table={}
    for i in opcodes:
        temp = i.find('-')
        opcode_table[i[:temp-1]]=i[temp+2:temp+6]
    return opcode_table#return a dictionary whose key value pair is opcodeName:opcodeBinaryCode
def Output(instructions,symbol_table,opcode_table,errorFirst,errorSecond):
    #print(errorFirst+"a")
    if(errorFirst!=None or errorSecond!=None) and errorFirst != '':
        machineCodeFile = open('machineCode.txt','w')
        symbolTableFile=open('symbolTable.txt','w')
        if(errorFirst!=None and errorSecond!=None):
            if(errorFirst[1]<=errorSecond[1]):
                machineCodeFile.write(errorFirst[0])
                symbolTableFile.write(errorFirst[0])
                print(errorFirst[0])
            else:
                machineCodeFile.write(errorSecond[0])
                symbolTableFile.write(errorSecond[0])
                print(errorSecond[0])
        elif(errorFirst!=None):
            machineCodeFile.write(errorFirst[0])
            symbolTableFile.write(errorFirst[0])
            print(errorFirst[0])
        elif(errorSecond!=None):
            machineCodeFile.write(errorSecond[0])
            symbolTableFile.write(errorSecond[0])
            print(errorSecond[0])
        machineCodeFile.close()
        symbolTableFile.close()
    else:
        machineCodeFile = open('machineCode.txt','w')
        for line in instructions:
            if(line.find(',')!=-1):
                continue
            if(line.find(':')!=-1):
                line = line[line.find(':')+1:]
            line = line.split()
            if(len(line)==1):
                machineCodeFile.write(str(opcode_table[line[0]]+8*'0')+'\n')
            else:
                for i in range(len(line)):
                    if(i==0):
                        machineCodeFile.write(str(opcode_table[line[0]]))
                    else:
                        binString = findSymbol(symbol_table,line[i])
                        machineCodeFile.write(str(binString)+'\n')
        machineCodeFile.close()
        symbolTableFile=open('symbolTable.txt','w')
        symbolTableFile.write("<-label_table->\n")
        for i in symbol_table['label_table']:
            #symbolTableFile.write(str(i)+" "+str(symbol_table['label_table'][i])+'\n')
            symbolTableFile.write("{0:20} {1}\n".format(str(i), str(symbol_table['label_table'][i])))
        symbolTableFile.write("\n<-symbol_table->\n")
        for i in symbol_table['variable_table']:
            #symbolTableFile.write(str(i)+" "+str(symbol_table['variable_table'][i])+'\n')
            symbolTableFile.write("{0:20} {1}\n".format(str(i), str(symbol_table['variable_table'][i])))
        symbolTableFile.write("\n<-instruction_table->\n")
        x = 0
        while x < len(instructions) :
            s1 = instructions[x]
            if(s1.find(':')!=-1):
                s1 = s1[s1.find(':')+1:]
            #symbolTableFile.write(s1.strip() + " " + '{:08b}'.format(x) + '\n')
            symbolTableFile.write("{0:20} {1}\n".format(s1.strip(), '{:08b}'.format(x)))
            x = x + 1
        symbolTableFile.close()
def findSymbol(symbolTable,symbolName):
    if(symbolName in symbolTable['variable_table']):
        return symbolTable['variable_table'][symbolName]
    if(symbolName in symbolTable['label_table']):
        return symbolTable['label_table'][symbolName]
def secondPass(instructions,symbol_table,opcode_table):
    for i in range(len(instructions)):
        line = instructions[i]
        if(line.find(',')!=-1):
            line=line[line.find(',')+1:]
            Newline = line.split()
            if(len(Newline)!=1):
                return 'Error in line '+str(i)+': invalid no of parameters',i
        if(line.find(':')!=-1):
            line = line[line.find(':')+1:]
        line = line.split()

        if(len(line)>1):
            if(line[0] in ('BRP','BRN','BRZ')):
                for j in range(1,len(line)):
                    if(line[j] in variable_table):
                        return 'Error in line '+str(i)+': variable cant be used as a label',i
                    if((line[j] in label_table)==False):
                        return 'Error in line '+str(i)+': '+line[1]+' is not declared',i
            else:
                for j in range(1,len(line)):
                    if(line[j] in label_table):
                        return 'Error in line '+str(i)+': label cant be used as a variable',i
                    if((line[j] in variable_table)==False):
                        return 'Error in line '+str(i)+': '+line[1]+' is not declared',i
def process(instructions,string):# discard everything after last STP
    newInstructions=instructions.copy()
    for i in range(len(instructions)):
        if(instructions[i].find(' ;')!=-1):
            instructions[i]=instructions[i][:instructions[i].find(' ;')]
    j = len(instructions) - 1
    while(j >= 0) :
        s = instructions[j]
        if s.find(':') != -1 :
            s = s[s.find(':')+1:]
        lst = s.split()
        if (lst[0] == string) :
            newInstructions = instructions[0:j+1]
            break
        j = j - 1
        #newInstructions.append(instructions[i])
        #if(instructions[i]==string):
        #    break
    return newInstructions
inputFile = open("input.txt",'r')# opens the input file of assembly code for reading
label_table={}#dictionary for labels
variable_table={}#dictionary for variables
symbol_table={'label_table':label_table,'variable_table':variable_table}#symbol table contains both variable table and label table
opcodeFile = open("opcode.txt",'r')#opens the opcode file
opcodes = opcodeFile.readlines()#gets all the opcode name and values in a list
opcode_table=setOpcodes(opcodes)#sets the opcode list a dictionary - opcode table
error = ''#error string which will store the error message

instructions = inputFile.readlines()#contains the instructions in a list
instructions = process(instructions,'STP')#cuts the part of instructions after STP if found and removes comments
insLength = len(instructions)
addressCounter = len(instructions)
errorFirstPass = firstPass(instructions,symbol_table,opcode_table,addressCounter)#performs 1st pass and return error if any
errorSecondPass=secondPass(instructions,symbol_table,opcode_table)#performs 2nd pass and return error if any
inputFile.close()
opcodeFile.close()
if insLength > 21 :
        machineCodeFile = open('machineCode.txt','w')
        symbolTableFile=open('symbolTable.txt','w')
        machineCodeFile.write('Error : Not enough space for complete program')
        symbolTableFile.write('Error : Not enough space for complete program')
        print('Error : Not enough space for complete program')
        exit()
Output(instructions,symbol_table,opcode_table,errorFirstPass,errorSecondPass)#stores the machine code,symbol tables in a file or else reports the first error if any
