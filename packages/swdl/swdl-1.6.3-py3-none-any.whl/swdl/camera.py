import simplejson as json


class Camera:
    def __init__(
        self,
        cid: str,
        dataservce,
        current_task: str = "",
        hardware_platform: str = "K2",
        address: str = "",
        system_state: str = "",
        tickets: list = None,
        owner_club_id: str = "",
        stitching: str = "TBD",
        lenses: str = "",
    ):
        self.id = cid
        self.dataservice = dataservce
        self.current_task = current_task
        self.hardware_platform = hardware_platform
        self.address = address
        self.system_state = system_state
        self.tickets = tickets
        self.owner_club_id = owner_club_id
        self.stitching = stitching
        self.lenses = lenses
        if not self.tickets:
            self.tickets = []
        if isinstance(tickets, str):
            try:
                self.tickets = json.loads(tickets)
            except json.errors.JSONDecodeError:
                self.tickets = []

    @classmethod
    def from_json(
        cls,
        dataservice,
        RowKey: str,
        currentTask: str = "",
        hardwarePlatform: str = "K2",
        address: str = "",
        systemState: str = "",
        tickets: list = None,
        ownerClubId: str = "",
        stitching: str = "TBD",
        lenses: str = "",
        *args,
        **kwargs
    ):
        return Camera(
            cid=RowKey,
            dataservce=dataservice,
            current_task=currentTask,
            hardware_platform=hardwarePlatform,
            address=address,
            system_state=systemState,
            tickets=tickets,
            owner_club_id=ownerClubId,
            stitching=stitching,
            lenses=lenses,
        )

    def update(self, **kwargs):
        self.dataservice.update_camera(self, kwargs)

    def set_stitching_status(self, status: str):
        self.dataservice.set_camera_stitching_status(self.id, status)

    def __repr__(self):
        return str(self.__dict__)
