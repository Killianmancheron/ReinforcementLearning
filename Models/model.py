import tensorflow as tf
from keras import Input, Model
from keras.layers import Conv2D, MaxPool2D, Flatten, Dense

def build_model(input_shape):
  inputs = Input(shape=input_shape)
  x = Conv2D(32,5, activation='relu', padding='same')(inputs)
  x = MaxPool2D()(x)
  x = Conv2D(32,5, activation='relu', padding='same')(x)
  x = MaxPool2D()(x)
  x = Conv2D(1,3, activation='relu', padding='same')(x)
  x = Flatten()(x)
  x = Dense(512, activation=tf.nn.relu)(x)
  x = Dense(128, activation=tf.nn.relu)(x)
  x = Dense(32, activation=tf.nn.relu)(x)
  outputs = Dense(4, activation='linear')(x)
  model = Model(inputs=inputs, outputs=outputs)
  return model