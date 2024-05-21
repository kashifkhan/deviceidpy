import platform
from pathlib import Path
import os


REGISTRY_PATH = 'SOFTWARE\Microsoft\DeveloperTools'
REGISTRY_KEY = 'deviceid'
DEVICEID_LOCATION = 'Microsoft/DeveloperTools/deviceid'

class Store:
    def __new__(cls) -> 'Store':
        os_name: str = platform.system()
        if os_name in ('Windows'):
            return WindowsStore()
        
        if os_name not in ('Darwin', 'Linux'):
            raise NotImplementedError(f'OS {os_name} is not supported')
        
        return super().__new__(cls)
    
    def __init__(self) -> None:
        self._os_name: str = platform.system()
    
    def _build_path(self) -> Path:
        if self._os_name in ('Darwin'):
            home = os.getenv('HOME')
            if home is None:
                raise ValueError('HOME environment variable not set')
            
            return Path(f'{home}/Library/Application Support/{DEVICEID_LOCATION}')
        
        home = os.getenv("XDG_CACHE_HOME", f"{os.getenv('HOME')}/.cache")

        if not home:
            raise ValueError('HOME environment variable not set')
        
        return Path(home).joinpath(DEVICEID_LOCATION)
    
    def retrieve_id(self) -> str:
        """
        Retrieve the device id from the store location.
        :return: The device id.
        :rtype: str
        """
        device_id: str = ""
        file_path = self._build_path()
            
        # check if file doesnt exist and raise an Exception
        if not file_path.is_file():
            raise FileExistsError(f'File {file_path.stem} does not exist')
            
        device_id = file_path.read_text(encoding='utf-8')
        return device_id
    
    def store_id(self, device_id: str) -> None:
        """
        Store the device id in the store location.
        :param str device_id: The device id to store.
        :type device_id: str
        """
        file_path = self._build_path()

        # create the folder location if it does not exist
        try:
            file_path.parent.mkdir(parents=True)
        except FileExistsError:
            pass

        file_path.touch()
        file_path.write_text(device_id, encoding='utf-8')
                

class WindowsStore(Store):
    def retrieve_id(self) -> str:
        """
        Retrieve the device id from the windows registry.
        """
        import winreg

        device_id: str
            
        try:
            with winreg.OpenKeyEx(winreg.HKEY_CURRENT_USER, REGISTRY_PATH, reserved=0, access=winreg.KEY_READ | winreg.KEY_WOW64_64KEY ) as key_handle:
                device_id = winreg.QueryValueEx(key_handle, REGISTRY_KEY)
            return device_id[0]
        except OSError as oex:
            raise oex
    
    def store_id(self, device_id: str) -> None:
        """
        Store the device id in the windows registry.
        :param str device_id: The device id to store.
        """
        import winreg
            
        try:
            with winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, REGISTRY_PATH, reserved=0, access=winreg.KEY_ALL_ACCESS | winreg.KEY_WOW64_64KEY ) as key_handle:
                device_id = winreg.SetValueEx(key_handle, REGISTRY_KEY, 0, winreg.REG_SZ, device_id)
        except OSError as oex:
            raise oex
        


            



            
        
            

            
            





