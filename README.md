# Ollama model exporter

This script exports a model from your ollama installation into a tar file. This makes it possible to transfer models between machines without re-downloading from the Internet
or going through the process of setting up a local Ollama registry.

## Exporting a model

`python3 ollama_export_model.py MANIFEST_FILE TAR_FILE`

* **MANIFEST_FILE** is a model's manifest file in your ollama models directory, for example `~/.ollama/models/manifests/huggingface.co/unsloth/gemma-3n-E4B-it-GGUF/Q4_K_XL`.
   Browse your `.ollama/models/manifests` directory to find the right manifest file for the model to be exported.
* **TAR_FILE** The name of the tar file where the model is exported to.

## Importing a model

Transfer the tar file to the target system, then run (replace **TAR_FILE** and `~/.ollama` if needed):

`tar -xf TAR_FILE -C ~/.ollama`

Now the model should be visible in `ollama ls` and work with `ollama run MODEL` without any downloading.
