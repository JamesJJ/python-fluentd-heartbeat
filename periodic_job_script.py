import logging as log
import os
import sys
import time
import json
import random
from fluent import sender
from pprint import pformat as pf
from pprint import pprint as pp


log_level = str(os.getenv('LOG_LEVEL', 'INFO')).upper()

sleep_duration = int(os.getenv('SLEEP_DURATION', 600))

fluentd_host = str(
    os.getenv(
        'FLUENTD_HOST',
        'localhost'))

fluentd_port = int(
    os.getenv(
        'FLUENTD_PORT',
        24224))

fluentd_tag = str(
    os.getenv(
        'FLUENTD_TAG',
        'heartbeat'))

json_mode = str(
    os.getenv(
        'JSON_MODE',
        'string'))

message_key = str(
    os.getenv(
        'MESSAGE_KEY',
        ''))

message = str(
    os.getenv(
        'MESSAGE',
        '{ }'))

if json_mode == 'string':
    json_mode = 'string'
elif json_mode == 'object':
    json_mode = 'object'
else:
    json_mode = 'none'


log.getLogger('').setLevel(log.getLevelName(log_level))
log.debug("""LOG_LEVEL: {0}""".format(str(log_level)))
log.debug("""SLEEP_DURATION: {0}""".format(str(sleep_duration)))
log.debug("""FLUENTD_HOST: {0}""".format(str(fluentd_host)))
log.debug("""FLUENTD_PORT: {0}""".format(str(fluentd_port)))
log.debug("""FLUENTD_TAG: {0}""".format(str(fluentd_tag)))
log.debug("""MESSAGE: {0}""".format(str(message)))
log.debug("""JSON_MODE: {0}""".format(str(json_mode)))


def this_version_string():
    si = sys.implementation.name if hasattr(sys, 'implementation') else 'python_unknown'
    sv = sys.version_info
    return json.dumps({"python": """{0}-{1}.{2}.{3}-{4}-{5}""".format(si,
                                                                      sv.major,
                                                                      sv.minor,
                                                                      sv.micro,
                                                                      sv.releaselevel,
                                                                      sv.serial).lower(),
                       "config": str(os.getenv('APP_CONFIG_VERSION',
                                               'unknown'))},
                      indent=None,
                      sort_keys=True)


def do_sleep(t):
    st = random.randint(int(t * 0.6), int(t * 1.4))
    log.debug('Sleeping for {0} seconds'.format(st))
    time.sleep(st)
    log.debug('Now awake (slept {0})'.format(st))


def send_message():
    log.debug('Sending Message')
    if json_mode == 'object':
        out = json.loads(message.format(unixs=int(time.time()), unixms=int(time.time() * 1000)))
    elif json_mode == 'string':
        out = json.dumps(
            json.loads(
                message.format(
                    unixs=int(
                        time.time()),
                    unixms=int(
                        time.time() *
                        1000))),
            separators=(
                ',',
                ':'))
    else:
        out = message.format(unixs=int(time.time()), unixms=int(time.time() * 1000))
    fluent = sender.FluentSender(fluentd_tag, host=fluentd_host,
                                 port=fluentd_port,
                                 timeout=2.0,
                                 verbose=False,
                                 nanosecond_precision=True,
                                 )
    if not fluent.emit(None, ({message_key: out} if message_key else out)):
        print(fluent.last_error)
        fluent.clear_last_error()


if __name__ == '__main__':

    log.info('STARTING: {0}'.format(this_version_string()))

    while True:
        do_sleep(sleep_duration)
        send_message()
