from random import choice
from feedparser import parse
from errbot.botplugin import BotPlugin
from errbot.jabberbot import botcmd

class Posters(BotPlugin):
    @botcmd
    def fixor(self, mess, args):
        """
            There ! I fixed it !
            from http://thereifixedit.files.wordpress.com/
        """
        myfeed = parse('http://feeds.feedburner.com/ThereIFixedIt')
        feeds = myfeed['entries']
        return choice(feeds).media_content[1]['url'].encode()

    @botcmd
    def wtf(self, mess, args):
        """
        (De)motivates you
        from VeryDemotivational
        """
        myfeed = parse('http://feeds.feedburner.com/VeryDemotivational')
        feeds = myfeed['entries']
        return choice(feeds).media_content[1]['url'].encode()
