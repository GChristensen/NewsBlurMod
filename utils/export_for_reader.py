"""Export script for the migration to NewsSharp (utils/export_for_reader.py).

Reads users, profiles, feeds with at least one subscription, subscriptions, folder trees and feed
icons from the NewsBlurMod databases and writes one JSON document to stdout. Read-only.

Usage (inside the NewsBlurMod repository, where the Django settings can reach Postgres and Mongo):

    uv run python utils/export_for_reader.py > export.json

Then, in the NewsSharp project: uv run python manage.py import_newsblur export.json
"""
import datetime
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newsblur_web.settings")

import django  # noqa: E402

django.setup()

from django.contrib.auth.models import User  # noqa: E402

from apps.profile.models import Profile  # noqa: E402
from apps.reader.models import UserSubscription, UserSubscriptionFolders  # noqa: E402
from apps.rss_feeds.models import Feed, MFeedIcon  # noqa: E402


def load_json(text, default):
    try:
        return json.loads(text) if text else default
    except ValueError:
        return default


def main():
    subscriptions = list(UserSubscription.objects.values("user_id", "feed_id", "user_title"))
    feed_ids = sorted({sub["feed_id"] for sub in subscriptions})
    user_ids = sorted({sub["user_id"] for sub in subscriptions} | set(User.objects.values_list("id", flat=True)))

    users = [
        {"id": user.id, "username": user.username, "is_staff": user.is_staff, "date_joined": user.date_joined.isoformat()}
        for user in User.objects.filter(id__in=user_ids).order_by("id")
    ]
    feeds = [
        {
            "id": feed.id,
            "feed_address": feed.feed_address,
            "feed_link": feed.feed_link,
            "feed_title": feed.feed_title,
            "favicon_color": feed.favicon_color,
            "favicon_not_found": feed.favicon_not_found,
        }
        for feed in Feed.objects.filter(id__in=feed_ids).order_by("id")
    ]
    folders = {
        str(row.user_id): load_json(row.folders, [])
        for row in UserSubscriptionFolders.objects.filter(user_id__in=user_ids)
    }
    preferences, view_settings = {}, {}
    for profile in Profile.objects.filter(user_id__in=user_ids):
        preferences[str(profile.user_id)] = {
            "timezone": str(profile.timezone),
            "days_of_unread": profile.days_of_unread,
            "feed_pane_size": profile.feed_pane_size,
            "preferences": load_json(profile.preferences, {}),
            "collapsed_folders": load_json(profile.collapsed_folders, []),
        }
        view_settings[str(profile.user_id)] = load_json(profile.view_settings, {})
    icons = [
        {"feed_id": icon.feed_id, "data": icon.data, "color": icon.color, "icon_url": icon.icon_url}
        for icon in MFeedIcon.objects.filter(feed_id__in=feed_ids)
        if icon.data
    ]
    document = {
        "version": 1,
        "exported_at": datetime.datetime.utcnow().isoformat() + "Z",
        "users": users,
        "feeds": feeds,
        "subscriptions": subscriptions,
        "folders": folders,
        "icons": icons,
        "view_settings": view_settings,
        "preferences": preferences,
    }
    json.dump(document, sys.stdout)
    sys.stderr.write(
        "exported %d users, %d feeds, %d subscriptions, %d icons\n"
        % (len(users), len(feeds), len(subscriptions), len(icons))
    )


if __name__ == "__main__":
    main()
