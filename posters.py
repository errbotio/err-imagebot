from random import choice
from feedparser import parse
import re

# Backward compatibility
from errbot.version import VERSION
from errbot.utils import version2array
if version2array(VERSION) >= [1,6,0]:
    from errbot import botcmd, BotPlugin
else:
    from errbot.botplugin import BotPlugin
    from errbot.jabberbot import botcmd

def get_random_url_from_feed(feed_url):
    feeds = parse(feed_url)['entries']
    html = choice([feed.content[0].value for feed in feeds if len(feed.content)>0])
    return re.search(r'.*src="(.*\.(jpg|png))".*',html).group(1) # find the first thing that matches an image

class Posters(BotPlugin):

    @botcmd(template='showme')
    def fixor(self, mess, args):
        """
            There ! I fixed it !
            from http://thereifixedit.files.wordpress.com/
        """
        return {'content':'There I fixed it !', 'url':get_random_url_from_feed('http://feeds.feedburner.com/ThereIFixedIt')}

    @botcmd(template='showme')
    def wtf(self, mess, args):
        """
        (De)motivates you
        from VeryDemotivational
        """
        return {'content':'Very demotivational !', 'url':get_random_url_from_feed('http://feeds.feedburner.com/VeryDemotivational')}
