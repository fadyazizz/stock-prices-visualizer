import matplotlib
import csv
import statistics
import math
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

# returns an array containing all the data in the open column
def getopen(read):
    arr=[]
    counter=0
    for row in read:
        if(counter==0):
            counter=counter+1
            continue
        arr.append(float(row[1]))
    return arr
# returns an array containing all the data in the close coloumn
def getclose(read):
    arr=[]
    counter = 0
    for row in read:
        if (counter == 0):
            counter = counter + 1
            continue
        arr.append(float(row[3]))
    return arr

# returns an array containing all the data in the date column
def getdate(read):
    arr = []
    counter = 0
    for row in read:
        if (counter == 0):
            counter = counter + 1
            continue
        arr.append(row[0])
    return arr
# returns an array containing all the data in the high column
def gethigh(read):
    arr = []
    counter = 0
    for row in read:
        if (counter == 0):
            counter = counter + 1
            continue
        arr.append(float(row[2]))
    return arr
# returns an array containing all the data in the low column
def getlow(read):
    arr = []
    counter = 0
    for row in read:
        if (counter == 0):
            counter = counter + 1
            continue
        arr.append(float(row[3]))
    return arr
# returns an array containing all the data in the adjusted close column
def getadj(read):
    arr = []
    counter = 0
    for row in read:
        if (counter == 0):
            counter = counter + 1
            continue
        arr.append(float(row[5]))
    return arr
# returns an array containing all the data in the volume column
def getvolume(read):
    arr = []
    counter = 0
    for row in read:
        if (counter == 0):
            counter = counter + 1
            continue
        arr.append(int(row[6]))
    return arr
# the read is the read csv file and the column is which array is needed to plot the chart
def parser(read,column):
    if(column=='Date'):
        return getdate(read)
    else:
        if(column=='Open'):
            return getopen(read)
        elif(column=='High'):
            return gethigh(read)
        elif(column=='Low'):
            return getlow(read)
        elif(column=='Close'):
            return getclose(read)
        elif(column=='Adj Close'):
            return getadj(read)
        elif(column=='Volume'):
            return getvolume(read)
        else:
            raise Exception

# the user sends the path of the csv file and the column to read which can be date, high ,low, close, adjusted close, Volume.
def filereader(path,cloumnToRead):
    with open(path) as file:
        read=csv.reader(file)
        #the return is what is returned from the parser method that maps the required coloumn to the array
        return parser(read,cloumnToRead)

#return the minimum value in the array
def getmin(arr):
    min=arr[0]
    counter=1
    while(counter<len(arr)):
        if(min>arr[counter]):
            min=arr[counter]
        counter=counter+1
    return min
#return the max value in the array
def getmax(arr):
    max=arr[0]
    counter = 1
    while (counter < len(arr)):
        if (max < arr[counter]):
            max = arr[counter]
        counter = counter + 1
    return max
#draws a histogram by sending the data values as an array and the name of the chart
def histogram(arr,name):
    plt.figure('histogram')
    plt.hist(arr,rwidth=0.9)
    
    plt.xlabel('classes')
    plt.ylabel('frequency')
    plt.title(name)

# this class creates an object of frequency classes so each object contains a lowerbound and an upperbound
class freqClass:
    def __init__(self,lowerbound,upperbound):
        self.lowerbound=lowerbound
        self.upperbound=upperbound
# this method is called in freqgetter and class getter methods which counts the number of occurances if data values in a certain frequency class
def search(arr,lowerbound,upperbound):
    freq=0
    for i in arr:
        if(i>=lowerbound and i<upperbound):
          freq=freq+1
    return freq
#return an array in which every cell in the array contains frequencyclass object
def freqgetter(arr):
    range=getmax(arr)-getmin(arr)
    width=(range+1)/10
    width=math.ceil(width)
    counter=1
    min=getmin(arr)
    classarr=[freqClass(min,min+width)]
    freq=search(arr,min,min+width)
    freqarr=[freq]
    min=min+width
    while(counter<10):
        classarr.append(freqClass(min,min+width))
        freqarr.append(search(arr,classarr[counter].lowerbound,classarr[counter].upperbound))
        counter=counter+1
        min=min+width
    return freqarr
#return an array in which every cell in the array contains the number of occurances of its corresponding frequency class
def classgetter(arr):
    range = getmax(arr) - getmin(arr)
    width = (range + 1) / 10
    width = math.ceil(width)
    counter = 1
    min = getmin(arr)
    classarr = [freqClass(min, min + width)]
    freq = search(arr, min, min + width)
    freqarr = [freq]

    min = min + width
    while (counter < 10):
        classarr.append(freqClass(min, min + width))
        freqarr.append(search(arr, classarr[counter].upperbound, classarr[counter].upperbound))
        counter = counter + 1
        min = min + width
    return classarr




def ogive(arr,name):
    x=[]
    cl=classgetter(arr)
    x.append(cl[0].lowerbound)


    y=freqgetter(arr)
    y.insert(0,0)

    counter=0
    while(counter<len(cl)):
        x.append(cl[counter].upperbound)
        counter=counter+1
    counter=1
    while(counter<len(y)):
        y[counter]=y[counter]+y[counter-1]
        counter=counter+1
    plt.figure('ogive')
    plt.title(name)
    plt.plot(x,y)


def freqpolygon(arr,name):
    y=freqgetter(arr)
    y.insert(0,0)
    temp=classgetter(arr)
    width=temp[0].upperbound-temp[0].lowerbound
    width=width/2
    x=[temp[0].lowerbound-width]
    counter=0
    while(counter<len(temp)):
        x.append(temp[counter].lowerbound+width)
        counter=counter+1
    plt.figure('frequency polygon')
    plt.title(name)
    plt.plot(x, y)



def mean(arr):
    sum=0
    for i in arr:
        sum=sum+i
    mean=sum/len(arr)
    return mean

def median(arr):
    return statistics.median(arr)
def mode(arr):
    return statistics.mode(arr)
def main():
    arr=filereader('/Users/macuser/Desktop/intern/AAPl.csv','Close')
    ogive(arr,'close')
    histogram(arr,'close')
    freqpolygon(arr,'close')
    plt.show()

if __name__ == '__main__':
    main()

