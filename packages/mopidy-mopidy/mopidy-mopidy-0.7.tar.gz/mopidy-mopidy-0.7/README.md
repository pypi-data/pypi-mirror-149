# Mopidy-Mopidy
Backend plugin for Mopidy Satellites.

Plugin can be used to run satellite mopidy server, which gets music content from master mopidy server.

Master server must have [Mopidy-Master](https://github.com/stffart/mopidy-master) plugin installed

Features:
- Playlists lookup on master
- Library browsing on master
- Do search from master library


### Installation
Install [Mopidy-Master](https://github.com/stffart/mopidy-master) on master server first.


Then install mopidy-mopidy on other servers by running:

```
pip install mopidy-mopidy
```

### Configuration

```
[http]
enabled = true
hostname = satellite ip (must be available from master for synchronization)
port = 6680
#disable csrf protection for connecting to mopidy websocket from any client in network
csrf_protection = false


[mopidy_mopidy]
enabled = true
master = your_master_host
name = satellite name
ip = satellite ip (must be available from master for synchronization)
```

