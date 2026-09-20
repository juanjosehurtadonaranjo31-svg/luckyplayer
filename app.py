from flask import Flask, request, send_file
import subprocess
import os

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download_audio():
    data = request.get_json()
    if not data or 'url' not in data:
        return {"error": "Falta la URL en la petición JSON"}, 400
        
    url = data.get('url')
    output_file = "audio_output.mp3"
    
    # Limpiar archivo previo si existe
    if os.path.exists(output_file):
        os.remove(output_file)

    try:
        # Comando ligero y optimizado para evitar caídas por memoria en Render
        result = subprocess.run([
            "yt-dlp",
            "--extract-audio",
            "--audio-format", "mp3",
            "--audio-quality", "5",
            "--cookies", "cookies.txt",
            "--extractor-args", "youtube:player_client=web",
            "--no-playlist",
            "-o", output_file,
            url
        ], capture_output=True, text=True, timeout=90)
        
        # Manejo de errores simplificado y directo
        if result.returncode != 0:
            error_msg = result.stderr or result.stdout or "Error desconocido"
            return {"error": f"Fallo yt-dlp: {error_msg}"}, 500
        
        if os.path.exists(output_file):
            return send_file(output_file, as_attachment=True, download_name="song.mp3")
        else:
            return {"error": "El archivo de audio no se generó físicamente en el servidor"}, 500
            
    except subprocess.TimeoutExpired:
        return {"error": "La descarga tardó demasiado tiempo (Timeout)."}, 504
    except Exception as e:
        return {"error": f"Error general: {str(e)}"}, 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
