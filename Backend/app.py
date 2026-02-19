from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Realtime Picture Animation Backend is Running!"

@app.route('/animate', methods=['POST'])
def animate():
    try:
        image = request.files.get('image')
        audio = request.files.get('audio')

        if image is None or audio is None:
            return jsonify({"error": "Please provide both image and audio"}), 400

        img_path = os.path.join("temp", image.filename)
        audio_path = os.path.join("temp", audio.filename)
        os.makedirs("temp", exist_ok=True)
        image.save(img_path)
        audio.save(audio_path)

        # Placeholder for model output
        output_path = "temp/output.mp4"

        return jsonify({"output": output_path})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)