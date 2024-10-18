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

# Define the function to extract transcript details
def extract_transcript_details(youtube_video_url, language_code="en"):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id, languages=[language_code])
        transcript = " ".join([i["text"] for i in transcript_text])
        return transcript
    except NoTranscriptFound:
        st.error(f"No transcripts found in the requested language: {language_code}. Please try a different language.")
        return None
    except TranscriptsDisabled:
        st.error("Transcripts are disabled for this video.")
        return None
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

# Updated function to handle various response structures
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    try:
        response = model.generate_content(prompt + transcript_text)
        print("Full API Response:", response)
        if response and hasattr(response, "text"):
            return response.text
        elif response and hasattr(response, "candidates") and response.candidates:
            candidate = response.candidates[0]
            if hasattr(candidate, "text"):
                return candidate.text
            elif hasattr(candidate, "finish_message"):
                return candidate.finish_message  
            else:
                return "The response did not contain a valid summary. Try with another video."
        else:
            return "The response did not return a valid summary. Try with another video."
    except AttributeError as e:
        st.error(f"An attribute error occurred while processing the response: {e}")
        return "Error processing the summary due to an unexpected response structure."
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return "Error generating summary. Please try again."


# Updated CSS for Video Insights to be black
st.markdown(
    """
    <style>
    .main {
        display: flex;
        justify-content: center;  /* Center horizontally */
        align-items: center;  /* Center vertically */
        height: 100vh;  /* Full height */
        background-color: #C1E1C1;  /* Updated background color */
    }
    /* Targeting the main Streamlit container */
    .stApp {
        background-color: #C1E1C1;  /* Ensure the background is applied */
    }
    h1, h2, h3 {
        text-align: center; /* Center-align all headers */
        margin-bottom: 1.5rem;
        color: #C70039;  /* Dark red for headers */
    }
    .stTextInput > div > div > input {
        color: #33333;
        background-color: #FFD700;  /* Yellow background color for the search bar */
        border: 2px solid #9478FA;
        width: 100%;  /* Full width to avoid black side patches */
        padding: 0.5rem; /* Add padding for better alignment */
        margin: 0 auto; /* Center the search bar */
        display: block;
    }
    .stButton>button {
        background-color: #C70039;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: all 0.3s ease;
        margin: 10px auto;  /* Center the button */
        display: block;     /* Block display for centering */
    }
    .stButton>button:hover {
        background-color: #7B5FD9;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    body {
        background-color: #C1E1C1;  /* Updated background color for the page */
    }
    /* Setting Video Insights text and its contents to black */
    .video-insights h2, .video-insights p, .video-insights ul, .video-insights li {
        color: black;  /* Black color for video insights section */
    }
    .footer {
        text-align: center;
        margin-top: 2rem;
        padding: 1rem;
        color: #333333;  /* Dark gray footer text */
    }
    </style>
    """,
    unsafe_allow_html=True
)
