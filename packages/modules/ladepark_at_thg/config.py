from typing import Optional


class LadeparkAtThgConfiguration:
    def __init__(self, server_url: Optional[str] = None, api_key: Optional[str] = None):
        self.server_url = server_url
        self.api_key = api_key
