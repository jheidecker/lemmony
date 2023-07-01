
# lemmony

Lemmy by default, will only collect new content from federated servers when a user looks for it and/or subscribes to that remote content.

This script should help lemmy self-hosters with few or one user, who want to browse All.

The script gets all of the publicly federated communities and "adds" them to your local instance. All should be populated with activity from around the lemmyverse.

## To use:

Replace the variables with your data:

```
local_instance = 'your.instance.com'
username = 'bot_user'
password = 'bot_password'
```
then:

`python lemmony.py`

## DISCLAIMER

This will cause load and subsequent incoming network activity on your instance. A raspberry-pi or your internet may not be able to accommodate updates from all of the lemmyverse's communities.
