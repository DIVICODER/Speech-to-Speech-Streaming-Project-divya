# Speech-to-Speech-Streaming-Project-divya
🚀 Translate and sync speech in videos with real-time streaming support!

This project extracts speech from videos, translates it, generates new audio, and synchronizes it with the video while preserving the original timing.

📌 Features
✅ Extracts full audio from video
✅ Transcribes speech using OpenAI Whisper
✅ Translates using Google Translate API
✅ Generates natural speech using gTTS (Google Text-to-Speech)
✅ Synchronizes translated speech to match video timing
✅ Supports live streaming & batch processing
✅ Works with MP4, AVI, MOV, MKV

🛠 Installation
1️⃣ Clone the Repository
bash
Copy
Edit
git clone https://github.com/your-username/Speech-to-Speech-Streaming-Project.git
cd Speech-to-Speech-Streaming-Project
2️⃣ Install Dependencies
Ensure you have Python 3.8+, then install required libraries:

bash
Copy
Edit
pip install -r requirements.txt
3️⃣ Install FFmpeg (Required for Audio Processing)
🔹 Windows
Download FFmpeg from here.

Extract it and add the bin folder to your system PATH.

🔹 Mac/Linux
bash
Copy
Edit
sudo apt update && sudo apt install ffmpeg -y   # Ubuntu/Debian  
brew install ffmpeg  # macOS (using Homebrew)
🚀 How to Use
1️⃣ Run the Application
bash
Copy
Edit
streamlit run app.py
This will open a web UI in your browser.

2️⃣ Upload a Video
Supports formats: MP4, AVI, MOV, MKV

The app will extract audio and display the original video.

3️⃣ Select a Target Language
Choose a language from the dropdown menu.

4️⃣ Click "Convert Video"
The app will extract, transcribe, translate, generate speech, and sync the new audio with the video.

A download button will appear when processing is complete.

⚙️ How it Works
1️⃣ Extract Audio
Uses ffmpeg to extract the original audio track from the video.

2️⃣ Transcribe Audio
Uses Whisper AI to convert speech into text.

3️⃣ Translate Text
Uses Google Translate API to translate the text.

4️⃣ Convert to Speech
Uses gTTS (Google Text-to-Speech) to generate natural-sounding speech.

5️⃣ Synchronize Audio
Adjusts the speed of the translated audio to match the original video duration:

bash
Copy
Edit
ffmpeg -i audio.mp3 -filter:a "atempo=<speed_factor>" adjusted_audio.mp3
Merges the new speech with the original video without losing quality.

🖥️ Example Usage
python
Copy
Edit
python app.py
Upload a video, select a language, and wait for the translated video with synchronized audio.

📌 Dependencies
Python 3.8+

Streamlit (pip install streamlit)

Whisper AI (pip install openai-whisper)

gTTS (pip install gtts)

Deep Translator (pip install deep-translator)

FFmpeg (apt install ffmpeg or brew install ffmpeg)

🛠 Troubleshooting
Issue	Solution
ffmpeg not found	Install FFmpeg and add it to PATH.
Whisper model download error	Try whisper.load_model("tiny") instead of "base".
Translation failed	Check your internet connection (Google Translate API requires internet).
Audio not in sync	Ensure FFmpeg is correctly installed and the atempo filter is applied.
📜 License
This project is open-source under the MIT License.

🎬 Enjoy real-time speech-to-speech video translation! 🚀✨
