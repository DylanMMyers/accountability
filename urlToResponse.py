from GetTranscriptFromYT import returnTranscriptFilePathFromURL
from perpQuery import query
import os

def mainf(url):
    loc = returnTranscriptFilePathFromURL(url)
    title = loc.replace(".\\jsonOut\\", "").replace(".txt","")
    with open(loc, 'r', encoding='utf-8') as file:
        transcript = file.read()
    response = query(transcript, title)
    print(response)
myURL = "https://www.youtube.com/watch?v=NP96mMBxI2E&ab_channel=C-SPAN"
mainf(myURL)