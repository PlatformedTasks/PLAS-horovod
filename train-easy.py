import numpy as np
import tensorflow as tf
import horovod.tensorflow.keras as hvd
hvd.init()
# Create toy dataset.
n = 1024
X = np.random.randn(n, 128)
Y = np.random.randn(n, 32)
# Distributed optimizer.
optimizer = tf.keras.optimizers.Adam()
optimizer = hvd.DistributedOptimizer(optimizer)
# Build model.
input_layer = tf.keras.layers.Input(shape=(128,))
next_layer = tf.keras.layers.Dense(128, activation='relu')(input_layer)
next_layer = tf.keras.layers.Dense(64, activation='relu')(next_layer)
next_layer = tf.keras.layers.Dense(64, activation='relu')(next_layer)
output_layer = tf.keras.layers.Dense(32)(next_layer)
model = tf.keras.models.Model(inputs=input_layer, outputs=output_layer)
model.compile(optimizer=optimizer, loss="mse", experimental_run_tf_function=False)
# Training.

callbacks = [hvd.callbacks.BroadcastGlobalVariablesCallback(0), hvd.callbacks.MetricAverageCallback()]

if hvd.rank() == 1:
    callbacks.append(tf.keras.callbacks.ModelCheckpoint('./checkpoint-{epoch}.h5'))

train_history = model.fit(
    X, Y,
    batch_size=256,
    epochs=10,
    callbacks=callbacks,
    verbose=2 if hvd.rank() == 0 else 0)
print(train_history.history)

