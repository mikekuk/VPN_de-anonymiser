import numpy as np
import tensorflow as tf

def local_similarity(array1, array2, kernel_size=(5, 5)):
    import tensorflow as tf

    assert array1.shape == array2.shape, "Input arrays must have the same shape"

    input_shape = array1.shape
    inputs = tf.keras.layers.Input(input_shape)
    conv = tf.keras.layers.Conv2D(1, kernel_size, padding='same', activation='relu')(inputs)
    model = tf.keras.Model(inputs, conv)

    conv_array1 = model(array1[np.newaxis, ...]).numpy()
    conv_array2 = model(array2[np.newaxis, ...]).numpy()

    mse = tf.keras.losses.MeanSquaredError()
    similarity = mse(conv_array1, conv_array2).numpy()

    return similarity


with open("arrays/AWS_4_host/360.cn-EC2AMAZ-31JQHDO-65-12-2023_04_03__12_02_48.npy", "rb") as f:
    array1 = np.load(f)
print(array1.shape)

with open("arrays/AWS_4_host/360.cn-EC2AMAZ-31JQHDO-65-12-2023_04_03__12_02_48.npy", "rb") as f:
    array2 = np.load(f)




similarity = local_similarity(array1, array2)
print("Local similarity:", similarity)
