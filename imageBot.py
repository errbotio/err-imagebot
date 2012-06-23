from random import choice
import re
import socket
from errbot.botplugin import BotPlugin
from errbot.jabberbot import botcmd
from urllib2 import urlopen, Request, quote
import simplejson
from lxml import objectify
from random import choice
from bs4 import BeautifulSoup

def extract_rss_urls(feed_url):
    rss_content = urlopen(feed_url).read()
    rss = objectify.fromstring(rss_content)
    return [re.search('src=\"(.+?)\"', description.text).groups()[0] for description in rss.xpath("//item/description")]

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

    @botcmd
    def showme(self, mess, args):
        """ Shows you an image based on the arguments
        Example: !showme a monkey
        """
        if not args:
            return 'Am I supposed to guess the image you want ?...'
        request = Request(GOOGLE_IMAGE_URL % (quote(args), self.local_addr), None, {'Referer': 'http://www.gootz.net/'})
        response = urlopen(request)
        results = simplejson.load(response)
        lucky_result = choice(results['responseData']['results'])
        return '%s : %s' % (lucky_result['content'], lucky_result['unescapedUrl'])


    @botcmd
    def stockphoto(self, mess, args):
        """
        Display dubious pictures from http://awkwardstockphotos.com/
        """
        return choice(extract_rss_urls('http://awkwardstockphotos.com/rss'))

    @botcmd
    def facepalm(self, mess, args):
        """
        To use in case of real stupid mistake...
        """
        return urlopen('http://facepalm.org/img.php').geturl()

    @botcmd
    def fp(self, mess, args):
        """
        Alias on !facepalm
        """
        return self.facepalm(mess, args)

    @botcmd
    def animals(self, mess, args):
        """
        Fun gifs from http://animalsbeingdicks.com/
        """
        body = urlopen(urlopen('http://animalsbeingdicks.com/random').geturl()).read()
        soup = BeautifulSoup(body)
        ps = soup.select(".entry")[0].find_all('p')
        self.send(mess.getFrom(), ps[0].img['src'], message_type=mess.getType())
        return unicode(ps[1].contents[0])
