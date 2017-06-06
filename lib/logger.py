import syslog
import logging
from logging import handlers

def init_logger(use_syslog=False, logfile=None, email=None):
    _log = logging.getLogger('namecheap-dyndns')
    _log.setLevel(logging.DEBUG)
    formatter = logging.Formatter(fmt='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    sth = logging.StreamHandler()
    sth.setLevel(logging.DEBUG)
    sth.setFormatter(formatter)
    _log.addHandler(sth)
    if use_syslog:
        sh = handlers.SysLogHandler(address='/dev/log') # /var/log/syslog for OS X
        sh.setLevel(logging.DEBUG)
        sh.setFormatter(formatter)
        _log.addHandler(sh)
    if logfile:
        rh = handlers.RotatingFileHandler(filename=logfile, maxBytes=20*1000*1000, backupCount=3)
        rh.setLevel(logging.DEBUG)
        rh.setFormatter(formatter)
        _log.addHandler(rh)
    if email:
        eh = handlers.SMTPHandler(
            mailhost=(email.server,587),
            fromaddr=email.fromaddr,
            toaddrs=email.to,
            subject='namecheap-dyndns error',
            credentials=(email.user, email.pw),
            secure=()
        )
        eh.setLevel(logging.ERROR) # only send emails when errors happen
        eh.setFormatter(formatter)
        _log.addHandler(eh)

def log_msg(msg, *args):
    _log = logging.getLogger('namecheap-dyndns')
    _log.info(msg.format(*args))

def log_err(msg, *args):
    _log = logging.getLogger('namecheap-dyndns')
    _log.error(msg.format(*args))
