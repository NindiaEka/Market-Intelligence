from urllib.parse import urlparse

from .models import PageLink


IMPORTANT_KEYWORDS = [
    # English
    "profile",
    "history",
    "about",
    "investor",
    "financial",
    "annual",
    "sustainability",
    "governance",
    "business",
    "services",
    "structure",
    "milestone",
    
    # Indonesia
    "tentang",
    "profil",
    "perusahaan",
    "investor",
    "hubungan-investor",
    "produk",
    "layanan",
    "solusi",
    "bisnis",
    "keberlanjutan",
    "tata-kelola",
    "karir",
]


class ImportantLinkSelector:

    def __init__(
        self,
        base_domain: str,
        max_links: int = 10
    ):
        self.base_domain = base_domain
        self.max_links = max_links

    def select(
        self,
        links: list[PageLink]
    ) -> list[PageLink]:

        selected_links = []
        seen_urls = set()

        for link in links:

            # skip duplicate url
            if link.url in seen_urls:
                continue

            # skip external domain
            if urlparse(link.url).netloc != self.base_domain:
                continue

            text = (
                f"{link.title} {link.url}"
            ).lower()

            if any(
                keyword in text
                for keyword in IMPORTANT_KEYWORDS
            ):

                selected_links.append(link)
                seen_urls.add(link.url)
                
                print(f"Selected: {link.title}"
)

        return selected_links[:self.max_links]
    
    