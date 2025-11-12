"""
Script per scaricare il modello Resemble Chatterbox da Hugging Face
"""
import os
from huggingface_hub import snapshot_download

def download_chatterbox_model():
    """Scarica il modello Resemble Chatterbox"""

    model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "chatterbox")

    print("📥 Download Resemble Chatterbox da Hugging Face...")
    print(f"📁 Cartella destinazione: {model_path}")
    print("⚠️  Nota: Il modello ha ~500M parametri, il download potrebbe richiedere tempo")

    try:
        # Scarica il modello
        snapshot_download(
            repo_id="resemble-ai/resemble_enhance",
            local_dir=model_path,
            local_dir_use_symlinks=False
        )

        print("✅ Download completato!")
        print(f"📁 Modello salvato in: {model_path}")
        print("\n💡 NOTA IMPORTANTE:")
        print("   Resemble Chatterbox è principalmente un modello di enhancement audio.")
        print("   Per TTS completo, potrebbe essere necessario combinarlo con altri modelli.")
        print("   Controllare la documentazione ufficiale per dettagli.")

        return True

    except Exception as e:
        print(f"❌ Errore durante il download: {e}")
        print("\n💡 SUGGERIMENTO:")
        print("   Se il modello non è disponibile su HuggingFace,")
        print("   potrebbe essere necessario clonare il repository ufficiale:")
        print("   git clone https://github.com/resemble-ai/resemble-enhance")
        return False

if __name__ == "__main__":
    download_chatterbox_model()
