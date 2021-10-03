# coal_free

Recreating [an awesome power generation graphic](https://www.theguardian.com/environment/ng-interactive/2019/may/25/the-power-switch-tracking-britains-record-coal-free-run) from the Guardian

# Instructions

- Get an API key by following the [BMRS API guide](https://www.elexon.co.uk/documents/training-guidance/bsc-guidance-notes/bmrs-api-and-data-push-user-guide-2/)
- Save the key as an environment variable caled `bmrs_key`

To deploy locally:

- `sam build`
- `sam local start-api`
