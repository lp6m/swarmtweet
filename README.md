# swarmtweet

## deploy
fix `secret/__init__.py` to your foursquare app id and secret.
```sh
gcloud run deploy
```
After you get deployed URL on Google cloud, fix `url_prefix` in `setting/__init__.py` to your deployed URL and re-deploy.

