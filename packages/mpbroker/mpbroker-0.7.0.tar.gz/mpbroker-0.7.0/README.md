# README

Media Player Broker (mpb) is an application that helps you play and track media you have watched over disparet locations. mpb keeps track of what you have played at Location A so when you are at Location B you can see what you have watched from either location to avoid digging through history command output over SSH.

mpb is not a player itself but it can be configured to launch your player of choice to view media.


### The Need

Rather than living in the cloud I have my videos duplicated at various locations. I needed something that remembers what episode of MacGyver I had watched in one location so when I was in another location I could continue watching the next episode without digging through `history` output or keeping track of what was played where.

mpb consists of a CLI application (the client) and a database (couchdb). From the client you `injest` your media metadata. This extracts the file names from file paths and stores the data in the database. After injesting, you can `list` your media which shows you the media Item, whether it has been watched or not along with a Rating, Notes, and the Sources the item is available at. You can then use the `play` command along with the Item to watch the Item. After playback is completed you are prompted to mark the item as played/watched, Rate it and add Notes - all of which are used in the `list` command to show what you have already watched and what is new.

mpb can also be used by multiple 'users' - you can share a 'user' so your wife can see what you have watched or you can keep separate users so your wife sees what she has watched and you know what you have watched.


### Install

We recommend using [pipx](https://github.com/pypa/pipx) to install mpbroker: `pipx install mpbroker`. You can also install via pip: `pip install --user mpbroker`.

mpbroker uses a config file to store your setup. This file contains information such as your media player, the database url, and types of data to injest. You can grab the sample config file from  [mpbroker/example/user_config.toml](https://gitlab.com/drad/mpbroker/-/blob/master/mpbroker/example/user_config.toml) and place it in a config location. mpbroker searches the following locations for the config file (in order of precedence):

- $MPB_CONFIG_HOME: set this environment variable to any path you like and place the mpbroker `user_config.toml` file in this location
- $XDG_CONFIG_HOME/mpbroker
- $APPDATA/mpbroker
- $HOME/.config/mpbroker


### Configure

#### Notices
- an example `user_config.toml` file can be found in the [project example directory](https://gitlab.com/drad/mpbroker/-/tree/master/mpbroker/example)
- if you do not want to use the standard locations and do not want to set a `MPB_CONFIG_HOME` envvar you can set `MPB_CONFIG_HOME` on the command line before calling mpb such as `MPB_CONFIG_HOME=/opt/tmp mpb list 'The_Matrix'`

To set up MPB you need to:
- create your `user_config.toml` file (see above for locations of this file)
- configure your user_config.toml file (at a minimum you will need to set/change the `database.db_uri` value)
- ensure your mpb database is available
  + use the `db-init` command to initialize your db if it is a new instance!

If you are testing mpb or do not have a database you can use docker-compose to start a local database with `docker-compose up` from the [project's docker-compose.yml file](https://gitlab.com/drad/mpbroker). If you use the local database your `database.db_uri` would be: `http://admin:couchdb@localhost:5984`


### Using MPB

mpb has built in help (`mpb --help`) which should give you enough info to get going.

A Quick Start:

- you will likely want to `injest` some media
- next you can use `list` to view/find an item to play
- finally you can `play` an item


### Injestion

Injestion is the process of loading media metadata into your mpbroker database.

#### Extract Metadata

Extracting metadata on injestion increases the injestion time but adds the following data to each injested media item:

    file_size: # filesize in human readable format (569 MiB, 1.1 GiB)
    file_type: # file type (video/H265)
    file_format: # file format (Matroska)
    encoding: # encoding (x265)
    duration: # duration in human readable format (1 h 52 min, 2 h 48 min)
    resolution: # resulution in width x height format (720 x 480)
    aspect_ratio: # display aspect ratio (16:9)
    audio_format:  audio format (AAC)
    audio_sampling: audio sample rate (48000)

```
# Loading ~500 videos

- with metadata extraction: 6.05s
- without metadata extraction: 99.05s
```
