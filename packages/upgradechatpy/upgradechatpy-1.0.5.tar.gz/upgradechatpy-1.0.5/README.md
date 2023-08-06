# UpgradeChatPy

UpgradeChatPy is a simple asyncio wrapper around Upgrade.Chat's API.

[Docs are available here](https://upgradechatpy.readthedocs.io/en/latest/).

## Example Usage

```python
import upgradechat
client = upgradechat.UpgradeChat(CLIENT_ID, CLIENT_SECRET)
await client.get_orders(discord_id=123456789123456789)
```
