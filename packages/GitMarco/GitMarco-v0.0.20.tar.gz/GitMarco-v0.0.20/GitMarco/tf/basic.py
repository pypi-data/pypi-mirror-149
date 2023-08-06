import tensorflow as tf


def basic_dense_model(input_shape: tuple,
                      output_shape: int,
                      neurons: tuple = (32, 32),
                      activation='relu',
                      regularizer: float = 0.0,
                      dropout: float = 0.0,
                      optimizer: str = 'adam',
                      learning_rate: float = 0.001,
                      loss: str = 'mse',
                      out_activation: str = 'linear'):
    """
    :param input_shape: input shape
    :param output_shape: output_shape
    :param neurons: number of neurons for every dense layer
    :param activation: activation for hidden layers
    :param regularizer: kernel regularizer
    :param dropout: dropout rate for hidden layers
    :param optimizer: optimizer
    :param learning_rate: learning rate
    :param loss: loss function
    :param out_activation: output layer activation
    :return: a compiled tf.keras model

    Creation of a basic dense neural network model
    """
    x = tf.keras.layers.Input(shape=input_shape)
    in_ = x
    for item in neurons:
        x = tf.keras.layers.Dense(item,
                                  activation=activation,
                                  kernel_regularizer=tf.keras.regularizers.l2(regularizer))(x)
        x = tf.keras.layers.Dropout(dropout)(x)

    x = tf.keras.layers.Dense(output_shape, activation=out_activation)(x)

    model = tf.keras.models.Model(inputs=[in_],
                                  outputs=[x])

    optimizer = tf.keras.optimizers.get(optimizer)
    optimizer.learning_rate = learning_rate
    model.compile(optimizer=optimizer, loss=loss)

    return model
