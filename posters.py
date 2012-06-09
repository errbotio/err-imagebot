from random import choice
from feedparser import parse
from errbot.botplugin import BotPlugin
from errbot.jabberbot import botcmd

def get_random_url_from_feed(feed_url):
    return choice([feed.media_content[1]['url'] for feed in parse(feed_url)['entries'] if len(feed.media_content)>1])

class Posters(BotPlugin):

    @botcmd
    def fixor(self, mess, args):
        """
            There ! I fixed it !
            from http://thereifixedit.files.wordpress.com/
        """
        return get_random_url_from_feed('http://feeds.feedburner.com/ThereIFixedIt')

    @botcmd
    def wtf(self, mess, args):
        """
        (De)motivates you
        from VeryDemotivational
        """
        return get_random_url_from_feed('http://feeds.feedburner.com/VeryDemotivational')
