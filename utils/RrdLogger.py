#!/usr/bin/env python
# -*- coding: utf-8 -*-
from logging.handlers import TimedRotatingFileHandler
import logging
import sys
import os
import time


workdir = os.path.split(os.path.realpath(__file__))[0]


class RrdLogger(object):
    def __init__(self):
        self._LoggerInstance = None

    def getLogger(self, name):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        timeFormator = '%Y%m%d'
        nowString = time.strftime(timeFormator, time.localtime(time.time()))
        file_name = 'log_{}.log'.format(nowString)
        # os.chdir(workdir)
        root_path = os.path.abspath(os.path.join(workdir, ".."))
        _folder_path = os.path.join(root_path, 'RrdLogs')
        if not os.path.exists(_folder_path):
            os.mkdir(_folder_path)
        filePath = os.path.join(_folder_path, file_name)
        t = int(time.time())
        if TimedRotatingFileHandler(filePath).when.startswith('D') and time.localtime(t).tm_mday==time.localtime(TimedRotatingFileHandler(filePath).rolloverAt).tm_mday:
            return 1
            if t >= TimedRotatingFileHandler(filePath).rolloverAt:
                return 1
            else:
                return 0
        else:
             pass

        # FileHandler
        fh = logging.FileHandler(filePath,mode='a', encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('******%(asctime)s - %(name)s - %(filename)s,line %(lineno)s - %(levelname)s: %(message)s')
        fh.setFormatter(formatter)

        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(formatter)
        sh.setLevel(logging.DEBUG)
        logger.addHandler(fh)
        logger.addHandler(sh)
        # logger.addHandler(uh)

        return logger


