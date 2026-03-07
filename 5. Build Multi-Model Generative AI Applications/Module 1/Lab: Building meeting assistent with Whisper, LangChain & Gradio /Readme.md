## Meeting assistent with Whisper, LangChain, and Gradio

### installing virutal env
```bash
pip3 install virtualenv 
virtualenv venv # create a virtual environment venv
source venv/bin/activate # activate my_env
```

### required packages
```bash
# installing required libraries in my_env
pip install transformers==4.35.2 \
torch==2.1.1 \
gradio==5.9.0 \
langchain==0.3.12 \
langchain-community==0.3.12 \
langchain_ibm==0.3.5 \
ibm-watsonx-ai==1.1.16 \
pydantic==2.10.3
```

### ffmpeg
- codec for audio
```bash
sudo apt update
sudo apt install ffmpeg -y
```

