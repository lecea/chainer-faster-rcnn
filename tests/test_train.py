#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib  # isort:skip
matplotlib.use('Agg')  # isort:skip

import sys  # isort:skip
sys.path.insert(0, '.')  # isort:skip

import chainer
from chainer import iterators
from chainer import optimizers
from chainer import training
from chainer.training import extensions
from datasets.pascal_voc_dataset import VOC
from models.faster_rcnn import FasterRCNN

if __name__ == '__main__':
    batchsize = 1
    
    train_dataset = VOC('train')
    valid_dataset = VOC('val')

    train_iter = iterators.SerialIterator(train_dataset, batchsize)
    model = FasterRCNN()
    model.rpn_train = True
    # model.rcnn_train = True
    model.to_gpu(0)

    # optimizer = optimizers.Adam()
    # optimizer.setup(model)
    optimizer = optimizers.MomentumSGD(lr=0.001)
    optimizer.setup(model)
    optimizer.add_hook(chainer.optimizer.WeightDecay(0.0005))

    updater = training.StandardUpdater(train_iter, optimizer, device=0)
    trainer = training.Trainer(updater, (100, 'epoch'), out='tests/train_test')
    trainer.extend(extensions.LogReport(trigger=(1, 'iteration')))
    trainer.extend(extensions.PrintReport([
        'epoch', 'iteration',
        'main/RPN/rpn_loss',
        'main/RPN/rpn_loss_cls',
        'main/RPN/rpn_loss_bbox',
        'main/loss_cls',
        'main/loss_bbox',
        'main/loss_rcnn',
        'elapsed_time',
    ]), trigger=(1, 'iteration'))

    trainer.run()
