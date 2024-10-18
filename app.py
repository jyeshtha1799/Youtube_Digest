import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled

# Streamlit Page Configuration: Place this line at the very top
st.set_page_config(page_title="TubeDigest", page_icon="🎬", layout="wide")

# Load environment variables
load_dotenv()


