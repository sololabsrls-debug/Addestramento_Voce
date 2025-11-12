"""
Script per scaricare il modello Coqui XTTS v2
"""
import os
from TTS.api import TTS

def download_xtts_model():
    """Scarica e inizializza il modello XTTS v2"""

    model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
    os.makedirs(model_path, exist_ok=True)

    print("📥 Download Coqui XTTS v2...")
    print(f"📁 Cartella modelli: {model_path}")

    try:
        # Inizializza TTS - questo scaricherà automaticamente il modello
        tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2")

        print("✅ Modello XTTS v2 scaricato e pronto!")
        print(f"📊 Lingue supportate: {len(tts.languages)} lingue")
        print(f"🌍 Include: {', '.join(tts.languages[:5])}...")

        return True

    except Exception as e:
        print(f"❌ Errore durante il download: {e}")
        return False

if __name__ == "__main__":
    download_xtts_model()
