import platform
from typing import Optional
import uuid

from store import Store


class DeviceID:
    def __init__(self):
        self.store = Store()

    
    def get_device_id(self) -> str:
        device_id: Optional[str]  = None
        
        try:
            device_id = self.store.retrieve_id()
            return device_id
        except (OSError, FileExistsError) as oex:
            pass

        device_id = str(uuid.uuid4()).lower()

        self.store.store_id(device_id)

        return device_id



k = print(DeviceID().get_device_id())



