# import yt_dlp
# from deepgram import Deepgram
# import asyncio, os

# def returnTranscriptFilePathFromURL(url):
#     ################ DOWNLOAD VIDEO ##################
#     ydl_opts = {
#     'format': 'bestaudio/best',
#     'outtmpl': './dj_app/scripts/audOut/%(title)s.mp3'
#     }

#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         info_dict = ydl.extract_info(url, download=False)
#         videoTitle = info_dict.get('title', None)
#         ydl.download(url)

#     VIDEO_FILE = ".\\dj_app\\scripts\\audOut\\" + videoTitle + ".mp3"

#     ########## CONVERTING VIDEO TO TRANSCRIPT (JSON) ##################

#     DEEPGRAM_API_KEY = 'd39e79e5d1cecef3561049b576e5135cc0b49234' 
#     PARAMS = {'punctuate': True, 'tier': 'enhanced', 'detect_entities' : True}
#     transcription_file = ".\\dj_app\\scripts\\jsonOut\\" + videoTitle + '.txt'
#     async def main(): 
#         deepgram = Deepgram(DEEPGRAM_API_KEY)
#         with open(VIDEO_FILE, 'rb') as audio: 
#             source = {'buffer': audio, 'mimetype': 'audio/mp3'} 
#             response = await deepgram.transcription.prerecorded(source, PARAMS) 
#             transcript = response["results"]["channels"][0]["alternatives"][0]["transcript"] # Output the transcript print("Transcript:", transcript)
            
#             os.remove(VIDEO_FILE) # Delete video
            
#             with open(transcription_file, "w") as outfile: 
#                 outfile.write(transcript)

#     asyncio.run(main())
#     return transcription_file

from openai import OpenAI

YOUR_API_KEY = "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"

def query(transcript, title):
    """
    Queries the Perplexity API with the provided transcript and title.

    Parameters:
    - transcript (str): The transcript from the political event.
    - title (str): The title of the event for context.

    Returns:
    - response (str): The API's response containing the assessment.
    """
    prompt = f"""
    You are about to receive a transcript from some political event, like a speech or debate. Identify which political figures are speaking and assess the accuracy and truth of their statement. For each political figure you identify, rate them from 1-5 on how accurate and truthful their statements were. Provide a summary for each political figure and what they said, how truthful certain statements were and provide further context or explanations of how what they said is accurate, deceptive, or a lie. Avoid categorizing statements similar to “I want to be a good president” and such general statements. Please also state what the most deceptive statement was. When selecting sources try to use a mix of typically conservative and liberal sources to provide a wider world view on the situation. Based on these sources, provide a confidence score out of 100 for how accurate your assessment is of each candidate, with 100 being fully confident. Please cite these sources at the bottom of the response. The transcript has the link “{title}”, which may help provide you with context. PLEASE DO NOT PROVIDE A TABLE OR ANY OTHER CONTEXT BEFORE THE OUTPUT, JUST PROVIDE THE DATA IN THE FORMAT BELOW:

    A response may look like:
    (Political Figure) : (rating/5):
    Most deceptive statement: (text here)
    Summary of truthfulness of a statement: (text here)
    (Sources for that statement)
    
    Here is the transcript:
    {transcript}
    """

    messages = [
        {
            "role": "system",
            "content": (
                "You are an artificial intelligence assistant and you need to "
                "engage in a helpful, detailed, polite conversation with a user."
            ),
        },
        {
            "role": "user",
            "content": (
                prompt
            ),
        },
    ]

    client = OpenAI(api_key=YOUR_API_KEY, base_url="https://api.perplexity.ai")

    response = client.chat.completions.create(
        model="llama-3.1-sonar-small-128k-online",
        messages=messages,
    )
    
    result_text = response.choices[0].message.content   # Adjust this based on the response structure
    #print(result_text)
    return result_text

from youtube_transcript_api import YouTubeTranscriptApi
def getTranscript(url):
    try:
        video_id = url.remove("https://www.youtube.com/watch?v=","")[:15]
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_list.find_transcript(['en'])
        totalTranscript = ""
        for item in transcript.fetch():
            totalTranscript += item['text'] + " "
        return totalTranscript
    except:
        print("Something went wrong with getting transcript!")


import os


def mainf(url):
    #loc = returnTranscriptFilePathFromURL(url)
    #title = loc.replace(".\\dj_app\\scripts\\jsonOut\\", "").replace(".txt","")
    # with open(loc, 'r', encoding='utf-8') as file:
    #     transcript = file.read()
    transcript = getTranscript(url)
    response = query(transcript, url)
    return response

