#!/usr/bin/env/python3

import pandas as pd

class Word:
    lemma = ""
    pos = ""
    value = 0
    variants = []
    def toString(self):
        return self.lemma + "\t" + self.pos + "\t" + str(self.value) + "\t" + ",".join(self.variants)

class Sentiment:
    positiv = {}
    negativ = {}

    def df(self, whichOne):
        theDict = {}
        if whichOne == "positiv":
            theDict = self.positiv
        else:
            theDict = self.negativ

        theList = []
        for entry in theDict:
            word = theDict[entry]
            tempList = []
            tempList.append(word.lemma)
            tempList.append(word.pos)
            tempList.append(float(word.value))
            tempList.append(",".join(word.variants))
            theList.append(tempList)

            
        df = pd.DataFrame(theList, columns=["lemma", "pos", "value", "variants"])
        #df = df["value"].to_numeric()
        #df["value"] =df.to_numeric(df["value"])
        df = df.astype({"value": float}, errors='raise') 

        return df


    def readFile(self, filename):
        dic = {}

        infile = open(filename, encoding="utf-8", mode="r")
        lines = infile.readlines()
        infile.close()

        for line in lines:
            line = line.strip()
            rec = line.split("\t")

            word =  Word()
            word.lemma = rec[0].split("|")[0]
            word.pos = rec[0].split("|")[1]
            word.value = float(rec[1])
            if len(rec) == 3:
                word.variants = rec[2].split(",")
            else:
                word.variants = []
            dic[word.lemma] = word
        return dic    

    def __init__(self, posFile, negFile):
            self.positiv = self.readFile(posFile)
            self.negativ = self.readFile(negFile)

if __name__ == "__main__":
    sentiment = Sentiment("SentiWS_v1.8c_Positive.txt", "SentiWS_v1.8c_Negative.txt")
    print("Size positive:", len(sentiment.positiv))
    print("Size negativ:", len(sentiment.negativ))
    
    word = " "
    while word != "":
        word = input("Enter a word: ")
        if word in sentiment.positiv:
            print("Positiv: ", sentiment.positiv[word].toString())
        elif word in sentiment.negativ:
            print("Negativ: ", sentiment.negativ[word].toString())
        else:
            print("Word not found.")
        print("--------------------------")

    posdf = sentiment.df("positiv")
    print(posdf.head())
    print("Good bye.")


