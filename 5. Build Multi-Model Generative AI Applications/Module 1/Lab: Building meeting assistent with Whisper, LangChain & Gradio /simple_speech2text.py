import requests

def download_audio(url, file_path):
    # Send a GET request to the URL to download the file
    response = requests.get(url)
    
    # Define the local file path where the audio file will be saved
    audio_file_path = file_path
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
    	# If successful, write the content to the specified local file path
    	with open(audio_file_path, "wb") as file:
    		file.write(response.content)
    		print("File downloaded successfully")
    else:
    	# If the request failed, print an error message
    	print("Failed to download the file")

import torch
from transformers import pipeline

def speech2text(audio_file):
    # Initialize the speech-to-text pipeline from Hugging Face Transformers
    # This uses the "openai/whisper-tiny.en" model for automatic speech recognition (ASR)
    # The `chunk_length_s` parameter specifies the chunk length in seconds for processing
    pipe = pipeline(
      "automatic-speech-recognition",
      model="openai/whisper-tiny.en",
      chunk_length_s=30,
    )
    
    # Perform speech recognition on the audio file
    # The `batch_size=8` parameter indicates how many chunks are processed at a time
    # The result is stored in `prediction` with the key "text" containing the transcribed text
    prediction = pipe(audio_file, batch_size=8)["text"]
    
    # Print the transcribed text to the console
    return prediction


if __name__ == "__main__":
    # URL of the audio file to be downloaded
    url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/hTqGqoC-LrW6S79HjuJUkg/trimmed-02.wav"
    
    # file-path to save the sample audio file
    file_path = "sample-meeting.wav"
    
    # to download the audio file for conversion
    download_audio(url, file_path)

    # convert the audio file to text
    text = speech2text(file_path)
    print(text)