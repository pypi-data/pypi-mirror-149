''' crontab tasks. '''
from authc import gunload, get_redis_cn
import json
import os
from threading import Thread
import random
import datetime
import time
import socket

import bs4
import codefast as cf
import requests
from ojbk import report_self

from .pipe import author
from .toolkits.telegram import Channel
import codefast as cf

socket.setdefaulttimeout(30)

postman = Channel('messalert')


def decode(key: str) -> str:
    return author.get(key)


class PapaPhone(object):
    def __init__(self) -> None:
        self.url = 'https://h5.ha.chinamobile.com/h5-rest/flow/data'
        self.params = {'channel': 2, 'version': '7.0.2'}
        self.rate_bucket_cnt = 0

    def get_headers(self) -> dict:
        return json.loads(get_redis_cn().get('7103_cmcc_headers'))

    def check_once(self) -> dict:
        try:
            headers = self.get_headers()
            resp = cf.net.get(self.url, data=self.params,
                              headers=headers).json()
            cf.info(headers)
            cf.info('check once result', resp)

            report_self('papaphone')
            return resp
        except Exception as e:
            cf.error('check once error:', e)
            return {'error': str(e)}

    def monitor(self) -> dict:
        ERROR_CNT = 0
        while True:
            js = self.check_once()
            if 'data' not in js:
                ERROR_CNT += 1
                if ERROR_CNT > 3:
                    msg = 'Cellphone flow query failed 3 times. Error message: %s' % js[
                        'error']
                    postman.post(msg)
            else:
                general_flow = js['data']['flowList'][0]
                total, used = general_flow['totalFlow'], general_flow[
                    'flowUsed']
                msg = '{} / {} GB ({} %) data consumed'.format(
                    used, total,
                    float(used) / float(total) * 100)
                _cnt = int(float(used) * 3)
                if _cnt != self.rate_bucket_cnt:
                    self.rate_bucket_cnt = _cnt
                    postman.post(msg)
                if datetime.datetime.now().hour == 8:
                    postman.post('daily report: ' + msg)
                ERROR_CNT = 0
            time.sleep(random.randint(3600, 5400))


class GithubTasks(object):
    '''Github related tasks '''
    @classmethod
    def git_commit_reminder(cls) -> None:
        cnt = cls._count_commits()
        prev_cnt, file_ = 10240, 'github.commits.json'
        if os.path.exists(file_):
            prev_cnt = json.load(open(file_, 'r'))['count']
        json.dump({'count': cnt}, open(file_, 'w'), indent=2)

        if cnt > prev_cnt:
            return

        msg = (
            'Github commit reminder \n\n' +
            f"You haven't do any commit today. Your previous commit count is {cnt}"
        )
        postman.post(msg)

    @classmethod
    def tasks_reminder(cls):
        url = decode('GIT_RAW_PREFIX') + '2021/ps.md'

        tasks = cls._request_proxy_get(url).split('\n')
        todo = '\n'.join(t for t in tasks if not t.startswith('- [x]'))
        postman.post('TODO list \n' + todo)

    @classmethod
    def _request_proxy_get(cls, url: str) -> str:
        px = decode('http_proxy').lstrip('http://')
        for _ in range(5):
            try:
                res = requests.get(url,
                                   proxies={'https': px},
                                   headers={'User-Agent': 'Aha'},
                                   timeout=3)
                if res.status_code == 200:
                    return res.text
            except Exception as e:
                print(e)
        else:
            return ''

    @classmethod
    def _count_commits(cls) -> int:
        resp = cls._request_proxy_get(decode('GITHUB_MAINPAGE'))
        if resp:
            soup = bs4.BeautifulSoup(resp, 'lxml')
            h2 = soup.find_all('h2', {'class': 'f4 text-normal mb-2'}).pop()
            commits_count = next(
                int(e) for e in h2.text.split() if e.isdigit())
            return commits_count
        return 0


class HappyXiao(object):
    ''' happyxiao articles poster'''
    @classmethod
    @cf.utils.retry(total_tries=3)
    def rss(cls, url: str = 'https://happyxiao.com/') -> None:
        rsp = bs4.BeautifulSoup(requests.get(url).text, 'lxml')
        more = rsp.find_all('a', attrs={'class': 'more-link'})
        articles = {m.attrs['href']: '' for m in more}
        jsonfile = 'hx.json'

        if not os.path.exists(jsonfile):
            open(jsonfile, 'w').write('{}')

        j = json.load(open(jsonfile, 'r'))
        res = '\n'.join(cls.brief(k) for k in articles.keys() if k not in j)
        j.update(articles)
        json.dump(j, open(jsonfile, 'w'), indent=2)
        if res:
            postman.post(res.replace('#', '%23'))

    @classmethod
    def brief(cls, url) -> str:
        rsp = bs4.BeautifulSoup(requests.get(url).text, 'lxml')
        art = rsp.find('article')
        res = url + '\n' + art.text.replace('\t', '') + str(art.a)
        return res


if __name__ == '__main__':
    t = Thread(target=PapaPhone().monitor)
    t.start()
