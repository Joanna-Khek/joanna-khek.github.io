##########################
#  1. IMPORT LIBRARIES  ##
##########################
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns

# sklearn
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import itertools

# keras
from keras.utils.np_utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPool2D
from keras.optimizers import RMSprop
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ReduceLROnPlateau

# set seed
np.random.seed(2)

###########################
##  2. DATA PREPARATION  ##
###########################
# import data
train = pd.read_csv("C:\\Users\\joann\\OneDrive\\Desktop\\My Files\\Data Science\\Digit Recognizer MNIST\\train.csv")
test = pd.read_csv("C:\\Users\\joann\\OneDrive\\Desktop\\My Files\\Data Science\\Digit Recognizer MNIST\\test.csv")

Y_train = train["label"]
X_train = train.drop("label", axis=1)

# quite balanced counts
sns.countplot(Y_train)
Y_train.value_counts()

# check for null and missing values
X_train.isnull().any().describe()
test.isnull().any().describe()

# normalize to reduce the effect of illumination's differences. Helps CNN converge faster too
X_train = X_train/255.0
test = test/255.0

# reshape image in 3 dimensions 28x28x1 (because 784 total pixel = 28*28)
X_train = X_train.values.reshape(-1, 28, 28, 1)
test = test.values.reshape(-1, 28, 28, 1)

# encode labels to one hot vectors (eg: 2 --> [0,0,1,0,0,0,0,0,0,0])
Y_train = to_categorical(Y_train, num_classes = 10)

# check the shape
X_train.shape #(42000, 28, 28, 1)
Y_train.shape #(42000, 10)

###########################
##  3. TRAIN TEST SPLIT  ##
###########################
random_seed = 2
# stratify to ensure some labels are not over represented in the validation set
X_train, X_val, Y_train, Y_val = train_test_split(X_train, Y_train, test_size=0.1,
                                                  stratify = Y_train,
                                                  random_state = random_seed)
# image example
plt.imshow(X_train[1][:,:,0]) # 28 x 28

#######################################
##  4. CONVOLUTIONAL NEURAL NETWORK  ##
#######################################
# (Conv2D --> RELU)*2 --> MaxPool2D --> (Dropout)*2 --> Flatten --> Dense --> Dropout --> Out
# Conv2D: each filter transform a part of the image (kernel size) using the kernel filter.
# MaxPool2D: downsampling filter. reduce computational cost and to some extent reduce overfitting
# Combining convolutional and pooling layers, CNN are able to combine local features and 
# learn more global features of the image.
# Dropout: regularization method, improved generalization and reduces overfitting
# relu: add non-linearity to the network
# flatten layer: convert the final feature maps into 1D vector

model = Sequential()
model.add(Conv2D(filters = 32, kernel_size = (5,5), padding = "Same",
                 activation = "relu", input_shape = (28, 28, 1))) # channel is 1 because grayscale image
model.add(Conv2D(filters = 32, kernel_size = (5,5), padding = "Same",
                 activation = "relu"))
model.add(MaxPool2D(pool_size=(2,2)))
model.add(Dropout(0.25))
model.add(Conv2D(filters = 64, kernel_size = (3,3), padding = "Same",
                 activation = "relu"))
model.add(MaxPool2D(pool_size=(2,2), strides=(2,2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(256, activation = "relu"))
model.add(Dropout(0.5))
model.add(Dense(10, activation = "softmax")) # multiclass

# set optimizer
optimizer = RMSprop(lr=0.001, rho=0.9, epsilon=1e-08, decay=0.0)

# compile the model
model.compile(optimizer = optimizer, loss = "categorical_crossentropy",
              metrics=["accuracy"])

# setting a learnig rate annealer 
# Reduce learning rate when a metric has stopped improving.
learning_rate_reduction = ReduceLROnPlateau(monitor = "val_acc",
                                            patience = 3,
                                            verbose = 1,
                                            factor = 0.5,
                                            min_lr = 0.00001)

epochs = 30
batch_size = 86

# data augmentation
# to avoid overfitting problem, we expand artifically our dataset.
datagen = ImageDataGenerator(
        featurewise_center = False, # set input mean to 0
        samplewise_center = False, # set each sample mean to 0
        featurewise_std_normalization = False, # divide inputs by std of the dataset
        samplewise_std_normalization = False, # divide each input by its std
        zca_whitening = False, # a linear algebra operation that reduces the redundancy in the matrix of pixel images.
        rotation_range = 10, # randomly rotate images in the range (degrees 0 to 180)
        zoom_range = 0.1, # randomly zoom image
        width_shift_range = 0.1, # shifts randomly (fraction of total width)
        height_shift_range = 0.1, # shifts randomly (fraction of total height)
        horizontal_flip = False, # randomly flip images (could misclassify 6 and 9)
        vertical_flip = False) # randomly flip images (could misclassify 6 and 9))

datagen.fit(X_train)

# fit the model
history = model.fit_generator(datagen.flow(X_train, Y_train, batch_size=batch_size),
                              epochs = epochs,
                              validation_data = (X_val, Y_val),
                              verbose = 2, 
                              steps_per_epoch = X_train.shape[0]//batch_size,
                              callbacks = [learning_rate_reduction])

#############################
##  4. EVALUATE THE MODEL  ##
#############################
# plot the loss and accuracy curves for training and validation
fig, ax = plt.subplots(2,1)
ax[0].plot(history.history["loss"], color="b", label="Training loss")
ax[0].plot(history.history["val_loss"], color = "r", label="validation loss", axes=ax[0])
legend = ax[0].legend(loc="best", shadow=True)

ax[1].plot(history.history["acc"], color="b", label="Training accuracy")
ax[1].plot(history.history["val_acc"], color="r", label="Validation accuracy")
legend = ax[1].legend(loc="best", shadow=True)

# confusion matrix
def plot_confusion_matrix(cm, classes,
                          normalize = False,    # set to true if want normalized
                          title = "Confusion Matrix",
                          cmap = plt.cm.Blues):
    plt.figure(figsize=(8,8))
    plt.imshow(cm, interpolation="nearest", cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)
    
    if normalize:
        cm = cm.astype("float")/ cm.sum(axis=1)[:, np.newaxis]
        
    thresh = cm.max()/ 2.
    
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment = "center",
                 color = "white" if cm[i, j] > thresh else "black")
        
        plt.tight_layout()
        plt.ylabel("True label")
        plt.xlabel("Predicted label")
        
# predict the values from the validation dataset
Y_pred = model.predict(X_val)
# convert predictions classes to one hot vectors
# get index of the highest probability 
Y_pred_classes = np.argmax(Y_pred, axis = 1)
# convert validation observations to one hot vectors
Y_true = np.argmax(Y_val, axis=1)

# compute the confusion matrix
confusion_mtx = confusion_matrix(Y_true, Y_pred_classes)
# plot the confusion matrix
plot_confusion_matrix(confusion_mtx, classes = range(10))

#############################
## 5. ERROR INVESTIGATION  ##
#############################
errors = (Y_pred_classes - Y_true != 0)
Y_pred_classes_errors = Y_pred_classes[errors]
Y_pred_errors = Y_pred[errors]
Y_true_errors = Y_true[errors]
X_val_errors = X_val[errors]

def display_errors(errors_index, img_errors, pred_errors, obs_errors):
    n = 0
    nrows = 2
    ncols = 3
    fig, ax = plt.subplots(nrows, ncols, sharex=True, sharey=True)
    for row in range(nrows):
        for col in range(ncols):
            error = errors_index[n]
            ax[row, col].imshow((img_errors[error]).reshape((28,28)))
            ax[row, col].set_title("Predicted label: {}\nTrue label :{}".format(pred_errors[error],
              obs_errors[error]))
            n += 1
            
# probabilities of the wrong predicted numbers
Y_pred_errors_prob = np.max(Y_pred_errors, axis=1)

# predicted probabilities of the true values in the error set
true_prob_errors = np.diagonal(np.take(Y_pred_errors, Y_true_errors, axis=1))

# difference between the probabilities of the predicted label and the true label
delta_pred_true_errors = Y_pred_errors_prob - true_prob_errors

# sorted list of the delta prob errors
sorted_delta_errors = np.argsort(delta_pred_true_errors)

# top 6 errors
most_important_errors = sorted_delta_errors[-6:]

# show the top 6 errors
display_errors(most_important_errors, X_val_errors, Y_pred_classes_errors, Y_true_errors)

#####################
##  6. PREDICTION  ##
#####################
results = model.predict(test)
results = np.argmax(results, axis=1)
results = pd.Series(results, name="Label")

#####################
##  7. SUBMISSION  ##
#####################
submission = pd.concat([pd.Series(range(1, 28001), name = "ImageId"), results],
                                  axis=1)

submission.to_csv("C:\\Users\\joann\\OneDrive\\Desktop\\My Files\\Data Science\\Digit Recognizer MNIST\\submission.csv", index=False)