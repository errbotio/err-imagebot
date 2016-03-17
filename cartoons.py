from random import choice

from errbot import botcmd, BotPlugin
from imagebot import extract_rss_urls


class Cartoons(BotPlugin):
    @botcmd(template='showme')
    def dilbert(self, mess, args):
        """ by Scott Adams
        http://www.dilbert.com/
        """
        urls = extract_rss_urls('http://feed.dilbert.com/dilbert/most_popular?format=xml')
        urls.extend(extract_rss_urls('http://feed.dilbert.com/dilbert/daily_strip?format=xml'))
        return {'content': 'Random Dilbert', 'url': choice(urls)}

    @botcmd(template='showme')
    def xkcd(self, mess, args):
        """
        Display random XKCD from RSS feed from http://xkcd.com
        """
        urls = extract_rss_urls('http://xkcd.com/rss.xml')
        return {'content': 'Random XKCD', 'url': choice(urls)}
