import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import io
from ISR.models import RDN

st.title("Super Resolution Playground")
st.markdown("""
This is an experiment to use streamlit for some low power ai application.
The code is available [here](https://github.com/freerafiki/super_res_st).
""")

st.header("Usage")
st.markdown(
    """
Just upload a small image (less than 500x500 pixels, otherwise the server starts to complain).
It will upscale it (to the double of the resolution when possible).
Images can be JPEG, PNG or BMP.
Nothing special, just an experiment to see the workflow.
""")

st.header("Credits")
st.markdown("""
- It uses the ISR [image super resolution](https://github.com/idealo/image-super-resolution) module
- It is inspired from the [opyrator example](https://github.com/ml-tooling/opyrator#image-super-resolution)
- It is built with [streamlit](https://streamlit.io/)
""")

pic = st.file_uploader("image")
# st.sidebar.markdown("## Parameters")
# st.sidebar.markdown("""
# Select the render factor.
# Higher values tend to make less errors but also to have less brilliant colors.
# """)
#
# render_factor = st.sidebar.slider("render factor",
#                                   min_value=2, max_value=40, value=30)

if pic is not None:
    st.write("working on it.. it may take a while..")
    # To read file as bytes:
    bytes_data = pic.getvalue()
    image = Image.open(io.BytesIO(bytes_data))
    lr_img = np.array(image)
    if lr_img.shape[0]*lr_img.shape[1] > 250000:
        st.write(
            f"the image is a bit too big ({lr_img.shape[0]}x{lr_img.shape[1]} pixels).")
        st.write(
            "Use an image smaller than 500x500, otherwise it's too much for this small server.")
        st.write("Just upload a new one and it will start again.")
    else:
        rdn = RDN(weights='psnr-small')
        sr_img = rdn.predict(lr_img)
        result = Image.fromarray(sr_img)
        st.write("### here you are")
        col1, col2 = st.columns(2)
        with col1:
            st.write("input image")
            st.image(image)
        with col2:
            st.write("upscaled image")
            st.image(result)
        st.write(
            "To save the image, just right-click on the upscaled image and choose 'Save as'")
