from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SlackService:
    def __init__(self, content_engine):
        self.app = App(token=os.environ["SLACK_BOT_TOKEN"])
        self.content_engine = content_engine
        self.setup_handlers()

    def setup_handlers(self):
        @self.app.message("!generate")
        async def handle_generate_command(message, say):
            try:
                # Extract topic from message
                topic = message['text'].replace('!generate', '').strip()
                if not topic:
                    await say("Please provide a topic after !generate")
                    return

                # Default preferences
                preferences = {
                    "style": "professional",
                    "target_audience": "general",
                    "include_visuals": True,
                    "fact_check_level": "standard"
                }

                # Generate content
                result = await self.content_engine.generate_content(topic, preferences)
                
                # Format response for Slack
                blocks = self._format_content_for_slack(result)
                await say(blocks=blocks)

            except Exception as e:
                logger.error(f"Error handling generate command: {str(e)}")
                await say("Sorry, there was an error generating content.")

    def _format_content_for_slack(self, content: Dict[str, Any]) -> list:
        """Format content into Slack blocks"""
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": content["title"]
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": content["content"][:3000] + "..."  # Slack has message length limits
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Stats:* Words: {content['stats']['word_count']} | Reading time: {content['stats']['reading_time']} min"
                    }
                ]
            }
        ]
        return blocks

    def start(self):
        """Start the Slack bot"""
        handler = SocketModeHandler(self.app, os.environ["SLACK_APP_TOKEN"])
        handler.start() 