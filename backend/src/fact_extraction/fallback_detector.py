class FallbackExtractor:

    def __init__(
        self,
        extractors
    ):
        self.extractors = extractors

    def extract(
        self,
        markdown
    ):

        last_error = None

        for extractor in self.extractors:

            try:

                return extractor.extract(
                    markdown
                )

            except Exception as e:

                print(
                    f"Extractor failed: {e}"
                )

                last_error = e

        raise last_error
    
