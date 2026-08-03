import os
import shutil
import subprocess
import requests

def full_push():
    print("=== FULL SYNC & PUSH TO HUGGINGFACE SPACE: Balajikrishnan031/Keffi-Backend ===")

    src_dir = r"e:\Keffi Ai\Platform\Backend"
    hf_dir = r"e:\Keffi Ai\Platform\hf_space_temp"

    if not os.path.exists(hf_dir):
        print("Cloning Hugging Face Space repository...")
        subprocess.run(['git', 'clone', 'https://huggingface.co/spaces/Balajikrishnan031/Keffi-Backend', hf_dir], check=True)

    # 1. Copy all backend files
    ignore_items = ['.git', '__pycache__', '.env', '.venv']
    for item in os.listdir(src_dir):
        if item in ignore_items:
            continue
        s = os.path.join(src_dir, item)
        d = os.path.join(hf_dir, item)
        if os.path.isdir(s):
            if os.path.exists(d):
                shutil.rmtree(d)
            shutil.copytree(s, d, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        else:
            shutil.copyfile(s, d)

    print("[SUCCESS] All local backend files copied to hf_space_temp")

    # 2. Global Replacement of Neffi -> Keffi across text files
    replaced_count = 0
    for root, dirs, files in os.walk(hf_dir):
        if '.git' in root:
            continue
        for fname in files:
            ext = os.path.splitext(fname)[1].lower()
            if ext in ['.py', '.json', '.md', '.html', '.txt', '.dockerfile', '.yml', '.yaml'] or fname == 'Dockerfile':
                fpath = os.path.join(root, fname)
                try:
                    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    new_content = content.replace('Neffi', 'Keffi').replace('neffi', 'keffi')
                    if new_content != content:
                        with open(fpath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        replaced_count += 1
                        print(f"  [REPLACED BRANDING] {fname}")
                except Exception as e:
                    print(f"  [ERROR] {fname}: {e}")

    print(f"[SUCCESS] Checked and replaced branding in {replaced_count} files.")

    # 3. Git Add, Commit, Push
    subprocess.run(['git', 'add', '.'], cwd=hf_dir, check=True)
    
    status_res = subprocess.run(['git', 'status', '--porcelain'], cwd=hf_dir, capture_output=True, text=True)
    if not status_res.stdout.strip():
        print("[NOTE] All backend files are already 100% up-to-date on HuggingFace Space main branch!")
    else:
        print("[GIT CHANGES DETECTED]:")
        print(status_res.stdout.strip())
        
        commit_res = subprocess.run(['git', 'commit', '-m', 'Full Keffi Clinical AI Backend Engine Sync to HuggingFace Space Balajikrishnan031/Keffi-Backend'], cwd=hf_dir, capture_output=True, text=True)
        print("[COMMIT RESULT]:", commit_res.stdout)

        push_res = subprocess.run(['git', 'push', 'origin', 'main'], cwd=hf_dir, capture_output=True, text=True)
        print("[PUSH STDOUT]:", push_res.stdout)
        print("[PUSH STDERR]:", push_res.stderr)

    # 4. Verify Live Endpoint Status
    print("\n=== VERIFYING LIVE HUGGING FACE BACKEND ENDPOINT ===")
    try:
        url = "https://balajikrishnan031-keffi-backend.hf.space/"
        resp = requests.get(url, timeout=10)
        print(f"[HTTP {resp.status_code}] Response from {url}:")
        print(resp.text)
    except Exception as e:
        print("[LIVE VERIFICATION NOTE]:", e)

    print("\n=== FULL HUGGINGFACE SPACE PUSH COMPLETE ===")

if __name__ == "__main__":
    full_push()
