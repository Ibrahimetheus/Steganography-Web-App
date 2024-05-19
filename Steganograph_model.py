import streamlit as st
from PIL import Image
from stegano import lsb
import io

# Function to encode a message into an image
def encode_message(image, message):
    # Convert the uploaded image to a format Stegano can handle
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    # Hide the message in the image
    secret_image = lsb.hide(io.BytesIO(img_byte_arr), message)
    return secret_image

# Function to decode a message from an image
def decode_message(image):
    try:
        hidden_message = lsb.reveal(image)
        if hidden_message is None:
            raise ValueError("No hidden message found")
        return hidden_message
    except Exception as e:
        return str(e)

# Streamlit app layout
st.title("Steganography Web App")

# Important message section with privacy icon
st.sidebar.markdown("""
    <div style="display:flex; align-items:center;">
        <img src="https://emojicdn.elk.sh/🔒" width="25" height="25" style="margin-right: 10px;">
        <span style="font-size: 16px; font-weight: bold;">
                    </span> This app does not store any information of your interactions, including uploaded images or messages.
    </div>
""", unsafe_allow_html=True)


# Information section
with st.expander("What is Steganography and How to Use This App"):
    st.markdown("""
    **Steganography** is the practice of hiding secret information within another non-secret medium. 
    The term is derived from the Greek words **steganos**, meaning "covered," and **graphein**, meaning "writing." 
    In the context of digital images, steganography typically involves hiding a message within the pixel data of an image.
    
    **How to Use This App:**
    1. **Encode a Message:**
        - Upload an image using the "Choose an image..." button under the "Encode a Message" section.
        - Enter the secret message you want to hide in the text area.
        - Click the "Encode" button. The app will embed the message into the image.
        - Download the encoded image using the "Download Encoded Image" button.
    2. **Decode a Message:**
        - Upload the previously encoded image using the "Choose the encoded image..." button under the "Decode a Message" section.
        - Click the "Decode" button. The app will reveal the hidden message if there is one.
    3. **Reset the App:**
        - If you want to start over, click the "Reset" button to clear all inputs and outputs and reset the app.
    """)

st.header("Hide a secret message inside an image")

# Encoding section
st.subheader("Encode a Message")
uploaded_image = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"], key="encode")

if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    st.write("")

    # Message input for encoding
    message = st.text_area("Enter the message you want to hide")
    if st.button("Encode"):
        if message:
            secret_image = encode_message(image, message)
            
            # Save the secret image to a BytesIO object
            buf = io.BytesIO()
            secret_image.save(buf, format='PNG')
            byte_im = buf.getvalue()

            st.image(secret_image, caption='Secret Image', use_column_width=True)
            st.success("Message encoded successfully")
            st.download_button(label="Download Encoded Image", data=byte_im, file_name="secret_image.png", mime="image/png")
        else:
            st.error("Please enter a message to encode")

# Decoding section
st.subheader("Decode a Message")
uploaded_encoded_image = st.file_uploader("Choose the encoded image...", type=["png", "jpg", "jpeg"], key="decode")

if uploaded_encoded_image is not None:
    encoded_image = Image.open(uploaded_encoded_image)
    st.image(encoded_image, caption='Encoded Image', use_column_width=True)
    st.write("")

    if st.button("Decode"):
        hidden_message = decode_message(uploaded_encoded_image)
        if hidden_message and "No hidden message found" not in hidden_message:
            st.success(f"Hidden message: {hidden_message}")
        else:
            st.error("No hidden message found or image is invalid")

# Add a reset button to redo the process
if st.button("Reset"):
    st.experimental_rerun()
