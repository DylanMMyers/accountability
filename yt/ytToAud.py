import yt_dlp

url = "https://www.youtube.com/watch?v=NP96mMBxI2E&ab_channel=C-SPAN"

ydl_opts = {
   'format': 'bestaudio/best',
   'outtmpl': './out/%(title)s.mp3'
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
   info_dict = ydl.extract_info(url, download=False)
   title = info_dict.get('title', None)
   ydl.download(url)