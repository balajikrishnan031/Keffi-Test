import os
import shutil
import subprocess

def deploy_to_hf():
    print("=== DEPLOYING KEFFI BACKEND TO HUGGING FACE SPACE ===")

    src_dir = r"e:\Keffi Ai\Platform\Backend"
    hf_dir = r"e:\Keffi Ai\Platform\hf_space_temp"

    if not os.path.exists(hf_dir):
        print("Cloning Hugging Face Space repository...")
        subprocess.run(['git', 'clone', 'https://huggingface.co/spaces/Balajikrishnan031/Keffi-Backend', hf_dir], check=True)

    # Copy files from src_dir to hf_dir
    ignore_items = ['.git', '__pycache__', '.env', '.venv']
    for item in os.listdir(src_dir):
        if item in ignore_items:
            continue
        s = os.path.join(src_dir, item)
        d = os.path.join(hf_dir, item)
        if os.path.isdir(s):
            if os.path.exists(d):
                shutil.rmtree(d)
            shutil.copytree(s, d)
        else:
            shutil.copyfile(s, d)

    print("[SUCCESS] Files copied to hf_space_temp")

    # Replace Neffi -> Keffi across text files in hf_space_temp
    for root, dirs, files in os.walk(hf_dir):
        if '.git' in root:
            continue
        for fname in files:
            ext = os.path.splitext(fname)[1].lower()
            if ext in ['.py', '.json', '.md', '.html', '.txt', '.Dockerfile']:
                fpath = os.path.join(root, fname)
                try:
                    with open(fpath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    new_content = content.replace('Neffi', 'Keffi').replace('neffi', 'keffi')
                    if new_content != content:
                        with open(fpath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"Updated Neffi -> Keffi in: {fname}")
                except Exception as e:
                    print(f"Error updating {fname}: {e}")

    # Commit and push to Hugging Face
    print("Git adding and committing to Hugging Face Space...")
    subprocess.run(['git', 'add', '.'], cwd=hf_dir, check=True)
    
    commit_res = subprocess.run(['git', 'commit', '-m', 'Update Keffi Clinical AI Backend with Keffi branding and live API endpoints'], cwd=hf_dir, capture_output=True, text=True)
    print("Commit Output:", commit_res.stdout or commit_res.stderr)

    push_res = subprocess.run(['git', 'push', 'origin', 'main'], cwd=hf_dir, capture_output=True, text=True)
    print("Push Output STDOUT:", push_res.stdout)
    print("Push Output STDERR:", push_res.stderr)

    print("=== DEPLOYMENT COMPLETED ===")

if __name__ == "__main__":
    deploy_to_hf()
