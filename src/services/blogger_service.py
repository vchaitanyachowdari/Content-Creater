from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import markdown
import asyncio
import logging
from typing import Optional

class BloggerService:
    """Service for interacting with Blogger API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.logger = logging.getLogger(__name__)

    def publish_post(self, title: str, content: str) -> str:
        """Publish a post to Blogger"""
        # Implementation for publishing to Blogger
        self.logger.info(f"Publishing post: {title}")
        # Simulate publishing
        return "https://yourblog.blogspot.com/post-url"

    def setup_service(self):
        SCOPES = ['https://www.googleapis.com/auth/blogger']
        try:
            flow = InstalledAppFlow.from_client_secrets_file(
                self.credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
            self.service = build('blogger', 'v3', credentials=creds)
            self._set_blog_id()
        except Exception as e:
            self.logger.error(f"Blogger service setup failed: {e}")
            raise

    def _set_blog_id(self):
        blogs = self.service.blogs().listByUser(userId='self').execute()
        if blogs['items']:
            self.blog_id = blogs['items'][0]['id']
            self.logger.info(f"Connected to blog: {blogs['items'][0]['name']}")

    async def save_draft(self, content: str, title: str) -> str:
        try:
            html_content = markdown.markdown(content)
            post = {
                'kind': 'blogger#post',
                'title': title,
                'content': html_content,
                'status': 'DRAFT'
            }
            
            result = await asyncio.to_thread(
                self.service.posts().insert(
                    blogId=self.blog_id,
                    body=post,
                    isDraft=True
                ).execute
            )
            return result['url']
        except Exception as e:
            self.logger.error(f"Failed to save draft: {e}")
            raise 