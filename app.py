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
    
    # Limpiamos archivo anterior si existe en el entorno
    if os.path.exists(output_file):
        os.remove(output_file)

    try:
        # Ejecutamos yt-dlp usando las cookies y omitiendo el cliente android para evitar conflictos
        result = subprocess.run([
            "yt-dlp", 
            "--extract-audio", 
            "--audio-format", "mp3",
            "--cookies", "cookies.txt",  # Utiliza tus cookies autenticadas
            "-o", output_file, 
            url
        ], capture_output=True, text=True, check=True)
        
        if os.path.exists(output_file):
            return send_file(output_file, as_attachment=True, download_name="song.mp3")
        else:
            return {"error": "El archivo de audio no se generó físicamente en el servidor"}, 500
            
    except subprocess.CalledProcessError as e:
        error_detalles = e.stderr if e.stderr else e.stdout
        return {"error": f"Fallo yt-dlp: {error_detalles}"}, 500
    except Exception as e:
        return {"error": f"Error general: {str(e)}"}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
