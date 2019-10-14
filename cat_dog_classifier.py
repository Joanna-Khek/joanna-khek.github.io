########################
##  import libraries  ##
########################
import numpy as np
import pandas as pd
from keras.callbacks import EarlyStopping, ReduceLROnPlateau
from keras.preprocessing.image import ImageDataGenerator, load_img
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dropout, Flatten, Dense, Activation, BatchNormalization
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import random
import os

########################
##  define constants  ##
########################
FAST_RUN = False
IMAGE_WIDTH = 128
IMAGE_HEIGHT = 128
IMAGE_SIZE = (IMAGE_WIDTH, IMAGE_HEIGHT)
IMAGE_CHANNELS = 3

#####################
##  training data  ##
#####################
filenames = os.listdir("train")
categories = []
for filename in filenames:
    category = filename.split(".")[0]
    if category == "dog":
        categories.append(1)
    else:
        categories.append(0)
        
df = pd.DataFrame({
        "filename": filenames,
        "category": categories
        })
    
df["category"].value_counts().plot.bar()

####################################
##  Convolutional neural network  ##
####################################
model = Sequential()

## Feature Extractors
# layer 1
model.add(Conv2D(filters=32, kernel_size=(3,3), activation="relu",
                 input_shape = (IMAGE_WIDTH, IMAGE_HEIGHT, IMAGE_CHANNELS)))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.25))

# layer 2
model.add(Conv2D(filters=64, kernel_size=(3,3), activation="relu"))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.25))

# layer 3
model.add(Conv2D(filters=128, kernel_size=(3,3), activation="relu"))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.25))

## Classifier
model.add(Flatten())
model.add(Dense(512, activation="relu"))
model.add(BatchNormalization())
model.add(Dropout(0.5))
model.add(Dense(2, activation="softmax")) # 2 class

model.compile(loss="categorical_crossentropy", optimizer="rmsprop",
              metrics=["accuracy"])

model.summary()

# to prevent overfitting
# patience: number of epochs that produced the monitored quantity
#           with no improvement after which training will be stopped.
earlystop = EarlyStopping(patience=10)

# reduce learning rate when the accuracy has not increase for 2 steps
# factor: factor by which the learning rate will be reduced. 
#         new_lr = lr * factor
# min_lr: lower bound on the learning rate.
learning_rate_reduction = ReduceLROnPlateau(monitor="val_acc",
                                            patience=2,
                                            verbose=1,
                                            factor=0.5,
                                            min_lr=0.0001)

callbacks = [earlystop, learning_rate_reduction]

# convert 1 to dog and 0 to cat since image generator class_mode = "categorical"
df["category"] = df["category"].replace({0: "cat", 1: "dog"})

train_df, validate_df = train_test_split(df, test_size=0.2, random_state=42)
train_df = train_df.reset_index(drop=True)
validate_df = validate_df.reset_index(drop=True)

train_df["category"].value_counts().plot.bar()

total_train = train_df.shape[0]
total_validate = validate_df.shape[0]
batch_size = 15

#########################################
##  training and validation generator  ##
#########################################
train_datagen = ImageDataGenerator(
        rotation_range = 15,
        rescale = 1./255,
        shear_range = 0.1,
        zoom_range = 0.2,
        horizontal_flip = True,
        width_shift_range = 0.1,
        height_shift_range = 0.1)

train_generator = train_datagen.flow_from_dataframe(
        train_df,
        "train",
        x_col = "filename",
        y_col = "category",
        target_size = IMAGE_SIZE,
        class_mode = "categorical",
        batch_size = batch_size)

validation_datagen = ImageDataGenerator(rescale = 1./255)
validation_generator = validation_datagen.flow_from_dataframe(
        validate_df,
        "train",
        x_col = "filename",
        y_col = "category",
        target_size = IMAGE_SIZE,
        class_mode = "categorical",
        batch_size = batch_size)


# see sample
example_df = train_df.sample(n=1).reset_index(drop=True)
example_generator = train_datagen.flow_from_dataframe(
        example_df,
        "train",
        x_col = "filename",
        y_col = "category",
        target_size = IMAGE_SIZE,
        class_mode = "categorical")

plt.figure(figsize=(12,12))
for i in range (0,5):
    plt.subplot(5, 3, i+1)
    for X_batch, Y_batch in example_generator:
        image = X_batch[0]
        plt.imshow(image)
        break
    
plt.tight_layout()
plt.show()

#########################
##  fitting the model  ##
#########################
epochs = 5 if FAST_RUN else 20
history = model.fit_generator(
        train_generator,
        epochs = epochs,
        validation_data = validation_generator,
        validation_steps = total_validate//batch_size,
        steps_per_epoch = total_train//batch_size,
        callbacks = callbacks)

# save model
model.save_weights("model.h5")

###########################
##  virtualize training  ##
###########################
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12))
ax1.plot(history.history["loss"], color="b", label="Training loss")
ax1.plot(history.history["val_loss"], color="r", label="Validation loss")
ax1.set_xticks(np.arange(1, epochs, 1))
ax1.set_yticks(np.arange(0, 1, 0.1))

ax2.plot(history.history["acc"], color="b", label="Training accuracy")
ax2.plot(history.history["val_acc"], color="r", label="Validation accuracy")
ax2.set_xticks(np.arange(1, epochs, 1))

legend = plt.legend(loc="best", shadow=True)
plt.tight_layout()
plt.show()

####################
##  testing data  ##
####################
test_filenames = os.listdir("test")
test_df = pd.DataFrame({
        "filename": test_filenames})
nb_samples = test_df.shape[0]

# create testing generator
test_gen = ImageDataGenerator(rescale=1./255)
test_generator = test_gen.flow_from_dataframe(
        test_df,
        "test",
        x_col = "filename",
        y_col = None,
        class_mode = None,
        target_size = IMAGE_SIZE,
        batch_size = batch_size,
        shuffle = False)

##################
##  prediction  ##
##################
predict = model.predict_generator(test_generator, steps=np.ceil(nb_samples/batch_size))
# for categorical classification the prediction will come with probability of each category.
# Pick the category that have the highest probability with numpy average max

test_df["category"] = np.argmax(predict, axis=1)

# map back to cat or dog
label_map = dict((v,k) for k,v in train_generator.class_indices.items())
test_df["category"] = test_df["category"].replace(label_map)

# map back to 1 or 0
test_df["category"] = test_df["category"].replace({"dog":1, "cat":0})

# see predicted result with image
sample_test = test_df.head(20)
sample_test.head()
plt.figure(figsize=(12,24))
for index, row in sample_test.iterrows():
    filename = row["filename"]
    category = row["category"]
    img = load_img("test/" + filename, target_size=IMAGE_SIZE)
    plt.subplot(5,4,index+1)
    plt.imshow(img)
    plt.xlabel(filename + "(" + "{}".format(category) + ")")
plt.tight_layout()
plt.show()

# submission
submission_df = test_df.copy()
submission_df["id"] = submission_df["filename"].str.split(".").str[0]
submission_df["label"] = submission_df["category"]
submission_df.drop(["filename", "category"], axis=1, inplace=True)
submission_df.to_csv("submission.csv", index=False)