import platform
import uuid

from src.deviceid.store import Store


class DeviceID:
    def __init__(self):
        self.store = Store()

    
    def get_device_id(self) -> str:
        try:
            return self.store.retrieve_id()
        except Exception:
            pass

        device_id: str = str(uuid.uuid4()).lower()

        # store the id

        self.store.store_id(device_id)

        return device_id

