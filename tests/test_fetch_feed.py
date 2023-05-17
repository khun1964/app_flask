import main, server, client
import os
import json
import feedparser
import requests
from datetime import datetime
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint


def test_working_feed():
    """
    The only business method we have for now is the feed reader one.
    As a consequence, the only valid test is the one getting data from a working feed
    and checking there are feed entries in.
    """
    feed_entries = server.fetch_feed("https://stackoverflow.com/feeds")
    assert len(feed_entries)>0