import argparse
import json
import pathlib
import re
import tarfile

parser = argparse.ArgumentParser()
parser.add_argument("manifest_path", type=str)
parser.add_argument("outfile", type=str)
args = parser.parse_args()

manifest_path = pathlib.Path(args.manifest_path).absolute()
manifest_path_parts = manifest_path.parts
manifest_path_part_ollama = max(
        i for i, p in enumerate(manifest_path_parts)
        if p == ".ollama")
base_path_parts = manifest_path_parts[:manifest_path_part_ollama + 1]
base_path = pathlib.Path(*base_path_parts)
print(f"Detected base path: '{base_path}'")

print(f"Loading manifest file: '{manifest_path}'")
manifest = json.loads(open(manifest_path).read())

digests = []

digests.append(manifest["config"]["digest"])
for layer in manifest["layers"]:
    digests.append(layer["digest"])

blobs_path = base_path.joinpath(pathlib.Path("models", "blobs"))

blobs = []
for digest in digests:
    file_name = re.sub(r"(sha256):(\w+)", r"\1-\2", digest)
    file_path = blobs_path.joinpath(file_name)
    blobs.append(file_path)
print(f"Detected {len(blobs)} blob files in manifest.")

in_files = [manifest_path]
in_files += blobs

assert(all(f.is_file() for f in in_files))
print(f"Including {len(in_files)} files into tar archive:")

outfile = pathlib.Path(args.outfile)
with tarfile.open(outfile, "w") as tar:
    for i, in_file in enumerate(in_files):
        file_size = in_file.stat().st_size
        arcname = in_file.relative_to(base_path)
        print(f"Including file {i+1}/{len(in_files)}: "
                f"{arcname} ({file_size} bytes)")
        tar.add(in_file, arcname=arcname)

assert(outfile.is_file() and outfile.stat().st_size > 0)
print(f"Created tar file {outfile} ({outfile.stat().st_size} bytes)")
