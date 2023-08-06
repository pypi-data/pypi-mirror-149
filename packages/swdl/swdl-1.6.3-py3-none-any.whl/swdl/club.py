class Club:
    def __init__(
        self,
        id: str,
        city: str = "",
        latitude: float = 0,
        longitude: float = 8.832628399999999,
        commercial_ready: bool = False,
        has_system: bool = False,
        zip: int = 0,
        color: str = "#000000",
        name: str = "",
        location: str = "",
        did: str = "",
        dataservice=None,
    ):
        self.datasevice = dataservice
        self.id = id
        self.city = city
        self.latitude = latitude
        self.longitude = longitude
        self.commercial_ready = commercial_ready
        self.has_system = has_system
        self.zip = zip
        self.color = color
        self.name = name
        self.location = location
        self.did = did

    @classmethod
    def from_json(
        cls,
        dataservice,
        id: str,
        city: str = "",
        latitude: float = 0,
        longitude: float = 8.832628399999999,
        commercialReady: bool = False,
        hasSystem: bool = False,
        zip: int = 0,
        color: str = "#000000",
        name: str = "",
        location: str = "",
        dId: str = "",
        *args,
        **kwargs
    ):
        return Club(
            id=id,
            city=city,
            latitude=latitude,
            longitude=longitude,
            commercial_ready=commercialReady,
            has_system=hasSystem,
            zip=zip,
            color=color,
            name=name,
            location=location,
            did=dId,
            dataservice=dataservice,
        )
