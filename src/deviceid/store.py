import platform
import os


class Store:
    def __init__(self) -> None:
        self.os_name: str = platform.platform()
    
    def retrieve_id(self) -> str:
        if self.os_name in ('Linux'):
            root_path: str = os.getenv("XDG_CACHE_HOME", os.path.join(os.getenv("HOME"), ".cache"))
            folder_path: str = os.path.join(root_path, "Microsoft/DeveloperTools/")

            # check if folder path doesnt exist and raise an Exception
            if not os.path.isdir(folder_path):
                raise FileNotFoundError()
            
            with open(f'{folder_path}deviceid') as f:
                device_id = f.read()
                return device_id
        
        elif self.os_name in ('Darwin'):
            folder_path: str = '$HOME/Library/Application Support/Microsoft/DeveloperTools/'

            # check if folder path doesnt exist and raise an Exception
            if not os.path.isdir(folder_path):
                raise FileNotFoundError()
            
            with open(f'{folder_path}deviceid') as f:
                device_id = f.read()
                return device_id
        
        elif self.os_name == 'Windows':
            import winreg
            
            try:
                key_handle = winreg.OpenKeyEx(winreg.HKEY_CURRENT_USER, 'SOFTWARE\Microsoft\ DeveloperTools', reserved=0, access=winreg.KEY_READ | winreg.KEY_WOW64_64KEY )
            except OSError:
                raise FileNotFoundError()
            
            try:
                device_id = winreg.QueryValueEx(key_handle, 'SOFTWARE\Microsoft\ DeveloperTools')
            except OSError:
                raise FileNotFoundError
            
            winreg.CloseKey(key_handle)

            return device_id
    
    def store_id(self, device_id: str) -> None:
        if self.os_name in ('Linux'):
            root_path: str = os.getenv("XDG_CACHE_HOME", os.path.join(os.getenv("HOME"), ".cache"))
            folder_path: str = os.path.join(root_path, "Microsoft/DeveloperTools/")

            # check if folder path doesnt exist and raise an Exception
            if not os.path.isdir(folder_path):
                raise FileNotFoundError()
            
            with open(f'{folder_path}deviceid') as f:
                f.write(device_id)
        
        elif self.os_name in ('Darwin'):
            folder_path: str = '$HOME/Library/Application Support/Microsoft/DeveloperTools/'

            # check if folder path doesnt exist and raise an Exception
            if not os.path.isdir(folder_path):
                raise FileNotFoundError()
            
            with open(f'{folder_path}deviceid') as f:
                f.write(device_id)
        
        elif self.os_name == 'Windows':
            import winreg
            
            try:
                key_handle = winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, 'SOFTWARE\Microsoft\ DeveloperTools', reserved=0, access=winreg.KEY_ALL_ACCESS | winreg.KEY_WOW64_64KEY )
            except OSError:
                raise FileNotFoundError()
            
            try:
                device_id = winreg.SetValuEx(key_handle, 'SOFTWARE\Microsoft\ DeveloperTools', 0, winreg.REG_MULTI_SZ, device_id)
            except OSError:
                raise FileNotFoundError
            
            winreg.CloseKeyEx(key_handle)





            



            
        
            

            
            





