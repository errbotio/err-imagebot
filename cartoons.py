from random import choice

from errbot import botcmd, BotPlugin, PY2
from imageBot import extract_rss_urls

if PY2:
    from urllib2 import quote, urlopen
else:
    from urllib.request import urlopen
    from urllib.parse import quote


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

    @botcmd
    def shout(self, mess, args):
        """
        Display the queried ascii art
        """
        args = args.strip()
        if not args:
            return 'What can I shout for you ?'
        return urlopen('http://asciime.heroku.com/generate_ascii?s=%s' % quote(args)).read()
