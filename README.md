# NewsBlur

 * NewsBlur is a personal news reader bringing people together 
   to talk about the world. A new sound of an old instrument.
 * [www.newsblur.com](http://www.newsblur.com).
 * Created by [Samuel Clay](http://www.samuelclay.com). 
 * Twitter: [@samuelclay](http://twitter.com/samuelclay) and 
   [@newsblur](http://twitter.com/newsblur).

<a href="https://f-droid.org/repository/browse/?fdid=com.newsblur" target="_blank">
<img src="https://f-droid.org/badge/get-it-on.png" alt="Get it on F-Droid" height="80"/></a>
<a href="https://play.google.com/store/apps/details?id=com.newsblur" target="_blank">
<img src="https://play.google.com/intl/en_us/badges/images/generic/en-play-badge.png" alt="Get it on Google Play" height="80"/></a>

## Features

 1. Shows the original site (you have to see it to believe it).
 2. Hides stories you don't want to read based on tags, keywords, authors, etc.
 3. Highlights stories you want to read, based on the same criteria.

## Technologies

### Server-side
 * [Python 3.7+](http://www.python.org): The language of choice.
 * [Django](http://www.djangoproject.com): Web framework written in Python, used 
   to serve all pages.
 * [Celery](http://ask.github.com/celery) & [RabbitMQ](http://www.rabbitmq.com): 
   Asynchronous queueing server, used to fetch and parse RSS feeds.
 * [MongoDB](http://www.mongodb.com), [Pymongo](https://pypi.python.org/pypi/pymongo), & 
   [Mongoengine](http://www.github.com/hmarr/mongoengine): Non-relational database, 
   used to store stories, read stories, feed/page fetch histories, and proxied sites.
 * [PostgreSQL](http://www.postgresql.com): Relational database, used to store feeds, 
   subscriptions, and user accounts.
 * [Redis](http://redis.io): Programmer's database, used to assemble stories for the river, store story ids, manage feed fetching schedules, and the minuscule bit of caching that NewsBlur uses.
 * [Elasticsearch](http://elasticsearch.org): Search database, use for searching stories. Optional.
 
### Client-side and design

 * [jQuery](http://www.jquery.com): Cross-browser compliant JavaScript code. IE works without effort.
 * [Underscore.js](http://underscorejs.org/): Functional programming for JavaScript. 
   Indispensable.
 * [Backbone.js](http://backbonejs.org/): Framework for the web app. Also indispensable.
 * Miscellaneous jQuery Plugins: Everything from resizable layouts, to progress 
   bars, sortables, date handling, colors, corners, JSON, animations. 
   [See the complete list](https://github.com/samuelclay/NewsBlur/tree/master/media/js).


### Prerequisites
    * Docker
    * Docker-Compose

## Installation Instructions
 1. Run `make nb` to build Newsblur containers. This will set up all necessary databases, celery tasks, node applications,
    flask database monitor, NGINX, and a Haproxy load balancer.

 2. Navigate to: 

         https://nb.local.com 

    Create an account. At the end of the account creation process, you
    will be redirected to https://localhost/profile/stripe_form. Hit
    the back button a few times, and you will be inside the app.

## Contribution Instructions

* Making Changes:
    * To apply changes to the Python or JavaScript code, use the `make` command.
    * To apply changes to the docker-compose.yml file, use the `make rebuild` command.
    * To apply changes to the docker/haproxy/haproxy.conf file, node packages, or any new database migrations you will need to use the `make nb` command.

* Adding Python packages:
    Currently, the docker-compose.yml file uses the newsblur/newsblur_python3 image. It is built using the Dockerfile found in `docker/newsblur_base_image.Dockerfile`. Because of how the docker image is set up, you will need to create your own image and direct your docker-compose.yml file to use it. Please follow the following steps to do so.

    1. Add your new site-packages to config/requirements.txt.
    2. Add the following lines of code to your docker-compose.yml file to replace anywhere where it says `image: newsblur/newsblur_python3`

    <code>
        build:
          context: .
          dockerfile: docker/newsblur_base_image.Dockerfile
    </code>

    3. Run the `make nb` command to rebuild your docker-compose containers

* Debugging Python
    * To debug your code, drop `import pdb; pdb.set_trace()` into the Python code where you would like to start debugging
    and run `make` and then `make debug`.

* Using Django shell within Docker
    * Make sure your docker containers are up and run `make shell` to open
    the Django shell within the newsblur_web container.

### Running unit and integration tests

NewsBlur comes complete with a test suite that tests the functionality of the rss_feeds,
reader, and feed importer. To run the test suite:

    `make test`


## Keeping NewsBlur Running **** is this still applicable?

These commands keep NewsBlur fresh and updated. While on a development server, these 
commands do not need to be run more than once. However, you will probably want to run
the `refresh_feeds` command regularly so you have new stories to test with and read.

### Fetching feeds **** is this still applicable?

If you just want to fetch feeds once, you can use the `refresh_feeds` management command:

    ./manage.py refresh_feeds
  
If you want to fetch feeds regardless of when they were last updated:

    ./manage.py refresh_feeds --force
    
You can also fetch the feeds for a specific user:

    ./manage.py refresh_feeds --user=newsblur
    
You'll want to put this `refresh_feeds` command on a timer to keep your feeds up to date.

### Feedback **** is this still applicable?

To populate the feedback table on the homepage, use the `collect_feedback` management 
command every few minutes:

    ./manage.py collect_feedback

### Statistics **** is this still applicable?

To populate the statistics graphs on the homepage, use the `collect_stats` management 
command every few minutes:

    ./manage.py collect_stats

### Bootstrapping Search **** is this still applicable?

Once you have an elasticsearch server running, you'll want to bootstrap it with feed and story indexes.

    ./manage.py index_feeds
    
Stories will be indexed automatically.

If you need to move search servers and want to just delete everything in the search database, you need to reset the MUserSearch table. Run 
    `make shell`

    >>> from apps.search.models import MUserSearch
    >>> MUserSearch.remove_all()
    
### If feeds aren't fetching:
  check that the `tasked_feeds` queue is empty. You can drain it by running:
    `make shell`
    
    ```
    Feed.drain_task_feeds()
    ```
    
    This happens when a deploy on the task servers hits faults and the task servers lose their 
    connection without giving the tasked feeds back to the queue. Feeds that fall through this 
    crack are automatically fixed after 24 hours, but if many feeds fall through due to a bad 
    deploy or electrical failure, you'll want to accelerate that check by just draining the 
    tasked feeds pool, adding those feeds back into the queue. This command is idempotent.
      
## Author

 * Created by [Samuel Clay](http://www.samuelclay.com).
 * Email address: <samuel@newsblur.com>
 * [@samuelclay](http://twitter.com/samuelclay) on Twitter.
 

## License

NewsBlur is licensed under the MIT License. (See LICENSE)
