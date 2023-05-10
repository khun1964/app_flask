import main

def test_working_feed():
    """
    The only business method we have for now is the feed reader one.
    As a consequence, the only valid test is the one getting data from a working feed
    and checking there are feed entries in.
    """
    feed_entries = main.fetch_feed("https://stackoverflow.com/feeds")
    assert len(feed_entries)>0