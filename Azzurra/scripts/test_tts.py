"""
Script di test per Azzurra-voice TTS
Misura qualità e latenza della sintesi vocale
"""
import os
import time
import torch
import soundfile as sf
from transformers import VitsModel, AutoTokenizer
from datetime import datetime

class AzzuraTTSTest:
    def __init__(self):
        self.model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "azzurra-voice")
        self.output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "audio_output")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = None
        self.tokenizer = None

    def load_model(self):
        """Carica il modello Azzurra-voice"""
        print(f"🔄 Caricamento modello Azzurra-voice su {self.device}...")
        start_time = time.time()

        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            self.model = VitsModel.from_pretrained(self.model_path).to(self.device)

            load_time = time.time() - start_time
            print(f"✅ Modello caricato in {load_time:.2f}s")
            return True

        except Exception as e:
            print(f"❌ Errore nel caricamento: {e}")
            return False

    def synthesize(self, text, output_filename=None):
        """
        Sintetizza il testo in audio

        Args:
            text: Testo da sintetizzare
            output_filename: Nome file output (opzionale)

        Returns:
            dict con metriche (latenza, RTF, ecc.)
        """
        if not self.model:
            print("❌ Modello non caricato!")
            return None

        print(f"\n🎤 Sintesi: '{text}'")

        # Tokenizzazione
        inputs = self.tokenizer(text, return_tensors="pt").to(self.device)

        # Sintesi
        start_time = time.time()
        with torch.no_grad():
            output = self.model(**inputs)

        synthesis_time = time.time() - start_time

        # Estrai audio
        audio = output.waveform.squeeze().cpu().numpy()
        sample_rate = self.model.config.sampling_rate

        # Calcola metriche
        audio_duration = len(audio) / sample_rate
        rtf = synthesis_time / audio_duration if audio_duration > 0 else 0

        # Salva audio
        if output_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"azzurra_{timestamp}.wav"

        output_path = os.path.join(self.output_dir, output_filename)
        sf.write(output_path, audio, sample_rate)

        # Risultati
        metrics = {
            "text": text,
            "synthesis_time": synthesis_time,
            "audio_duration": audio_duration,
            "rtf": rtf,
            "sample_rate": sample_rate,
            "output_file": output_path
        }

        print(f"⏱️  Tempo sintesi: {synthesis_time:.3f}s")
        print(f"🎵 Durata audio: {audio_duration:.3f}s")
        print(f"📊 RTF: {rtf:.3f}x")
        print(f"💾 Salvato: {output_path}")

        return metrics

def main():
    """Test principale"""
    print("=" * 60)
    print("🎯 TEST AZZURRA-VOICE TTS")
    print("=" * 60)

    # Frasi di test in italiano
    test_phrases = [
        "Ciao, sono Azzurra. Come posso aiutarti oggi?",
        "Il meteo di oggi prevede sole con temperature miti.",
        "Grazie per aver chiamato. Ti trasferisco subito all'operatore.",
        "La tua richiesta è stata presa in carico e verrà processata entro ventiquattro ore."
    ]

    # Inizializza tester
    tester = AzzuraTTSTest()

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
        metrics = tester.synthesize(phrase, f"test_{i}.wav")
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
        print(f"✅ Test completato con successo!")

if __name__ == "__main__":
    main()
