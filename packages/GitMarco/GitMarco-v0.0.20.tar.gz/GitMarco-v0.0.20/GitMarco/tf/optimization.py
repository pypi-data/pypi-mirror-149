import os

import numpy as np
from ..graphics.matplotlib import plot_2d
import pandas as pd
import tensorflow as tf
from tqdm import tqdm


class GradientOptimizer(object):
    def __init__(self,
                 model,
                 df,
                 scaler,
                 loss,
                 iterations: int = 1,
                 n_labels: int = 1,
                 n_features: int = 1,
                 learning_rate: float = 0.001,
                 scheduler=None,
                 starting_sample=None,
                 log: bool = False,
                 log_step: int = 1,
                 optimizer: str = 'Adam',
                 fit_scaler: bool = True,
                 ):

        if isinstance(model, str):
            if os.path.exists(model):
                self.model = tf.keras.models.load_model(model)
        else:
            self.model = model

        print('Model correctly loaded')

        df = pd.read_excel(df) if isinstance(df, str) else df
        self.df = df
        print('Dataset correctly loaded')

        scaler.fit(df) if fit_scaler else None
        standard_df = pd.DataFrame(scaler.transform(df), columns=df.columns)
        self.scaler = scaler

        self.min_values = standard_df.describe().T['min'][:df.shape[1] - n_labels].to_numpy()
        self.max_values = standard_df.describe().T['max'][:df.shape[1] - n_labels].to_numpy()

        self.learning_rate = learning_rate if scheduler is None else learning_rate

        self.loss = loss
        self.loss.update_params(dict(
            min_values=self.min_values,
            max_values=self.max_values,
            model=self.model
        ))

        self.iterations = iterations
        self.log = log
        self.log_step = log_step
        self.n_labels = n_labels
        self.n_features = n_features
        self.starting_sample = starting_sample
        self.sample = None
        self.optimizer = None
        self.optimizer_str = optimizer
        self.losses = []
        self.samples = []

        self.reset()

    def reset(self):
        if self.starting_sample is None:
            self.sample = (np.random.rand(self.n_features) * (self.max_values -
                                                              self.min_values) + self.min_values).reshape(1, -1)
        else:
            self.sample = self.starting_sample

        assert len(self.sample.shape) == 2, 'Imput sample must be 2D'

        self.sample = tf.Variable(self.sample)
        self.optimizer = tf.keras.optimizers.get(self.optimizer_str)
        self.optimizer.learning_rate = self.learning_rate

        self.losses = []
        self.samples = []

    def run(self):
        for i in tqdm(range(self.iterations)):
            with tf.GradientTape(persistent=True) as tape:
                tape.watch(self.sample)
                loss = self.loss(self.sample)
                self.losses.append(tf.identity(loss).numpy())
                self.samples.append(tf.identity(self.sample))

            if i % self.log_step == 0 and self.log:
                print(f'{i}. Loss: {loss}')
            grads = tape.gradient(loss, self.sample)
            self.optimizer.apply_gradients(zip([grads], [self.sample]))

    def history(self):
        plot = plot_2d(np.arange(len(self.losses)),
                       np.array(self.losses, dtype=np.float32),
                       title='History',
                       show=False,
                       xlabel='epochs',
                       ylabel='reward',
                       size=(8, 6),
                       line_width=1,
                       line_color='blue',
                       label='history'
                       )
        return plot

    def get_best_sample(self):
        return self.samples[np.argmin(self.losses)]

    def get_results(self, sample=None) -> pd.DataFrame:

        sample = self.get_best_sample() if sample is None else sample

        return pd.DataFrame(
            self.scaler.inverse_transform(np.hstack((sample.numpy().reshape(-1),
                                                     self.model(sample)[0].numpy().reshape(-1))).reshape(1, -1)),
            columns=self.df.columns)

    def compare_bounds(self, sample=None):
        sample = self.get_best_sample() if sample is None else sample

        tmp = pd.concat([self.df.describe().T['min'], self.df.describe().T['max'],
                         self.get_results(sample).T], axis=1)
        tmp.columns = ['min', 'max', 'sample']
        tmp['check'] = np.logical_and(tmp['min'] <= tmp['sample'],
                                      tmp['max'] >= tmp['sample'])
        return tmp


class OptiLoss(object):
    def __init__(self, params: dict = None):
        self.update_params(params)

    def update_params(self, params: dict = None):
        if params is None:
            params = {}
        for key in params:
            vars(self)[key] = params[key]

    def __call__(self, sample):
        return -1
