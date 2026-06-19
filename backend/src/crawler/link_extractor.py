import re

from .models import PageLink


class LinkExtractor:

    def extract(
        self,
        markdown: str
    ) -> list[PageLink]:

        pattern = r"\[([^\]]+)\]\((https?://[^)]+)\)"

        matches = re.findall(
            pattern,
            markdown
        )

        links = []

        for title, url in matches:

            if not title.strip():
                continue

            links.append(
                PageLink(
                    title=title.strip(),
                    url=url.strip()
                )
            )

        return links