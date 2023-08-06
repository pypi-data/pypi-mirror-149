# python-trovo

This is a Python wrapper for some of the [Trovo API](https://developer.trovo.live/docs/APIs.html) functions, specifically:

- Main API
  - 5.1. Get Game Categories (`get_all_game_categories`)
  - 5.2. Search Categories (`get_game_categories`)
  - 5.3. Get top channels (`get_top_channels`)
  - 5.4. Get Users (get channel id) (`get_users`)
  - 5.5. Get Channel Info by ID (`get_channel_info_by_id`)
  - 5.10. Get Emotes (`get_emotes`)
  - 5.11. Get channel viewers (`get_channel_viewers`)
  - 5.12. Get channel followers (`get_channel_followers`)
  - 5.13 Get Live Stream Urls (`get_livestream_urls`)
  - 5.14 Get Clips Info (`get_clips_info`)
  - 5.15 Get Past Streams Info (`get_past_streams_info`)

To obtain a connection, just run the following command:
```python
import trovoApi

c = trovoApi.TrovoClient("client_id")
print(c.get_all_game_categories())
```