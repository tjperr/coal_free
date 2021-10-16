# coal_free

Recreating [an awesome power generation graphic](https://www.theguardian.com/environment/ng-interactive/2019/may/25/the-power-switch-tracking-britains-record-coal-free-run) from the Guardian

# Instructions

- Get an API key by following the [BMRS API guide](https://www.elexon.co.uk/documents/training-guidance/bsc-guidance-notes/bmrs-api-and-data-push-user-guide-2/)
- Save the key as an environment variable caled `bmrs_key`

To deploy locally:

1. Start Docker
2. Save environment variable `bmrs_key`
3. `sam build`
4. `sam local start-api` or `sam local invoke`

To deploy to prod:

1. Save environment variable `bmrs_key`
2. `sam deploy --parameter-overrides ParameterKey=Key,ParameterValue=$bmrs_key`

To deploy the site:

- Upload static site content with `aws s3 cp site/* s3://STATIC_SITE_NAME_HERE/`
