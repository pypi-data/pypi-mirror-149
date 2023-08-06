import logging
import os
import sys
import warnings
from os.path import expanduser
import os
import json

from treform.utility.base_util import db_hostname, is_my_pc
from treform.utility.log_util import LogUtil

class Config():
    def __init__(self, json_file):
        warnings.simplefilter(action='ignore', category=FutureWarning)  # ignore future warnings

        self.log = None
        if self.log is None:
            if len(sys.argv) == 1:  # by Pycharm or console
                if is_my_pc():  # my pc (pycharm client, mac)
                    self.log = LogUtil.get_logger(None, level=logging.DEBUG, console_mode=True)  # global log
                else:  # gpu pc (batch job, ubuntu)
                    self.log = LogUtil.get_logger(sys.argv[0], level=logging.DEBUG, console_mode=True)  # global log # console_mode=True for jupyter
            else:  # by batch script
                self.log = LogUtil.get_logger(sys.argv[0], level=logging.INFO, console_mode=False)  # global log

        #json_file = '/resources/korean_spelling_config.json'
        with open(json_file, encoding='utf-8') as f:
            config = json.load(f)

        self.HOME_DIR = config["HOME_DIR"]
        self.log.info('HOME_DIR: %s' % self.HOME_DIR)

        self.SPELLING_MODEL_DIR = config["SPELLING_MODEL_DIR"]

        self.PROJECT_DIR = os.path.join(self.HOME_DIR, '')

        self.DATA_DIR = os.path.join(self.PROJECT_DIR, 'data')
        self.log.info('DATA_DIR: %s' % self.DATA_DIR)
        if not os.path.exists(self.DATA_DIR):
            os.mkdir(self.DATA_DIR)

        self.MODELS_DIR = os.path.join(self.PROJECT_DIR, 'models')
        self.log.info('MODELS_DIR: %s' % self.MODELS_DIR)
        if not os.path.exists(self.MODELS_DIR):
            os.mkdir(self.MODELS_DIR)

        #################################################
        # tensorboard log dir
        #################################################
        self.TENSORBOARD_LOG_DIR = os.path.join(self.HOME_DIR, 'tensorboard_log')
        # log.info('TENSORBOARD_LOG_DIR: %s' % TENSORBOARD_LOG_DIR)
        if not os.path.exists(self.TENSORBOARD_LOG_DIR):
            os.mkdir(self.TENSORBOARD_LOG_DIR)

        #################################################
        # mnist
        #################################################
        self.MNIST_DIR = os.path.join(self.HOME_DIR, 'workspace', 'nlp4kor_tensorflow-mnist')
        self.MNIST_DATA_DIR = os.path.join(self.MNIST_DIR, 'data')
        self.MNIST_CNN_MODEL_DIR = os.path.join(self.MNIST_DIR, 'models', 'cnn')
        self.MNIST_DAE_MODEL_DIR = os.path.join(self.MNIST_DIR, 'models', 'dae')

        #################################################
        # ko.wikipedia.org
        #################################################
        self.KO_WIKIPEDIA_ORG_DIR = os.path.join(self.HOME_DIR, 'spelling_training')

        self.KO_WIKIPEDIA_ORG_INFO_FILE = os.path.join(self.KO_WIKIPEDIA_ORG_DIR, 'ko.wikipedia.org.info.txt')
        self.KO_WIKIPEDIA_ORG_URLS_FILE = os.path.join(self.KO_WIKIPEDIA_ORG_DIR, 'ko.wikipedia.org.urls.txt')
        self.KO_WIKIPEDIA_ORG_CHARACTERS_FILE = os.path.join(self.KO_WIKIPEDIA_ORG_DIR, 'ko.wikipedia.org.characters')

        self.KO_WIKIPEDIA_ORG_SENTENCES_FILE = os.path.join(self.KO_WIKIPEDIA_ORG_DIR, 'ko.wikipedia.org.sentences.gz')
        self.KO_WIKIPEDIA_ORG_TRAIN_SENTENCES_FILE = os.path.join(self.KO_WIKIPEDIA_ORG_DIR, 'ko.wikipedia.org.train.sentences.gz')
        self.KO_WIKIPEDIA_ORG_VALID_SENTENCES_FILE = os.path.join(self.KO_WIKIPEDIA_ORG_DIR, 'ko.wikipedia.org.valid.sentences.gz')
        self.KO_WIKIPEDIA_ORG_TEST_SENTENCES_FILE = os.path.join(self.KO_WIKIPEDIA_ORG_DIR, 'ko.wikipedia.org.test.sentences.gz')

        self.KO_WIKIPEDIA_ORG_SPELLING_ERROR_CORRECTION_MODEL_DIR = os.path.join(self.KO_WIKIPEDIA_ORG_DIR, 'models', 'spelling_error_correction')

        #################################################
        # ko.wikipedia.org
        #################################################
        self.WIKIPEDIA_DIR = config["WIKIPEDIA_DIR"]

        # text (with string)
        #WIKIPEDIA_DATA_DIR = os.path.join(WIKIPEDIA_DIR, 'data')
        self.WIKIPEDIA_DATA_DIR = self.WIKIPEDIA_DIR
        if not os.path.exists(self.WIKIPEDIA_DATA_DIR):
            os.mkdir(self.WIKIPEDIA_DATA_DIR)

        # info
        self.WIKIPEDIA_INFO_FILE = os.path.join(self.WIKIPEDIA_DATA_DIR, 'ko.wikipedia.org.info.txt')
        self.WIKIPEDIA_URLS_FILE = os.path.join(self.WIKIPEDIA_DATA_DIR, 'ko.wikipedia.org.urls.txt')

        self.WIKIPEDIA_CHARACTERS_FILE = os.path.join(self.WIKIPEDIA_DATA_DIR, 'ko.wikipedia.org.characters')
        self.WIKIPEDIA_SENTENCES_FILE = os.path.join(self.WIKIPEDIA_DATA_DIR, 'ko.wikipedia.org.sentences.gz')

        self.WIKIPEDIA_TRAIN_SENTENCES_FILE = os.path.join(self.WIKIPEDIA_DATA_DIR, 'ko.wikipedia.org.train.sentences.gz')
        self.WIKIPEDIA_VALID_SENTENCES_FILE = os.path.join(self.WIKIPEDIA_DATA_DIR, 'ko.wikipedia.org.valid.sentences.gz')
        self.WIKIPEDIA_TEST_SENTENCES_FILE = os.path.join(self.WIKIPEDIA_DATA_DIR, 'ko.wikipedia.org.test.sentences.gz')

        # csv (with character id)
        self.WIKIPEDIA_TRAIN_FILE = os.path.join(self.WIKIPEDIA_DATA_DIR, 'ko.wikipedia.org.train.sentences.cid.gz')
        self.WIKIPEDIA_VALID_FILE = os.path.join(self.WIKIPEDIA_DATA_DIR, 'ko.wikipedia.org.valid.sentences.cid.gz')
        self.WIKIPEDIA_TEST_FILE = os.path.join(self.WIKIPEDIA_DATA_DIR, 'ko.wikipedia.org.test.sentences.cid.gz')

        self.WIKIPEDIA_NE_FILE = os.path.join(self.WIKIPEDIA_DATA_DIR, 'ko.wikipedia.org.sentences.ne.gz')