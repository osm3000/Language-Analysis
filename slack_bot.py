from slack import WebClient
from slack.errors import SlackApiError
import configurations
import platform

SECRETS = configurations.get_secrets_file()


class BasicBot:
    def __init__(self) -> None:
        self.client = WebClient(token=SECRETS["AUTH_SLACK"]["TOKEN"])
        self.msg = "Nothing"

    def __enter__(self):
        return self._send

    def __exit__(self, exc_type, exc_value, exc_traceback):
        del self.client

    def _send(self, msg):
        msg = platform.node() + " -- " + msg
        response = self.client.chat_postMessage(channel="#bot_events", text=msg)
        return response