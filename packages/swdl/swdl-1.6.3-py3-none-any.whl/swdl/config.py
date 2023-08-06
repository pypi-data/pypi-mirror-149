import os


class Settings:
    """Contains configuration variables for SWDL."""

    def __init__(self):

        self.SW_CLOUD_API_ENV = os.environ.get("SW_CLOUD_API_ENV", "prod")

        self.DISCOVERY_URL = (
            "https://aisw-ww-prod.ew.r.appspot.com/api-discovery/service/prod"
        )
        if self.SW_CLOUD_API_ENV.lower() == "dev":
            self.DISCOVERY_URL = (
                "https://aisw-ww-prod.ew.r.appspot.com/api-discovery/service/dev"
            )
        self.API_KEY = "AIzaSyD7ZaM7-weZiC9zhuv0LA_BLtbKMq6vcLs"
