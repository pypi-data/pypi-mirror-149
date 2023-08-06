from typing import Any, Dict, List, Optional

import requests

from .errors import DictionaryNotFound, LimitReached, Unauthorized
from .models import Dictionary, Hit, Language, create_hit

__all__ = ("Client",)


class Client:
    base_url = "https://api.pons.com/v1"
    secret: str

    def __init__(self, secret: str) -> None:
        self.secret = secret

    def request(
        self, endpoint: str, *, send_secret: bool = False, **params: Any
    ) -> List[Any]:
        headers = {"X-Secret": self.secret} if send_secret else None
        res = requests.request(
            "GET", self.base_url + endpoint, params=params, headers=headers
        )

        status = res.status_code
        if status == 204:
            return []
        if status == 403:
            raise Unauthorized()
        if status == 404:
            raise DictionaryNotFound()
        if status == 503:
            raise LimitReached()
        return res.json()

    def get_dictionaries(self, language: Language) -> List[Dictionary]:
        data = self.request("/dictionaries", language=language)
        return [
            Dictionary(
                key=dictionary["key"],
                simple_label=dictionary["simple_label"],
                directed_label=dictionary["directed_label"],
                languages=dictionary["languages"],
            )
            for dictionary in data
        ]

    def query(
        self,
        term: str,
        dictionary_key: str,
        source_language: Language,
        output_language: Optional[Language] = None,
        *,
        fuzzy: bool = False,
        references: bool = False,
    ) -> Dict[Language, List[Hit]]:
        data = self.request(
            "/dictionary",
            q=term,
            l=dictionary_key,
            fm=fuzzy,
            ref=references,
            language=output_language,
            send_secret=True,
            **{"in": source_language},
        )
        return {
            entry["lang"]: [create_hit(hit) for hit in entry["hits"]] for entry in data
        }
