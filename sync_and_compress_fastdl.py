import os
import shutil
import bz2
import glob
import subprocess

CSTRIKE = r"c:\Games\Counter-Strike 1.6 Russian\CS16_Mini_Skin_System\CS16_Server_Ready\cstrike"
FASTDL = r"c:\Games\Counter-Strike 1.6 Russian\CS16_FastDL_Pack"

print("[FASTDL SYNC] Starting full asset audit and bz2 compression...")

def compress_bz2(src_path, dst_bz2_path):
    with open(src_path, 'rb') as f_in:
        data = f_in.read()
    compressed = bz2.compress(data, compresslevel=9)
    with open(dst_bz2_path, 'wb') as f_out:
        f_out.write(compressed)

# 1. Sync all WAD files
wad_files = glob.glob(os.path.join(CSTRIKE, "*.wad")) + glob.glob(os.path.join(CSTRIKE, "*.WAD"))
print(f"Found {len(wad_files)} WAD files to process...")

for src in wad_files:
    fname = os.path.basename(src)
    dst_raw = os.path.join(FASTDL, fname)
    dst_bz2 = dst_raw + ".bz2"
    
    # Copy raw if not exists or different size
    if not os.path.exists(dst_raw) or os.path.getsize(dst_raw) != os.path.getsize(src):
        shutil.copy2(src, dst_raw)
        print(f"  [RAW] Copied {fname}")
        
    # Compress bz2 if not exists or raw is newer
    if not os.path.exists(dst_bz2) or os.path.getmtime(dst_bz2) < os.path.getmtime(src):
        compress_bz2(src, dst_bz2)
        print(f"  [BZ2] Compressed {fname}.bz2 ({os.path.getsize(dst_bz2)/1024/1024:.2f} MB)")

# 2. Sync all Maps and .res and .txt files
map_extensions = ["*.bsp", "*.res", "*.txt"]
for ext in map_extensions:
    for src in glob.glob(os.path.join(CSTRIKE, "maps", ext)):
        fname = os.path.basename(src)
        dst_raw = os.path.join(FASTDL, "maps", fname)
        dst_bz2 = dst_raw + ".bz2"
        os.makedirs(os.path.dirname(dst_raw), exist_ok=True)
        
        if not os.path.exists(dst_raw) or os.path.getsize(dst_raw) != os.path.getsize(src):
            shutil.copy2(src, dst_raw)
            print(f"  [MAP RAW] {fname}")
            
        if fname.endswith(".bsp") or fname.endswith(".res"):
            if not os.path.exists(dst_bz2) or os.path.getmtime(dst_bz2) < os.path.getmtime(src):
                compress_bz2(src, dst_bz2)
                print(f"  [MAP BZ2] {fname}.bz2")

# 3. Sync Models, Sounds, Sprites, Overviews
folders = ["models", "sound", "sprites", "overviews", "gfx"]
for folder in folders:
    src_folder = os.path.join(CSTRIKE, folder)
    if not os.path.exists(src_folder):
        continue
    for root, dirs, files in os.walk(src_folder):
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in [".mdl", ".wav", ".mp3", ".spr", ".bmp", ".tga", ".txt"]:
                src_path = os.path.join(root, f)
                rel_path = os.path.relpath(src_path, CSTRIKE)
                dst_raw = os.path.join(FASTDL, rel_path)
                dst_bz2 = dst_raw + ".bz2"
                os.makedirs(os.path.dirname(dst_raw), exist_ok=True)
                
                # Copy raw
                if not os.path.exists(dst_raw) or os.path.getsize(dst_raw) != os.path.getsize(src_path):
                    shutil.copy2(src_path, dst_raw)
                    
                # Compress bz2
                if ext in [".mdl", ".wav", ".spr", ".tga", ".bmp"]:
                    if not os.path.exists(dst_bz2) or os.path.getmtime(dst_bz2) < os.path.getmtime(src_path):
                        compress_bz2(src_path, dst_bz2)

print("[FASTDL SYNC] Audit and compression finished successfully!")
