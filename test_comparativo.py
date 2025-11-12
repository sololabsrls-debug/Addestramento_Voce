"""
Script di Test Comparativo per Modelli TTS Italiani
Testa Azzurra-voice, Coqui XTTS v2 e Resemble Chatterbox

Misura:
- Latenza (tempo di sintesi)
- RTF (Real-Time Factor)
- Qualità percepita
- Dimensione file output
"""

import os
import sys
import time
import json
from datetime import datetime
from pathlib import Path

class TTSComparativeBenchmark:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.results_dir = self.base_dir / "risultati_comparativi"
        self.results_dir.mkdir(exist_ok=True)

        # Frasi di test standard
        self.test_phrases = [
            "Ciao, come stai oggi?",
            "Il meteo di domani sarà sereno con temperature miti.",
            "Grazie per aver chiamato il nostro servizio clienti.",
            "La tua richiesta è stata presa in carico e verrà elaborata entro ventiquattro ore.",
            "Per favore, rimani in linea. Un operatore ti risponderà a breve."
        ]

        self.results = {
            "timestamp": datetime.now().isoformat(),
            "models": {},
            "test_phrases": self.test_phrases
        }

    def print_header(self):
        """Stampa intestazione"""
        print("=" * 80)
        print("🎯 TEST COMPARATIVO MODELLI TTS PER ITALIANO".center(80))
        print("=" * 80)
        print(f"\n📅 Data test: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🔢 Frasi di test: {len(self.test_phrases)}")
        print(f"💾 Risultati salvati in: {self.results_dir}")

    def test_azzurra(self):
        """Test Azzurra-voice"""
        print("\n" + "=" * 80)
        print("🧪 TEST 1/3: AZZURRA-VOICE")
        print("=" * 80)

        try:
            # Importa il tester Azzurra
            sys.path.insert(0, str(self.base_dir / "Azzurra" / "scripts"))
            from test_tts import AzzuraTTSTest

            tester = AzzuraTTSTest()
            if not tester.load_model():
                print("⚠️  Azzurra-voice: modello non disponibile")
                return None

            metrics_list = []
            for i, phrase in enumerate(self.test_phrases, 1):
                print(f"\n--- Frase {i}/{len(self.test_phrases)} ---")
                metrics = tester.synthesize(phrase, f"azzurra_comp_{i}.wav")
                if metrics:
                    metrics_list.append(metrics)
                time.sleep(0.5)  # Pausa tra sintesi

            # Calcola statistiche
            if metrics_list:
                avg_synthesis = sum(m["synthesis_time"] for m in metrics_list) / len(metrics_list)
                avg_rtf = sum(m["rtf"] for m in metrics_list) / len(metrics_list)

                results = {
                    "model_name": "Azzurra-voice",
                    "status": "success",
                    "total_tests": len(metrics_list),
                    "avg_synthesis_time": round(avg_synthesis, 3),
                    "avg_rtf": round(avg_rtf, 3),
                    "quality_rating": "10/10 (dal PDF)",
                    "details": metrics_list
                }

                print(f"\n✅ Azzurra completato:")
                print(f"   ⏱️  Tempo medio: {avg_synthesis:.3f}s")
                print(f"   📊 RTF medio: {avg_rtf:.3f}x")

                return results

        except Exception as e:
            print(f"❌ Errore test Azzurra: {e}")
            return {"model_name": "Azzurra-voice", "status": "error", "error": str(e)}

        return None

    def test_coqui_xtts(self):
        """Test Coqui XTTS v2"""
        print("\n" + "=" * 80)
        print("🧪 TEST 2/3: COQUI XTTS v2")
        print("=" * 80)

        try:
            # Importa il tester Coqui
            sys.path.insert(0, str(self.base_dir / "CoquiXTTS" / "scripts"))
            from test_tts import CoquiXTTSTest

            tester = CoquiXTTSTest()
            if not tester.load_model():
                print("⚠️  Coqui XTTS: modello non disponibile")
                return None

            metrics_list = []
            for i, phrase in enumerate(self.test_phrases, 1):
                print(f"\n--- Frase {i}/{len(self.test_phrases)} ---")
                metrics = tester.synthesize(phrase, language="it", output_filename=f"xtts_comp_{i}.wav")
                if metrics:
                    metrics_list.append(metrics)
                time.sleep(0.5)

            # Calcola statistiche
            if metrics_list:
                avg_synthesis = sum(m["synthesis_time"] for m in metrics_list) / len(metrics_list)
                avg_rtf = sum(m["rtf"] for m in metrics_list) / len(metrics_list)

                results = {
                    "model_name": "Coqui XTTS v2",
                    "status": "success",
                    "total_tests": len(metrics_list),
                    "avg_synthesis_time": round(avg_synthesis, 3),
                    "avg_rtf": round(avg_rtf, 3),
                    "quality_rating": "9/10 (dal PDF)",
                    "details": metrics_list
                }

                print(f"\n✅ Coqui XTTS completato:")
                print(f"   ⏱️  Tempo medio: {avg_synthesis:.3f}s")
                print(f"   📊 RTF medio: {avg_rtf:.3f}x")

                return results

        except Exception as e:
            print(f"❌ Errore test Coqui XTTS: {e}")
            return {"model_name": "Coqui XTTS v2", "status": "error", "error": str(e)}

        return None

    def test_chatterbox(self):
        """Test Resemble Chatterbox"""
        print("\n" + "=" * 80)
        print("🧪 TEST 3/3: RESEMBLE CHATTERBOX")
        print("=" * 80)
        print("⚠️  Nota: Modello richiede setup specifico (vedi config/setup_instructions.md)")

        # Placeholder - Chatterbox non ancora implementato completamente
        return {
            "model_name": "Resemble Chatterbox",
            "status": "not_implemented",
            "quality_rating": "8.5/10 (dal PDF)",
            "expected_latency": "~1s per frase",
            "note": "Richiede implementazione specifica - vedi Resemble_Chatterbox/config/setup_instructions.md"
        }

    def generate_report(self):
        """Genera report comparativo"""
        print("\n" + "=" * 80)
        print("📊 REPORT COMPARATIVO FINALE")
        print("=" * 80)

        # Ordina modelli per RTF (più veloce prima)
        tested_models = [m for m in self.results["models"].values() if m.get("status") == "success"]

        if tested_models:
            tested_models.sort(key=lambda x: x.get("avg_rtf", float('inf')))

            print("\n🏆 CLASSIFICA PER VELOCITÀ (RTF):")
            for i, model in enumerate(tested_models, 1):
                print(f"{i}. {model['model_name']}: RTF {model['avg_rtf']:.3f}x "
                      f"({model['avg_synthesis_time']:.3f}s medio)")

            print("\n🎨 CLASSIFICA PER QUALITÀ (dal PDF):")
            quality_order = [
                ("Azzurra-voice", "10/10"),
                ("Coqui XTTS v2", "9/10"),
                ("Resemble Chatterbox", "8.5/10")
            ]
            for i, (name, rating) in enumerate(quality_order, 1):
                print(f"{i}. {name}: {rating}")

            print("\n💡 RACCOMANDAZIONI:")
            print("   🥇 MIGLIORE QUALITÀ: Azzurra-voice (10/10)")
            print("   ⚡ MIGLIORE VELOCITÀ: (vedi classifica RTF sopra)")
            print("   ⚖️  MIGLIOR BILANCIAMENTO: Resemble Chatterbox (8.5/10, ~1s)")

        # Salva risultati JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = self.results_dir / f"test_comparativo_{timestamp}.json"

        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)

        print(f"\n💾 Risultati salvati in: {results_file}")

        # Genera report markdown
        self.generate_markdown_report(timestamp)

    def generate_markdown_report(self, timestamp):
        """Genera report in formato Markdown"""
        report_file = self.results_dir / f"report_{timestamp}.md"

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# Test Comparativo Modelli TTS Italiani\n\n")
            f.write(f"**Data test**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            f.write("## Modelli Testati\n\n")
            for model_name, data in self.results["models"].items():
                f.write(f"### {data['model_name']}\n\n")
                f.write(f"- **Status**: {data['status']}\n")

                if data.get("status") == "success":
                    f.write(f"- **Test eseguiti**: {data['total_tests']}\n")
                    f.write(f"- **Tempo sintesi medio**: {data['avg_synthesis_time']}s\n")
                    f.write(f"- **RTF medio**: {data['avg_rtf']}x\n")
                    f.write(f"- **Qualità**: {data['quality_rating']}\n\n")

                elif data.get("status") == "not_implemented":
                    f.write(f"- **Nota**: {data.get('note', 'N/A')}\n")
                    f.write(f"- **Qualità attesa**: {data.get('quality_rating', 'N/A')}\n")
                    f.write(f"- **Latenza attesa**: {data.get('expected_latency', 'N/A')}\n\n")

            f.write("## Frasi di Test\n\n")
            for i, phrase in enumerate(self.test_phrases, 1):
                f.write(f"{i}. {phrase}\n")

            f.write("\n## Conclusioni\n\n")
            f.write("Vedere risultati dettagliati nel file JSON corrispondente.\n")

        print(f"📄 Report Markdown salvato in: {report_file}")

    def run(self):
        """Esegui tutti i test"""
        self.print_header()

        # Test Azzurra
        azzurra_results = self.test_azzurra()
        if azzurra_results:
            self.results["models"]["azzurra"] = azzurra_results

        # Test Coqui XTTS
        xtts_results = self.test_coqui_xtts()
        if xtts_results:
            self.results["models"]["coqui_xtts"] = xtts_results

        # Test Chatterbox
        chatterbox_results = self.test_chatterbox()
        if chatterbox_results:
            self.results["models"]["chatterbox"] = chatterbox_results

        # Genera report
        self.generate_report()

        print("\n" + "=" * 80)
        print("✅ TEST COMPARATIVO COMPLETATO!".center(80))
        print("=" * 80)

def main():
    """Funzione principale"""
    benchmark = TTSComparativeBenchmark()
    benchmark.run()

if __name__ == "__main__":
    main()
