from flask import Flask, request, send_file
import subprocess
import os
import traceback

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download_audio():
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return {"error": "Falta la URL"}, 400
        
    output_file = "audio_output.mp3"
    
    if os.path.exists(output_file):
        os.remove(output_file)

    try:
        # Ejecutamos yt-dlp y capturamos la salida detallada de error si falla
        result = subprocess.run([
            "yt-dlp", 
            "--extract-audio", 
            "--audio-format", "mp3",
            "--extractor-args", "youtube:player_client=android",
            "-o", output_file, 
            url
        ], capture_output=True, text=True, check=True)
        
        if os.path.exists(output_file):
            return send_file(output_file, as_attachment=True, download_name="song.mp3")
        else:
            return {"error": "El archivo no se generó físicamente"}, 500
            
    except subprocess.CalledProcessError as e:
        # Esto nos devolverá el error exacto de yt-dlp en el JSON que ve tu app
        error_detalles = e.stderr if e.stderr else e.stdout
        return {"error": f"Fallo yt-dlp: {error_detalles}"}, 500
    except Exception as e:
        return {"error": f"Error general: {str(e)}"}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
