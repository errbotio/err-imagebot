from random import choice
import socket
import json


from errbot import PY2
if PY2:
    from urllib2 import quote, urlopen, Request
else:
    from urllib.request import urlopen, Request
    from urllib.parse import quote

import feedparser
from bs4 import BeautifulSoup

from errbot import botcmd, BotPlugin


def extract_rss_urls(feed_url):
    rss = feedparser.parse(feed_url)
    return [entry.link for entry in rss.entries]

GOOGLE_IMAGE_URL = ('https://ajax.googleapis.com/ajax/services/search/images?' +
                    'v=1.0&q=%s&userip=%s')


class ImageBot(BotPlugin):
    def callback_connect(self):
        # small hack because google wants the private address of the user to avoid automated searchs
        s = None
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("gmail.com", 80))
            self.local_addr = s.getsockname()[0]
        finally:
            if s:
                s.close()

    @botcmd(template='showme')
    def showme(self, mess, args):
        """ Shows you an image based on the arguments
        Example: !showme a monkey
        """
        if not args:
            return 'Am I supposed to guess the image you want ?...'
        request = Request(GOOGLE_IMAGE_URL % (quote(args.encode('utf-8')), self.local_addr), None,
                          {'Referer': 'http://www.gootz.net/'})
        response = urlopen(request)
        results = json.loads(response.read().decode('utf-8'))
        lucky_result = choice(results['responseData']['results'])
        return {'content': lucky_result['content'], 'url': lucky_result['unescapedUrl']}

    @botcmd(template='showme')
    def stockphoto(self, mess, args):
        """
        Display dubious pictures from http://awkwardstockphotos.com/
        """
        return {'content': 'Random StockPhoto', 'url': choice(extract_rss_urls('http://awkwardstockphotos.com/rss'))}

    @botcmd(template='showme')
    def facepalm(self, mess, args):
        """
        To use in case of real stupid mistake...
        """
        fp_urls = (
          'http://i.imgur.com/FSjAzgr.gif',
          'http://i.imgur.com/QtFZ0PR.gif',
          'http://i.imgur.com/xgjt5AI.gif',
          'http://i.imgur.com/e6327Nd.gif',
          'http://i.imgur.com/SOATEDJ.gif',
          'http://i.imgur.com/lfL0UvH.webm',
          'http://i.imgur.com/uDNqsKs.gif',
          'http://i.imgur.com/3j7CNAP.webm',
          'http://i.imgur.com/4p6uYDA.webm',
          'http://i.imgur.com/iYxCSIx.gif',
          'http://i.imgur.com/m6jAMAE.gif',
          'http://i.imgur.com/CMYo71o.gif',
          'http://i.imgur.com/kvtwvtz.gif',
          'http://i.imgur.com/Oeelidy.gif',
          'http://i.imgur.com/NYOyGqw.gif',
          'http://i.imgur.com/X4WIDWW.gif')
        return {'content': 'Random Facepalm', 'url': choice(fp_urls)}

    @botcmd(template='showme')
    def fp(self, mess, args):
        """
        Alias on !facepalm
        """
        return self.facepalm(mess, args)

    @botcmd(template='showme')
    def animals(self, mess, args):
        """
        Fun gifs from http://animalsbeingdicks.com/
        """
        body = urlopen(urlopen('http://animalsbeingdicks.com/random').geturl()).read()
        soup = BeautifulSoup(body)
        ps = soup.select(".entry")[0].find_all('p')
        return {'content': str(ps[1].contents[0]), 'url': ps[0].img['src']}

