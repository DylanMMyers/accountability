import yt_dlp
from deepgram import Deepgram
import asyncio, os

def returnTranscriptFilePathFromURL(url):
    ################ DOWNLOAD VIDEO ##################
    url = "https://www.youtube.com/watch?v=NP96mMBxI2E&ab_channel=C-SPAN"

    ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': './audOut/%(title)s.mp3'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        videoTitle = info_dict.get('title', None)
        ydl.download(url)

    VIDEO_FILE = ".\\audOut\\" + videoTitle + ".mp3"

    ########## CONVERTING VIDEO TO TRANSCRIPT (JSON) ##################

    DEEPGRAM_API_KEY = 'd39e79e5d1cecef3561049b576e5135cc0b49234' 
    PARAMS = {'punctuate': True, 'tier': 'enhanced', 'detect_entities' : True}
    transcription_file = ".\\jsonOut\\" + videoTitle + '.txt'
    async def main(): 
        deepgram = Deepgram(DEEPGRAM_API_KEY)
        with open(VIDEO_FILE, 'rb') as audio: 
            source = {'buffer': audio, 'mimetype': 'audio/mp3'} 
            response = await deepgram.transcription.prerecorded(source, PARAMS) 
            transcript = response["results"]["channels"][0]["alternatives"][0]["transcript"] # Output the transcript print("Transcript:", transcript)
            
            os.remove(VIDEO_FILE) # Delete video
            
            with open(transcription_file, "w") as outfile: 
                outfile.write(transcript)

    asyncio.run(main())
    return transcription_file