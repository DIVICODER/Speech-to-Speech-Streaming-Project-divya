import os
import streamlit as st
import tempfile
import subprocess
from pathlib import Path
import whisper
from deep_translator import GoogleTranslator
from gtts import gTTS

# Load Whisper model
model = whisper.load_model("base")

# Function to extract audio from video
def extract_audio(video_path, output_audio_path):
    command = f'ffmpeg -i "{video_path}" -q:a 0 -map a "{output_audio_path}" -y'
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if result.returncode != 0:
        st.error("❌ Error extracting audio.")
        return None
    return output_audio_path

# Transcribe full audio
def transcribe_audio(audio_path):
    try:
        result = model.transcribe(audio_path)
        return result["text"]
    except Exception as e:
        st.error(f"❌ Whisper transcription error: {e}")
        return None

# Translate transcribed text
def translate_text(text, target_language):
    try:
        translated = GoogleTranslator(source="auto", target=target_language).translate(text)
        return translated
    except Exception as e:
        return f"❌ Translation Error: {e}"

# Generate speech from translated text
def generate_speech(text, output_audio_path, language):
    try:
        tts = gTTS(text=text, lang=language)
        tts.save(output_audio_path)
        return output_audio_path
    except Exception as e:
        st.error(f"❌ Speech synthesis error: {e}")
        return None

# Function to sync translated audio to video with speed correction
def sync_audio_to_video(video_path, audio_path, output_path):
    try:
        # Get video and audio durations
        video_duration = float(subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", video_path],
            capture_output=True, text=True, check=True
        ).stdout.strip())

        audio_duration = float(subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", audio_path],
            capture_output=True, text=True, check=True
        ).stdout.strip())

        # Calculate speed factor
        speed_factor = audio_duration / video_duration
        adjusted_audio_path = os.path.splitext(audio_path)[0] + "_adjusted.mp3"

        # Adjust the audio speed precisely
        subprocess.run(
            ["ffmpeg", "-i", audio_path, "-filter:a", f"atempo={speed_factor}", "-vn", adjusted_audio_path, "-y"],
            check=True, capture_output=True
        )

        # Merge the adjusted audio with the original video
        subprocess.run(
            ["ffmpeg", "-i", video_path, "-i", adjusted_audio_path, "-c:v", "copy", "-map", "0:v:0", "-map", "1:a:0",
             "-shortest", output_path, "-y"],
            check=True, capture_output=True
        )

        return output_path

    except subprocess.CalledProcessError as e:
        st.error(f"❌ FFmpeg Error: {e}")
        return None
    except Exception as e:
        st.error(f"❌ Unexpected Error: {e}")
        return None

# Streamlit UI
st.set_page_config(page_title="AI Video Translator", page_icon="🎬", layout="wide")
st.title("🎬 AI Video Translator with Accurate Sync")

uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov", "mkv"])
if uploaded_file:
    temp_dir = tempfile.TemporaryDirectory()
    temp_path = Path(temp_dir.name)
    
    input_video_path = temp_path / "input_video.mp4"
    with open(input_video_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("✅ Video uploaded successfully!")
    st.video(str(input_video_path))

    # Select Language
    LANGUAGE_OPTIONS = {"English": "en", "Spanish": "es", "French": "fr", "German": "de", "Italian": "it", "Tamil": "ta"}
    target_language = st.selectbox("Choose target language:", list(LANGUAGE_OPTIONS.keys()))

    if st.button("Convert Video"):
        progress_bar = st.progress(0)
        status_text = st.empty()

        # Step 1: Extract Audio
        status_text.text("Step 1/5: Extracting audio from video...")
        extracted_audio_path = temp_path / "extracted_audio.wav"
        extracted_audio = extract_audio(str(input_video_path), str(extracted_audio_path))
        if not extracted_audio:
            st.error("Failed to extract audio.")
            temp_dir.cleanup()
            st.stop()
        progress_bar.progress(20)

        # Step 2: Transcribe Audio
        status_text.text("Step 2/5: Transcribing full audio...")
        transcript = transcribe_audio(str(extracted_audio))
        if not transcript:
            st.error("Failed to transcribe audio.")
            temp_dir.cleanup()
            st.stop()
        progress_bar.progress(40)

        st.text_area("Original Transcript", transcript, height=100)

        # Step 3: Translate Text
        status_text.text(f"Step 3/5: Translating text to {target_language}...")
        translated_text = translate_text(transcript, LANGUAGE_OPTIONS[target_language])
        if not translated_text:
            st.error("Translation failed.")
            temp_dir.cleanup()
            st.stop()
        progress_bar.progress(60)

        st.text_area(f"Translated Text ({target_language})", translated_text, height=100)

        # Step 4: Generate Translated Speech
        status_text.text("Step 4/5: Generating translated speech...")
        cloned_audio_path = temp_path / f"translated_audio_{target_language.lower()}.mp3"
        cloned_audio = generate_speech(translated_text, str(cloned_audio_path), LANGUAGE_OPTIONS[target_language])
        if not cloned_audio:
            st.error("Failed to generate translated speech.")
            temp_dir.cleanup()
            st.stop()
        progress_bar.progress(80)

        # Step 5: Sync Audio to Video
        status_text.text("Step 5/5: Synchronizing translated audio with video...")
        output_video_path = temp_path / f"output_video_{target_language.lower()}.mp4"
        final_video = sync_audio_to_video(str(input_video_path), str(cloned_audio), str(output_video_path))
        if not final_video:
            st.error("Failed to sync audio with video.")
            temp_dir.cleanup()
            st.stop()
        progress_bar.progress(100)

        st.success("✅ Conversion complete! The translated audio is now correctly synced.")
        st.subheader("Converted Video")
        st.video(str(output_video_path))

        with open(output_video_path, "rb") as file:
            st.download_button("Download Final Video", file, file_name=f"translated_video_{target_language.lower()}.mp4", mime="video/mp4")

    # Cleanup temporary directory
    temp_dir.cleanup()
