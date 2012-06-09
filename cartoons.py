from random import choice
import re
from urllib2 import urlopen
from errbot.botplugin import BotPlugin
from errbot.jabberbot import botcmd
from lxml import objectify

def extract_urls(feed_url):
    rss_content = urlopen(feed_url).read()
    rss = objectify.fromstring(rss_content)
    return [re.search('src=\"(.+?)\"', description.text).groups()[0] for description in rss.xpath("//item/description")]

class Cartoons(BotPlugin):
    @botcmd
    def dilbert(self, mess, args):
        """ by Scott Adams
        http://www.dilbert.com/ 
        """
        urls = extract_urls('http://feed.dilbert.com/dilbert/most_popular?format=xml')
        urls.extend(extract_urls('http://feed.dilbert.com/dilbert/daily_strip?format=xml'))
        return choice(urls)

    @botcmd
    def xkcd(self, mess, args):
        """
        Display random XKCD from RSS feed from http://xkcd.com
        """
        urls = extract_urls('http://xkcd.com/rss.xml')
        return choice(urls)
