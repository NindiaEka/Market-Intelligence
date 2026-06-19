class FallbackCapabilityDetector:

    def __init__(self, detectors):
        self.detectors = detectors

    def detect(self, facts):
        last_error = None

        for detector in self.detectors:

            try:

                return detector.detect(
                    facts
                )

            except Exception as e:

                print(
                    f"Detector failed: {e}"
                )

                last_error = e

        raise last_error