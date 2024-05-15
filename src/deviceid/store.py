import platform
from pathlib import Path
import os
from typing import Optional

REGISTRY_PATH = "SOFTWARE\Microsoft\DeveloperTools"
REGISTRY_KEY = "deviceid"
DEVICEID_LOCATION = "Microsoft/DeveloperTools/deviceid"


class Store:
    def __init__(self) -> None:
        self.os_name: str = platform.system()
    
    def retrieve_id(self) -> str:
        if self.os_name in ('Windows'):
            return self._read_from_registry()

        file_path: Path = self._build_path()
            
        # check if file doesnt exist and raise an Exception
        if not file_path.is_file():
            raise FileExistsError(f'File {file_path.stem} does not exist')
            
        device_id = file_path.read_text(encoding='utf-8')
        return device_id
        
    def store_id(self, device_id: str) -> None:
        if self.os_name in ('Windows'):
            self._write_to_registry(device_id)
            return
        
        file_path: Path = self._build_path()
        
        try:
            file_path.parent.mkdir(parents=True)
        except FileExistsError:
            pass

        file_path.touch()
        file_path.write_text(device_id, encoding='utf-8')

    def _build_path(self) -> Path:
        if self.os_name in ('Darwin'):
            return Path(f'$HOME/Library/Application Support/{DEVICEID_LOCATION}')
        
        return Path(os.getenv("XDG_CACHE_HOME", f"{os.getenv('HOME')}/.cache")).joinpath(DEVICEID_LOCATION)
        
    def _read_from_registry(self) -> str:
        import winreg

        device_id: str # RUN on py3.8, ALPINE and 
            
        try:
            with winreg.OpenKeyEx(winreg.HKEY_CURRENT_USER, REGISTRY_PATH, reserved=0, access=winreg.KEY_READ | winreg.KEY_WOW64_64KEY ) as key_handle:
                device_id = winreg.QueryValueEx(key_handle, REGISTRY_KEY)
            return device_id[0]
        except OSError:
            raise
    
    def _write_to_registry(self, device_id: str) -> None:
        import winreg
            
        try:
            with winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, REGISTRY_PATH, reserved=0, access=winreg.KEY_ALL_ACCESS | winreg.KEY_WOW64_64KEY ) as key_handle:
                device_id = winreg.SetValueEx(key_handle, REGISTRY_KEY, 0, winreg.REG_SZ, device_id)
        except OSError as oex:
            raise oex


            



            
        
            

            
            





