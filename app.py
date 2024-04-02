import streamlit as st
import nltk
from gtts import gTTS
import os
import tempfile

# Download necessary NLTK resources
nltk.download('punkt')

def text_to_speech(text, language='en'):
    """Converts text to speech and offers download functionality."""

    # Tokenize the text into sentences
    sentences = nltk.sent_tokenize(text)

    # Create a temporary directory for audio files
    with tempfile.TemporaryDirectory() as tmpdir:
        audio_files = []

        # Convert each sentence to speech and save to temporary files
        for idx, sentence in enumerate(sentences):
            tts = gTTS(text=sentence, lang=language, slow=False)
            filename = f"output_{idx}.mp3"
            filepath = os.path.join(tmpdir, filename)
            tts.save(filepath)
            audio_files.append(filepath)

        # Concatenate the audio files (optional for single sentence input)
        if len(sentences) > 1:
            output_filename = "final_output.mp3"
            output_filepath = os.path.join(tmpdir, output_filename)
            os.system(f"ffmpeg -i \"concat:{'|'.join(audio_files)}\" {output_filepath}")
            audio_to_display = output_filepath
        else:
            audio_to_display = audio_files[0]  # Use the first file for single sentence

        # Display the audio player
        st.audio(audio_to_display, format='audio/mp3')

        # Download the audio file using Streamlit download_button
        with open(audio_to_display, "rb") as f:
            st.download_button(label="Download Audio", data=f, file_name="speech.mp3")

        # Clean up temporary audio files (not strictly necessary in this case)
        for file in audio_files:
            os.remove(file)

    st.success("Text-to-speech conversion complete.")

def main():
    st.title("Text to Speech Converter")

    input_text = st.text_area("Enter text to convert to speech")

    if st.button("Convert to Speech"):
        if input_text:
            text_to_speech(input_text)
        else:
            st.warning("Please enter some text to convert.")

    # CSS for background animation
    st.markdown(
        """
        <style>
        .animated-background {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            
        }

        @keyframes move-ai {
            0% {
                transform: translateY(0) translateX(-100%);
            }
            50% {
                transform: translateY(0) translateX(100%);
            }
            100% {
                transform: translateY(0) translateX(-100%);
            }
        }

        .ai {
            position: absolute;
            top: 50%;
            left: 50%;
            width: 200px;
            height: 200px;
            background-image: url('https://t4.ftcdn.net/jpg/02/60/29/17/360_F_260291791_hIIDgqNrjgr17ykPb5oSKaNPREZpm8BJ.jpg');
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
            animation: move-ai 35s linear infinite;
            transform: translate(-50%, -50%);
            border-radius: 50%;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
        }
        
        </style>
        <div class="animated-background">
            <div class="ai"></div>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
