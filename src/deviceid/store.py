import platform
from pathlib import Path
import os
from typing import Optional

REGISTRY_KEY = r'SOFTWARE\Microsoft\DeveloperTools\deviceid'
DEVICEID_LOCATION = r'Microsoft/DeveloperTools/deviceid'


class Store:
    def __init__(self) -> None:
        self.os_name: str = platform.system()
    
    def _build_path(self) -> Path:
        if self.os_name in ('Linux'):
            return Path(os.getenv("XDG_CACHE_HOME", f"{os.getenv("HOME")}/.cache")).joinpath(DEVICEID_LOCATION)
        
        elif self.os_name in ('Darwin'):
            return Path(f'$HOME/Library/Application Support/{DEVICEID_LOCATION}')
        
        raise ValueError(f'Unsupported OS: {self.os_name}')
    
    def retrieve_id(self) -> Optional[str]:
        if self.os_name in ('Windows'):
            return self._read_from_registry()

        file_path: Path = self._build_path()
            
        # check if file doesnt exist and raise an Exception
        if not file_path.is_file():
            return None
            
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
        
    def _read_from_registry(self) -> Optional[str]:
        import winreg

        device_id: Optional[str] = None
            
        try:
            with winreg.OpenKeyEx(winreg.HKEY_CURRENT_USER, REGISTRY_KEY, reserved=0, access=winreg.KEY_READ | winreg.KEY_WOW64_64KEY ) as key_handle:
                device_id = winreg.QueryValueEx(key_handle, REGISTRY_KEY)
            return device_id
        except OSError:
            return None
    
    def _write_to_registry(self, device_id: str) -> None:
        import winreg
            
        try:
            with winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, REGISTRY_KEY, reserved=0, access=winreg.KEY_ALL_ACCESS | winreg.KEY_WOW64_64KEY ) as key_handle:
                device_id = winreg.SetValuEx(key_handle, REGISTRY_KEY, 0, winreg.REG_SZ, device_id)
        except OSError as oex:
            raise oex
             
    
    




            



            
        
            

            
            





