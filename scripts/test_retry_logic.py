#!/usr/bin/env python3
"""
Test rapido per verificare retry logic e checkpoint system
"""

import sys
import time
from pathlib import Path

# Aggiungi directory scripts al path
sys.path.insert(0, str(Path(__file__).parent))

from download_ljspeech_italian import retry_with_backoff, load_checkpoint, save_checkpoint
from requests.exceptions import RequestException

def test_retry_success():
    """Test retry con successo al terzo tentativo"""
    print("Test 1: Retry con successo al terzo tentativo")

    attempt_count = {'count': 0}

    def failing_function():
        attempt_count['count'] += 1
        if attempt_count['count'] < 3:
            raise RequestException("Test error")
        return "Success!"

    try:
        result = retry_with_backoff(failing_function, max_retries=5, initial_wait=0.1, max_wait=1)
        print(f"✅ Test 1 PASSED: {result} dopo {attempt_count['count']} tentativi\n")
    except Exception as e:
        print(f"❌ Test 1 FAILED: {e}\n")

def test_retry_rate_limit():
    """Test gestione rate limit"""
    print("Test 2: Gestione rate limit")

    attempt_count = {'count': 0}

    def rate_limited_function():
        attempt_count['count'] += 1
        if attempt_count['count'] < 2:
            raise RequestException("429 rate limit exceeded")
        return "Success after rate limit!"

    try:
        start = time.time()
        result = retry_with_backoff(rate_limited_function, max_retries=5, initial_wait=0.1, max_wait=1)
        elapsed = time.time() - start
        print(f"✅ Test 2 PASSED: {result} dopo {elapsed:.2f}s e {attempt_count['count']} tentativi\n")
    except Exception as e:
        print(f"❌ Test 2 FAILED: {e}\n")

def test_checkpoint():
    """Test checkpoint save/load"""
    print("Test 3: Checkpoint save/load")

    test_checkpoint_path = "/tmp/test_checkpoint.json"

    # Test save
    checkpoint_data = {
        'processed': 150,
        'metadata': ['file1.wav|text1', 'file2.wav|text2']
    }

    save_checkpoint(test_checkpoint_path, checkpoint_data)
    print(f"✅ Checkpoint salvato")

    # Test load
    loaded_checkpoint = load_checkpoint(test_checkpoint_path)

    if loaded_checkpoint['processed'] == 150 and len(loaded_checkpoint['metadata']) == 2:
        print(f"✅ Test 3 PASSED: Checkpoint caricato correttamente")
        print(f"   Processed: {loaded_checkpoint['processed']}")
        print(f"   Metadata entries: {len(loaded_checkpoint['metadata'])}\n")
    else:
        print(f"❌ Test 3 FAILED: Dati checkpoint non corrispondono\n")

    # Cleanup
    import os
    if os.path.exists(test_checkpoint_path):
        os.remove(test_checkpoint_path)

def test_max_retries_exceeded():
    """Test fallimento dopo max retries"""
    print("Test 4: Fallimento dopo max retries")

    attempt_count = {'count': 0}

    def always_failing_function():
        attempt_count['count'] += 1
        raise RequestException("Persistent error")

    try:
        retry_with_backoff(always_failing_function, max_retries=3, initial_wait=0.1, max_wait=1)
        print(f"❌ Test 4 FAILED: Doveva sollevare eccezione\n")
    except Exception as e:
        print(f"✅ Test 4 PASSED: Fallito dopo {attempt_count['count']} tentativi come previsto")
        print(f"   Errore: {str(e)[:50]}...\n")

if __name__ == "__main__":
    print("="*60)
    print("  TEST RETRY LOGIC E CHECKPOINT SYSTEM")
    print("="*60)
    print()

    test_retry_success()
    test_retry_rate_limit()
    test_checkpoint()
    test_max_retries_exceeded()

    print("="*60)
    print("  TUTTI I TEST COMPLETATI")
    print("="*60)
