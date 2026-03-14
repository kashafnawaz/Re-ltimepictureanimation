# Teammates Guide - Real-Time Picture Animation API

## Base URL
http://KASHAF_IP:8000
> Ask Kashaf for her laptop IP address when testing together

---

## FRONTEND TEAM GUIDE

### Step 1 - Upload Image + Audio
POST http://KASHAF_IP:8000/generate
Content-Type: multipart/form-data

Fields:
- image: (jpg/png file)
- audio: (wav/mp3 file)

Response:
{
  "job_id": "abc12345",
  "status": "started"
}
Save the job_id — you need it for next steps!

---

### Step 2 - Check Progress
GET http://KASHAF_IP:8000/status/{job_id}

Response:
{
  "job_id": "abc12345",
  "status": "running_sadtalker"
}

Status values:
- started              = Job created
- running_sadtalker    = Generating talking video
- sadtalker_completed  = Talking video ready
- running_animegan     = Applying anime style
- completed            = Final video ready
- failed               = Something went wrong

Poll this endpoint every 10 seconds to update progress bar!

---

### Step 3 - Get SadTalker Video (optional preview)
GET http://KASHAF_IP:8000/result/{job_id}/sadtalker
Returns the talking face video (before anime style)

---

### Step 4 - Get Final Anime Video
GET http://KASHAF_IP:8000/result/{job_id}/final
Returns the final anime-style talking video

---

### Complete Frontend Flow
1. User uploads image + audio
2. Call POST /generate → get job_id
3. Every 10 seconds call GET /status/{job_id}
4. When status = "sadtalker_completed" → show preview video
5. When status = "completed" → show download button
6. User clicks download → GET /result/{job_id}/final

---

### JavaScript Example
const formData = new FormData();
formData.append('image', imageFile);
formData.append('audio', audioFile);

const response = await fetch('http://KASHAF_IP:8000/generate', {
  method: 'POST',
  body: formData
});
const { job_id } = await response.json();

const interval = setInterval(async () => {
  const res = await fetch(`http://KASHAF_IP:8000/status/${job_id}`);
  const { status } = await res.json();

  if (status === 'sadtalker_completed') {
    videoElement.src = `http://KASHAF_IP:8000/result/${job_id}/sadtalker`;
  }

  if (status === 'completed') {
    clearInterval(interval);
    downloadBtn.href = `http://KASHAF_IP:8000/result/${job_id}/final`;
    downloadBtn.style.display = 'block';
  }

  if (status === 'failed') {
    clearInterval(interval);
    alert('Something went wrong!');
  }
}, 10000);

---

## DATABASE TEAM GUIDE

Your endpoints (independent):
- POST /register  → save user to database
- POST /login     → return token to frontend

Coordinate with Kashaf:
- What token format you use after login
- Kashaf will add one line in /generate to verify token

---

## Processing Time
- SadTalker  = ~1 hour (CPU)
- AnimeGANv2 = ~7 minutes (CPU)
- Total      = ~1 hour 10 minutes

---

## Contact
For any API issues contact: Kashaf