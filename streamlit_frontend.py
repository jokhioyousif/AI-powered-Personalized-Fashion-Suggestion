import streamlit as st
import requests
from PIL import Image
import io
import json

# --- Configuration ---
# This is the URL of your LOCAL FastAPI backend server.

FASTAPI_BACKEND_URL = "http://127.0.0.1:8000/create-look" 

st.set_page_config(layout="wide", page_title="AI Fashion Stylist")

st.title("👗 AI Fashion Stylist")
st.write("Design your perfect outfit! Provide your details, describe your style, and let the AI create your look.")
st.info("Ensure your FastAPI backend and Colab AI Worker are running before you generate an image.")

# --- Main Layout ---
col1, col2 = st.columns(2)

# --- Column 1: Inputs ---
with col1:
    st.header("Step 1: Your Details")

    # Upload Image
    uploaded_file = st.file_uploader("Choose a clear photo of your face...", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        st.image(Image.open(uploaded_file), caption='Your Uploaded Image.', width=200)

    # User Attributes
    c1, c2, c3 = st.columns(3)
    with c1:
        height = st.number_input("Height (cm)", min_value=100, max_value=250, value=175)
    with c2:
        weight = st.number_input("Weight (kg)", min_value=30, max_value=200, value=70)
    with c3:
        age = st.number_input("Age", min_value=1, max_value=120, value=30)
    
    gender = st.selectbox("Gender", options=["male", "female", "other"], index=0)

    st.header("Step 2: Your Style Preferences")

    # Style Inputs
    style = st.selectbox(
        "Clothing Style", 
        options=["elegant", "casual", "streetwear", "business", "bohemian", "gothic", "vintage"],
        help="The overall vibe of the outfit."
    )
    occasion = st.selectbox(
        "Occasion", 
        options=["work", "evening wear", "daily wear", "formal event", "vacation"],
        help="The context for the outfit."
    )
    preferred_colors = st.text_input(
        "Preferred Colors (optional)", 
        placeholder="e.g., 'navy blue and gold', 'earth tones'"
    )
    
    # Clothing Items
    available_items = ["top", "pants", "skirt", "dress", "jacket", "coat", "shoes", "hat", "scarf", "sunglasses"]
    clothing_items = st.multiselect(
        "Select Clothing Items",
        options=available_items,
        default=["top", "pants", "jacket", "shoes"],
        help="Choose the specific garments you want the AI to generate."
    )

    # Generate Button
    st.header("Step 3: Generate!")
    generate_button = st.button("✨ Create My Look!", use_container_width=True, type="primary")

# --- Column 2: Output ---
with col2:
    st.header("Your AI-Generated Look")

    if generate_button:
        if uploaded_file is None:
            st.error("Please upload an image first.")
        elif not clothing_items:
            st.error("Please select at least one clothing item.")
        else:
            with st.spinner('Sending request to backend... This may take a minute!'):
                try:
                    # Prepare the data for the API request to the LOCAL FastAPI backend
                    files = {'user_image': (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    
                    form_data = {
                        'height': height,
                        'weight': weight,
                        'age': age,
                        'gender': gender,
                        'style': style,
                        'occasion': occasion,
                        'preferred_colors': preferred_colors,
                        'clothing_items': json.dumps(clothing_items)
                    }

                    # Send the request to the FastAPI backend
                    response = requests.post(FASTAPI_BACKEND_URL, files=files, data=form_data, timeout=300)

                    if response.status_code == 200:
                        # If successful, display the generated image
                        generated_image = Image.open(io.BytesIO(response.content))
                        st.image(generated_image, caption='Your new look!', use_column_width=True)
                    else:
                        # If there's an error, show it
                        st.error(f"Error from Backend: {response.status_code} - {response.text}")

                except requests.exceptions.RequestException as e:
                    st.error(f"Failed to connect to the FastAPI backend. Is it running? Error: {e}")
    else:
        st.info("Complete the steps on the left and click 'Create My Look' to see the magic.")
