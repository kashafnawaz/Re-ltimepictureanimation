# Real-Time Picture Animation & Cartoonification

A backend pipeline that converts a static image + audio into an anime-style talking video.

## Pipeline
1. **SadTalker** → generates talking face video from image + audio
2. **AnimeGANv2** → stylizes video into anime style
3. **ffmpeg** → merges audio into final video

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | Home |
| POST | /generate | Upload image + audio, start pipeline |
| GET | /status/{job_id} | Check job progress |
| GET | /result/{job_id}/sadtalker | Get talking video |
| GET | /result/{job_id}/final | Get final anime video |

## Setup Instructions

### 1. Clone the repo
```
git clone https://github.com/kashafnawaz/Re-ltimepictureanimation.git
cd Re-ltimepictureanimation
```

### 2. Create virtual environment
```
cd Backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Download checkpoints
Download these files and place in `Backend/checkpoints/`:
- epoch_20.pth
- audio2pose_00140-model.pth
- audio2exp_00300-model.pth
- mapping_00109-model.pth.tar
- mapping_00229-model.pth.tar
- facevid2vid_00189-model.pth
- wav2lip.pth
- shape_predictor_68_face_landmarks.dat

### 4. Setup AnimeGANv2 conda environment
```
conda create -n animegan_env python=3.7
conda activate animegan_env
pip install tensorflow==1.15 opencv-python tqdm
```

### 5. Run the API
```
cd Backend
venv\Scripts\activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 6. Open API docs
```
http://localhost:8000/docs
```

## Project Structure
```
RealtimePictureAnimation/
├── Backend/
│   ├── main.py          ← FastAPI server
│   ├── app.py           ← Pipeline orchestration
│   ├── workers/
│   │   ├── sadtalker.py ← SadTalker integration
│   │   └── animegan.py  ← AnimeGANv2 integration
│   └── requirements.txt
├── models/
│   ├── SadTalker/       ← SadTalker model
│   └── AnimeGANv2/      ← AnimeGANv2 model
└── Frontend/            ← Frontend (separate team)
```

## Team
- Backend & AI Pipeline: Kashaf
- Frontend: Team member
- Database: Team member