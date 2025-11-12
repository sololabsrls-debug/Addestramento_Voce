"""
Script per scaricare il modello Azzurra-voice da Hugging Face
"""
import os
import sys
from huggingface_hub import snapshot_download

# Fix per UTF-8 su Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def download_azzurra_model():
    """Scarica il modello Azzurra-voice nella cartella models/"""

    model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "azzurra-voice")

    print("📥 Download Azzurra-voice da Hugging Face...")
    print(f"📁 Cartella destinazione: {model_path}")

    try:
        snapshot_download(
            repo_id="cartesia/azzurra-voice",
            local_dir=model_path,
            local_dir_use_symlinks=False
        )
        print("✅ Download completato!")
        print(f"📁 Modello salvato in: {model_path}")

    except Exception as e:
        print(f"❌ Errore durante il download: {e}")
        return False

    return True

if __name__ == "__main__":
    download_azzurra_model()
