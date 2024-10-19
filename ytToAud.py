import yt_dlp

url = "https://www.youtube.com/watch?v=NP96mMBxI2E&ab_channel=C-SPAN"

vids = [url]

ydl_opts = {
   'format': 'bestaudio/best',
   'postprocessors': [{
       'key': 'FFmpegExtractAudio',
       'preferredcodec': 'mp3',
       'preferredquality': '192',
   }],
   # change this to change where you download it to
   'outtmpl': './out/%(title)s.mp3',

}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
   ydl.download(vids)