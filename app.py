import whisper
import gradio as gr
import time
from deep_translator import GoogleTranslator

# Initialize the model
model = whisper.load_model("base")

device = model.device

# Mapping of full language names to language codes
language_mapping = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Chinese (Simplified)": "zh-cn",
    "Japanese": "ja",
    "Urdu": "ur"
}

def transcribe(audio, target_language):
    # Load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio(audio)
    audio = whisper.pad_or_trim(audio)

    # Make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(device)
    # Decode the audio
    options = whisper.DecodingOptions()
    result = whisper.decode(model, mel, options)
    transcribed_text = result.text

    # Translate the transcribed text
    target_language_code = language_mapping[target_language]
    translator = GoogleTranslator(source='auto', target=target_language_code)
    translated_text = translator.translate(transcribed_text)
    
    return transcribed_text, translated_text

# Gradio Interface
gr.Interface(
    title='Translation and Transcription System',
    fn=transcribe,
    inputs=[gr.Audio(type="filepath"), gr.Dropdown(choices=list(language_mapping.keys()), label="Target Language")],
    outputs=[gr.Textbox(label="Transcribed Text"), gr.Textbox(label="Translated Text")],
    live=True
).launch()