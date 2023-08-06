import tensorflow as tf


def random_dataset(shape=(32, 10), seed=22):
    """
    :param shape: shape of the desired tensor
    :param seed: random seed
    :return: a random tf tensor of the specified shape
    """
    return tf.random.uniform(shape, seed)


def limit_memory(memory_limit: int = 4096):
    print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
    try:
        if len(tf.config.list_physical_devices('GPU')) > 0:
            for gpu in tf.config.experimental.list_physical_devices(
                    "GPU"): tf.config.experimental.set_virtual_device_configuration(
                gpu,
                [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=memory_limit)])
            print(f'Setting memory limit to {memory_limit} for any GPU')
    except ValueError as e:
        print(e)
