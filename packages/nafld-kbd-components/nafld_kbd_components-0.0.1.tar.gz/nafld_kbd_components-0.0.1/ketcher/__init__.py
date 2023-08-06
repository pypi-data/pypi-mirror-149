import os
import streamlit.components.v1 as components

_RELEASE = True
# _RELEASE = False

component_name = "ketcher"

if not _RELEASE:
    _component_func = components.declare_component(
        component_name,
        url="http://localhost:3000",  # dev server port
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "build")
    _component_func = components.declare_component(component_name, path=build_dir)


def ketcher(name=component_name, key=None):
    component_value = _component_func(name=name, key=key, default=0)
    return component_value
