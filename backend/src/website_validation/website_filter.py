from urllib.parse import urlparse


class WebsiteFilter:

    BAD_DOMAINS = [
        "globaldata.com",
        "ooredoo.com",
        "wordpress.com",
    ]

    BAD_PATHS = [
        "/wiki/",
        "/vendor/",
        "/vendors/",
        "/public/",
        "/directory/",
        "/listing/",
        "/portal/",
        "/careers/",
        "/company-profile/",
        "/profile/",
    ]

    def is_company_website(
        self,
        url: str
    ) -> bool:

        url = url.lower()

        # reject bad domains
        if any(
            bad_domain in url
            for bad_domain in self.BAD_DOMAINS
        ):
            return False

        # reject bad paths
        if any(
            bad_path in url
            for bad_path in self.BAD_PATHS
        ):
            return False

        # hanya terima homepage/root domain
        path = urlparse(url).path.lower()

        # if path not in ["", "/"]:
        #     return False
        
        print(url)

        path = urlparse(url).path.lower()

        print(path)

        return True