import logging
import io
from . import settings as djsciops_settings

log = logging.getLogger("Primary")
log_format = logging.Formatter(
    "[%(asctime)s][%(funcName)s][%(levelname)s]: %(message)s"
)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(log_format)

log.setLevel(level=djsciops_settings.LOG_LEVEL.upper())
log.handlers = [stream_handler]

# https://github.com/tqdm/tqdm/issues/313#issuecomment-267959111
class TqdmToLogger(io.StringIO):
    """
    Output stream for TQDM which will output to logger module instead of
    the StdOut.
    """

    logger = None
    level = None
    buf = ""

    def __init__(self, logger, level=None):
        super(TqdmToLogger, self).__init__()
        self.logger = logger
        self.level = level or logging.INFO

    def write(self, buf):
        self.buf = buf.strip("\r\n\t ")

    def flush(self):
        self.logger.log(self.level, self.buf)
