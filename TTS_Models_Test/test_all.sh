#!/bin/bash
# Script per testare tutti i modelli TTS automaticamente

echo "========================================="
echo "Test Automatico Modelli TTS - Italiano"
echo "========================================="
echo ""

# Conta i modelli
total_models=$(find . -maxdepth 1 -type d -name "[0-9]*" | wc -l)
current=0

for dir in [0-9]*/; do
    if [ -f "$dir/setup.sh" ]; then
        current=$((current + 1))
        echo ""
        echo "[$current/$total_models] Testing: $dir"
        echo "========================================="

        cd "$dir"

        # Setup
        echo "→ Installazione dipendenze..."
        if ./setup.sh > setup.log 2>&1; then
            echo "  ✓ Setup completato"
        else
            echo "  ✗ Setup fallito (vedi setup.log)"
            cd ..
            continue
        fi

        # Generate
        echo "→ Generazione audio..."
        if python3 generate.py > generate.log 2>&1; then
            echo "  ✓ Audio generato"

            # Verifica se output.wav esiste
            if [ -f "output.wav" ]; then
                size=$(du -h output.wav | cut -f1)
                echo "  ℹ File output.wav: $size"
            else
                echo "  ⚠ output.wav non trovato"
            fi
        else
            echo "  ✗ Generazione fallita (vedi generate.log)"
        fi

        cd ..
        echo ""
    fi
done

echo "========================================="
echo "Test completati!"
echo "========================================="
echo ""
echo "Risultati disponibili in:"
for dir in [0-9]*/; do
    if [ -f "$dir/output.wav" ]; then
        echo "  ✓ $dir/output.wav"
    else
        echo "  ✗ $dir/output.wav (non generato)"
    fi
done
echo ""
echo "Per ascoltare gli audio, usa un player come:"
echo "  vlc 01_Piper/output.wav"
echo "  mpv 07_Coqui_XTTS/output.wav"
echo ""
