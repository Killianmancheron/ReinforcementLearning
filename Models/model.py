import tensorflow as tf

def build_model(input_shape):
  inputs = tf.keras.Input(shape=input_shape)
  x = tf.keras.layers.Conv2D(32,5, activation='relu', padding='same')(inputs)
  x = tf.keras.layers.MaxPool2D()(x)
  x = tf.keras.layers.Conv2D(32,5, activation='relu', padding='same')(x)
  x = tf.keras.layers.MaxPool2D()(x)
  x = tf.keras.layers.Conv2D(1,3, activation='relu', padding='same')(x)
  x = tf.keras.layers.Flatten()(x)
  x = tf.keras.layers.Dense(512, activation=tf.nn.relu)(x)
  x = tf.keras.layers.Dense(128, activation=tf.nn.relu)(x)
  x = tf.keras.layers.Dense(32, activation=tf.nn.relu)(x)
  outputs = tf.keras.layers.Dense(4, activation='sigmoid')(x)
  model = tf.keras.Model(inputs=inputs, outputs=outputs)
  return model