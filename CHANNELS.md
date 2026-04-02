# Channel Adaptation Notes

Keep the workflows generic.

Only the proactive delivery route should change.

## Core placeholders

- `{{PRIMARY_UPDATE_CHANNEL}}`
- `{{PRIMARY_UPDATE_TARGET}}`

## Typical mappings

- Slack -> `slack` + channel or DM target
- Telegram -> `telegram` + chat id / username
- Signal -> `signal` + phone / configured target
- Discord -> `discord` + channel / thread id
- Google Chat -> `googlechat` + space target

## How to use this in the pack

- Use the placeholders in cron delivery blocks
- Use the placeholders in any skill text that sends proactive updates
- Do not hardcode Slack unless the install is intentionally Slack-only

## Suggested pattern

- main-session sweeps can stay delivery-free if they already run in the user's active channel
- isolated jobs that should announce completion should use `{{PRIMARY_UPDATE_CHANNEL}}` + `{{PRIMARY_UPDATE_TARGET}}`
- noisy jobs should default to `delivery.mode = none`

## Good defaults

Use one primary route for operational nudges.

Examples:
- founder DM
- private ops channel
- dedicated assistant thread

Avoid spraying the same update into multiple places.
