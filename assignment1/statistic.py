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
        ## calculating arithmetic mean
        average = sum(ratings) / (len(ratings))
        # round arithmetic to 5 digits
        average = round(average, 5)

        # sorting for median
        ratings.sort()
        # calculating the median

        if n % 2 != 0:
            median = ratings[int(n / 2)]
        else:
            # case when the len of the data is even.
            median = float((ratings[int((n - 1) / 2)] + ratings[int(n / 2)]) / 2.0)

        # calculating mode
        mode = calcMode(ratings)

        return average, median, mode


def calcMode(ratings):
    numCount = {}
    max = 0
    for i in ratings:
        if i in numCount.keys():
            numCount[i] += 1
        else:
            numCount[i] = 1
    for i in numCount.keys():
        if numCount[i] > max:
            max = numCount[i]
            mode = i
    if max != 1:
        return mode
    elif max == 1:
        print("All elements of list appear once.")
        return -1


def readFile(filename):
    reader = csv.reader(open('ml-latest-small/' + filename))
    for data in reader:
        print(data)
