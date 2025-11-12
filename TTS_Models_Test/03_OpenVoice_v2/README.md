# OpenVoice v2 - Italiano

## Caratteristiche
- **Licenza**: MIT License
- **Velocità**: Veloce per conversion (RTF ~0.2)
- **Qualità**: Eccellente per voice cloning
- **Modello**: OpenVoice v2 (cross-lingual)
- **Dimensione**: ~300 MB
- **GPU**: Consigliata
- **Particolarità**: Voice cloning cross-lingua, tone color control

## Installazione

```bash
chmod +x setup.sh
./setup.sh
```

## Generazione Audio

```bash
python3 generate.py
```

## Note Importanti
- **OpenVoice v2 è principalmente un modello di voice cloning/conversion**
- Non genera audio da zero, ma converte audio esistente
- Richiede un audio base (da altro TTS) e un audio di riferimento
- Eccellente per clonare voci e applicare tone color specifico
- Supporta conversione cross-lingua (es: parlare italiano con voce inglese)

## Caso d'uso tipico:
1. Genera audio base con altro TTS (es: Coqui XTTS, Piper)
2. Usa OpenVoice v2 per applicare il tone color di una voce di riferimento
3. Ottieni audio con contenuto del base TTS ma voce del riferimento

## Alternativa per test diretto:
Per test TTS diretto in italiano, usa invece:
- Coqui XTTS v2 (ottimo per qualità e versatilità)
- Piper (veloce e leggero)
- Parler-TTS (controllo espressivo)
