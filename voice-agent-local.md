# FREE LOCAL VOICE AGENT SETUP

## Architecture: 100% Free, Unlimited Calls

**Stack:**
- **Asterisk** (free PBX, handles calls)
- **Google Voice** (free US number + unlimited incoming)
- **Whisper** (free speech-to-text, local)
- **TTS (piper/coqui)** (free text-to-speech, local)
- **LLM (Ollama)** (free AI brain, local qwen3.5)

**Cost:** $0/month, unlimited outbound calls via Google Voice

---

## STEP 1: Install Asterisk (PBX)

```bash
sudo apt update
sudo apt install -y asterisk asterisk-config asterisk-modules
sudo systemctl enable asterisk
sudo systemctl start asterisk
```

---

## STEP 2: Connect Google Voice (Free Outbound)

**Google Voice setup:**
1. Create Google Voice account (voice.google.com)
2. Get free US phone number
3. Enable "Google Voice for G Suite" or use Obihai adapter ($40 one-time, connects GV to Asterisk)

**Alternative (100% free but hacky):**
- Use Linphone/SIP client with Google Voice
- Route through Asterisk via SIP trunk

**Config:** `/etc/asterisk/pjsip.conf`
```ini
[googlevoice]
type=endpoint
context=outbound
disallow=all
allow=ulaw
auth=googlevoice-auth
aors=googlevoice

[googlevoice-auth]
type=auth
auth_type=userpass
username=YOUR_GOOGLE_VOICE_NUMBER
password=YOUR_APP_PASSWORD

[googlevoice]
type=aor
contact=sip:YOUR_GV_NUMBER@sip.google.com
```

---

## STEP 3: Install Whisper (Speech-to-Text)

```bash
pip install openai-whisper
# Download base model (faster, good enough for calls)
whisper --model base --help
```

**Or faster option (whisper.cpp):**
```bash
git clone https://github.com/ggerganov/whisper.cpp
cd whisper.cpp
make
./main -m models/ggml-base.en.bin -f audio.wav
```

---

## STEP 4: Install Piper TTS (Text-to-Speech)

```bash
wget https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_amd64.tar.gz
tar -xvzf piper_amd64.tar.gz
./piper --model en_US-lessac-medium --output_file output.wav < input.txt
```

**Voice models:**
- en_US-lessac-medium (professional male)
- en_US-ljspeech-high (clear female)

---

## STEP 5: Build Call Handler Script

**Location:** `/home/andrew/.openclaw/workspace/voice-agent.py`

```python
#!/usr/bin/env python3
import sys
import subprocess
import json
from asterisk.agi import AGI

# Initialize Asterisk AGI
agi = AGI()

def transcribe_audio(audio_file):
    """Use Whisper to transcribe caller speech"""
    result = subprocess.run(
        ['whisper', audio_file, '--model', 'base', '--language', 'en', '--output_format', 'txt'],
        capture_output=True, text=True
    )
    return result.stdout.strip()

def generate_response(user_text):
    """Use Ollama to generate AI response"""
    prompt = f"""You are a professional business development representative for Sorensen Group Corporation.
You are calling to offer AI automation services.

Caller said: "{user_text}"

Respond naturally, professionally, and keep it under 30 words."""
    
    result = subprocess.run(
        ['ollama', 'run', 'qwen3.5:9b-q4_K_M', prompt],
        capture_output=True, text=True
    )
    return result.stdout.strip()

def speak(text):
    """Convert text to speech and play to caller"""
    # Generate audio with Piper
    subprocess.run(
        ['./piper', '--model', 'en_US-lessac-medium', '--output_file', '/tmp/response.wav'],
        input=text.encode(), check=True
    )
    # Play audio to caller via Asterisk
    agi.stream_file('/tmp/response', escape_digits='')

def main():
    agi.answer()
    
    # Initial greeting
    speak("Hello, this is Andrew from Sorensen Group Corporation. We help businesses automate repetitive tasks with AI. Do you have a minute to talk?")
    
    # Listen for response (record 5 seconds)
    agi.appexec('Record', '/tmp/caller_response.wav,5,5')
    
    # Transcribe
    user_text = transcribe_audio('/tmp/caller_response.wav')
    
    # Generate AI response
    response = generate_response(user_text)
    
    # Speak response
    speak(response)
    
    # Continue conversation loop (add more turns as needed)
    
    agi.hangup()

if __name__ == '__main__':
    main()
```

---

## STEP 6: Asterisk Dialplan (Auto-dial Logic)

**Edit:** `/etc/asterisk/extensions.conf`

```ini
[outbound]
exten => _1NXXNXXXXXX,1,Answer()
 same => n,AGI(voice-agent.py)
 same => n,Hangup()

[autodial]
exten => s,1,Originate(PJSIP/${TARGET_NUMBER}@googlevoice,exten,outbound,_1${TARGET_NUMBER},1)
```

**Trigger call from command line:**
```bash
asterisk -rx "originate PJSIP/+15555551234@googlevoice extension s@autodial"
```

---

## STEP 7: OpenClaw Integration

**Create wrapper script:** `/home/andrew/.openclaw/workspace/make-call.sh`

```bash
#!/bin/bash
TARGET=$1
MESSAGE=$2

# Trigger Asterisk to dial
asterisk -rx "originate PJSIP/${TARGET}@googlevoice extension s@autodial"
```

**Make executable:**
```bash
chmod +x /home/andrew/.openclaw/workspace/make-call.sh
```

**Call from Watson:**
```bash
./make-call.sh "+15613376371" "Testing local voice agent"
```

---

## COST BREAKDOWN

| Component | Cost | Notes |
|-----------|------|-------|
| Asterisk | $0 | Open source |
| Google Voice | $0 | Free US number + unlimited calls |
| Whisper | $0 | Local transcription |
| Piper TTS | $0 | Local synthesis |
| Ollama/Qwen | $0 | Local AI |
| **TOTAL** | **$0/month** | **Unlimited calls** |

**Optional (one-time):**
- Obihai adapter: $40 (easier Google Voice integration)
- Better microphone: $20-50 (if call quality poor)

---

## LIMITATIONS & FIXES

**Issue:** Google Voice may block automated calls
**Fix:** Use SIP trunk provider with pay-as-you-go ($0.01/min, still 100x cheaper than Twilio)

**Issue:** Whisper transcription slow
**Fix:** Use whisper.cpp (10x faster) or Deepgram API (first 12K min/month free)

**Issue:** Call quality poor
**Fix:** Adjust Asterisk codec settings (use G.711 ulaw)

---

## INSTALL NOW? (30-45 minutes)

**Yes:** I'll guide you step-by-step
**Later:** I'll run overnight text automation instead, we'll add voice tomorrow

**Your call (literally).**
