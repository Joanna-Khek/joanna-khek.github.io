# ----------- National Data Science Challenge 2019 ------------ #
###################
##  PREPARATION  ##
###################
# import libraries
import numpy as np 
import pandas as pd 
import os 
import re 
from nltk.stem import WordNetLemmatizer
import json
import csv

stemmer = WordNetLemmatizer()

# check directory 
os.getcwd()

# reading the file 
df_train = pd.read_csv("/Users/joanna/Desktop/Kaggle Shopee/dataset/train.csv")
df_test = pd.read_csv("/Users/joanna/Desktop/Kaggle Shopee/dataset/test.csv")

# mapping categories.json 
with open('/Users/joanna/Desktop/Kaggle Shopee/dataset/categories.json') as f:
    categories_json = json.load(f)

category_titles = {}
for category_class in categories_json:
    for category_name in categories_json[category_class]:
        category_titles[categories_json[category_class][category_name]] = category_name
print(category_titles)

category_mapper = {}
product_type_mapper = {}

for category in categories_json.keys():
    for key, value in categories_json[category].items():
        category_mapper[value] = key
        product_type_mapper[value] = category

##########################
##  DATA PREPROCESSING  ##
##########################
# Apply the mapper to get new columns: category_type and product_type
df_train['Category_type'] = df_train['Category'].map(category_mapper)
df_train['Product_type'] = df_train['Category'].map(product_type_mapper)

# converts to lowercase
df_train["title"] = df_train["title"].apply(lambda x: " ".join(x.lower() for x in x.split()))
df_test["title"] = df_test["title"].apply(lambda x: " ".join(x.lower() for x in x.split()))

# remove punctuation
df_train["title"] = df_train["title"].str.replace('[^\w\s]','')
df_test["title"] = df_test["title"].str.replace('[^\w\s]','')

# remove all special characters
df_train["title"] = df_train["title"].apply(lambda x: re.sub(r'\W', ' ', str(x)))
df_test["title"] = df_test["title"].apply(lambda x : re.sub(r'\W', ' ', str(x)))

# substitute multiple spaces with single space
df_train["title"] = df_train["title"].apply(lambda x: re.sub(r'\s+', ' ', str(x), flags=re.I))
df_test["title"] = df_test["title"].apply(lambda x: re.sub(r'\s+', ' ', str(x), flags=re.I))

# lemmatization
df_train["title"] = df_train["title"].apply(lambda x: x.split())
df_train["title"] = df_train["title"].apply(lambda x: [stemmer.lemmatize(i) for i in x])
df_train["title"] = df_train["title"].apply(lambda x: " ".join(x))

df_test["title"] = df_test["title"].apply(lambda x: x.split())
df_test["title"] = df_test["title"].apply(lambda x: [stemmer.lemmatize(i) for i in x])
df_test["title"] = df_test["title"].apply(lambda x: " ".join(x))

# add in _label_ to the labels
df_train['Category_type']=['__label__'+s.replace(' or ', '$').replace(', or ','$').replace(',','$').replace(' ','_').replace(',','__label__').replace('$$','$').replace('$',' __label__').replace('___','__') for s in df_train["Category_type"]]
df_train.to_csv(r"/Users/joanna/Desktop/Kaggle Shopee/train_full_processed.csv")

# the full training model
df_train_full = df_train.loc[:,["title", "Category_type"]]
df_train_full["title"] = df_train_full["title"].replace('\n',' ', regex=True).replace('\t',' ', regex=True)
df_train_full.to_csv(r'/Users/joanna/fastText/full_train.txt', index=False, sep=' ', header=False, quoting=csv.QUOTE_NONE, quotechar="", escapechar=" ")

# create train and validation split set from the full training model
from sklearn.model_selection import train_test_split
train, validation = train_test_split(df_train, test_size=0.2, random_state=101)

# training set
train = train.loc[:,["title", "Category_type"]]
train["title"] = train["title"].replace('\n',' ', regex=True).replace('\t',' ', regex=True)
train.to_csv(r'/Users/joanna/fastText/train_1.txt', index=False, sep=' ', header=False, quoting=csv.QUOTE_NONE, quotechar="", escapechar=" ")
train.to_csv(r'/Users/joanna/Desktop/Kaggle Shopee/train_80.csv')

# test set
test = df_test.loc[:,["title"]]
test.to_csv(r'/Users/joanna/fastText/test_1.txt',index=False, sep=' ', header=False, quoting=csv.QUOTE_NONE, quotechar="", escapechar=" ")

# validation set
validation = validation.loc[:,["title","Category_type"]]
validation["title"] = validation["title"].replace('\n',' ', regex=True).replace('\t',' ', regex=True)
validation.to_csv(r'/Users/joanna/fastText/validation_1.txt', index=False, sep=' ', header=False, quoting=csv.QUOTE_NONE, quotechar="", escapechar=" ")
validation.to_csv(r'/Users/joanna/Desktop/Kaggle Shopee/validation_20.csv')

######################
##  fastText model  ##
######################
# to be run on terminal
#./fasttext supervised -input train_1.txt -output model_final -lr 0.25 -epoch 5 -dim 200 -wordNgrams 4 -loss softmax
#./fasttext test model_final.bin validation_1.txt
#./fasttext predict model_final.bin test_1.txt > prediction.txt

###########################
##  LOGISTIC REGRESSION  ##
###########################
filepath_dict = {'train':"../input/train_80.csv",
                 'valid':"../input/validation_20.csv"
                }
df_list = []
for source, filepath in filepath_dict.items():
    df = pd.read_csv(filepath)
    df['source'] = source  # Add another column filled with the source name
    df_list.append(df)
    
df = pd.concat(df_list)

# Training data - train_80
df_train = df[df['source'] == 'train']
# Rename columns in train_80
df_train.columns = ["itemid","title","Category_type","Category","source"]
train_sentences = df_train['title'].values
train_category = df_train['Category'].values

# Validation data - validation_20
validation = df[df['source']=='valid']
# Rename Columns in validation_20
validation.columns = ["itemid","title","Category_type","Category","source"]
validation_sen = validation['title'].values
validation_category = validation['Category'].values

# Split train 80 into training and testing set
from sklearn.model_selection import train_test_split
sentence_train,sentence_test,y_train,y_test = train_test_split(train_sentences,train_category,test_size=0.2,random_state=1000)

from sklearn.feature_extraction.text import TfidfVectorizer

x_train = []
x_test = []

vectorizer = TfidfVectorizer(analyzer='word', token_pattern=r'\w{1,}',max_df = 0.8, min_df = 20,ngram_range=(1, 4),encoding='utf-8',strip_accents='unicode')
# Vectorise based on whole of train_80
vectorizer.fit(train_sentences.astype('U'))

# Use the same vectoriser to prepare training and testing data 
x_train = vectorizer.transform(sentence_train.astype('U'))
x_test = vectorizer.transform(sentence_test.astype('U'))

# Baseline Model - logistic Regression(no tuning)
from sklearn.linear_model import LogisticRegression

logistic_classifier = LogisticRegression(multi_class='multinomial',solver='saga')

logistic_classifier.fit(x_train, y_train)


# Save the model
import pickle
filename = 'finalized_model.sav'
pickle.dump(logistic_classifier, open(filename, 'wb'))
#loaded_model = pickle.load(open(filename, 'rb'))
#result = loaded_model.score(X_test, Y_test)

logistic_prediction = logistic_classifier.predict(x_test)

# Accuracy Score of logistic regression
score = logistic_classifier.score(x_test, y_test)

print("Accuracy:", score)

# Confusion Matrix of logistic regression
#from xgboost.metrics import confusion_matrix
from sklearn.metrics import confusion_matrix

logistic_cf = confusion_matrix(y_test,logistic_prediction )
logistic_cf = pd.DataFrame(logistic_cf)
logistic_cf.to_csv("confusion_matrix.csv", index=True)

# Output
x_validation = vectorizer.transform(validation_sen.astype('U'))

prediction = logistic_classifier.predict(x_validation)
output = {'itemid': validation['itemid'].values,
         'Category': validation_category,
         'prediction': prediction}

output = pd.DataFrame(output)
output.to_csv("logistic_regression.csv", index=True)



