import pandas as pd
import re


path = "../recommendation/ml-25m/"


def readFiles(factor):
    movies = pd.read_csv(path + ("movies.csv"), engine="python")
    genome_scores = pd.read_csv(path + "genome-scores.csv", engine="python")
    genome_tags = pd.read_csv(path + "genome-tags.csv", engine="python")
    ratings = pd.read_csv(path + "ratings.csv", engine="python")
    tags = pd.read_csv(path + "tags.csv", engine="python")
    print("READ IN FILE")
    moviesDf = pd.DataFrame(movies).sample(int(movies.size / factor))
    genome_scoresDf = pd.DataFrame(genome_scores).sample(int(genome_scores.size / factor))
    genome_tags = pd.DataFrame(genome_tags).sample(int(genome_tags.size / factor))
    ratings = pd.DataFrame(ratings).sample(int(ratings.size / factor))
    tagsDf = pd.DataFrame(tags).sample(int(tags.size / factor))
    return moviesDf, genome_scoresDf, genome_tags, ratings, tagsDf


def exportCSV(path, factor):
    dataFrames = readFiles(factor)

    dataFrames[0].to_csv(path + "movies-sample.csv")
    dataFrames[1].to_csv(path + "genome-score-sample.csv")
    dataFrames[2].to_csv(path + "genome-tags-sample.csv")
    dataFrames[3].to_csv(path + "ratings-sample.csv")
    dataFrames[4].to_csv(path + "tags-sample.csv")





def toPlainString(s):
    x = re.sub(pattern=r"[['[]", string=s, repl="")
    x = re.sub(pattern=r"[]]", string=x, repl="")
    x = re.sub(pattern=r"\d", string=x, repl="")

    return x


def convertToYoutubeId(s):
    x = re.sub(pattern="\W", string=s, repl=" ")
    x = re.sub(pattern="\s", string=x, repl="")
    return x


if __name__ == '__main__':
    print()
