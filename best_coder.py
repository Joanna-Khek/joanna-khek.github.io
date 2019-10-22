# import libraries
import numpy as np
import pandas as pd
import os 
import re 
from nltk.stem import WordNetLemmatizer
import csv
from itertools import chain

# read data
data = pd.read_csv("Keyword_spam_question.csv")
data_ref = pd.read_csv("Extra Material 2 - keyword list_with substring.csv")

# remove words in brackets
regex = re.compile("[\(\[].*?[\)\]]")
data["name"] = data["name"].apply(lambda x:  re.sub(regex,"",x))

# strip symbols
data["name"] = data["name"].apply(lambda x:  re.sub("[^A-Za-z0-9]"," ", x))

# strip whitespaces
data["name"] = data["name"].apply(lambda x:  " ".join(x.split()))
data_ref["Keywords"] = data_ref["Keywords"].apply(lambda x: " ".join(x.split()))

# convert to lowercase
data["name"] = data["name"].str.lower()
data_ref["Keywords"] = data_ref["Keywords"].str.lower()

# split the keywords
# return list from series of comma-separated strings
def chainer(s):
    return list(chain.from_iterable(s.str.split(',')))

# calculate lengths of splits
lens = data_ref['Keywords'].str.split(',').map(len)


# create new dataframe, repeating or chaining as appropriate
data_ref_clean = pd.DataFrame({'Group': np.repeat(data_ref['Group'], lens),
                    'Keywords': chainer(data_ref['Keywords'])})

# get minimum group of keywords
data_ref_clean = data_ref_clean.groupby(['Keywords'], as_index=False)['Group'].min()
cols = ["Group", "Keywords"]
data_ref_clean = data_ref_clean[cols]

# create dictionary
data_ref_clean_dict = pd.Series(data_ref_clean.Group.values,index=data_ref_clean.Keywords).to_dict()

test = []
for i in range(0, len(data)):
    test.append([str(data_ref_clean_dict[word]) for word in data["name"][i].split() if word in data_ref_clean_dict])

dup = []
for i in range (0, len(submission)):
    dup.append(list(set(submission["groups_found"][i])))

submission = pd.DataFrame({"index": range(0,len(data)),
              "groups_found": dup})
    
submission.to_csv("submission.csv", index=False)

