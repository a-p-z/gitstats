import logging


class PercentageLogging:

    def __init__(self, step, total):
        self.step = step
        self.total = total
        self.last_logged_percentage = -1

    def info(self, i, msg, *args, **kwargs):
        percentage = int(100 * i / self.total)
        if percentage > self.last_logged_percentage and percentage % self.step == 0:
            self.last_logged_percentage = percentage
            args = list(args)
            args.append(percentage)
            logging.info(msg, *args, **kwargs)

        if i == self.total - 1:
            args = list(args)
            args.append(100)
            logging.info(msg, *args, **kwargs)
