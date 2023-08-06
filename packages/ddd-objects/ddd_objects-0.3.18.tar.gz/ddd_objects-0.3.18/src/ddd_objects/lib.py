import string, random, hashlib
import os, logging
import time, datetime

def get_random_string(l=10):
    letters = string.digits + string.ascii_letters
    return ''.join(random.choice(letters) for i in range(l))

class Logger:
    def __init__(self, log_fn='/tmp/log/log.log', timezone=8):
        def _timezone_converter(sec, what):
            localtime = datetime.datetime.utcnow() + datetime.timedelta(hours=timezone)
            return localtime.timetuple()
        logging.Formatter.converter = _timezone_converter
        log_dir = os.path.dirname(log_fn)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        logging.basicConfig(
            level = logging.INFO,
            format = '%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        handler = logging.FileHandler(log_fn)
        console = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        console.setLevel(logging.ERROR)
        formatter = logging.Formatter('%(asctime)s -  %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.addHandler(console)
        self.labels = 'none'
        self.info = self.logger.info
        self.warn = self.logger.warn
        self.error = self.logger.error

    def start_timer(self):
        self.curr = time.time()

    def get_runtime(self, format='s', log_metrics=False, labels=None):
        curr = time.time()
        t = (curr-self.curr)
        if labels is None:
            labels = self.labels
        if format=='s':
            pass
        elif format=='m':
            t = t/60
        elif format=='h':
            t = t/3600
        else:
            raise ValueError('wrong value for parameter "format"!')
        if log_metrics:
            self.info(f'runtime: {t}, labels: {labels}')
        return t

    def set_process_value(self, value, total=None, labels=None):
        if total is None:
            total = 100
        if labels is None:
            labels = self.labels
        self.info(f'the task is completed {value/total} percent, labels: {labels}')

    def set_labels(self, labels=None, file_name=None):
        if labels is None:
            labels = '/'.join(file_name.split('/')[-2:])
            labels = '.'.join(labels.split('.')[:-1])
            labels += f'-{get_random_string(5)}'
            labels = f'task%{labels}|'
        self.labels = labels

def get_md5(txt):
    md5hash = hashlib.md5(str(txt).encode('utf-8'))
    return md5hash.hexdigest()