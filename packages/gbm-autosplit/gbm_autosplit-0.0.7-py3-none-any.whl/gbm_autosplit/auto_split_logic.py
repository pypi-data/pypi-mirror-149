import logging
import copy

import numpy
from numpy import random

from gbm_autosplit import utils


logger = logging.getLogger(__name__)


def tune_n_estimator(learner, x, y, **kwargs):
    learner_clone = copy.deepcopy(learner)
    xtr, ytr, xva, yva = split_xy(x, y, learner.ratio_training)
    learner_clone.call_parent_fit(
        xtr, ytr, eval_set=[(xva, yva)], **kwargs
    )
    learner.set_params(n_estimators=utils.get_n_estimators(learner_clone))
    learner.set_params(early_stopping_rounds=None)
    if learner.n_estimators == learner.max_n_estimators:
        logger.warning("n_estimators reached max_n_estimators: {}".format(learner.n_estimators))


def split_xy(x, y, training_ratio):
    sample_size = len(y)
    size_training = int(training_ratio * sample_size)
    indices_list = numpy.arange(x.shape[0])
    random.shuffle(indices_list)
    indices_training = indices_list[:size_training]
    indices_validation = indices_list[size_training:]
    return x[indices_training, :], y[indices_training], x[indices_validation, :], y[indices_validation]
