import json

from pycrfsuite_spacing import PyCRFSuiteSpacing
from pycrfsuite_spacing import TemplateGenerator
from pycrfsuite_spacing import CharacterFeatureTransformer

import tensorflow as tf


class BaseSegmentation:
    IN_TYPE = [str]
    OUT_TYPE = [str]


class SegmentationKorean(BaseSegmentation):
    def __init__(self, model=None):
        # model_path = 'demo_model.crfsuite'
        to_feature = CharacterFeatureTransformer(
            TemplateGenerator(
                begin=-2,
                end=2,
                min_range_length=3,
                max_range_length=3)
        )
        self.inst = PyCRFSuiteSpacing(to_feature)
        self.inst.load_tagger(model)

    def __call__(self, *args, **kwargs):
        return self.inst(args[0])


from treform.segmentation.lstmWordSegmentationModel import *
from treform.segmentation.wordSegmentationModelUtil import *


class LSTMSegmentationKorean(BaseSegmentation):
    def __init__(self, model_path='./model'):
        self.model = model_path
        dic_path = self.model + '/' + 'dic.pickle'

        # config
        self.n_steps = 30  # time steps
        self.padd = '\t'  # special padding chracter
        with open(dic_path, 'rb') as handle:
            self.char_dic = pickle.load(handle)  # load dic
        n_input = len(self.char_dic)  # input dimension, vocab size
        self.n_hidden = 8  # hidden layer size
        self.n_classes = 2  # output classes,  space or not
        self.vocab_size = n_input

        self.x = tf.placeholder(tf.float32, [None, self.n_steps, n_input])
        self.y_ = tf.placeholder(tf.int32, [None, self.n_steps])
        self.early_stop = tf.placeholder(tf.int32)

        # LSTM layer
        # 2 x n_hidden = state_size = (hidden state + cell state)
        self.istate = tf.placeholder(tf.float32, [None, 2 * self.n_hidden])
        weights = {
            'hidden': weight_variable([n_input, self.n_hidden]),
            'out': weight_variable([self.n_hidden, self.n_classes])
        }
        biases = {
            'hidden': bias_variable([self.n_hidden]),
            'out': bias_variable([self.n_classes])
        }

        self.y = RNN(self.x, self.istate, weights, biases, self.n_hidden, self.n_steps, n_input, self.early_stop)

        self.batch_size = 1
        self.logits = tf.reshape(tf.concat(self.y, 1), [-1, self.n_classes])

        NUM_THREADS = 1
        config = tf.ConfigProto(intra_op_parallelism_threads=NUM_THREADS,
                                inter_op_parallelism_threads=NUM_THREADS,
                                log_device_placement=False)
        self.sess = tf.Session(config=config)
        init = tf.global_variables_initializer()
        self.sess.run(init)
        saver = tf.train.Saver()  # save all variables
        checkpoint_dir = self.model
        ckpt = tf.train.get_checkpoint_state(checkpoint_dir)
        if ckpt and ckpt.model_checkpoint_path:
            saver.restore(self.sess, ckpt.model_checkpoint_path)
            sys.stderr.write("model restored from %s\n" % (ckpt.model_checkpoint_path))
        else:
            sys.stderr.write("no checkpoint found" + '\n')
            sys.exit(-1)

    def __call__(self, *args, **kwargs):

        sentence = args[0]
        sentence_size = len(sentence)
        tag_vector = [-1] * (sentence_size + self.n_steps)  # buffer n_steps
        pos = 0
        while pos != -1:
            batch_xs, batch_ys, next_pos, count = next_batch(sentence, pos, self.char_dic, self.vocab_size,
                                                             self.n_steps, self.padd)
            '''
            print 'window : ' + sentence[pos:pos+n_steps]
            print 'count : ' + str(count)
            print 'next_pos : ' + str(next_pos)
            print batch_ys
            '''
            c_istate = np.zeros((self.batch_size, 2 * self.n_hidden))
            feed = {self.x: batch_xs, self.y_: batch_ys, self.istate: c_istate, self.early_stop: count}
            argmax = tf.arg_max(self.logits, 1)
            result = self.sess.run(argmax, feed_dict=feed)

            # overlapped copy and merge
            j = 0
            result_size = len(result)
            while j < result_size:
                tag = result[j]
                if tag_vector[pos + j] == -1:
                    tag_vector[pos + j] = tag
                else:
                    if tag_vector[pos + j] == CLASS_1:  # 1
                        if tag == CLASS_0:  # 1 -> 0
                            sys.stderr.write("1->0\n")
                            tag_vector[pos + j] = tag
                    else:  # 0
                        if tag == CLASS_1:  # 0 -> 1
                            sys.stderr.write("0->1\n")
                            tag_vector[pos + j] = tag
                j += 1
            pos = next_pos
        # generate output using tag_vector
        print
        'out = ' + to_sentence(tag_vector, sentence)

        return to_sentence(tag_vector, sentence)

    def close(self):
        self.sess.close()


class CNNSegmentationKorean(BaseSegmentation):
    def __init__(self, model_file='./model', training_config='', char_file=''):
        self.model_file = model_file
        self.training_config = training_config
        self.char_file = char_file

        #self.model, self.vocab_table = self.load(model_file=model_file, training_config=training_config, char_file=char_file)


    def load(self, model_file='', training_config='', char_file=''):
        with open(training_config, encoding='utf-8') as f:
            config = json.load(f)

        with open(char_file, encoding='utf=8') as f:
            content = f.read()
            keys = ["<pad>", "<s>", "</s>", "<unk>"] + list(content)
            values = list(range(len(keys)))

            vocab_initializer = tf.lookup.KeyValueTensorInitializer(keys, values, key_dtype=tf.string, value_dtype=tf.int32)
            vocab_table = tf.lookup.StaticHashTable(vocab_initializer, default_value=3)

        #To be implemented
        model = None

        model.load_weights(model_file)
        model(tf.keras.Input([None], dtype=tf.int32))
        model.summary()

        return model, vocab_table

    def predict(self, model, vocab_table, input_str):
        inference = self.get_inference_fn(model, vocab_table)
        input_str = tf.constant(input_str)
        result = inference(input_str).numpy()
        #print(b"".join(result).decode("utf8"))
        return b"".join(result).decode("utf8")

    def get_inference_fn(self, model, vocab_table):
        @tf.function
        def inference(tensors):
            byte_array = tf.concat(
                [["<s>"], tf.strings.unicode_split(tf.strings.regex_replace(tensors, " +", " "), "UTF-8"), ["</s>"]], axis=0
            )
            strings = vocab_table.lookup(byte_array)[tf.newaxis, :]

            model_output = tf.argmax(model(strings), axis=-1)[0]
            return convert_output_to_string(byte_array, model_output)

        return inference


    #def __call__(self, *args, **kwargs):
    #    return self.predict(self.model, self.vocab_table, args[0])

def convert_output_to_string(byte_array, model_output):
    sequence_length = tf.size(model_output)
    while_condition = lambda i, *_: i < sequence_length

    def while_body(i, o):
        o = tf.cond(
            model_output[i] == 1,
            lambda: tf.concat([o, [byte_array[i], " "]], axis=0),
            lambda: tf.cond(
                (model_output[i] == 2) and (byte_array[i] == " "),
                lambda: o,
                lambda: tf.concat([o, [byte_array[i]]], axis=0),
                ),
            )
        return i + 1, o

    _, strings_result = tf.while_loop(
        while_condition,
        while_body,
        (tf.constant(0), tf.constant([], dtype=tf.string)),
        shape_invariants=(tf.TensorShape([]), tf.TensorShape([None])),
    )
    return strings_result

if __name__ == "__main__":
    model_file = '../../models/checkpoint-12.ckpt'
    training_config = '../../resources/config.json'
    char_file = '../../resources/chars-4996'

    spacing = CNNSegmentationKorean()

    model, vocab_table = spacing.load(model_file=model_file, training_config=training_config, char_file=char_file)
    input_str = '오늘은우울한날이야...ㅜㅜ'
    result = spacing.predict(model, vocab_table, input_str)
    result = result.replace('<s>','')
    result = result.replace('</s>', '')
    print(result)