import pytest
import bpy
from bpy import context

import blender
from blender.default_cfg import *
from blender.graph import *
from blender.util import *

TEST_DATA = [
    [1.34,2,5,10,20,2000,20_000],
    [5,6,4,100,1,15,2],
    [2,3,4,5,7,8000,10]
    ]

# DATA = TEST_DATA

@pytest.fixture
def data():
    return TEST_DATA

@pytest.fixture(scope="session", autouse=True)
def setup_cfg(request):
    # prepare something ahead of all tests
    blender.default_cfg.DATA = TEST_DATA


def test_cfg():
    assert TEST_DATA
    assert blender.default_cfg.DATA == TEST_DATA
    assert blender.default_cfg.COLOR_PALETTE[-1] == "73609c"
    assert blender.default_cfg.DATA[0][0] == 1.34
    assert blender.default_cfg.DATA[0][0] != 1

def test_util_add_and_delete():
    bpy.ops.mesh.primitive_cube_add(size = 1)
    context.active_object.name = f"cube_test"
    assert len(bpy.data.objects) == 1
    delete_all()
    assert len(bpy.data.objects) == 0

def test_util_error():
    with pytest.raises(ZeroDivisionError) as excinfo:
        force_div_by_zero_error()
    # assert str(excinfo.value) == 'division by zero'

def test_util_value_error_match():
    # with pytest.raises(ValueError, match=r'must be \d+$'):
    with pytest.raises(ValueError, match=r'math domain'):
        force_value_error()

def test_util_value_error_match_custom_message():
    with pytest.raises(CustomError) as excinfo:
        force_value_error_custom(-2)
        assert excinfo.value.message == 'everything is broken'

def test_data_fix(data):
    assert data[0][0] == 1.34
