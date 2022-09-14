# Rajdhani

## Deployment

To deploy this project yourself, you will need a server to host the deployment platform.

Instructions for that can be found at https://github.com/pipalacademy/boring-serverless

One extra step that you can add to it is installing the Python dependencies for this
repository:

```
mkdir apps
git clone https://github.com/pipalacademy/rajdhani apps/pipalacademy
venv/bin/python -m pip install -r apps/pipalacademy/requirements.txt
rm -rf apps/pipalacademy
```

Once this is done, you'll have to update the
[`.github/workflows/deploy.yml`](.github/workflows/deploy.yml) file to set the server_url
to your server where you hosted the deployment platform.

For each fork, you'll have to perform a one-time action to enable GitHub actions on the
repository. This can be found in the "Actions" tab on the repository page.

In the `boring-serverless/config.yml` file on your server, you will need to add repository
names that you want to host on your platform. This is a basic authentication check before
deployment.

All set!

enabled github actions
