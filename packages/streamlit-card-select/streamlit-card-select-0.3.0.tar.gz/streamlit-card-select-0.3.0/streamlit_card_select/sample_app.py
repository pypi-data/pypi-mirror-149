import streamlit as st


def app():
    from streamlit_card_select.component import card_select
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
    selected = card_select(options=options, default="four", imgHeight=200)
    st.write(f"Selected: {selected}")

    # slider data
    st.markdown('### Slider options:')
    st.json(options)


if __name__ == "__main__":
    app()
