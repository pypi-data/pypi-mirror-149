import tensorflow as tf


def r_squared(y, y_pred):
    """
    :param y: true valuse (tf.Tensor or np.ndarray)
    :param y_pred: predicted values (tf.Tensor or np.ndarray)
    :return:

    r2 score metric for tensorflow
    """
    residual = tf.reduce_sum(tf.square(tf.subtract(y, y_pred)))
    total = tf.reduce_sum(tf.square(tf.subtract(y, tf.reduce_mean(y))))
    r2 = tf.subtract(1.0, tf.math.divide(residual, total))
    return r2
