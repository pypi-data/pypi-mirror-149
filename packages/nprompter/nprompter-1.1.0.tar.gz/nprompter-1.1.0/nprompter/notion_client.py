from typing import Dict, List

import requests


def query_db(status: str) -> Dict:
    return {"filter": {"or": [{"property": "Status", "select": {"equals": status}}]}}


class NotionClient:
    def __init__(self, notion_api_key: str, notion_version: str):
        self.headers = {
            "Authorization": f"Bearer {notion_api_key}",
            "Notion-Version": notion_version,
        }

    def query_database(self, database_id: str) -> Dict:
        database = requests.get(
            f"https://api.notion.com/v1/databases/{database_id}",
            headers=self.headers,
        ).json()
        return database

    def get_pages(self, page_status: str, database_id: str) -> List[Dict]:
        query = query_db(page_status)
        database = requests.post(
            f"https://api.notion.com/v1/databases/{database_id}/query",
            json=query,
            headers=self.headers,
        ).json()
        return database["results"]

    def get_blocks(self, page_id: str) -> List[Dict]:
        page = requests.get(
            f"https://api.notion.com/v1/blocks/{page_id}/children",
            headers=self.headers,
        ).json()
        return page["results"]
