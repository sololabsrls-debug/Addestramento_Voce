#!/usr/bin/env python3
"""
XTTS v2 ottimizzato per chiamate telefoniche in tempo reale

Questo script è configurato per:
- Latenza minima (1-2 secondi con GPU)
- Qualità audio telefonica (8kHz/16kHz)
- Streaming audio per ridurre perceived latency
- Gestione robusta degli errori
- Voice cloning con voce aziendale personalizzata

REQUISITI:
- GPU NVIDIA con 6GB+ VRAM (RTX 3060 o superiore)
- Python 3.9+
- pip install TTS torch torchaudio soundfile

Per produzione: considera RTX 3060/3070 o A4000
"""

import torch
import time
import os
import numpy as np
import soundfile as sf
from pathlib import Path

# Configurazione ottimale per chiamate
class XTTSCallConfig:
    """Configurazione ottimizzata per chiamate telefoniche"""

    # Audio settings
    SAMPLE_RATE = 24000  # XTTS native (convertiamo dopo per telefonia)
    PHONE_SAMPLE_RATE = 8000  # Standard telefonia (o 16000 per HD)

    # Performance settings
    STREAMING = True  # Abilita streaming per ridurre latency
    USE_GPU = True
    GPU_ID = 0

    # Quality vs Speed trade-off
    TEMPERATURE = 0.75  # Più basso = più consistente, più veloce
    LENGTH_PENALTY = 1.0
    REPETITION_PENALTY = 5.0
    TOP_K = 50
    TOP_P = 0.85

    # Chunk settings per streaming
    CHUNK_SIZE = 20  # Dimensione chunk per streaming (tokens)

    @classmethod
    def get_device(cls):
        if cls.USE_GPU and torch.cuda.is_available():
            return f"cuda:{cls.GPU_ID}"
        return "cpu"

class XTTSRealtimeEngine:
    """
    Engine XTTS ottimizzato per chiamate real-time
    """

    def __init__(self, speaker_wav=None, language="it"):
        """
        Inizializza l'engine

        Args:
            speaker_wav: Path dell'audio di riferimento per voice cloning
            language: Lingua (it, en, es, fr, de, etc.)
        """
        self.config = XTTSCallConfig()
        self.language = language
        self.speaker_wav = speaker_wav
        self.model = None
        self.is_loaded = False

        print(f"🎯 Inizializzazione XTTS per chiamate real-time")
        print(f"   Device: {self.config.get_device()}")
        print(f"   GPU disponibile: {torch.cuda.is_available()}")

        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1e9
            print(f"   GPU: {gpu_name} ({gpu_memory:.1f} GB)")

        self._load_model()

    def _load_model(self):
        """Carica il modello XTTS v2"""
        from TTS.api import TTS

        print("\n⏳ Caricamento modello XTTS v2...")
        start = time.time()

        try:
            self.model = TTS(
                model_name="tts_models/multilingual/multi-dataset/xtts_v2",
                gpu=self.config.USE_GPU
            )

            elapsed = time.time() - start
            self.is_loaded = True

            print(f"✓ Modello caricato in {elapsed:.2f} secondi")

            # Warm-up: prima inferenza è sempre più lenta
            print("🔥 Warm-up GPU...")
            self._warmup()

        except Exception as e:
            print(f"✗ Errore caricamento modello: {e}")
            raise

    def _warmup(self):
        """Warm-up del modello per ridurre latenza prima chiamata"""
        if not self.speaker_wav or not os.path.exists(self.speaker_wav):
            print("⚠️ Nessun audio di riferimento per warm-up")
            return

        try:
            # Genera un breve audio di test
            _ = self.synthesize("Test", return_numpy=True)
            print("✓ Warm-up completato")
        except Exception as e:
            print(f"⚠️ Warm-up fallito: {e}")

    def synthesize(self, text, output_file=None, return_numpy=False):
        """
        Sintetizza testo in audio

        Args:
            text: Testo da sintetizzare
            output_file: Path file output (opzionale)
            return_numpy: Se True, ritorna array numpy invece di salvare

        Returns:
            Se return_numpy=True: (audio_array, sample_rate)
            Altrimenti: path del file salvato
        """
        if not self.is_loaded:
            raise RuntimeError("Modello non caricato")

        if not self.speaker_wav:
            raise ValueError("Nessun audio di riferimento configurato")

        start_time = time.time()

        try:
            # Genera audio
            # XTTS non supporta nativamente lo streaming, ma possiamo
            # spezzare il testo in chunks per ridurre perceived latency

            wav = self.model.tts(
                text=text,
                speaker_wav=self.speaker_wav,
                language=self.language
            )

            inference_time = time.time() - start_time

            # Converti in numpy array se necessario
            if isinstance(wav, list):
                wav = np.array(wav, dtype=np.float32)

            audio_duration = len(wav) / self.config.SAMPLE_RATE
            rtf = inference_time / audio_duration  # Real-time factor

            print(f"⚡ Generato {audio_duration:.2f}s audio in {inference_time:.2f}s (RTF: {rtf:.2f}x)")

            if return_numpy:
                return wav, self.config.SAMPLE_RATE

            # Salva file
            if output_file:
                sf.write(output_file, wav, self.config.SAMPLE_RATE)
                return output_file

            return wav, self.config.SAMPLE_RATE

        except Exception as e:
            print(f"✗ Errore sintesi: {e}")
            raise

    def synthesize_streaming(self, text, chunk_size=50):
        """
        Sintetizza con simulazione di streaming (chunked processing)
        Utile per ridurre perceived latency in conversazioni

        Args:
            text: Testo da sintetizzare
            chunk_size: Dimensione chunk in caratteri

        Yields:
            Tuple (audio_chunk, sample_rate)
        """
        # Split testo in chunks intelligenti (per frasi/pause)
        import re

        # Split su punteggiatura
        sentences = re.split(r'([.!?]\s+)', text)
        current_chunk = ""

        for i, part in enumerate(sentences):
            current_chunk += part

            # Genera quando abbiamo abbastanza testo o è l'ultimo
            if len(current_chunk) > chunk_size or i == len(sentences) - 1:
                if current_chunk.strip():
                    try:
                        wav, sr = self.synthesize(current_chunk.strip(), return_numpy=True)
                        yield wav, sr
                        current_chunk = ""
                    except Exception as e:
                        print(f"⚠️ Errore chunk: {e}")
                        continue

    def convert_to_phone_audio(self, wav, sample_rate):
        """
        Converte audio a formato telefonico (8kHz o 16kHz)

        Args:
            wav: Audio array
            sample_rate: Sample rate originale

        Returns:
            Audio convertito a sample rate telefonico
        """
        from scipy import signal

        target_sr = self.config.PHONE_SAMPLE_RATE

        if sample_rate == target_sr:
            return wav

        # Resample
        num_samples = int(len(wav) * target_sr / sample_rate)
        wav_resampled = signal.resample(wav, num_samples)

        return wav_resampled.astype(np.float32)

    def set_speaker(self, speaker_wav):
        """Cambia l'audio di riferimento (speaker)"""
        if not os.path.exists(speaker_wav):
            raise FileNotFoundError(f"File non trovato: {speaker_wav}")

        self.speaker_wav = speaker_wav
        print(f"✓ Speaker cambiato: {speaker_wav}")

        # Re-warm-up con nuovo speaker
        self._warmup()


# ============================================================================
# INTEGRAZIONE CON SISTEMI TELEFONICI
# ============================================================================

class TelephonyIntegration:
    """Helper per integrare XTTS con sistemi telefonici"""

    @staticmethod
    def save_for_twilio(wav, sample_rate, output_file):
        """
        Salva audio in formato ottimale per Twilio
        Twilio preferisce: mu-law, 8kHz, mono
        """
        from scipy.io import wavfile
        from scipy import signal

        # Resample a 8kHz
        if sample_rate != 8000:
            num_samples = int(len(wav) * 8000 / sample_rate)
            wav = signal.resample(wav, num_samples)
            sample_rate = 8000

        # Normalizza
        wav = np.clip(wav, -1.0, 1.0)

        # Converti a 16-bit PCM
        wav_int16 = (wav * 32767).astype(np.int16)

        # Salva
        wavfile.write(output_file, sample_rate, wav_int16)
        print(f"✓ Salvato per Twilio: {output_file} (8kHz, 16-bit PCM)")

    @staticmethod
    def save_for_asterisk(wav, sample_rate, output_file):
        """
        Salva audio per Asterisk PBX
        Asterisk preferisce: 8kHz o 16kHz, mono, WAV
        """
        from scipy import signal

        target_sr = 8000  # o 16000 per HD

        if sample_rate != target_sr:
            num_samples = int(len(wav) * target_sr / sample_rate)
            wav = signal.resample(wav, num_samples)

        wav = np.clip(wav, -1.0, 1.0)
        wav_int16 = (wav * 32767).astype(np.int16)

        sf.write(output_file, wav_int16, target_sr, subtype='PCM_16')
        print(f"✓ Salvato per Asterisk: {output_file} ({target_sr}Hz)")

    @staticmethod
    def to_opus_codec(wav_file, output_file):
        """
        Converti in Opus codec (usato da WebRTC/VoIP moderno)
        Richiede: ffmpeg installato
        """
        import subprocess

        cmd = [
            'ffmpeg', '-i', wav_file,
            '-c:a', 'libopus',
            '-b:a', '16k',  # 16 kbps per chiamate vocali
            '-vbr', 'on',
            '-compression_level', '10',
            '-frame_duration', '20',
            '-application', 'voip',
            '-y',  # Sovrascrivi
            output_file
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✓ Convertito in Opus: {output_file}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Errore conversione Opus: {e}")
            return False


# ============================================================================
# ESEMPIO: Server per chiamate real-time
# ============================================================================

class RealtimeCallServer:
    """
    Server simulato per gestire chiamate real-time
    In produzione, integra con Twilio, Asterisk, FreeSWITCH, etc.
    """

    def __init__(self, speaker_wav, language="it"):
        self.engine = XTTSRealtimeEngine(speaker_wav, language)
        self.call_history = []

    def handle_call(self, call_id, messages):
        """
        Gestisce una chiamata: riceve messaggi e genera risposte audio

        Args:
            call_id: ID della chiamata
            messages: Lista di messaggi da sintetizzare

        Returns:
            Lista di file audio generati
        """
        print(f"\n📞 Gestione chiamata {call_id}")
        print("=" * 70)

        audio_files = []

        for idx, message in enumerate(messages):
            print(f"\n💬 Messaggio {idx+1}: {message[:50]}...")

            # File output
            output_file = f"call_{call_id}_msg_{idx+1}.wav"

            # Genera audio
            start = time.time()
            self.engine.synthesize(message, output_file)
            latency = time.time() - start

            print(f"   Latenza: {latency:.2f}s")

            # Salva per sistema telefonico
            wav, sr = self.engine.synthesize(message, return_numpy=True)
            phone_file = f"call_{call_id}_msg_{idx+1}_phone.wav"
            TelephonyIntegration.save_for_twilio(wav, sr, phone_file)

            audio_files.append(phone_file)

            # Tracking
            self.call_history.append({
                'call_id': call_id,
                'message': message,
                'latency': latency,
                'file': phone_file
            })

        print(f"\n✓ Chiamata {call_id} completata: {len(audio_files)} messaggi generati")
        return audio_files

    def get_average_latency(self):
        """Calcola latenza media"""
        if not self.call_history:
            return 0

        latencies = [h['latency'] for h in self.call_history]
        return sum(latencies) / len(latencies)


# ============================================================================
# ESEMPI E TEST
# ============================================================================

def test_latenza():
    """Test di latenza per varie lunghezze di testo"""

    print("""
╔════════════════════════════════════════════════════════════════════════╗
║                    TEST LATENZA PER CHIAMATE                           ║
╚════════════════════════════════════════════════════════════════════════╝
    """)

    # Verifica audio di riferimento
    speaker_wav = "mia_voce_riferimento.wav"

    if not os.path.exists(speaker_wav):
        print(f"⚠️ Audio di riferimento non trovato: {speaker_wav}")
        print("\n💡 Per questo test, devi prima creare un audio di riferimento.")
        print("   Registra 10 secondi della voce che vuoi usare per le chiamate.")
        return

    # Inizializza engine
    engine = XTTSRealtimeEngine(speaker_wav, "it")

    # Test messaggi di varie lunghezze (tipici di chiamate)
    test_cases = [
        ("Breve", "Ciao, come posso aiutarti?"),
        ("Media", "Grazie per aver chiamato. Il tuo ordine numero 12345 è stato spedito e arriverà domani."),
        ("Lunga", "Buongiorno, ho controllato la sua pratica e posso confermare che la richiesta è stata approvata. Le invierò una email di conferma con tutti i dettagli entro oggi. C'è qualcos'altro con cui posso assisterla?"),
    ]

    print("\n" + "=" * 70)
    print("BENCHMARK LATENZA")
    print("=" * 70)

    results = []

    for name, text in test_cases:
        print(f"\n📊 Test: {name} ({len(text)} caratteri)")
        print(f"   Testo: {text[:50]}...")

        # Misura latenza
        start = time.time()
        wav, sr = engine.synthesize(text, return_numpy=True)
        latency = time.time() - start

        audio_duration = len(wav) / sr
        rtf = latency / audio_duration

        print(f"   Latenza: {latency:.2f}s")
        print(f"   Audio duration: {audio_duration:.2f}s")
        print(f"   RTF: {rtf:.2f}x")

        results.append({
            'name': name,
            'chars': len(text),
            'latency': latency,
            'duration': audio_duration,
            'rtf': rtf
        })

    # Riepilogo
    print("\n" + "=" * 70)
    print("RIEPILOGO")
    print("=" * 70)

    print(f"\n{'Tipo':<10} {'Caratteri':<12} {'Latenza':<12} {'RTF':<10} {'Accettabile?'}")
    print("-" * 70)

    for r in results:
        acceptable = "✓ SÌ" if r['latency'] < 2.0 else "✗ NO"
        print(f"{r['name']:<10} {r['chars']:<12} {r['latency']:.2f}s{'':<7} {r['rtf']:.2f}x{'':<5} {acceptable}")

    avg_latency = sum(r['latency'] for r in results) / len(results)
    print(f"\nLatenza media: {avg_latency:.2f}s")

    print("\n" + "=" * 70)
    print("CONSIDERAZIONI PER PRODUZIONE")
    print("=" * 70)
    print("""
✓ Target per chiamate real-time: < 2 secondi
✓ Per conversazioni fluide: < 1.5 secondi ideale
✓ Con GPU RTX 3060+: 0.5-1.5s tipico
✓ Strategie per ridurre latenza:
  - Pre-genera risposte comuni (IVR, FAQ)
  - Usa streaming/chunking per frasi lunghe
  - Warm-up del modello all'avvio
  - Ottimizza temperature e sampling parameters
    """)

def demo_chiamata_completa():
    """Demo di una chiamata completa"""

    print("""
╔════════════════════════════════════════════════════════════════════════╗
║                    DEMO CHIAMATA COMPLETA                              ║
╚════════════════════════════════════════════════════════════════════════╝
    """)

    speaker_wav = "mia_voce_riferimento.wav"

    if not os.path.exists(speaker_wav):
        print("⚠️ Crea prima un audio di riferimento: mia_voce_riferimento.wav")
        return

    # Simula una chiamata al servizio clienti
    server = RealtimeCallServer(speaker_wav, "it")

    call_messages = [
        "Benvenuto al servizio clienti. Come posso aiutarti oggi?",
        "Ho verificato il tuo account e tutto risulta in ordine.",
        "Il tuo pacco è in consegna e arriverà entro domani alle 18.",
        "C'è qualcos'altro con cui posso assisterti?",
        "Grazie per aver chiamato. Buona giornata!"
    ]

    audio_files = server.handle_call("DEMO_001", call_messages)

    print("\n" + "=" * 70)
    print("STATISTICHE CHIAMATA")
    print("=" * 70)
    print(f"Messaggi generati: {len(audio_files)}")
    print(f"Latenza media: {server.get_average_latency():.2f}s")
    print(f"File audio: {', '.join(audio_files[:3])}...")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import sys

    print("""
╔════════════════════════════════════════════════════════════════════════╗
║              XTTS v2 - SISTEMA PER CHIAMATE REAL-TIME                  ║
╚════════════════════════════════════════════════════════════════════════╝

Questo sistema è ottimizzato per gestire chiamate telefoniche con latenza
minima e qualità audio naturale.
    """)

    # Verifica GPU
    if not torch.cuda.is_available():
        print("⚠️ WARNING: Nessuna GPU rilevata!")
        print("   Per chiamate real-time è ALTAMENTE consigliata una GPU NVIDIA")
        print("   Latenza attesa su CPU: 10-30 secondi (NON real-time)")
        print()
        risposta = input("Vuoi continuare comunque? (s/n): ")
        if risposta.lower() != 's':
            sys.exit(0)

    print("\nScegli un'opzione:\n")
    print("  1. Test latenza (benchmark varie lunghezze)")
    print("  2. Demo chiamata completa")
    print("  3. Genera singolo messaggio")
    print("  0. Esci\n")

    scelta = input("Scelta: ").strip()

    if scelta == "1":
        test_latenza()
    elif scelta == "2":
        demo_chiamata_completa()
    elif scelta == "3":
        speaker_wav = input("Audio di riferimento (default: mia_voce_riferimento.wav): ").strip()
        if not speaker_wav:
            speaker_wav = "mia_voce_riferimento.wav"

        if not os.path.exists(speaker_wav):
            print(f"✗ File non trovato: {speaker_wav}")
        else:
            text = input("Testo da sintetizzare: ").strip()
            if text:
                engine = XTTSRealtimeEngine(speaker_wav, "it")
                engine.synthesize(text, "output_singolo.wav")
                print("✓ Salvato: output_singolo.wav")
    else:
        print("Ciao!")
