from random import choice
from feedparser import parse
import re

from errbot import botcmd, BotPlugin


def get_random_url_from_feed(feed_url):
    feeds = parse(feed_url)['entries']
    html = choice([feed.content[0].value for feed in feeds if len(feed.content) > 0])

    found = re.search(r".*<img class='event-item-lol-image' src='(.*)' id=.*", html)
    if not found:
        return 'http://404.com'
    return found.group(1)  # find the first thing that matches an image


class Posters(BotPlugin):
    @botcmd(template='showme')
    def fixor(self, mess, args):
        """
            There ! I fixed it !
            from http://thereifixedit.files.wordpress.com/
        """
        return {'content': 'There I fixed it !',
                'url': get_random_url_from_feed('http://feeds.feedburner.com/ThereIFixedIt')}

    @botcmd(template='showme')
    def wtf(self, mess, args):
        """
        (De)motivates you
        from VeryDemotivational
        """
        return {'content': 'Very demotivational !',
                'url': get_random_url_from_feed('http://feeds.feedburner.com/VeryDemotivational')}
