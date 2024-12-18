import tensorflow as tf
from keras.layers import Layer
from keras import activations
import keras.backend as K

class GCNLayer(Layer):
    def __init__(self, units, activation='relu', initializer='glorot_uniform', sparse=False, use_bias=True, **kwargs):
        self.activation = activations.get(activation)
        self.output_dim = units
        self.initializer = initializer
        self.sparse = sparse
        self.use_bias = use_bias

        super(GCNLayer, self).__init__(**kwargs)

    def build(self, input_shape):
        self.kernel = self.add_weight(name='kernel',
                                          shape=(input_shape[0][-1], self.output_dim),
                                          initializer=self.initializer,
                                          trainable=True)
        if self.use_bias:
            self.bias = self.add_weight(name='bias',
                                              shape=(self.output_dim,),
                                              initializer='zeros',
                                              trainable=True)
        else:
            self.bias = None

        super(GCNLayer, self).build(input_shape)

    def call(self, x):
        assert isinstance(x, list)
        nodes, edges = x
        identity = tf.eye(tf.shape(edges)[-1], batch_shape=[tf.shape(edges)[0]], dtype=edges.dtype)
        edges = edges + identity
        output = tf.matmul(edges,nodes)
        output = tf.matmul(output, self.kernel)

        if self.use_bias:
            output += self.bias

        return self.activation(output)

    def compute_output_shape(self, input_shape):
        assert isinstance(input_shape, list)
        return (None,input_shape[0][1], self.output_dim)

    def get_config(self):
        config = {
            'units': self.output_dim,
            'activation': activations.serialize(self.activation),
        }

        base_config = super(GCNLayer, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))
