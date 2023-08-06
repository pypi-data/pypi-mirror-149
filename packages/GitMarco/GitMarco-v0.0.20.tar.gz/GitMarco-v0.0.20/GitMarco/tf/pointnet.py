import os
from datetime import date
import tensorflow as tf
import numpy as np
import tensorflow.keras.backend as K


class Sampling(tf.keras.layers.Layer):
    def call(self, inputs):
        mean, log_var = inputs
        return K.random_normal(tf.shape(log_var)) * K.exp(log_var / 2) + mean

    def get_config(self):
        return {}


class OrthogonalRegularizer(tf.keras.regularizers.Regularizer):
    def __init__(self, num_features, l2reg=0.001):
        self.num_features = num_features
        self.l2reg = l2reg
        # self.eye = tf.eye(num_features)

    def __call__(self, x):
        x = tf.reshape(x, (-1, self.num_features, self.num_features))
        xxt = tf.tensordot(x, x, axes=(2, 2))
        xxt = tf.reshape(xxt, (-1, self.num_features, self.num_features))
        return tf.reduce_sum(self.l2reg * tf.square(xxt - tf.eye(self.num_features)))

    def get_config(self):
        return {
            'num_features': self.num_features,
            'l2reg': self.l2reg,
            # 'eye': self.eye

        }


def dense_bn(x, filters):
    x = tf.keras.layers.Dense(filters)(x)
    x = tf.keras.layers.BatchNormalization(momentum=0.0)(x)
    return tf.keras.layers.Activation("relu")(x)


def t_network(inputs,
              num_features,
              orto_reg: bool = True):
    # Initalise bias as the indentity matrix
    bias = tf.keras.initializers.Constant(np.eye(num_features).flatten())
    if orto_reg:
        reg = OrthogonalRegularizer(num_features)
    else:
        reg = None

    x = conv_bn(inputs, 32)
    x = conv_bn(x, 64)
    x = conv_bn(x, 512)
    x = tf.keras.layers.GlobalMaxPooling1D()(x)
    x = dense_bn(x, 256)
    x = dense_bn(x, 128)
    x = tf.keras.layers.Dense(
        num_features * num_features,
        kernel_initializer="zeros",
        bias_initializer=bias,
        activity_regularizer=reg,
    )(x)
    feat_t = tf.keras.layers.Reshape((num_features, num_features))(x)
    # Apply affine transformation to input features
    return tf.keras.layers.Dot(axes=(2, 1))([inputs, feat_t])


def conv_bn(x, filters):
    x = tf.keras.layers.Conv1D(filters, kernel_size=1, padding="valid")(x)
    x = tf.keras.layers.BatchNormalization(momentum=0.0)(x)
    return tf.keras.layers.Activation("relu")(x)


def exp_dim(global_feature, num_points):
    return tf.tile(global_feature, [1, num_points, 1])


class Pointnet(object):
    def __init__(self,
                 n_points: int = 1024,
                 setup: str = 'seg',  # class - seg - both
                 input_setup: str = 'grid',  # grid - both
                 n_fields: int = 1,
                 n_scalars: int = 1,
                 n_features: int = 1,
                 grid_size: int = 3,
                 orto_reg: bool = True,
                 encoding_size: int = 1024,
                 feature_transform: bool = True,
                 dropout_rate: float = 0.3,
                 out_class_activation: str = 'relu',
                 out_reg_activation: str = 'sigmoid',
                 class_neurons: tuple = (512, 256),
                 seg_kernels: tuple = (512, 256, 128, 128),
                 ):

        self.n_points = n_points
        self.setup = setup
        self.input_setup = input_setup
        self.n_fields = n_fields
        self.n_scalars = n_scalars
        self.n_features = n_features
        self.grid_size = grid_size
        self.orto_reg = orto_reg
        self.encoding_size = encoding_size
        self.feature_transform = feature_transform
        self.dropout_rate = dropout_rate
        self.out_class_activation = out_class_activation
        self.out_reg_activation = out_reg_activation
        self.class_neurons = class_neurons
        self.seg_kernels = seg_kernels

    def create_model(self):
        inputs = tf.keras.Input(shape=(self.n_points, self.grid_size))

        if self.input_setup == 'both':
            inputs_2 = tf.keras.Input(shape=[self.n_features, ])
        else:
            inputs_2 = None

        x = t_network(inputs, self.grid_size, orto_reg=self.orto_reg)
        x = conv_bn(x, 64)
        x = conv_bn(x, 64)
        if self.feature_transform:
            x = t_network(x, 64, orto_reg=self.orto_reg)
        feat_1 = x
        x = conv_bn(x, 64)
        x = conv_bn(x, 128)
        x = conv_bn(x, self.encoding_size)
        y = tf.keras.layers.GlobalMaxPooling1D()(x)

        if self.input_setup == 'both':
            y = tf.keras.layers.concatenate([inputs_2, y])

        if self.setup == 'seg':
            if self.input_setup == 'both':
                x = tf.keras.layers.Reshape((1, self.encoding_size + self.n_features))(y)
            else:
                x = tf.keras.layers.Reshape((1, self.encoding_size))(y)

            x = tf.keras.layers.Lambda(exp_dim, arguments={'num_points': self.n_points})(x)

            # point_net_seg
            x = tf.keras.layers.concatenate([feat_1, x])
            x = conv_bn(x, self.seg_kernels[0])
            x = conv_bn(x, self.seg_kernels[1])
            x = conv_bn(x, self.seg_kernels[2])
            x = conv_bn(x, self.seg_kernels[3])
            outputs = tf.keras.layers.Dense(self.n_fields,
                                            name="output_fields",
                                            activation=self.out_reg_activation)(x)

            if self.input_setup == 'grid':
                self.model = tf.keras.Model(inputs=inputs, outputs=outputs, name="PointNet")
            elif self.input_setup == 'both':
                self.model = tf.keras.Model(inputs=[inputs, inputs_2], outputs=outputs, name="PointNet")

        elif self.setup == 'class':
            x = dense_bn(y, self.class_neurons[0])
            x = tf.keras.layers.Dropout(self.dropout_rate)(x)
            x = dense_bn(x, self.class_neurons[1])
            x = tf.keras.layers.Dropout(self.dropout_rate)(x)

            outputs = tf.keras.layers.Dense(self.n_scalars,
                                            activation=self.out_class_activation,
                                            name='output_scalars')(x)
            if self.input_setup == 'grid':
                self.model = tf.keras.Model(inputs=inputs, outputs=outputs, name="PointNet")
            elif self.input_setup == 'both':
                self.model = tf.keras.Model(inputs=[inputs, inputs_2], outputs=outputs, name="PointNet")

        elif self.setup == 'both':
            if self.input_setup == 'both':
                x = tf.keras.layers.Reshape((1, self.encoding_size + self.n_features))(y)
            else:
                x = tf.keras.layers.Reshape((1, self.encoding_size))(y)
            x = tf.keras.layers.Lambda(exp_dim, arguments={'num_points': self.n_points})(x)

            # point_net_seg
            x = tf.keras.layers.concatenate([feat_1, x])
            x = conv_bn(x, self.seg_kernels[0])
            x = conv_bn(x, self.seg_kernels[1])
            x = conv_bn(x, self.seg_kernels[2])
            x = conv_bn(x, self.seg_kernels[3])
            outputs_seg = tf.keras.layers.Dense(self.n_fields,
                                                name="output_fields",
                                                activation=self.out_reg_activation)(x)
            x = dense_bn(y, self.class_neurons[0])
            x = tf.keras.layers.Dropout(self.dropout_rate)(x)
            x = dense_bn(x, self.class_neurons[1])
            x = tf.keras.layers.Dropout(self.dropout_rate)(x)

            outputs_class = tf.keras.layers.Dense(self.n_scalars,
                                                  activation=self.out_class_activation,
                                                  name='output_scalars')(x)
            if self.input_setup == 'grid':
                self.model = tf.keras.Model(inputs=inputs, outputs=[outputs_seg, outputs_class], name="PointNet")
            elif self.input_setup == 'both':
                self.model = tf.keras.Model(inputs=[inputs, inputs_2],
                                            outputs=[outputs_seg, outputs_class],
                                            name="PointNet")

        return self.model

    def model_2_image(self, path: str = ''):
        tf.keras.utils.plot_model(self.model, os.path.join(os.getcwd(),
                                                           path, 'PointNet' +
                                                           date.today().strftime("_%d_%m_%Y") +
                                                           '.png'),
                                  show_shapes=True,
                                  show_dtype=True,
                                  show_layer_names=True,
                                  rankdir="TB",
                                  expand_nested=True,
                                  dpi=96,
                                  layer_range=None,
                                  )


class PointnetAe(object):
    def __init__(self,
                 grid_size: int = 3,
                 n_geometry_points: int = 400,
                 n_global_variables: int = 0,
                 n_local_variables: int = 0,
                 dfferent_out_for_globals: bool = False,
                 type_decoder: str = 'dense',
                 is_variational: bool = True,
                 beta: int = 1,
                 encoding_size: int = 1024,
                 orto_reg: bool = True,
                 feature_transform: bool = True,
                 reg_dropout_value: float = 0.,
                 id_: str = 'ae',
                 seg_kernels: tuple = (512, 256, 128, 128),
                 out_reg_activation: str = 'sigmoid',
                 n_cnn_dec_layer: int = 3,
                 cnn_dec_filters: list = (64, 32, 16),
                 out_seg_activation: str = 'sigmoid',
                 out_dec_activation: str = 'sigmoid',
                 dense_dec_coeffs: tuple = (4, 8, 16),
                 ):

        self.grid_size = grid_size
        self.n_geometry_points = n_geometry_points
        self.n_global_variables = n_global_variables
        self.n_local_variables = n_local_variables
        self.different_out_for_globals = dfferent_out_for_globals
        self.type_decoder = type_decoder
        self.is_variational = is_variational
        self.beta = beta
        self.encoding_size = encoding_size
        self.orto_reg = orto_reg
        self.feature_transform = feature_transform
        self.reg_dropout_value = reg_dropout_value
        self.id_ = id_
        self.seg_kernels = seg_kernels
        self.out_reg_activation = out_reg_activation
        self.out_seg_activation = out_seg_activation
        self.out_dec_activation = out_dec_activation
        self.n_cnn_dec_layer = n_cnn_dec_layer
        self.cnn_dec_filters = cnn_dec_filters
        self.dense_dec_coeffs = dense_dec_coeffs

        self.model = None

        if type_decoder == 'cnn' and n_geometry_points % 2**n_cnn_dec_layer != 0:
            raise ValueError(f'Warning: n_geometry_points = {n_geometry_points}, '
                             f'n_cnn_dec_layer = {n_cnn_dec_layer} => '
                             f'the number of points bust be divisible for '
                             f'2^(n_cnn_dec_layer)')

    def create_model(self):
        # === ENCODER === #
        inputs = tf.keras.Input(shape=(self.n_geometry_points, self.grid_size))
        x = t_network(inputs, self.grid_size, orto_reg=self.orto_reg)
        x = conv_bn(x, 64)
        x = conv_bn(x, 64)

        if self.feature_transform:
            x = t_network(x, 64, orto_reg=self.orto_reg)

        x = conv_bn(x, 64)
        x = conv_bn(x, 128)
        x = conv_bn(x, self.encoding_size)
        coding = tf.keras.layers.GlobalMaxPooling1D()(x)
        encoder = tf.keras.Model(inputs=inputs, outputs=coding)

        #  === VARIATIONAL === #
        if self.is_variational:
            input_v_cod = tf.keras.Input([self.encoding_size])
            v_cod_string = 'Variational'

            # extracting mean and log value from latent parameters extracted from the encoder
            codings_mean = tf.keras.layers.Dense(self.encoding_size)(input_v_cod)  # μ
            codings_log_var = tf.keras.layers.Dense(self.encoding_size,
                                                    kernel_initializer=tf.keras.initializers.RandomNormal(mean=0.0,
                                                                                                          stddev=0.005,
                                                                                                          seed=None))(
                input_v_cod)  # γ

            # sample the corresponding Gaussian distribution
            coding = Sampling()([codings_mean, codings_log_var])

            v_cod = tf.keras.Model(inputs=input_v_cod, outputs=coding, name=v_cod_string)

            # loss for variational
            kl_loss = - 0.5 * self.beta * K.sum(
                1 + codings_log_var - K.exp(codings_log_var) - K.square(codings_mean),
                axis=-1)
            kl_loss = K.mean(kl_loss) / (self.n_geometry_points * self.grid_size)
            v_cod.add_loss(kl_loss)

            self.id_ += v_cod_string

        #  === DECODER ===  #
        input_decoder = tf.keras.Input([self.encoding_size])

        if self.type_decoder == 'dense':
            x = tf.keras.layers.Dense(self.encoding_size * self.dense_dec_coeffs[0], activation='relu')(input_decoder)
            x = tf.keras.layers.Dense(self.encoding_size * self.dense_dec_coeffs[1], activation='relu')(x)
            x = tf.keras.layers.Dense(self.encoding_size * self.dense_dec_coeffs[2], activation='relu')(x)
            x = tf.keras.layers.Dense(self.n_geometry_points * self.grid_size, activation=self.out_dec_activation)(x)
            out = tf.keras.layers.Reshape([self.n_geometry_points, self.grid_size])(x)
            decoder_string = 'DecoderDense'

        elif self.type_decoder == 'cnn':
            c1dt = lambda x_, f: tf.keras.layers.Conv1DTranspose(filters=f, kernel_size=3, activation='relu',
                                                                 strides=2,
                                                                 padding='same')(x_)

            x = tf.keras.layers.Dense(int(self.n_geometry_points / 2 ** self.n_cnn_dec_layer) * 64, activation='relu')(
                input_decoder)
            x = tf.keras.layers.Reshape([int(self.n_geometry_points / 2 ** self.n_cnn_dec_layer), 64])(x)

            for i in range(self.n_cnn_dec_layer): x = c1dt(x, self.cnn_dec_filters[i])

            out = tf.keras.layers.Conv1DTranspose(filters=self.grid_size, kernel_size=3,
                                                  activation=self.out_dec_activation,
                                                  padding='same')(
                x)
            decoder_string = 'DecoderCNN'

        decoder = tf.keras.Model(inputs=input_decoder, outputs=out, name=decoder_string)

        self.id_ += '_' + decoder_string

        # structure of the autoencoder
        if self.is_variational:
            cod = encoder(inputs)
            cod = v_cod(cod)
            o1 = decoder(cod)
        else:
            cod = encoder(inputs)
            o1 = decoder(cod)

        # === GLOBAL REGRESSOR === #
        if self.n_global_variables > 0:
            x = tf.keras.layers.Dense(self.encoding_size, activation='relu')(input_decoder)
            x = tf.keras.layers.Dropout(self.reg_dropout_value)(x)
            x = tf.keras.layers.Dense(int(self.encoding_size / 2), activation='relu')(x)
            x = tf.keras.layers.Dropout(self.reg_dropout_value)(x)

            if self.different_out_for_globals:
                out_reg_gv = [tf.keras.layers.Dense(1, activation=self.out_reg_activation)(x)
                              for _ in range(self.n_global_variables)]
            else:
                out_reg_gv = tf.keras.layers.Dense(self.n_global_variables, activation=self.out_reg_activation)(x)

            reg_gv = tf.keras.Model(inputs=input_decoder, outputs=out_reg_gv, name='reg_gv')

            self.id_ += '_with_RegModel'
            o2 = reg_gv(cod)

        # === LOCAL REGRESSOR === #

        if self.n_local_variables > 0:
            x = tf.keras.layers.Reshape((1, self.encoding_size))(input_decoder)
            x = tf.keras.layers.Lambda(exp_dim, arguments={'num_points': self.n_geometry_points})(x)
            x = conv_bn(x, self.seg_kernels[0])
            x = conv_bn(x, self.seg_kernels[1])
            x = conv_bn(x, self.seg_kernels[2])
            x = conv_bn(x, self.seg_kernels[3])
            outputs = tf.keras.layers.Dense(self.n_local_variables,
                                            name="output_fields",
                                            activation=self.out_seg_activation)(x)

            seg_gv = tf.keras.Model(inputs=input_decoder, outputs=outputs, name='seg_gv')
            self.id_ += 'with_SegModel'
            o3 = seg_gv(cod)

        if self.n_global_variables > 0 and self.n_local_variables == 0:
            model = tf.keras.Model(inputs=inputs, outputs=[o1, o2], name=self.id_)
        elif self.n_global_variables > 0 and self.n_local_variables > 0:
            model = tf.keras.Model(inputs=inputs, outputs=[o1, o2, o3], name=self.id_)
        elif self.n_global_variables == 0 and self.n_local_variables > 0:
            model = tf.keras.Model(inputs=inputs, outputs=[o1, o3], name=self.id_)
        else:
            model = tf.keras.Model(inputs=inputs, outputs=o1, name=self.id_)

        self.model = model

        return model

    def model_2_image(self, path: str = ''):
        tf.keras.utils.plot_model(self.model, os.path.join(os.getcwd(),
                                                           path, 'PointNet' +
                                                           date.today().strftime("_%d_%m_%Y") +
                                                           '.png'),
                                  show_shapes=True,
                                  show_dtype=True,
                                  show_layer_names=True,
                                  rankdir="TB",
                                  expand_nested=True,
                                  dpi=96,
                                  layer_range=None,
                                  )
