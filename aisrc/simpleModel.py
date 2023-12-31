
from keras.models import Model 
from keras.models import Sequential
from keras.layers import Dense, Input
from keras.layers import GaussianNoise                                                      # import noise layer
layer = GaussianNoise(0.1)                                                                  # define noise layer
from keras.layers import Activation
from keras.layers import LSTM
from keras.layers import Convolution1D
from keras.layers import Flatten
from keras.layers import MaxPool1D
from sklearn.utils.class_weight import compute_class_weight
from sklearn.utils import class_weight
from keras.layers import BatchNormalization
import numpy as np
import tensorflow as tf
from tensorflow import keras


def makeModel(train_inputs):
    
    model = Sequential()

    im_shape=(train_inputs.shape[1],1)
    
    model.add(Convolution1D(64, (6), activation='relu', input_shape=im_shape))              #inputs_cnn
    model.add(BatchNormalization())
    model.add(MaxPool1D(pool_size=(3), strides=(2), padding="same"))

    model.add(Convolution1D(64, (3), activation='relu', input_shape=im_shape))              #pool1
    model.add(BatchNormalization())
    model.add(MaxPool1D(pool_size=(2), strides=(2), padding="same"))

    model.add(Convolution1D(64, (3), activation='relu', input_shape=im_shape))              #pool2
    model.add(BatchNormalization())
    model.add(MaxPool1D(pool_size=(2), strides=(2), padding="same"))

    model.add(Flatten())

    model.add(Dense(64, activation='relu'))                                                 #flatten
    #model.add(LSTM(32))                                                                    #RNN Dropout Regularization
    #model.add(GaussianNoise(0.1))
    #model.add(Activation('relu'))                                                          #MLP Noise Regularization
    model.add(Dense(32, activation='relu'))                                                 #dense_end1
    #model.add(GaussianNoise(0.1))
    model.add(Dense(5, activation='softmax', name='main_output'))
    #model.add(GaussianNoise(0.1))

    #compile model using accuracy to measure model performance
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    return model


def trainModel(model, train_inputs, train_outputs, test_inputs, test_outputs):

    model.fit(train_inputs, train_outputs, epochs = 10, batch_size = 32, validation_data = (test_inputs, test_outputs))
    model.save("simplemodel")

    return model



#raw_train_outputs needs to be in the raw form before changed to binary in the to_categorical function
def trainModelClassWeight(model, train_inputs, train_outputs, test_inputs, test_outputs, raw_train_outputs):

    class_weights = class_weight.compute_class_weight(class_weight = "balanced", classes = np.unique(raw_train_outputs), y = raw_train_outputs)

    print(class_weights)
    
    class_weights = dict(enumerate(class_weights))#don't know whether this is necessary or not
    callbacks = [keras.callbacks.ModelCheckpoint("best model at epoch:{epoch}.h5", save_best_only=True)]#don't know whether this is necessary or not

    model.fit(train_inputs, train_outputs, epochs = 40, batch_size = 32, class_weight=class_weights, 
    callbacks = callbacks, validation_data=(test_inputs, test_outputs), shuffle=True)
    #shuffle and validation data can be removed

    model.save("simplemodelweighted")

    return model

