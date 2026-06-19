import re


class MarkdownCleaner:
    """
    Membersihkan hasil crawl dari:
    - menu navigasi
    - footer
    - repeated links
    - contact section
    - social media section
    - duplicate lines
    """

    MENU_KEYWORDS = [
        "Company Profile",
        "Profile and History",
        "Board of Commissioners",
        "Board of Directors",
        "Investor Relations",
        "Annual Reports",
        "Sustainability Reports",
        "Financial Reports",
        "Governance",
        "Corporate Social Responsibility",
        "WebMail",
        "Survey",
        "Sitemap",
        "Whistleblowing",
        "Privacy Policy",
        "Fraud Alert",
        "Scam Alert",
        "Follow Us",
        "Contact",
        "Tools",
        "Our Website",
        "Media & Information",
        "Ops Partnership",
        "KSOT Wells",
        "KSOT Structure",
        "CCS/CCUS",
    ]

    def clean(
        self,
        markdown: str
    ) -> str:

        lines = markdown.splitlines()

        cleaned_lines = []

        for line in lines:

            line = line.strip()

            if not line:
                continue

            # --------------------------------
            # Remove markdown menu links
            # --------------------------------
            if re.match(
                r"^\s*[\-\*]\s*\[.*?\]\(.*?\)\s*$",
                line
            ):
                continue

            # --------------------------------
            # Remove image links
            # --------------------------------
            if re.match(
                r"^!\[.*?\]\(.*?\)$",
                line
            ):
                continue

            # --------------------------------
            # Remove url only lines
            # --------------------------------
            if re.match(
                r"^https?://",
                line
            ):
                continue

            # --------------------------------
            # Remove menu keywords
            # --------------------------------
            if any(
                keyword.lower() in line.lower()
                for keyword in self.MENU_KEYWORDS
            ):
                continue

            # --------------------------------
            # Remove footer
            # --------------------------------
            if "copyright" in line.lower():
                continue

            if "all rights reserved" in line.lower():
                continue

            if "phone:" in line.lower():
                continue

            if "fax:" in line.lower():
                continue

            if line in [
                "* * *",
                "---"
            ]:
                continue

            cleaned_lines.append(line)

        # ====================================
        # Remove duplicate lines
        # ====================================

        seen = set()
        deduped = []

        for line in cleaned_lines:

            normalized = line.strip()

            if normalized in seen:
                continue

            seen.add(normalized)
            deduped.append(line)

        return "\n".join(deduped)