import whisper
import warnings

# Игнорируем предупреждение
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")

model = whisper.load_model("base") # загрузка модели

async def speech_to_text(audio_path : str) -> str:
    result = model.transcribe(audio_path, language="ru")
    return result["text"]