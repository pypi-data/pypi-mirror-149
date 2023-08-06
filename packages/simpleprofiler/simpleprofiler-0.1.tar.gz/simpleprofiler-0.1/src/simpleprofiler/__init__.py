# -*- coding: utf-8 -*-
from decorator import decorator
import inspect
import logging
import sys
import time

_logger = logging.getLogger(__name__)

class _LogTracer(object):
    def __init__(self, whitelist=None, blacklist=None, files=None, deep=False):
        self.profiles = {}
        self.whitelist = whitelist
        self.blacklist = blacklist
        self.files = files
        self.deep = deep
        self.first_frame = None

    def tracer(self, frame, event, arg):
        if not self.first_frame:
            self.first_frame = frame.f_code

        if not self.deep and self.first_frame != frame.f_code:
            return self.tracer

        if frame.f_code.co_name in ['<genexpr>', '__getattr__', '__iter__', '__init__']:
            return

        if self.files and frame.f_code.co_filename not in self.files:
            return self.tracer

        if frame.f_code not in self.profiles:
            try:
                lines, firstline = inspect.getsourcelines(frame)
                self.profiles[frame.f_code] = {
                    'filename': frame.f_code.co_filename,
                    'firstline': firstline,
                    'code': lines,
                    'calls': [],
                    'nb': 0,
                }
            except Exception:
                return
        codeProfile = self.profiles[frame.f_code]

        if not frame.f_lineno:
            codeProfile['nb'] += 1

        codeProfile['calls'].append({
            'event': event,
            'lineno': frame.f_lineno,
            'time': time.time(),
            'callno': codeProfile['nb'],
        })

        return self.tracer

def get_profile(method=None, whitelist=None, blacklist=(None,), files=None,
        minimum_time=0):

    deep = not method

    def _pyProfile(method, *args, **kwargs):
        log_tracer = _LogTracer(whitelist=whitelist, blacklist=blacklist, files=files, deep=deep)
        sys.settrace(log_tracer.tracer)
        try:
            result = method(*args, **kwargs)
        finally:
            sys.settrace(None)

        LOG_MARKER = method.__name__ + " > "

        log = ["\n%s %-10s%s\n" % (LOG_MARKER, 'calls', 'ms')]

        for v in log_tracer.profiles.values():
            v['report'] = {}
            l = len(v['calls'])
            for k, call in enumerate(v['calls']):
                if k+1 >= l:
                    continue

                if call['lineno'] not in v['report']:
                    v['report'][call['lineno']] = {
                        'nb_queries': 0,
                        'delay': 0,
                        'nb': 0,
                    }
                v['report'][call['lineno']]['nb'] += 1

                n = k+1
                while k+1 <= l and v['calls'][k+1]['callno'] != call['callno']:
                    n += 1
                if n >= l:
                    continue
                next_call = v['calls'][n]
                v['report'][call['lineno']]['delay'] += next_call['time'] - call['time']

            delay = 0
            for call in v['report'].values():
                delay += call['delay']

            if minimum_time and minimum_time > delay*1000:
                continue

            # todo: no color if output in a file
            log.append("\033[1;33m%s%s %s--------------------- %s, %s\033[1;0m\n\n" % (LOG_MARKER, '', '-' * (15-len('')), v['filename'], v['firstline']))
            
            for lineno, line in enumerate(v['code']):
                if (lineno + v['firstline']) in v['report']:
                    data = v['report'][lineno + v['firstline']]
                    log.append("%s%-10s%-10s%s" % (
                        LOG_MARKER,
                        str(data['nb']) if 'nb_queries' in data else '.',
                        str(round(data['delay']*100000)/100) if 'delay' in data else '',
                        line[:-1]))
                else:
                    log.append(LOG_MARKER)
                    log.append(" " * 20)
                    log.append(line[:-1])
                log.append('\n')

            log.append("\n%sTotal:\n%s%-10s%-10s\n\n" % (
                        LOG_MARKER,
                        LOG_MARKER,
                        str(data['nb']),
                        str(round(delay*100000)/100)))

        _logger.info(''.join(log))

        return result

    if not method:
        return lambda method: decorator(_pyProfile, method)

    wrapper = decorator(_pyProfile, method)
    return wrapper