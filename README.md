# NewsBlurMod

This is a fork of [NewsBlur](https://github.com/samuelclay/NewsBlur) for self-hosting with 
Docker under Windows.

## Modifications
* It is possible to self-host this repo under Windows as is. It could be run either 
  directly under Docker Desktop or under Docker Engine inside WSL2.
* Increased the limit of maximum 100 unread stories. The current limit is 2000.
* Disabled alphabetical sorting of feeds in the sidebar. It is possible to sort feeds using
  drag&drop or through the development JavaScript console.
* Enlarged preview images in the grid mode, changed content position of the images 
  to "contain" instead of "fill".
* New dark theme.
* The discovery dropdown is hidden.
* Single click on unread count to mark as read.
* Websub is enabled by default, throttling of websub pushes is turned off, subscription lease
  is infinite, so NewsBlurMod could seamlessly be used with [Feedxcavator](https://github.com/GChristensen/feedxcavator).
* Disabled Prometheus middleware.

## Installation Instructions

### Running under Linux (recommended)

Clone the repo and use the Makefile.unix to install NewsBlurMod: `sudo make -f Makefile.unix nb`

### Running under Docker Engine inside WSL2
* Enable 'Virtual Machine Platform' and 'WSL2' Windows system components.
* Install openSUSE Linux distribution by issuing `wsl --install openSUSE-Tumbleweed` in the terminal.
* Enable systemd in your WSL terminal by issuing `sudo -e /etc/wsl.conf` and placing the
  following text into it:
```
[boot]
systemd=true
```
Shutdown WSL with the command: `wsl --shutdown` in the Windows terminal.
* Start WSL again by issuing `wsl` in the Windows terminal. Install required packages using the following
 command in the WSL terminal:
```
sudo zypper in make git openssl nodejs21 docker docker-compose docker-compose-switch
```
* Configure docker:
```
sudo systemctl enable docker
sudo usermod -G docker -a $USER;
newgrp docker
sudo systemctl restart docker
```
* Clone the repo in the home directory of your WSL distribution with the following 
command: `git clone https://github.com/GChristensen/NewsBlurMod`
* Issue the following command to build NewsBlur: 

 `sudo make nb -f Makefile.unix`

Restart Windows after the build is finished.

### Running under Docker Desktop
This method may result in substantial performance loss on slow machines.

* Install [Docker Desktop](https://www.docker.com/products/docker-desktop/).
* Install the latest [Git for Windows](https://git-scm.com/download/win).
* Install [MSYS2](https://www.msys2.org/) and MINGW-w64.
* Issue the command `ms-settings:developers` in the terminal and enable developer settings. 
* Add full paths of `usr/bin` and `mingw64/bin` MSYS directories to the system PATH variable.
  Ensure that they appear before any Git directory. If there are some Git binaries
  in `usr/bin` rename or move them to make the original Git for Windows the default 
  Git implementation.
* Make the `mingw32-make.exe` from `mingw64/bin` directory available as `make.exe` by 
  creating a copy or a filesystem link to this file.
* Make sure that the directory where you will clone the repo has "Full control" 
  security permissions for unprivileged users.
* Clone this repository with the following command: 
```
git clone -c core.autocrlf=false -c core.symlinks=true https://github.com/GChristensen/NewsBlurMod 
```
* Add the following entry into the `C:\Windows\System32\drivers\etc\hosts` file:
```
127.0.0.1 newsblur
```
If you are deploying it on another machine, put the IP address of that machine instead of
`127.0.0.1`.
* Change the current directory of Windows terminal to the repo directory and execute `make nb`.

### User Configuration

* After the build is finished, open https://newsblur in the browser. Please read the original 
  readme below for more details.
* Create a user account and login.
* If all premium features are not enabled automatically, execute the following code in the terminal:
```
  make shell
  
  u = User.objects.get(username='YOUR_USERNAME')
  u.profile.activate_premium(True)
  u.profile.activate_archive(True)
  u.profile.activate_pro(True)
```
* On slow machines some servers, for example node, may start before databases are online.
  It is necessary to restart their corresponding containers to make them work properly.

----

# NewsBlur

- NewsBlur is a personal news reader bringing people together
  to talk about the world. A new sound of an old instrument.
- [www.newsblur.com](https://www.newsblur.com).
- Created by [Samuel Clay](https://www.samuelclay.com).
- X/Twitter: [@samuelclay](https://x.com/samuelclay) and
  [@newsblur](https://x.com/newsblur).

<a href="https://f-droid.org/repository/browse/?fdid=com.newsblur" target="_blank">
<img src="https://f-droid.org/badge/get-it-on.png" alt="Get it on F-Droid" height="80"/></a>
<a href="https://play.google.com/store/apps/details?id=com.newsblur" target="_blank">
<img src="https://play.google.com/intl/en_us/badges/images/generic/en-play-badge.png" alt="Get it on Google Play" height="80"/></a>

&nbsp;&nbsp;&nbsp;<a href="https://apps.apple.com/us/app/newsblur/id463981119"><img src="https://tools.applemediaservices.com/api/badges/download-on-the-app-store/black/en-us?size=250x83" alt="Download on the Apple App Store" height="55"></a>

## Features

1.  Shows the original site (you have to see it to believe it).
2.  Hides stories you don't want to read based on tags, keywords, authors, etc.
3.  Highlights stories you want to read, based on the same criteria.

## Technologies

### Server-side

- [Python 3.7+](http://www.python.org): The language of choice.
- [Django](http://www.djangoproject.com): Web framework written in Python, used
  to serve all pages.
- [Celery](http://ask.github.com/celery) & [RabbitMQ](http://www.rabbitmq.com):
  Asynchronous queueing server, used to fetch and parse RSS feeds.
- [MongoDB](http://www.mongodb.com), [Pymongo](https://pypi.python.org/pypi/pymongo), &
  [Mongoengine](http://www.github.com/hmarr/mongoengine): Non-relational database,
  used to store stories, read stories, feed/page fetch histories, and proxied sites.
- [PostgreSQL](http://www.postgresql.com): Relational database, used to store feeds,
  subscriptions, and user accounts.
- [Redis](http://redis.io): Programmer's database, used to assemble stories for the river, store story ids, manage feed fetching schedules, and the minuscule bit of caching that NewsBlur uses.
- [Elasticsearch](http://elasticsearch.org): Search database, used for searching stories. Optional.

### Client-side and design

- [jQuery](http://www.jquery.com): Cross-browser compliant JavaScript code. IE works without effort.
- [Underscore.js](http://underscorejs.org/): Functional programming for JavaScript.
  Indispensable.
- [Backbone.js](http://backbonejs.org/): Framework for the web app. Also indispensable.
- Miscellaneous jQuery Plugins: Everything from resizable layouts, to progress
  bars, sortables, date handling, colors, corners, JSON, animations.
  [See the complete list](https://github.com/samuelclay/NewsBlur/tree/master/media/js).

### Prerequisites

    * Docker
    * Docker-compose

## Installation Instructions

1.  Clone this repo
2.  Run `make nb` to build all of the NewsBlur containers. This will set up all necessary databases, front-end django apps, celery tasks, node apps, flask database monitor and metrics, nginx, and a haproxy load balancer.
3.  Navigate to:

         https://localhost

    Note: You will be warned that you are using a self signed certificate. In order to get around this warning you must type "thisisunsafe" as per [this blog post](https://dblazeski.medium.com/chrome-bypass-net-err-cert-invalid-for-development-daefae43eb12).

## Using a custom domain

1.  Run the custom domain script

    ```
    bash ./utils/custom_domain.sh <domain name>
    ```

    This script will do the following:

    - Change `NEWSBLUR_URL` and `SESSION_COOKIE_DOMAIN` in `newsblur_web/docker_local_settings.py`
    - Change the domain in `config/fixtures/bootstrap.json`

You can also change domains: `bash ./utils/custom_domain.sh <old domain> <new domain>`

2.  If you're using a custom subdomain, you'll also want to add it to `ALLOWED_SUBDOMAINS` in `apps/reader/views.py`

3.  A way to make sure you updated all the correct places:

    - Go to the website address in your browser
    - Open developer tools and look at the network tab
    - Try to login
    - Look again at the developer tools, there should be a POST call to /login
    - Observe the Response headers for that call
    - The value of the "set-cookie" header should contain a "Domain=" string

    If the string after `Domain=` is not the domain you are using to access the website, then your configuration still needs your custom domain.

    You can also confirm that there is a domain name mismatch in the database by running `make shell` & typing `Site.objects.all()[0]` to show the domain that NewsBlur is expecting.

## Making docker-compose work with your existing database

To make docker-compose work with your database, upgrade your local database to the docker-compose version and then volumize the database data path by changing the `./docker/volumes/` part of the volume directive in the service to point to your local database's data directory.

To make docker-compose work with an older database version, change the image version for the database service in the docker-compose file.

## Contribution Instructions

- Making Changes:

  - To apply changes to the Python or JavaScript code, use the `make` command.
  - To apply changes to the docker-compose.yml file, use the `make rebuild` command.
  - To apply changes to the docker/haproxy/haproxy.conf file, node packages, or any new database migrations you will need to use the `make nb` command.

- Adding Python packages:
  Currently, the docker-compose.yml file uses the newsblur/newsblur_python3 image. It is built using the Dockerfile found in `docker/newsblur_base_image.Dockerfile`. Because of how the docker image is set up, you will need to create your own image and direct your docker-compose.yml file to use it. Please follow the following steps to do so.

  1. Add your new site-packages to config/requirements.txt.
  2. Add the following lines of code to your docker-compose.yml file to replace anywhere where it says `image: newsblur/newsblur_python3`

    <code>
        build:
          context: .
          dockerfile: docker/newsblur_base_image.Dockerfile
    </code>

  3. Run the `make nb` command to rebuild your docker-compose containers

- Debugging Python

  - To debug your code, drop `import pdb; pdb.set_trace()` into the Python code where you would like to start debugging
    and run `make` and then `make debug`.

- Using Django shell within Docker
  - Make sure your docker containers are up and run `make shell` to open
    the Django shell within the newsblur_web container.

### Running unit and integration tests

NewsBlur comes complete with a test suite that tests the functionality of the rss_feeds,
reader, and feed importer. To run the test suite:

    `make test`

### Running a performance test

Performance tests use the locust performance testing tool. To run performance tests via CLI, use
`make perf-cli users=1 rate=1 host=https://localhost`. Feel free to change the users, rate, and host
variables in the command to meet you needs.

You can also run locust performance tests using a UI by running `make perf-ui` and then navigating to
http://127.0.0.1:8089. This allows you to chart and export your performance data.

To run locust using docker, just run `make perf-docker` and navigate to http://127.0.0.1:8089

## Author

- Created by [Samuel Clay](https://www.samuelclay.com).
- Email address: <samuel@newsblur.com>
- [@samuelclay](https://x.com/samuelclay) on X/Twitter.

## License

NewsBlur is licensed under the MIT License. (See LICENSE)
