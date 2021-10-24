import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import io
from app_utils import convertToJPG
from deoldify.visualize import *

st.title("Image Processing via streamlit")
st.markdown("""
Upload an image or write down the url if it's online.
Choose on the sidebar the option you want to use if things do not work.
""")
pic = st.file_uploader("image")
st.sidebar.markdown("## Parameters")
st.sidebar.markdown("""
Select the render factor.
Higher values tend to make less errors but also to have less brilliant colors.
""")

render_factor = st.sidebar.slider("render factor",
                                  min_value=2, max_value=40, value=30)

st.sidebar.markdown("""
Do you want to watermark the image?
So it is clear that is colorized using this tool.
""")
watermarked = st.sidebar.checkbox("watermarked", value=True)
if pic is not None:
    # To read file as bytes:
    bytes_data = pic.getvalue()
    #st.write(bytes_data)
    st.image(bytes_data)
    st.markdown("## yo")
    image = Image.open(io.BytesIO(bytes_data))
    st.image(image)
    st.write(type(image))

    image_colorizer = get_image_colorizer(artistic=True)
    try:
        result = image_colorizer.get_transformed_image(
            input_path, render_factor=render_factor, post_process=True, watermarked=True)
    except:
        convertToJPG(input_path)
        result = image_colorizer.get_transformed_image(
            input_path, render_factor=render_factor, post_process=True, watermarked=True)
    finally:
        if result is not None:
            result.save(output_path, quality=95)
            result.close()

    st.write(result)
