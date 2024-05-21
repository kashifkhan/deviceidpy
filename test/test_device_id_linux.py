import os
import platform
from pathlib import Path
from unittest.mock import patch

import pytest
from deviceid import get_device_id

def test_get_device_id():
    if platform.system() != 'Linux':
        pytest.skip("Linux Only")

    device_id = get_device_id()
    assert device_id
    assert isinstance(device_id, str)
    assert len(device_id) == 36

def test_get_devide_id_confirm_location():
    # create the id if not present already
    if platform.system() != 'Linux':
        pytest.skip("Linux Only")
    device_id = get_device_id()

    # lets get the id ourselves
    file_path = Path(os.getenv('XDG_CACHE_HOME', f"{os.getenv('HOME')}/.cache")).joinpath('Microsoft/DeveloperTools/deviceid')
    
    
    manual_device_id = file_path.read_text(encoding='utf-8')

    assert device_id == manual_device_id

def test_get_device_id_neither_location():
    if platform.system() != 'Linux':
        pytest.skip("Linux Only")
    # lets remove the HOME
    os.environ['XDG_CACHE_HOME'] = ''
    os.environ['HOME'] = ''

    
    device_id = get_device_id()
    assert device_id == ""

def test_get_device_id_permission_error():
    if platform.system() != 'Linux':
        pytest.skip("Linux Only")
    
    device_id = get_device_id()
    
    with patch.object(Path, 'touch', side_effect=PermissionError):
        device_id = get_device_id()
        assert device_id == ""

def test_get_device_id_permission_general_error():
    if platform.system() != 'Linux':
        pytest.skip("Linux Only")
    
    device_id = get_device_id()
    
    with patch.object(Path, 'touch', side_effect=Exception):
        device_id = get_device_id()
        assert device_id == ""