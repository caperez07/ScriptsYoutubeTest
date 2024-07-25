import yt_dlp
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

# Função para verificar se um vídeo tem legendas em português e inglês
def has_both_transcripts(video_id):
    try:
        transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
        languages = [transcript.language_code for transcript in transcripts]
        return 'pt' in languages and 'en' in languages
    except Exception as e:
        print(f"Could not retrieve transcripts for video ID {video_id}: {e}")
    return False

# Função para obter transcrições de vídeos em português e inglês
def get_transcripts(video_ids):
    transcripts = {}
    for video_id in video_ids:
        if has_both_transcripts(video_id):
            try:
                # Obtém transcrições em português e inglês
                transcript_pt = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt'])
                transcript_en = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
                transcripts[video_id] = {'pt': transcript_pt, 'en': transcript_en}
            except Exception as e:
                print(f"Could not retrieve transcripts for video ID {video_id}: {e}")
    return transcripts

# Função para salvar transcrições em arquivos SRT
def save_transcripts_as_srt(transcripts):
    formatter = SRTFormatter()
    for video_id, transcript_data in transcripts.items():
        # Salva transcrições em português
        if 'pt' in transcript_data:
            srt_data_pt = formatter.format_transcript(transcript_data['pt'])
            with open(f"{video_id}_pt.srt", "w", encoding="utf-8") as f:
                f.write(srt_data_pt)
            print(f"Portuguese transcript for video ID {video_id} saved as {video_id}_pt.srt")
        
        # Salva transcrições em inglês
        if 'en' in transcript_data:
            srt_data_en = formatter.format_transcript(transcript_data['en'])
            with open(f"{video_id}_en.srt", "w", encoding="utf-8") as f:
                f.write(srt_data_en)
            print(f"English transcript for video ID {video_id} saved as {video_id}_en.srt")

# Insira a URL do canal do YouTube
channel_url = 'https://www.youtube.com/alura/videos'

# Obtém todos os vídeos do canal
video_ids = get_channel_videos(channel_url)
print(f"Found {len(video_ids)} videos")

# Obtém as transcrições em português e inglês
transcripts = get_transcripts(video_ids)

# Salva as transcrições em arquivos SRT
save_transcripts_as_srt(transcripts)


## Não funcionou