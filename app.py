from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Load environment variables from .env file in project root directory
load_dotenv()

# Configure Google API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini Pro Vision
model = genai.GenerativeModel('gemini-pro-vision')

def get_gemini_response(uploaded_image, prompt):
  # Open the uploaded image using PIL
  image = Image.open(uploaded_image)

  # Generate response using Gemini Pro Vision model
  try:
      response = model.generate_content([image, prompt])
      return response.text
  except ValueError as e:
      # Handle the error when no text is extracted
      return f"Error: No text could be extracted from the image. \nReason: {e}"

# Initialization of Streamlit
def main():
  st.title("MultiLanguage Invoice Extractor")

  # Add a file uploader widget for the user to upload an image
  st.write("Upload an image:")
  uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

  # Check if an image has been uploaded
  if uploaded_image is not None:
    # Display the uploaded image
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Add a text input for the user to enter a prompt
    prompt = st.text_input("Enter a prompt:", "")

    # Add a button to generate response
    if st.button("Generate Response"):
      # Get the response from Gemini Pro Vision model
      response = get_gemini_response(uploaded_image, prompt)
      st.write("Generated Response:", response)

if __name__ == "__main__":
  main()