import os
import streamlit.components.v1 as components
from typing import List, Optional, Union

__all__ = ['sync', 'settings']

_RELEASE = True

if not _RELEASE:
    _component_func_sync = components.declare_component(
        "sync",
        url="http://localhost:3001",
    )
    _component_func_settings = components.declare_component(
        "settings",
        url="http://localhost:3002",
    )
    _component_func_hbjson = components.declare_component(
        "settings",
        url="http://localhost:3003",
    )    
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "sync")
    _component_func_sync = components.declare_component("sync", path=build_dir)
    build_dir = os.path.join(parent_dir, "settings")
    _component_func_settings = components.declare_component("settings", path=build_dir)
    build_dir = os.path.join(parent_dir, "hbjson")
    _component_func_hbjson = components.declare_component("get_hbjson", path=build_dir) 

def sync(
    defaultChecked: bool=False,
    delay: Optional[int]=500,
    key: str =None) -> str:
    """Create a sync token generator.

    Parameters
    ----------
    defaultChecked: bool
        Set if it has to be checked by default.
    delay: int
        Delay of the syncronization in milliseconds.
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.
    Returns
    -------
    str
        Sync token to connect to component to enable the syncronization.
    """
    component_value = _component_func_sync(
        defaultChecked=defaultChecked,
        delay=delay,
        key=key, 
        default=None)
    
    return component_value


def settings(
    data: dict,
    defaultChecked: bool=False,
    delay: Optional[int]=500,
    key: str =None) -> str:
    """Send/get settings to/from a CAD software.

    Parameters
    ----------
    data: dict or string. Dict to SET settings. String to GET settings.

        String MUST start with 'SETTINGS' keyword. You can use 'special.sync' output
        to generate a token when you change document info of the host software automatically.

        Dict MUST have following schema:
        data = {
                'earth_anchor': {
                    'lat': 41.2324,
                    'lon': 12.3234
                },
                units: 1,
                layers: ['Streamlit', 'JS', 'Python']
            }
        
        - Where Units mapping:
            - Millimeter = 2
            - Centimeter = 3
            - Meters = 4
            - Inches = 8
            - Feet = 9
        - layers array contains layers to create

    defaultChecked: bool
        Set if it has to be checked by default.
    delay: int
        Delay of the syncronization in milliseconds.
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.
    
    return:
        if String as 'data' it returns JSON settings inside streamlit
        because it is in GET mode. Otherwise nothing.
    """
    component_value = _component_func_settings(
        data=data,
        defaultChecked=defaultChecked,
        delay=delay,
        key=key, 
        default=None)
    
    units = {
        2: 'Millimeter',
        3: 'Centimeter',
        4: 'Meters',
        8: 'Inches',
        9: 'Feet'
    }

    if component_value:
        out_unit = component_value.get('units')
        if not out_unit:
            return component_value
        
        component_value = { **component_value, 
            **{'units': units.get(out_unit)} }

    return component_value


def get_hbjson(
    delay: Optional[int]=500,
    key: str =None) -> str:
    """Create a sync token generator.

    Parameters
    ----------
    delay: int
        Delay of the syncronization in milliseconds.
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.
    Returns
    -------
    str
        Sync token to connect to component to enable the syncronization.
    """
    component_value = _component_func_hbjson(
        delay=delay,
        key=key, 
        default=None)
    
    return component_value


if not _RELEASE:
    import streamlit as st
    # st.subheader("Sync Token in action")

    # # just one component like this
    # sync_token = sync(defaultChecked=True, 
    #     key='my-secret-key')
    # st.write(sync_token)
    
    # sync_token_2 = sync(defaultChecked=True, 
    #     key='my-secret-key-2')
    # st.write(sync_token_2)


    # data = {
    #         'earth_anchor': {
    #             'lat': 41.2324,
    #             'lon': 12.3234
    #         },
    #         'units': 2,
    #         'layers': ['Streamlit', 'JS']
    #     }

    # test = settings(
    #     data=data,
    #     defaultChecked=True)
    # st.write(test)

    my_model = get_hbjson(key='my-hbjson-model')
    st.write(my_model)