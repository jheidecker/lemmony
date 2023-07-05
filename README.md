
# lemmony

Lemmy by default, will only collect new content from federated servers when a user looks for it and/or subscribes to that remote content.

This script should help lemmy self-hosters with few or one user, who want to browse All.

The script gets all of the publicly federated communities and "adds" them to your local instance. All should be populated with activity from around the lemmyverse.

## Usage

The script requires an account to login to the instance. It is reccomended you create a "bot" user that is not used for interactive logins.

This will probably fail if the instance does not have a valid SSL certificate.

### Docker / Podman

```
sudo docker run ghcr.io/jheidecker/lemmony/lemmony lemmony-cli -l [your-instance] -u [username] -p [password] 
podman run ghcr.io/jheidecker/lemmony/lemmony lemmony-cli -l [your-instance] -u [username] -p [password] 
```
- [your instance] - the domain of the local instance i.e. lemmyrules.com. This is the same address (minus the https://) you use to access your lemmy instance. Depending on your setup, it might `host.domain.name` or just `domain.name`.
- [user] - the user account (login.)
- [password] - password for [user]

### Manual

Requires python3, and pip

```
git clone https://github.com/jheidecker/lemmony.git
cd lemmony
pip install build
python -m build
pip install dist/lemmony-0.0.1-py3-none-any.whl
```

This should install lemmony-cli as a command in your path:

```
# lemmony-cli
usage: lemmony-cli [-h] [-i INCLUDE [INCLUDE ...]] [-e EXCLUDE [EXCLUDE ...]] -l LOCAL -u USERNAME -p PASSWORD
lemmony-cli: error: the following arguments are required: -l/--local, -u/--username, -p/--password
```

### Include and exclude instances

By default lemmony tries to subscribe to as many communities as it can based on the global lists provided by [lemmyverse.net](lemmyverse.net) You can include and exclude instances using the optional `-i` and `-e` flags respectively. This way you cal only subscribe to favorites or exclude instances you do not want to subscribe to. The flags cannot be used at the same time. For example:

To add communities from all instances except `lemmy.world`:

```
# lemmony-cli -l my.lemmy -u my_bot -p my_password -e lemmy.world
```

To add communities from ONLY `lemmy.world`:

```
# lemmony-cli -l my.lemmy -u my_bot -p my_password -i lemmy.world
```

You can specify multiple instances seperated by spaces. For example: `-i lemmy.world lemmy.ml beehaw.org`

## DISCLAIMER

This will cause load and subsequent incoming network activity on your instance. A raspberry-pi or your internet may not be able to accommodate updates from all of the lemmyverse's communities!

## Development

