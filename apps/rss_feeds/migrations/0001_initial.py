# Generated by Django 2.0 on 2020-06-16 06:52

from django.db import migrations, models
import django.db.models.deletion
import utils.fields


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="DuplicateFeed",
            fields=[
                (
                    "id",
                    models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID"),
                ),
                ("duplicate_address", models.CharField(db_index=True, max_length=764)),
                ("duplicate_link", models.CharField(db_index=True, max_length=764, null=True)),
                ("duplicate_feed_id", models.CharField(db_index=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Feed",
            fields=[
                (
                    "id",
                    models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID"),
                ),
                ("feed_address", models.URLField(db_index=True, max_length=764)),
                ("feed_address_locked", models.NullBooleanField(default=False)),
                ("feed_link", models.URLField(blank=True, default="", max_length=1000, null=True)),
                ("feed_link_locked", models.BooleanField(default=False)),
                ("hash_address_and_link", models.CharField(max_length=64, unique=True)),
                ("feed_title", models.CharField(blank=True, default="[Untitled]", max_length=255, null=True)),
                ("is_push", models.NullBooleanField(default=False)),
                ("active", models.BooleanField(db_index=True, default=True)),
                ("num_subscribers", models.IntegerField(default=-1)),
                ("active_subscribers", models.IntegerField(db_index=True, default=-1)),
                ("premium_subscribers", models.IntegerField(default=-1)),
                ("active_premium_subscribers", models.IntegerField(default=-1)),
                ("last_update", models.DateTimeField(db_index=True)),
                ("next_scheduled_update", models.DateTimeField()),
                ("last_story_date", models.DateTimeField(blank=True, null=True)),
                ("fetched_once", models.BooleanField(default=False)),
                ("known_good", models.BooleanField(default=False)),
                ("has_feed_exception", models.BooleanField(db_index=True, default=False)),
                ("has_page_exception", models.BooleanField(db_index=True, default=False)),
                ("has_page", models.BooleanField(default=True)),
                ("exception_code", models.IntegerField(default=0)),
                ("errors_since_good", models.IntegerField(default=0)),
                ("min_to_decay", models.IntegerField(default=0)),
                ("days_to_trim", models.IntegerField(default=90)),
                ("creation", models.DateField(auto_now_add=True)),
                ("etag", models.CharField(blank=True, max_length=255, null=True)),
                ("last_modified", models.DateTimeField(blank=True, null=True)),
                ("stories_last_month", models.IntegerField(default=0)),
                ("average_stories_per_month", models.IntegerField(default=0)),
                ("last_load_time", models.IntegerField(default=0)),
                ("favicon_color", models.CharField(blank=True, max_length=6, null=True)),
                ("favicon_not_found", models.BooleanField(default=False)),
                ("s3_page", models.NullBooleanField(default=False)),
                ("s3_icon", models.NullBooleanField(default=False)),
                ("search_indexed", models.NullBooleanField(default=None)),
                (
                    "branch_from_feed",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="rss_feeds.Feed",
                    ),
                ),
            ],
            options={
                "db_table": "feeds",
                "ordering": ["feed_title"],
            },
        ),
        migrations.CreateModel(
            name="FeedData",
            fields=[
                (
                    "id",
                    models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID"),
                ),
                ("feed_tagline", models.CharField(blank=True, max_length=1024, null=True)),
                ("story_count_history", models.TextField(blank=True, null=True)),
                ("feed_classifier_counts", models.TextField(blank=True, null=True)),
                ("popular_tags", models.CharField(blank=True, max_length=1024, null=True)),
                ("popular_authors", models.CharField(blank=True, max_length=2048, null=True)),
                (
                    "feed",
                    utils.fields.AutoOneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, related_name="data", to="rss_feeds.Feed"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="duplicatefeed",
            name="feed",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="duplicate_addresses",
                to="rss_feeds.Feed",
            ),
        ),
    ]
