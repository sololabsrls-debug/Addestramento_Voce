# Bark TTS - Italiano

## Caratteristiche
- **Licenza**: MIT License
- **Velocità**: Lenta (RTF ~1.5-2.0)
- **Qualità**: Molto naturale ed espressiva
- **Dimensione modelli**: ~2 GB
- **GPU**: Consigliata (funziona anche su CPU ma lento)
- **Particolarità**: Può generare emozioni, risate, effetti sonori

## Installazione

```bash
chmod +x setup.sh
./setup.sh
```

Al primo utilizzo, Bark scaricherà automaticamente i modelli (~2GB).

## Generazione Audio

```bash
python3 generate.py
```

L'audio verrà salvato in `output.wav`.

## Note
- Bark è molto espressivo e può generare intonazioni emotive
- Supporta effetti sonori come [ride], [sospiro], ecc.
- Più lento di altri modelli ma con qualità molto naturale
- Ottimo per contenuti creativi e narrativi
- Può generare variazioni casuali (non deterministic)
