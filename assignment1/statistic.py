import csv

def computeMeanRating(filename):
    ratings = []

    try:
        f = open('../ml-latest-small/' + filename, 'r')
    except:
        print('File couldnt be read or found')
        raise
    finally:
        for line in f:
            columns = line.split(",")
            ## im quite sure this is not best practice
            if columns[2] != "rating":
                ratings.append(float((columns[2])))

        f.close()

        n = len(ratings)
        # sorting for median
        ratings.sort()

        # calculating Arithmetic Mean
        average = calcArithmeticMean(ratings, n)

        # calculating Median

        median = calcMedian(ratings, n)

        # calculating mode
        mode = calcMode(ratings)

        return average, median, mode

def calcMode(ratings):
        #Creating an Map where the amount of each number will be stored
        numCount = {}
        highestNum = 0

        #Fill the Map with the numbers which appear in the List
        for i in ratings:
            #if the number already appears in the list count up
            if i in numCount.keys():
                numCount[i] += 1
            else:
                numCount[i] = 1

        #check which number appears most often
        for i in numCount.keys():
            if numCount[i] > highestNum:
                highestNum = numCount[i]
                mode = i
        if highestNum != 1:
            return mode
        #case if every number only appears once
        elif highestNum == 1:
            print("All numbers in the list appear once.")
            return -1

def calcMedian(ratings, n):

        # calculating the median
        if n % 2 != 0:
            median = ratings[int(n / 2)]
        else:
            # case when the len of the data is even.
            median = float((ratings[int((n - 1) / 2)] + ratings[int(n / 2)]) / 2.0)
        return median

def calcArithmeticMean(ratings, n):
        sum = 0
        for i in ratings:
            sum += i
        ## calculating arithmetic mean
        average = sum / n
        # round arithmetic to 5 digits
        average = round(average, 5)
        return average