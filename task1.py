def sums(list):
    #list = input()
    sums = [0]
    currentSum = 0
    for item in list:
        currentSum+=item
        sums.append(currentSum)
    print sums
def bounds(list,lowerBound,upperBound):
    newList = []
    if (lowerBound > upperBound):
        print "incorrect bounds"
    for item in list:
        if (item < lowerBound):
            newList.append(lowerBound)
        elif (item > upperBound):
            newList.append(upperBound)
        else:
            newList.append(item)
    print newList
def sequence(n):
    print n
    while n != 1:
        if n%2==0:
            n /= 2
        else:
            n = 3*n+1
        print n
def bottles():
    numbers = ["no","one","two","three","four","five","six","seven","eight","nine","ten"]
    numberOfBottles = 10
    bottle = " green bottle"
    hanging = " hanging on the wall"
    bottles = " green bottles"
    ifStr = "And if one green bottle should accidentally fall,"
    willBe = "There'll be "
    while (numberOfBottles > 0):
        numberStr =  numbers[numberOfBottles].title()
        if (numberOfBottles != 1):
            print numberStr + bottles + hanging + ","
            print numberStr + bottles + hanging + ","
        else:
            print numberStr + bottle + hanging + ","
            print numberStr + bottle + hanging + ","
        print ifStr
        if (numberOfBottles != 2):
            print willBe + numbers[numberOfBottles-1] + bottles + hanging + "."
        else:
            print willBe + numbers[numberOfBottles-1] + bottles + hanging + "."
        numberOfBottles-=1
bottles()
def getPair(n,divisor):
    count = 0
    while n%divisor == 0:
        n/=divisor
        count+=1
    return [divisor,count]

def primes(n):
    divisor = 2
    divisors = []
    while divisor < n :
        if n%divisor == 0:
            [divisor,count]=getPair(n,divisor);
            divisors.append([divisor,count])
            n/= divisor**count
        divisor+=1
    print divisors


primes(144)
#sequence(3)
#sums()
#bounds([1,2,3,4,5,9],2,4)
