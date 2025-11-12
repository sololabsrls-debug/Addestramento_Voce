"""
Script di test per Coqui XTTS v2
Misura qualità e latenza della sintesi vocale con voice cloning
"""
import os
import time
import torch
from TTS.api import TTS
from datetime import datetime

class CoquiXTTSTest:
    def __init__(self):
        self.models_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
        self.output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "audio_output")
        self.voices_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "voices")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tts = None

        # Crea directory se non esistono
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.voices_dir, exist_ok=True)

    def load_model(self):
        """Carica il modello XTTS v2"""
        print(f"🔄 Caricamento Coqui XTTS v2 su {self.device}...")
        start_time = time.time()

        try:
            self.tts = TTS(
                model_name="tts_models/multilingual/multi-dataset/xtts_v2",
                progress_bar=True
            ).to(self.device)

            load_time = time.time() - start_time
            print(f"✅ Modello caricato in {load_time:.2f}s")
            print(f"🌍 Lingue disponibili: {', '.join(self.tts.languages[:10])}...")
            return True

        except Exception as e:
            print(f"❌ Errore nel caricamento: {e}")
            return False

    def synthesize(self, text, language="it", speaker_wav=None, output_filename=None):
        """
        Sintetizza il testo in audio

        Args:
            text: Testo da sintetizzare
            language: Codice lingua (default: "it")
            speaker_wav: Path al file audio per voice cloning (opzionale)
            output_filename: Nome file output (opzionale)

        Returns:
            dict con metriche (latenza, RTF, ecc.)
        """
        if not self.tts:
            print("❌ Modello non caricato!")
            return None

        print(f"\n🎤 Sintesi: '{text}'")
        if speaker_wav:
            print(f"🎭 Voice cloning da: {speaker_wav}")

        # Sintesi
        start_time = time.time()

        try:
            if output_filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"xtts_{timestamp}.wav"

            output_path = os.path.join(self.output_dir, output_filename)

            # XTTS v2 synthesis
            if speaker_wav:
                # Voice cloning mode
                self.tts.tts_to_file(
                    text=text,
                    file_path=output_path,
                    speaker_wav=speaker_wav,
                    language=language
                )
            else:
                # Standard synthesis (usa speaker predefinito)
                self.tts.tts_to_file(
                    text=text,
                    file_path=output_path,
                    language=language
                )

            synthesis_time = time.time() - start_time

            # Calcola durata audio
            import soundfile as sf
            audio_data, sample_rate = sf.read(output_path)
            audio_duration = len(audio_data) / sample_rate
            rtf = synthesis_time / audio_duration if audio_duration > 0 else 0

            # Risultati
            metrics = {
                "text": text,
                "synthesis_time": synthesis_time,
                "audio_duration": audio_duration,
                "rtf": rtf,
                "sample_rate": sample_rate,
                "language": language,
                "voice_cloning": speaker_wav is not None,
                "output_file": output_path
            }

            print(f"⏱️  Tempo sintesi: {synthesis_time:.3f}s")
            print(f"🎵 Durata audio: {audio_duration:.3f}s")
            print(f"📊 RTF: {rtf:.3f}x")
            print(f"💾 Salvato: {output_path}")

            return metrics

        except Exception as e:
            print(f"❌ Errore durante la sintesi: {e}")
            return None

def main():
    """Test principale"""
    print("=" * 60)
    print("🎯 TEST COQUI XTTS v2")
    print("=" * 60)

    # Frasi di test in italiano
    test_phrases = [
        "Ciao, sono un assistente virtuale. Come posso aiutarti?",
        "Il meteo di oggi è sereno con temperature piacevoli.",
        "Grazie per la chiamata. Ti metto in contatto con un operatore.",
        "La tua richiesta verrà elaborata entro le prossime ventiquattro ore."
    ]

    # Inizializza tester
    tester = CoquiXTTSTest()

    if not tester.load_model():
        print("❌ Impossibile caricare il modello. Esegui prima download_model.py")
        return

    # Test sintesi
    print("\n" + "=" * 60)
    print("🧪 ESECUZIONE TEST")
    print("=" * 60)

    all_metrics = []
    for i, phrase in enumerate(test_phrases, 1):
        print(f"\n--- Test {i}/{len(test_phrases)} ---")
        metrics = tester.synthesize(
            text=phrase,
            language="it",
            output_filename=f"test_{i}.wav"
        )
        if metrics:
            all_metrics.append(metrics)

    # Statistiche finali
    if all_metrics:
        print("\n" + "=" * 60)
        print("📊 STATISTICHE FINALI")
        print("=" * 60)

        avg_synthesis = sum(m["synthesis_time"] for m in all_metrics) / len(all_metrics)
        avg_rtf = sum(m["rtf"] for m in all_metrics) / len(all_metrics)

        print(f"🔢 Test eseguiti: {len(all_metrics)}")
        print(f"⏱️  Tempo sintesi medio: {avg_synthesis:.3f}s")
        print(f"📊 RTF medio: {avg_rtf:.3f}x")
        print(f"🌍 Lingua: italiano")
        print(f"✅ Test completato con successo!")

    print("\n💡 SUGGERIMENTO:")
    print("   Per testare il voice cloning, aggiungi un file audio (6-10s)")
    print(f"   nella cartella: {tester.voices_dir}")
    print("   e modifica lo script per usare speaker_wav=path_al_file")

if __name__ == "__main__":
    main()
