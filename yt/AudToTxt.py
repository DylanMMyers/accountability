from deepgram import Deepgram
import asyncio, json, os

DEEPGRAM_API_KEY = 'd39e79e5d1cecef3561049b576e5135cc0b49234' 
FILENAME = ".\\yt\\Audout\\Elon Musk at Trump rally in Butler, PA： FULL SPEECH.mp3"
PARAMS = {'punctuate': True, 'tier': 'enhanced', 'detect_entities' : True}

async def main(): 
    deepgram = Deepgram(DEEPGRAM_API_KEY)
    print("Currently transcribing ", FILENAME) 
    
    with open(FILENAME, 'rb') as audio: 
        source = {'buffer': audio, 'mimetype': 'audio/mp3'} 
        response = await deepgram.transcription.prerecorded(source, PARAMS) 
        json_object = json.dumps(response, indent=4) 
        
        base_filename = os.path.splitext(FILENAME)[0]
        transcription_file = base_filename + '.json'
        
        with open(transcription_file, "w") as outfile: 
            outfile.write(json_object) 
            print("Transcription saved to:", transcription_file)

asyncio.run(main())
