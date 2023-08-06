import logging

logger = logging.getLogger(__name__)


class MicroLibTemplate(object):

    @staticmethod
    def greeting(name):
        return 'Hello %s' % name
