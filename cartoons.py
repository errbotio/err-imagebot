from random import choice
import re
from urllib2 import urlopen
import urllib2
from botplugin import BotPlugin
from jabberbot import botcmd
from lxml import objectify

class Cartoons(BotPlugin):
    @botcmd
    def dilbert(self, mess, args):
        """ by Scott Adams
        http://www.dilbert.com/ 
        """
        rss_content = urlopen("http://feed.dilbert.com/dilbert/most_popular?format=xml").read()
        rss = objectify.fromstring(rss_content)
        urls = [re.search('src=\"(.+?)\"', description.text).groups()[0] for description in rss.xpath("//item/description")]
        rss_content = urlopen("http://feed.dilbert.com/dilbert/daily_strip?format=xml").read()
        rss = objectify.fromstring(rss_content)
        urls.extend([re.search('src=\"(.+?)\"', description.text).groups()[0] for description in rss.xpath("//item/description")])
        return choice(urls)

    @botcmd
    def xkcd(self, mess, args):
        """
        Display random XKCD from RSS feed from http://xkcd.com
        """
        rss_content = urllib2.urlopen("http://xkcd.com/rss.xml").read()
        rss = objectify.fromstring(rss_content)
        urls = [re.search('src=\"(.+?)\"', description.text).groups()[0] for description in rss.xpath("//item/description")]
        return choice(urls)
