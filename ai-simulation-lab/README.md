# AI Simulation Lab
Progetto personale di Alessio Cogoni, sviluppato con supporto AI.

Laboratorio locale di resilienza per API AI. Python 3.11+, nessuna dipendenza esterna.

## Avvio
```sh
python -m unittest -v
python app.py
```
Aprire http://127.0.0.1:8000. Per inferenza reale impostare HF_TOKEN e HF_MODEL nelle variabili d'ambiente (modello compatibile con il provider). Non pubblicare il token. Le richieste possono comportare costi.

Riferimento: https://huggingface.co/docs/inference-providers/tasks/chat-completion

## Limiti
I 12 scenari sono simulazioni deterministiche, non stress test reali. Il fallback segnala il problema, non genera risposte AI offline. I test usano risposte API simulate. Il server è destinato all'uso locale, non alla produzione. Non è garantita l'assenza di errori.
