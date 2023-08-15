from matplotlib import pyplot as plt
import numpy as np
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay, classification_report
from matplotlib.colors import BoundaryNorm
from tensorflow.keras import layers
import tensorflow as tf

import pickle

def plot_history(history):
    fig, axs = plt.subplots(1, 2, figsize=(10,5)) 
    (ax1, ax2) = axs
    ax1.plot(history.history['loss'], label='train')
    ax1.plot(history.history['val_loss'], label='validation')

    ax1.legend(loc="upper right")
    ax1.set_xlabel("# of epochs")
    ax1.set_ylabel("loss")

    ax2.plot(history.history['accuracy'], label='train')
    ax2.plot(history.history['val_accuracy'], label='validation')

    ax2.legend(loc="upper right")
    ax2.set_xlabel("# of epochs")
    ax2.set_ylabel("accuracy")

    print("Final training accuracy:", history.history['accuracy'][-1])
    print("Final validation accuracy:", history.history['val_accuracy'][-1])


# def plot_results(model, features_test, y_true, label_binariser):
#     unique_y = np.unique(y_true)
#     fig, ax = plt.subplots(figsize=(30, 30))
#     y_true = np.argmax(labels_test, axis=1)
#     predictions =  np.argmax(model.predict(features_test), axis=1)
#     cm = confusion_matrix(y_true, predictions, normalize='true')
#     disp = ConfusionMatrixDisplay(
#         confusion_matrix=cm,
#         display_labels=[label_binariser.classes_[x] for x in range(unique_y.min(), len(unique_y))]
#         )
#     disp.plot(xticks_rotation=270, values_format=".1f", ax=ax)
#     plt.show()
#     print(classification_report(y_true, predictions))



def label_others(labels: np.array, sites: np.array, min_samples: int):
    "Relabels as 'Other' if label not in sites, or count below min_samples"
    (unique, counts) = np.unique(labels, return_counts=True)
    frequencies = {key: value for key, value in zip(unique, counts)}

    for i, label in enumerate(labels):
        if (label not in sites) or frequencies[label] < min_samples:
            labels[i] = "Other"
    return labels


def vis_df_category(label, labels, features_df, scaler=10):
    
    cat = []

    for i, x in enumerate(features_df):
        if labels[i] == label:
            cat.append(x)

    # Convert the list to a NumPy array
    cat_np = np.array(cat)

    # Repeat each row along the y-axis by a factor of 100
    cat_scaled = np.repeat(cat_np, repeats=scaler, axis=0)

    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(15, 15))

    # Set color boundaries and normalization
    cmap = plt.get_cmap('viridis')
    bounds = [-1, 0, 1, 2]
    norm = BoundaryNorm(bounds, cmap.N)

    # Display the scaled data
    im = ax.imshow(cat_scaled, cmap=cmap, interpolation='nearest', norm=norm)

    # Add a colorbar
    cbar = fig.colorbar(im, ax=ax, ticks=[-1, 0, 1])

    # Modify y-axis tick labels
    y_ticks = ax.get_yticks()
    y_tick_labels = [str(int(y_tick // scaler)) for y_tick in y_ticks]
    ax.set_yticklabels(y_tick_labels)

    plt.show()



class PositionalEncoding(layers.Layer):
    def __init__(self, position, d_model, **kwargs):
        super(PositionalEncoding, self).__init__(**kwargs)
        self.position = position
        self.d_model = d_model
        self.pos_encoding = self.positional_encoding(position, d_model)

    def get_config(self):
        config = super(PositionalEncoding, self).get_config()
        config.update({
            'position': self.position,
            'd_model': self.d_model,
        })
        return config

    def call(self, inputs):
        return inputs + self.pos_encoding[:, tf.newaxis, :]

    def get_angles(self, position, i, d_model):
        angles = 1 / tf.pow(10000, (2 * (i // 2)) / tf.cast(d_model, tf.float32))
        return position * angles

    def positional_encoding(self, position, d_model):
        angle_rads = self.get_angles(
            position=tf.range(position, dtype=tf.float32)[:, tf.newaxis],
            i=tf.range(d_model, dtype=tf.float32)[tf.newaxis, :],
            d_model=d_model)
        sines = tf.math.sin(angle_rads[:, 0::2])
        cosines = tf.math.cos(angle_rads[:, 1::2])
        pos_encoding = tf.concat([sines, cosines], axis=-1)
        pos_encoding = pos_encoding[tf.newaxis, ...]
        return tf.cast(pos_encoding, tf.float32)

    def call(self, inputs):
        return inputs + self.pos_encoding[:, :tf.shape(inputs)[1], :]


def load_label_binarizer(path):
    with open(path + "binarizer", 'rb') as file:
        encoder = pickle.load(file)
    return encoder
