from random import choice
import requests
import feedparser
from bs4 import BeautifulSoup

from errbot import botcmd, BotPlugin


def extract_rss_urls(feed_url):
    rss = feedparser.parse(feed_url)
    return [entry.link for entry in rss.entries]


GOOGLE_IMAGE_URL = 'https://www.googleapis.com/customsearch/v1'

class ImageBot(BotPlugin):
    def get_configuration_template(self):
        return {'PROJECT_KEY': 'AIzaSyAdZYdygeThui2HVEcyNP27Y80ucFzcBQv',
                 'CX_ID': '004082647395918233991:3ewyx6ygcly'}

    @botcmd(template='showme')
    def showme(self, _, args):
        """ Shows you an image based on the arguments
        Example: !showme a monkey
        """
        if self.config is None:
            return 'This plugin needs to be configured with `!plugin config ImageBot` with a google project.\n\
            Get your own PROJECT_KEY and CX_ID from:\n\
            http://stackoverflow.com/questions/34035422/google-image-search-says-api-no-longer-available for details.'
        if not args:
            return 'Am I supposed to guess the image you want ?...'
        params = {'key': self.config['PROJECT_KEY'],
                  'cx': self.config['CX_ID'],
                  'q': args,
                  'imgSize': 'medium',
                  'searchType': 'image'}
        request = requests.request('GET', GOOGLE_IMAGE_URL, params=params)
        results = request.json()
        lucky_result = choice(results['items'])
        return {'content': lucky_result['htmlTitle'], 'url': lucky_result['link']}

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
          'http://i.imgur.com/uDNqsKs.gif',
          'http://i.imgur.com/iYxCSIx.gif',
          'http://i.imgur.com/m6jAMAE.gif',
          'http://i.imgur.com/CMYo71o.gif',
          'http://i.imgur.com/kvtwvtz.gif',
          'http://i.imgur.com/Oeelidy.gif',
          'http://i.imgur.com/NYOyGqw.gif',
          'http://i.imgur.com/X4WIDWW.gif',
          'http://i.imgur.com/GTxRRuv.gif',
          'http://i.imgur.com/GS5MDQo.jpg')
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
        body = requests.get('http://animalsbeingdicks.com/random').content
        soup = BeautifulSoup(body)
        ps = soup.select(".entry")[0].find_all('p')
        return {'content': str(ps[1].contents[0]), 'url': ps[0].img['src']}

