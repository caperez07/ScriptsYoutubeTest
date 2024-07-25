import requests
from bs4 import BeautifulSoup
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi

# Função para obter todos os vídeos de um canal usando scraping
def get_channel_videos(channel_url):
    response = requests.get(channel_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    video_ids = []

    # Adicionando mais debugging para entender a estrutura da página
    print("Scraping the page for video links...")

    for link in soup.find_all('a', href=True):
        href = link['href']
        if '/watch?v=' in href:
            video_id = href.split('/watch?v=')[1]
            if '&' in video_id:
                video_id = video_id.split('&')[0]
            if video_id not in video_ids:
                video_ids.append(video_id)

    print(f"Video IDs found: {video_ids}")
    return video_ids

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

# Função para imprimir transcrições
def print_transcripts(transcripts):
    for video_id, transcript in transcripts.items():
        print(f"Transcript for video ID {video_id}:\n")
        for entry in transcript:
            print(f"{entry['start']}s: {entry['text']}")
        print("\n")

# Insira a URL do canal do YouTube
channel_url = 'https://www.youtube.com/variety/videos'

# Obtém todos os vídeos do canal
video_ids = get_channel_videos(channel_url)
print(f"Found {len(video_ids)} videos")

# Obtém as transcrições
transcripts = get_transcripts(video_ids)

# Imprime as transcrições
print_transcripts(transcripts)

## Não deu erro mas não printou as trascrições
