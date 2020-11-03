import sys
import os
import time
import datetime
from concurrent import futures
import pytz
from dateutil import parser
import requests
import progressbar

PAPERTRAIL_API_TOKEN = os.environ.get('PAPERTRAIL_API_TOKEN', None)
ARCHIVES_URL = 'https://papertrailapp.com/api/v1/archives.json'
DEFAULT_REMAIN_SIZE = 25
HEADERS = {'X-Papertrail-Token': PAPERTRAIL_API_TOKEN}
MIN_INTERVAL_SEC = 0.1


def get_ppheader(response):
    hist = [response] + response.history
    for h in hist:
        if 'X-Rate-Limit-Remaining' not in h.headers:
            continue

        return (
                int(h.headers['X-Rate-Limit-Limit']),
                int(h.headers['X-Rate-Limit-Remaining']),
                int(h.headers['X-Rate-Limit-Reset'])
                )


def do_download(url, filename, index):
    while True:
        try:
            with requests.Session() as s:
                res = s.get(url, headers=HEADERS)
                finishtime = time.time_ns()
                (limit, rem, reset) = get_ppheader(res)

                if 200 <= res.status_code < 300:
                    with open(filename, "wb") as f:
                        for chunk in res.iter_content(chunk_size=128):
                            f.write(chunk)
                    return (limit, rem, reset, finishtime, index)
        except requests.ConnectionError:
            time.sleep(1)


def parse_span():
    if len(sys.argv) == 1:
        return None, None

    f = t = None
    fromstr = tostr = ''
    span = sys.argv[1].split('~')
    if len(span) == 1:
        fromstr = tostr = span[0]
    else:
        [fromstr, tostr, *_] = span

    if fromstr:
        f = parser.isoparse(fromstr)
        if not f.tzname():
            utc = pytz.timezone('UTC')
            f = utc.localize(f)

    if tostr:
        t = parser.isoparse(tostr)
        if not t.tzname():
            utc = pytz.timezone('UTC')
            t = utc.localize(t)

    if tostr and fromstr == tostr:
        t = t + datetime.timedelta(days=1)

    return f, t


def main():
    if not PAPERTRAIL_API_TOKEN:
        print('Not set the environment variable `PAPERTRAIL_API_TOKEN`',
              file=sys.stderr)
        sys.exit(1)

    _from, to = parse_span()

    r = requests.get(ARCHIVES_URL, headers=HEADERS)
    r.raise_for_status()

    archives = [ar for ar in r.json()
                if (not _from or _from <= parser.isoparse(ar["start"]))
                and (not to or parser.isoparse(ar["end"]) < to)
                ]

    with futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_list = []
        remain = DEFAULT_REMAIN_SIZE
        until_reset_sec = 0
        lasttime = time.time_ns()
        with progressbar.ProgressBar(max_value=len(archives)) as bar:
            for i, ar in enumerate(archives):
                future_list.append(
                    executor.submit(
                        do_download,
                        ar['_links']['download']['href'],
                        ar['filename'],
                        i
                    )
                )

                if len(future_list) < remain:
                    time.sleep(MIN_INTERVAL_SEC)
                    continue

                for future in future_list:
                    (_, rem, reset, finishtime, index) = future.result()
                    if finishtime > lasttime:
                        remain = rem
                        until_reset_sec = reset
                        lasttime = finishtime
                    bar.update(index)

                future_list = []

                if remain <= 0:
                    time.sleep(until_reset_sec)
                    remain = DEFAULT_REMAIN_SIZE
                    continue

                time.sleep(MIN_INTERVAL_SEC)
