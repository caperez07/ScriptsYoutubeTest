import yt_dlp
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import SRTFormatter

# Função para obter a lista de vídeos de um canal
def get_channel_videos(channel_url):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': True,
        'default_search': 'auto'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(channel_url, download=False)
        if 'entries' in result:
            video_ids = [entry['id'] for entry in result['entries']]
            return video_ids
        else:
            return []

# Função para obter transcrições de vídeos
def get_transcripts(video_ids):
    transcripts = {}
    for video_id in video_ids:
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            transcripts[video_id] = transcript
        except Exception as e:
            print(f"Could not retrieve transcript for video ID {video_id}: {e}")
    return transcripts

# Função para salvar transcrições em arquivos SRT
def save_transcripts_as_srt(transcripts):
    formatter = SRTFormatter()
    for video_id, transcript in transcripts.items():
        srt_data = formatter.format_transcript(transcript)
        with open(f"{video_id}.srt", "w") as f:
            f.write(srt_data)
        print(f"Transcript for video ID {video_id} saved as {video_id}.srt")

# Insira a URL do canal do YouTube
channel_url = 'https://www.youtube.com/@VanityFair/videos'

# Obtém todos os vídeos do canal
video_ids = get_channel_videos(channel_url)
print(f"Found {len(video_ids)} videos")

# Obtém as transcrições
transcripts = get_transcripts(video_ids)

# Salva as transcrições em arquivos SRT
save_transcripts_as_srt(transcripts)
