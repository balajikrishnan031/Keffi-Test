def sync_n8n_flow():
    """Sync groq_engine.py system prompt → n8n flow JSON"""
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    try:
        with open(os.path.join(BASE_DIR, 'groq_engine.py'), encoding='utf-8') as f:
            src = f.read()
        match = re.search(r'KEFFI_SYSTEM_PROMPT = """(.*?)"""', src, re.DOTALL)
        system_prompt = match.group(1) if match else "Keffi Clinical System Prompt"

        n8n_file_path = os.path.join(BASE_DIR, 'n8n_workflows', 'keffi_groq_flow.json')
        if os.path.exists(n8n_file_path):
            with open(n8n_file_path, encoding='utf-8') as f:
                flow = json.load(f)

            for node in flow.get('nodes', []):
                if node.get('name') == 'Groq Llama-3 API':
                    escaped_prompt = system_prompt.replace('\n', '\\n').replace('"', '\\"')
                    json_body_str = (
                        "={\n"
                        '  "model": "llama-3.3-70b-versatile",\n'
                        '  "messages": [\n'
                        '    {\n'
                        '      "role": "system",\n'
                        f'      "content": "{escaped_prompt}"\n'
                        '    },\n'
                        '    {\n'
                        '      "role": "user",\n'
                        '      "content": "[Context: {{ $json.body.context }}]\\n\\nPatient says: {{ $json.body.message }}"\n'
                        '    }\n'
                        '  ],\n'
                        '  "temperature": 0.35,\n'
                        '  "max_tokens": 500\n'
                        '}'
                    )
                    node['parameters']['jsonBody'] = json_body_str
                    break

            with open(n8n_file_path, 'w', encoding='utf-8') as f:
                json.dump(flow, f, indent=2, ensure_ascii=False)
            return {"status": "n8n flow synced successfully", "file": n8n_file_path}
    except Exception as e:
        return {"status": "n8n sync deferred", "error": str(e)}

if __name__ == "__main__":
    print(sync_n8n_flow())
