from typing import Any
from jellyfin_apiclient_python import JellyfinClient
from notion_client import Client as NotionClient
from .helper import Runner, JellyfinOptions, NotionOptions
from .helper import avid
import logging
from datetime import datetime


class Jellyfin2Notion(Runner):
    jellyfin_options: JellyfinOptions
    notion_options: NotionOptions
    jellyfin_parent_id: str
    jellyfin_limit: int
    should_update: bool
    dry_run: bool

    def run(self):
        client = JellyfinClient()
        client.config.app("avda", "0.0.1", "machine_name", "local-script")
        client.config.data["auth.ssl"] = self.jellyfin_options.ssl
        client.auth.connect_to_address(self.jellyfin_options.endpoint)
        client.auth.login(
            self.jellyfin_options.endpoint,
            self.jellyfin_options.username,
            self.jellyfin_options.password,
        )
        credentials = client.auth.credentials.get_credentials()
        client.authenticate(credentials)

        params = {
            "ParentId": self.jellyfin_parent_id,
            #     "NameStartsWith": letter,
            #    'searchTerm': "",
            "Recursive": True,
            "IncludeItemTypes": "Movie",
            "Fields": "IsFolder,Tags,Type,People,Name,PremiereDate",
            "SortBy": "DateCreated,SortName,ProductionYear",
            "SortOrder": "Descending",
        }

        if self.jellyfin_limit > 0:
            params["Limit"] = self.jellyfin_limit

        result = client.jellyfin.user_items(params=params)

        final_result = []

        for item in result["Items"]:
            try:
                date = datetime.fromisoformat(item["PremiereDate"]).strftime("%Y-%m-%d")
            except:
                date = ""

            id = avid.get_avid_from_title(item["Name"])
            title = item["Name"].replace("id", "")
            title = title.strip("-").strip()

            res = {
                "title": title,
                "date": date,
                "id": id,
                "actors": [a["Name"] for a in item["People"] if a["Type"] == "Actor"],
                "tags": item["Tags"],
            }
            final_result.append(res)

        logging.info(f"total {len(final_result)}")

        self.sync_to_notion(
            self.notion_options.api_key,
            self.notion_options.database_id,
            final_result,
            self.should_update,
        )

    def sync_to_notion(self, key, database_id, result, should_update):
        # Authenticate and setup the client
        notion = NotionClient(auth=key)
        database_id = database_id
        for item in result:
            self.update_or_add_item(notion, database_id, item, should_update)

    # Define a function to update or add an item in the database
    def update_or_add_item(
        self, notion: NotionClient, database_id: str, item: Any, should_update: bool
    ):
        # Check if the item already exists in the database
        results = notion.databases.query(
            **{
                "database_id": database_id,
                "filter": {"property": "番号", "title": {"equals": item["id"]}},
            }
        ).get("results")

        if results and (not should_update):
            logging.info(f'skip item {item["id"]} to notion')
            return

        properties: Any = {
            "标题": {"title": [{"text": {"content": item["title"]}}]},
        }

        if item["date"]:
            properties["日期"] = {"date": {"start": item["date"]}}

        if item["tags"] and len(item["tags"]) > 0:
            properties["标签"] = {
                "type": "multi_select",
                "multi_select": [{"name": item} for item in item["tags"]],
            }
        if item["actors"] and len(item["actors"]) > 0:
            properties["演员"] = {
                "type": "multi_select",
                "multi_select": [{"name": item} for item in item["actors"]],
            }

        if results:
            item_id = results[0].get("id")
            if not self.dry_run:
                notion.pages.update(**{"page_id": item_id, "properties": properties})
            logging.info(f'update record {item["id"]}')
        else:
            properties["番号"] = {
                "type": "rich_text",
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": item["id"]},
                    },
                ],
            }
            if not self.dry_run:
                notion.pages.create(
                    **{"parent": {"database_id": database_id}, "properties": properties}
                )
            if results:
                logging.info(f'update item {item["id"]} at notion')
            else:
                logging.info(f'add item {item["id"]} at notion')
