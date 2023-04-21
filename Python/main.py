import array,math #import bibliotek

#-----Konfiguracja zmiennych-----#
log=0     #0=ukryj obliczenia | 1=pokaż obliczenia   (znaczne spowolnienie)
decimals=2     #liczba miejsc po przecinku
sizeOut=13     #ilość wartości na wyjściu
minSizeInRows=4
name='Gesture'
#-----END---OF---CONFIG-----#


#Właściwy kod programu


def prepLearn():
    fileUp=open("dane/gestUp.txt","r")
    fileDown=open("dane/gestDown.txt","r")
    fileLeft=open("dane/gestLeft.txt","r")
    fileRight=open("dane/gestRight.txt","r")
    fileUndefinied=open("dane/gestUndefinied.txt","r")
    
    sizeOutRows=[]
    sizeOutRows.append(importDataToArray(fileUp,"Up"))
    sizeOutRows.append(importDataToArray(fileDown,"Down"))
    sizeOutRows.append(importDataToArray(fileLeft,"Left"))
    sizeOutRows.append(importDataToArray(fileRight,"Right"))
    sizeOutRows.append(importDataToArray(fileUndefinied,"Undefinied"))

    fileUp.close()
    fileDown.close()
    fileLeft.close()
    fileRight.close()
    fileUndefinied.close()

    #print('\nUp: {} | Down: {} | Left: {} | Right: {} | Undefinied: {}'.format(sizeOutRows[0],sizeOutRows[1],sizeOutRows[2],sizeOutRows[3],sizeOutRows[4]))


def importDataToArray(file,Classifier):
    #print('Gest:',Classifier,'\n')
    i=0
    In=[]
    while True:
        line=file.readline()
        if not line:
            #print('\nLiczba tablic wyjściowych dla {} = {}\n-------------------------------------------------\n'.format(Classifier,i))
            break
        if line != '\n':
            line=line.rstrip('\n')
            line=line.split(" ")
            line=[eval(i) for i in line]
            In.append(line)
        if line == '\n':
            i=i+resample(In,Classifier,i)
            In.clear()
    return i


def resample(In, Classifier,iteration):
    
    sizeInCols=len(In[0]) #ilość kolumn wejścia
    sizeInRows=len(In) #ilość wierszy wejścia
    
    if log==1:print('Input:',sizeInCols,'x',sizeInRows) #wyświetlenie rozmiaru wejścia
    if sizeInRows<minSizeInRows:return 0
    
    Out=[[0 for x in range(sizeOut)] for y in range(sizeInCols)] #inicjacja tablicy wyjścia
    
    if iteration==0 and Classifier=="Up":
        fileLearnPrep(sizeInCols)
    
    for j in range (sizeInCols): #pętla kolumn
        if log==1:print('\nKOLUMNA:',j) #wyświetlenie aktualnie przetwarzanej kolumny
        for i in range (sizeOut): #pętla wierszy
            x=i/(sizeOut-1)*(sizeInRows-1) #badane x
            x1=math.floor(x) #dolny x
            x2=math.ceil(x) #górny x
            y1=In[x1][j] #dolny y
            y2=In[x2][j] #górny y
            a=y2-y1 #obliczenie współczynnika a
            b=y2-a #obliczenie współczynnika b
            #y=round(a*(x-x1)+b,decimals) #obliczenie y dla badanego x
            y=a*(x-x1)+b #obliczenie y dla badanego x
            Out[j][i]=y #wpisanie y w tablicę wyjścia
            if log==1:print('Wiersz',i,'| x1:',x1,'x2:',x2,'y1:',y1,'y2:',y2,'a:',a,'b:',b,'x:',round(x,decimals),'y:',y) #wyświetlenie obliczeń
    if log==1:print() #<br>
    
    """for row in range (sizeInCols):
        for col in range (sizeOut):
            maxVal=max(Out[row])
            minVal=min(Out[row])
            if (maxVal-minVal) != 0:
                Out[row][col]=(Out[row][col]-minVal)/(maxVal-minVal)
            else:
                Out[row][col]=1.0"""

    printWekaReady(Out,Classifier)
    return 1


def fileLearnPrep(sizeInCols):
    open('learn.arff', 'w').close()
    fileLearn=open('learn.arff', 'a')
    fileLearn.write('@RELATION {}\n\n'.format(name))
    colNames=['red','green','blue','clear','proximity']
    for i in range (sizeInCols):
        for j in range (sizeOut):
            fileLearn.write('@ATTRIBUTE {}_{} NUMERIC\n'.format(colNames[i],j))
    fileLearn.write('@ATTRIBUTE class {Up,Down,Left,Right,Undefinied}\n\n@DATA\n')
    fileLearn.close()


def printWekaReady(Out,Classifier):
    Out=str(Out)
    Out=Out.replace('], [',', ')
    Out=Out.replace('[','')
    Out=Out.replace(']','')
    #print(Out,'\n')
    fileLearn=open('learn.arff', 'a')
    fileLearn.write('{}, {}\n'.format(Out,Classifier))
    fileLearn.close()


prepLearn()
