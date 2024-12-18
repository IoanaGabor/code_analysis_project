import keras
import keras.utils
from keras.layers import Input, Dense, Embedding, Activation, concatenate, Flatten, GRU, TimeDistributed, dot
from keras.models import Model

class CodeGNNGRU:
    def __init__(self, config):
        config['modeltype'] = 'codegnngru'

        self.config = config
        self.tdatvocabsize = config['tdatvocabsize']
        self.comvocabsize = config['comvocabsize']
        self.smlvocabsize = config['smlvocabsize']
        self.tdatlen = config['tdatlen']
        self.comlen = config['comlen']
        self.smllen = config['maxastnodes']

        self.config['batch_maker'] = 'graph_multi_1'

        self.embdims = 100
        self.smldims = 256
        self.recdims = 256
        self.tdddims = 256

    def create_model(self):

        tdat_input = Input(shape=(self.tdatlen,))
        com_input = Input(shape=(self.comlen,))
        node_input = Input(shape=(self.smllen,))
        edge_input = Input(shape=(self.smllen, self.smllen))

        tdel = Embedding(output_dim=self.embdims, input_dim=self.tdatvocabsize, mask_zero=False)
        tde = tdel(tdat_input)

        se = tdel(node_input)

        tenc = GRU(self.recdims, return_state=True, return_sequences=True)
        tencout, tstate_h = tenc(tde)

        de = Embedding(output_dim=self.embdims, input_dim=self.comvocabsize, mask_zero=False)(com_input)
        dec = GRU(self.recdims, return_sequences=True)
        decout = dec(de, initial_state=tstate_h)

        tattn = dot([decout, tencout], axes=[2, 2])
        tattn = Activation('softmax')(tattn)
        tcontext = dot([tattn, tencout], axes=[2, 1])

        astwork = se

        for i in range(self.config['asthops']):
            astwork = GCNLayer(100)([astwork, edge_input])

        astwork = GRU(self.recdims, return_sequences=True)(astwork, initial_state=tstate_h)

        aattn = dot([decout, astwork], axes=[2, 2])
        aattn = Activation('softmax')(aattn)
        acontext = dot([aattn, astwork], axes=[2, 1])

        context = concatenate([tcontext, decout, acontext])

        out = TimeDistributed(Dense(self.tdddims, activation="relu"))(context)

        out = Flatten()(out)
        out1 = Dense(self.comvocabsize, activation="softmax")(out)

        model = Model(inputs=[tdat_input, com_input, node_input, edge_input], outputs=out1)

        model.compile(loss='categorical_crossentropy', optimizer='adamax', metrics=['accuracy'])
        return self.config, model
