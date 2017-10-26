
class RemoteStatus(object):
    AVAILABLE = 0
    UN_AVAILABLE = 1

    def __init__(self):
        self.status = self.AVAILABLE

    def success(self):
        self.status = self.AVAILABLE

    def fail(self):
        self.status = self.UN_AVAILABLE

    def is_failed(self):
        return self.status == self.UN_AVAILABLE
