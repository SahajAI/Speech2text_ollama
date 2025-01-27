# Make sure that you have Ollama installed in your PC to use this
# To download Vosk Speech Recognition models to use locally you can go to : https://alphacephei.com/vosk/models
# Reference Video : https://www.youtube.com/watch?v=cMDHTXobwxk&t=749s
# Ollama Tutorial Reference Video : https://www.youtube.com/watch?v=UtSSMs6ObqY

Standard Commands :

conda create -p venv python=3.12 -y
conda activate venv/
pip install -r requirements.txt
python voice_ollama.py

