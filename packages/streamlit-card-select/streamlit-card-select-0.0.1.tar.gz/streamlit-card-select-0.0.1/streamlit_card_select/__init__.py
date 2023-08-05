import os
from typing import List
import streamlit.components.v1 as components


__version__ = "0.0.1"

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
# (This is, of course, optional - there are innumerable ways to manage your
# release process.)
_RELEASE = False

# Declare a Streamlit component. `declare_component` returns a function
# that is used to create instances of the component. We're naming this
# function "_component_func", with an underscore prefix, because we don't want
# to expose it directly to users. Instead, we will create a custom wrapper
# function, below, that will serve as our component's public API.

# It's worth noting that this call to `declare_component` is the
# *only thing* you need to do to create the binding between Streamlit and
# your component frontend. Everything else we do in this file is simply a
# best practice.

if not _RELEASE:
    _component_func = components.declare_component(
        # We give the component a simple, descriptive name ("my_component"
        # does not fit this bill, so please choose something better for your
        # own component :)
        "streamlit_card_select",
        # Pass `url` here to tell Streamlit that the component will be served
        # by the local dev server that you run via `npm run start`.
        # (This is useful while your component is in development.)
        url="http://localhost:3001",
    )
else:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("streamlit_card_select", path=build_dir)


# Create a wrapper function for the component. This is an optional
# best practice - we could simply expose the component function returned by
# `declare_component` and call it done. The wrapper allows us to customize
# our component's API: we can pre-process its input args, post-process its
# output value, and add a docstring for users.
def card_select(options: List[dict], default: str = None,  key=None):
    """Create a new instance of "streamlit_card_select".

    Parameters
    ----------
    options : List[dict]
        A list of dictionaries for the items to show as cards. Each dict has
        to contain a key: 'title' and optionally a 'description' and 'image'.
    default : str
        The default option to mark active if none was clicked so far
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.

    Returns
    -------
    int
        The index of the selected card in the passed options list.

    """
    # check the type of options
    if all([isinstance(_, dict) for _ in options]):
        _opt = options
    else:
        _opt = []
        for o in options:
            if isinstance(o, dict):
                _opt.append(o)
            elif isinstance(o, str):
                d = {'option': o}
                if 'http' in o:
                    d['image'] = o
                else:
                    d['title'] = o
                _opt.append(d)
            else:
                raise AttributeError('options must be a list of dicts or strings')
            
    # Call through to our private component function. Arguments we pass here
    # will be sent to the frontend, where they'll be available in an "args"
    # dictionary.
    #
    # "default" is a special argument that specifies the initial return
    # value of the component before the user has interacted with it.
    component_value = _component_func(options=_opt, key=key)

    if component_value is None:
        compontent_value = default

    # We could modify the value returned from the component if we wanted.
    # There's no need to do this in our simple example - but it's an option.
    return component_value


# Add some test code to play with the component while it's in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run my_component/__init__.py`
if not _RELEASE:
    import streamlit as st

    st.subheader("Card Grid")

    # create a list of options
    options = [
        dict(option="one", image="https://picsum.photos/200/300"),
        dict(option="two", title="Card 2", description="This is card 2", image="https://picsum.photos/200/300"),
        dict(option="three", title="Card 3", image="https://picsum.photos/200/300"),
        dict(option="four", title="Card 4", description="This is card 4"),
    ]

    # Create an instance of our component with a constant `name` arg, and
    # print its output value.
    selected = card_select(options=options)
    st.write(f"Selected: {selected}")
