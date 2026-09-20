from flask import Flask, request, send_file
import subprocess
import os

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download_audio():
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return {"error": "Falta la URL"}, 400
        
    output_file = "audio_output.mp3"
    
    # Limpiamos archivo anterior si existe
    if os.path.exists(output_file):
        os.remove(output_file)

    try:
        # Ejecuta yt-dlp con el cliente de Android en el servidor de Render
        subprocess.run([
            "yt-dlp", 
            "--extract-audio", 
            "--audio-format", "mp3",
            "--extractor-args", "youtube:player_client=android",
            "-o", output_file, 
            url
        ], check=True)
        
        if os.path.exists(output_file):
            return send_file(output_file, as_attachment=True, download_name="song.mp3")
        else:
            return {"error": "No se pudo generar el archivo"}, 500
            
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
