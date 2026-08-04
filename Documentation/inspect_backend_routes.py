import urllib.request
import json
import ssl

def inspect_routes():
    backend_url = "https://balajikrishnan031-keffi-backend.hf.space"
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    print("=== INSPECTING HUGGING FACE BACKEND API ROUTES ===")
    
    # Test openapi.json
    try:
        req = urllib.request.Request(f"{backend_url}/openapi.json")
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print("[OPENAPI SCHEMA FOUND!]:")
            paths = list(data.get("paths", {}).keys())
            print("Available Endpoints:", paths)
            return paths
    except Exception as e:
        print(f"[OPENAPI CHECK FAILED]: {e}")

    # Test common endpoint paths
    endpoints_to_test = [
        "/",
        "/health",
        "/api/chat",
        "/chat",
        "/api/predict",
        "/predict",
        "/api/v1/chat",
        "/api/session"
    ]

    for ep in endpoints_to_test:
        try:
            req = urllib.request.Request(f"{backend_url}{ep}")
            with urllib.request.urlopen(req, context=ctx, timeout=5) as resp:
                print(f"Endpoint '{ep}' -> STATUS {resp.status}")
        except urllib.error.HTTPError as e:
            print(f"Endpoint '{ep}' -> STATUS {e.code}")
        except Exception as e:
            print(f"Endpoint '{ep}' -> ERROR {e}")

if __name__ == "__main__":
    inspect_routes()
