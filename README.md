
# lemmony

Lemmy, by default, will only collect new content from federated servers when a user searches for it specifically and/or subscribes to that remote content.

This script uses the Lemmy API, Python and Docker to help Lemmy self-hosters with a few (or just one) user who want to browse an "All," with the most complete picture of the federated Lemmyverse!

The script gets all of the publicly federated communities and "makes them known" to your local instance and then subscribes to them. "All" should be populated with activity from around the Lemmyverse.

Per: [https://join-lemmy.org/docs/users/01-getting-started.html](https://join-lemmy.org/docs/users/01-getting-started.html)

> These previous ways will only show communities that are already known to the instance. Especially if you joined a small or inactive Lemmy instance, there will be few communities to discover. You can find more communities by browsing different Lemmy instances, or using the Lemmy Community Browser. When you found a community that you want to follow, enter its URL (e.g. https://feddit.de/c/main) or the identifier (e.g. !main@feddit.de) into the search field of your own Lemmy instance. Lemmy will then fetch the community from its original instance, and allow you to interact with it. The same method also works to fetch users, posts or comments from other instances.

Use is not limited to small instances, that's just what I wrote it for.

Here are some other similar projects:
 
 - [Lemmy Subscriber Bot (LSB)](https://github.com/lflare/lemmy-subscriber-bot)
 - [Lemmy Community Seeder (LCS)](https://github.com/Fmstrat/lcs)

## BIG DISCLAIMER

IF YOU DON'T UNDERSTAND WHAT THIS TOOL DOES, PLEASE CONSIDER CAREFULLY THE IMPLICATIONS OF RUNNING IT.

If you get errors (specifically KeyError,) the server is responding with rate-limit errors as a payload, instead of expected data. Try lowering the rate-limit. (`-r`)

This will cause load and subsequent incoming network activity on your instance and the network overall! A raspberry-pi or your internet may not be able to accommodate updates from all of the lemmyverse's communities!

## What lemmony does

1. Get a list of communities/magazines in the Lemmyverse from [lemmyverse.net](lemmyverse.net) that have > 0 posts, are not listed as suspicious, and meet the top and include/exclude conditions
2. Login to local instance as a specified user
3. "Makes known" (see above) any communities or magazines fetched above that have never been known on your local instance
4. Subscribes a user (follows) to all known communities on your local instance that are shown as "Unsubscribed" or, re-subscribes if the status is "Pending."

## Compatibility

Lemmy's API versioning is... not ideally stable. Check the release notes for the version of Lemmy the release was tested against. It SHOULD work with newer versions, but no guarantees it will work with older versions.

## Usage

The script requires an account to login to the instance. It is recommended you create a "bot" user, mark it as a bot, and use an obvious avatar. One is provided in the repository here for your convenience.

This will probably fail if the instance does not have a valid SSL certificate.

### docker / podman

```bash
# sudo docker pull ghcr.io/jheidecker/lemmony/lemmony
# sudo docker run ghcr.io/jheidecker/lemmony/lemmony lemmony-cli -l [your-instance] -u [username] -p [password]
```

or

```bash
# podman pull ghcr.io/jheidecker/lemmony/lemmony
# podman run ghcr.io/jheidecker/lemmony/lemmony lemmony-cli -l [your-instance] -u [username] -p [password] 
```

- [your instance] - the domain of the local instance i.e. lemmyrules.com. This is the same address (minus the https://) you use to access your lemmy instance. Depending on your setup, it might `host.domain.name` or just `domain.name`.
- [user] - the user account (login.)
- [password] - password for [user]

#### Other Options

Pass these flags to the command for more control:

- `-n` : skip subscribing to communities in the "Pending" state
- `-s` : subscribe only. skips the discovery and adding of new communities
- `-d` : discover only. skips subscribing to any communities
- `-r [number]` : will rate limit requests to LOCAL to X per second (default: 15)
- `-t [number]` : only discover top X communities **PER INSTANCE** based on active users per day (default: 10) (Lemmy only, does not apply to kbin!)
- `-k` : do not include kbin communities in discovery (will still subscribe if they meet conditions to subscribe)
- `-x` : forgo all other functions and unsubscribe the USER from all communities

### Build and Run Manually

Requires python3, and pip(3)

```bash
# git clone https://github.com/jheidecker/lemmony.git
# cd lemmony
# pip install build
# python -m build
# pip install dist/lemmony-[version]-py3-none-any.whl
```

This should install lemmony-cli as a command in your path:

```bash
# lemmony-cli
usage: lemmony-cli [-h] [-i INCLUDE [INCLUDE ...]] [-e EXCLUDE [EXCLUDE ...]] -l LOCAL -u USERNAME -p PASSWORD [-n] [-s] [-d] [-r RATE_LIMIT] [-t TOP_ONLY] [-k] [-x]

lemmony-cli: error: the following arguments are required: -l/--local, -u/--username, -p/--password
```

### Include and exclude instances

By default lemmony will only subscribe to communities based on your local instances allowed / blocked federation list. You can override this and include or exclude instances using the optional `-i` and `-e` flags respectively. This way you can only subscribe to favorite instances, or exclude instances you do not want. The flags cannot be used at the same time. For example:

To add communities from all instances except `lemmy.world`:

```bash
# lemmony-cli -l my.lemmy -u my_bot -p my_password -e lemmy.world
```

To add communities from ONLY `lemmy.world`:

```bash
# lemmony-cli -l my.lemmy -u my_bot -p my_password -i lemmy.world
```

You can specify multiple instances separated by spaces. For example: `-i lemmy.world lemmy.ml beehaw.org`

## Development Notes (build/test/release)

```bash
# git clone https://github.com/jheidecker/lemmony.git
# cd lemmony
```

- develop
- update `Containerfile` and `setup.cfg`

```bash
# export CR_PAT=secret_pat
# echo $CR_PAT | podman login ghcr.io -u secret_username --password-stdin
# podman build . -t ghcr.io/jheidecker/lemmony/lemmony:version --platform linux/amd64,linux/arm64
```

- push (requires access to ghcr package:)

```bash
# podman push ghcr.io/jheidecker/lemmony/lemmony:version
```

- test (pull, run, etc.)

```bash
# podman build . -t ghcr.io/jheidecker/lemmony/lemmony:latest --platform linux/amd64,linux/arm64
# podman push ghcr.io/jheidecker/lemmony/lemmony:latest
```

- bump release with release notes
