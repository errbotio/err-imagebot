from random import choice
import re
import socket
from errbot.botplugin import BotPlugin
from errbot.jabberbot import botcmd
import urllib2
import simplejson
from lxml import objectify

GOOGLE_IMAGE_URL = ('https://ajax.googleapis.com/ajax/services/search/images?' +
                    'v=1.0&q=%s&userip=%s')

class ImageBot(BotPlugin):
    def callback_connect(self):
        # small hack because google wants the private address of the user to avoid automated searchs
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("gmail.com", 80))
            self.local_addr = s.getsockname()[0]
        finally:
            s.close()

    @botcmd
    def showme(self, mess, args):
        """ Shows you an image based on the arguments
        Example: !showme a monkey
        """
        if not args:
            return 'Am I supposed to guess the image you want ?...'
        request = urllib2.Request(GOOGLE_IMAGE_URL % (urllib2.quote(args), self.local_addr), None, {'Referer': 'http://www.gootz.net/'})
        response = urllib2.urlopen(request)
        results = simplejson.load(response)
        lucky_result = results['responseData']['results'][0]
        return '%s : %s' % (lucky_result['content'], lucky_result['unescapedUrl'])


    @botcmd
    def stockphoto(self, mess, args):
        """
        Display dubious pictures from http://awkwardstockphotos.com/
        """
        rss_content = urllib2.urlopen("http://awkwardstockphotos.com/rss").read()
        rss = objectify.fromstring(rss_content)
        urls = [re.search('src=\"(.+?)\"', description.text).groups()[0] for description in rss.xpath("//item/description")]
        return choice(urls)