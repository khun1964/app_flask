import main

def test_working_feed():
    """
    A dummy test, used to make sure we can call pytest
    """
    feed_entries = main.fetch_feed("https://stackoverflow.com/feeds")
    assert len(feed_entries)>0