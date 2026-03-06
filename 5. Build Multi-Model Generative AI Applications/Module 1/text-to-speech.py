import torch
import torchaudio
from transformers import VitsModel, AutoTokenizer

def generate_speech(text):
    # Load pre-trained model and tokenizer
    model = VitsModel.from_pretrained("facebook/mms-tts-eng")
    tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-eng")   

    # Tokenize input text
    inputs = tokenizer(text, return_tensors="pt")which 

    # Generate speech
    with torch.no_grad():
        output = model.generate(**inputs).waveform # No Speaker_id

    return output

if __name__ == "__main__":
    text = "Hello, this is a test of the VITS text-to-speech model."
    speech = generate_speech(text)

    # Save the generated speech to a file
    torchaudio.save("output.wav", speech.cpu(), sample_rate=22050)