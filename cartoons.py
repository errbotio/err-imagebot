from random import choice

# Backward compatibility
from errbot.version import VERSION
from errbot.utils import version2array
if version2array(VERSION) >= [1,6,0]:
    from errbot import botcmd, BotPlugin
else:
    from errbot.botplugin import BotPlugin
    from errbot.jabberbot import botcmd


from imageBot import extract_rss_urls
from urllib2 import quote, urlopen

class Cartoons(BotPlugin):
    @botcmd(template='showme')
    def dilbert(self, mess, args):
        """ by Scott Adams
        http://www.dilbert.com/ 
        """
        urls = extract_rss_urls('http://feed.dilbert.com/dilbert/most_popular?format=xml')
        urls.extend(extract_rss_urls('http://feed.dilbert.com/dilbert/daily_strip?format=xml'))
        return {'content':'Random Dilbert', 'url':choice(urls)}

    @botcmd(template='showme')
    def xkcd(self, mess, args):
        """
        Display random XKCD from RSS feed from http://xkcd.com
        """
        urls = extract_rss_urls('http://xkcd.com/rss.xml')


    @botcmd
    def shout(self, mess, args):
        """
        Display the queried ascii art
        """
        args=args.strip()
        if not args:
            return 'What can I shout for you ?'
        return urlopen('http://asciime.heroku.com/generate_ascii?s=%s'%quote(args)).read()
