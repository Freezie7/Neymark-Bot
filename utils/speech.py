import whisper
import warnings
from pydub import AudioSegment, silence

def find_pauses(audio_path: str):
    audio = AudioSegment.from_file(audio_path)
    return silence.detect_silence(audio, silence_thresh=-40, min_silence_len=2000)


# Игнорируем предупреждение
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")

model = whisper.load_model("base") # загрузка модели

async def speech_to_text(audio_path : str) -> str:
    result = model.transcribe(audio_path, language="ru")
    return result["text"]