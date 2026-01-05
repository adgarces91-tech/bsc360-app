import requests

# PEGA TU API KEY AQUÍ
API_KEY = "AIzaSyAZ9SHYWV14RsWqkmJW0BOaTDF1z5CRbsk"

print("🔍 Consultando a Google qué modelos están disponibles para esta llave...")

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"

try:
    response = requests.get(url)
    data = response.json()
    
    if "models" in data:
        print("\n✅ ¡Tu llave funciona! Puede ver estos modelos:")
        for m in data["models"]:
            print(f" - {m['name']}")
            if "generateContent" in m["supportedGenerationMethods"]:
                print(f"   (Soporta generación de texto: SÍ)")
    else:
        print("\n❌ Tu llave conecta, pero NO ve ningún modelo. Respuesta:")
        print(data)

except Exception as e:
    print(f"Error de conexión: {e}")