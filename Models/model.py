import tensorflow as tf
from keras import Input, Model
from keras.layers import Conv2D, MaxPool2D, Flatten, Dense

def build_model(input_shape):
  inputs = Input(shape=input_shape)
  x = Conv2D(32,5, activation='relu', padding='same', name='Conv1')(inputs)
  x = MaxPool2D()(x)
  x = Conv2D(32,5, activation='relu', padding='same', name='Conv2')(x)
  x = MaxPool2D()(x)
  x = Conv2D(1,3, activation='relu', padding='same', name='Conv3')(x)
  x = Flatten()(x)
  x = Dense(512, activation='relu', name='Dense1')(x)
  x = Dense(128, activation='relu', name='Dense2')(x)
  x = Dense(32, activation='relu', name='Dense3')(x)
  outputs = Dense(4, activation='linear', name='Output')(x)
  model = Model(inputs=inputs, outputs=outputs)
  return model