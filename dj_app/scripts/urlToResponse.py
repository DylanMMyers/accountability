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
    You will receive a transcript from a political event, such as a speech or debate. Your task is to identify the political figures speaking and evaluate the accuracy and truthfulness of their statements. For each political figure, assign a rating from 1 to 5, where 1 represents mostly false or misleading statements and 5 represents highly accurate and truthful remarks.
    For each figure, provide the following and do not provide any context before this structure:
    -A summary of their statements.
    -An assessment of how truthful specific claims are, explaining whether certain statements are accurate, deceptive, or false. Avoid general statements like "I want to be a good president."
    -Highlight the most deceptive statement made by each figure.
    -Use a mix of conservative and liberal sources to provide a balanced analysis.
    -Based on these sources, assign a confidence score (out of 100) for how confident you are in your assessment of each figure's accuracy, with 100 being fully confident.
    -Cite the sources used at the end of your response.
    The transcript can be accessed here: {title}.
    Here is the transcript: {transcript}
    The format for your response should be as follows:
    (Political Figure) (NEWLINE)
    Overall From Source: (rating/5) (NEWLINE)
    Most deceptive statement: (rating for this statement where 1 is a lie, 5 is truthful: 1/5) (NEWLINE)
    (Most deceptive statement) (NEWLINE)
    Summary of truthfulness: (explanation) (NEWLINE)
    Sources: (list of sources, do not use links, instead provide name of the article and publisher)
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
        video_id = url.replace("https://www.youtube.com/watch?v=","")[:14]
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_list.find_transcript(['en'])
        totalTranscript = ""
        for item in transcript.fetch():
            totalTranscript += item['text'] + " "
        return totalTranscript
    except:
        print("Something went wrong with getting transcript!")
        return "ERROR"


import os


def mainf(url):
    #loc = returnTranscriptFilePathFromURL(url)
    #title = loc.replace(".\\dj_app\\scripts\\jsonOut\\", "").replace(".txt","")
    # with open(loc, 'r', encoding='utf-8') as file:
    #     transcript = file.read()
    transcript = getTranscript(url)
    if transcript == "ERROR":
        return "ERROR: request blocked or invalid link"
    response = query(transcript, url)
    if response == "":
        return "ERROR"
    return response

