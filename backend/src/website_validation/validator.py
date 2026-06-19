class WebsiteValidator:

    def is_valid(
        self,
        markdown: str,
        links_count: int
    ):

        if len(markdown.strip()) < 500:
            return False

        if links_count < 3:
            return False

        text = markdown.lower()

        invalid_patterns = [
            "404",
            "page not found",
            "not found"
        ]

        return not any(
            pattern in text
            for pattern in invalid_patterns
        )
        
