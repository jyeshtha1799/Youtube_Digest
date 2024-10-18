import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled

# Streamlit Page Configuration: Place this line at the very top
st.set_page_config(page_title="TubeDigest", page_icon="🎬", layout="wide")

# Load environment variables
load_dotenv()


# Use environment variable
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("GOOGLE_API_KEY not found. Please set the API key in your .env file or pass it directly.")

# Configure Google Generative AI
genai.configure(api_key=api_key)

# Define the prompt
prompt = """You are a YouTube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 words. Please provide the summary of the text given here:  """