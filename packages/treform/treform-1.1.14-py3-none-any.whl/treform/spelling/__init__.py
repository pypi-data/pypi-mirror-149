from treform.spelling import *
import treform
from treform.spelling.config import Config

import os

from treform.utility.dataset import DataSet
from treform.utility.num_util import NumUtil
from treform.utility.char_one_hot_vector import CharOneHotVector
from treform.utility.datafile_util import DataFileUtil
from treform.spelling.spelling_error_correction_upgraded import SpellingErrorCorrection
import tensorflow as tf


class BaseSpellingCorrector:
    IN_TYPE = [str]
    OUT_TYPE = [str]

class DAESpellingCorrector(BaseSpellingCorrector):
    IN_TYPE = [str]
    OUT_TYPE = [str]

    def __init__(self, json_file=''):
        config = Config(json_file)
        KO_WIKIPEDIA_ORG_SPELLING_ERROR_CORRECTION_MODEL_DIR = config.KO_WIKIPEDIA_ORG_SPELLING_ERROR_CORRECTION_MODEL_DIR
        KO_WIKIPEDIA_ORG_TRAIN_SENTENCES_FILE = config.KO_WIKIPEDIA_ORG_TRAIN_SENTENCES_FILE
        KO_WIKIPEDIA_ORG_VALID_SENTENCES_FILE = config.KO_WIKIPEDIA_ORG_VALID_SENTENCES_FILE
        KO_WIKIPEDIA_ORG_TEST_SENTENCES_FILE = config.KO_WIKIPEDIA_ORG_TEST_SENTENCES_FILE
        KO_WIKIPEDIA_ORG_CHARACTERS_FILE = config.KO_WIKIPEDIA_ORG_CHARACTERS_FILE
        KO_WIKIPEDIA_ORG_DIR = config.KO_WIKIPEDIA_ORG_DIR
        self.window_size = 10
        characters_file = KO_WIKIPEDIA_ORG_CHARACTERS_FILE
        #D:\python_workspace\treform\treform\spelling\models\spelling_error_correction\spelling_error_correction_model.sentences=3.window_size=10.noise_rate=0.1.n_hidden=100
        #self.model_file = os.path.join(KO_WIKIPEDIA_ORG_SPELLING_ERROR_CORRECTION_MODEL_DIR,
        #                            'spelling_error_correction_model.sentences=3.window_size=10.noise_rate=0.1.n_hidden=100')

        self.A = config.SPELLING_MODEL_DIR
        self.model_file = config.SPELLING_MODEL_DIR + "/model"
        self.model_meta_file = config.SPELLING_MODEL_DIR + "/model.meta"
        self.features_vector = CharOneHotVector(DataFileUtil.read_list(characters_file))
        labels_vector = CharOneHotVector(DataFileUtil.read_list(characters_file))
        self.n_features = len(self.features_vector) * self.window_size  # number of features
        n_classes = len(labels_vector) * self.window_size
        self.total_epoch = 5
        self.features_vector_size = self.n_features // self.window_size

    def __call__(self, *args, **kwargs):
        #model_path = "/home/bible/treform/spelling_training/models/spelling_error_correction/spelling_error_correction_model.sentences=3.window_size=10.noise_rate=0.1.n_hidden=100/model"

        tf.compat.v1.disable_v2_behavior()
        tf.compat.v1.disable_eager_execution()

        detection_graph = tf.compat.v1.get_default_graph()

        with detection_graph.as_default() as default_graph:

            with tf.compat.v1.Session() as sess:
                # Load the graph with the trained states
                loader = tf.compat.v1.train.import_meta_graph(self.model_meta_file)
                loader.restore(sess, self.model_file)

                # Get the tensors by their variable name
                # Make predictions
                dropout_keep_rate = 1.0
                dropout_keep_prob = tf.compat.v1.placeholder(tf.compat.v1.float32)
                X = detection_graph.get_tensor_by_name('X:0')  # shape=(batch_size, window_size * feature_vector.size)
                # X = tf.cast(X, dtype='float32')
                print(X)
                Y = detection_graph.get_tensor_by_name('Y:0')
                W1 = detection_graph.get_tensor_by_name('W1:0')
                print(W1)
                # W1 = tf.cast(W1, dtype='float32')
                b1 = detection_graph.get_tensor_by_name('b1:0')
                print(b1)

                # op = sess.graph.get_operations()
                # for m in op:
                #    print(m)

                # b1 = tf.cast(b1, dtype='float32')
                layer1 = tf.compat.v1.nn.sigmoid(tf.compat.v1.matmul(X, W1) + b1, name='layer1')
                layer1_dropout = tf.compat.v1.nn.dropout(layer1, dropout_keep_prob, name='layer1_dropout')

                noised_sentence = SpellingErrorCorrection.encode_noise(args[0], noise_rate=0.1)
                denoised_sentence = noised_sentence[:]  # will be changed with predict
                for start in range(0, len(noised_sentence) - self.window_size + 1):
                    chars = denoised_sentence[start: start + self.window_size]
                    original_chars = args[0][start: start + self.window_size]
                    _features = [chars]
                    _labels = [original_chars]

                    dataset = DataSet(features=_features, labels=_labels, features_vector=self.features_vector,
                                      labels_vector=self.features_vector)
                    dataset.convert_to_one_hot_vector()
                    try:
                        _y_hat, _cost, _accuracy = sess.run(['y_hat:0', 'cost:0', 'accuracy:0'],
                                                            feed_dict={X: dataset.features, Y: dataset.labels,
                                                                       dropout_keep_prob: dropout_keep_rate})

                        y_hats = [self.features_vector.to_values(_l) for _l in _y_hat]
                        #if _features[0] == y_hats[0]:
                        #    print('same   : "%s"' % (_features[0]))
                        #else:
                        #    print('denoise: "%s" -> "%s"' % (_features[0], y_hats[0]))
                        denoised_sentence = denoised_sentence.replace(_features[0], y_hats[0])
                    except:
                        print('"%s"%s "%s"%s' % (chars, dataset.features.shape, original_chars, dataset.labels.shape))

                    #print(denoised_sentence)

        return denoised_sentence
