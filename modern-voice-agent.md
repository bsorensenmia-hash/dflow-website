# MODERN FREE VOICE AGENT - 2026 BEST PRACTICES

## Architecture: State-of-the-Art Free Stack

**Components:**
1. **Vapi.ai / Bland.ai** (free tier) - turnkey voice agents
2. **Twilio Free Trial** ($15 credit, ~300 calls)
3. **Retell AI** (open source, self-hosted)
4. **OpenAI Realtime API** (voice-to-voice, lowest latency)
5. **VLLM + Whisper** (local, unlimited, slower but free)

**BEST OPTION FOR NOW: Twilio Free Trial → Then Transition**

---

## IMMEDIATE: TWILIO FREE TRIAL SETUP (5 minutes, 300 free calls)

### Step 1: Create Twilio Account
```bash
# Open in browser:
https://www.twilio.com/try-twilio

# Sign up with:
- Email: andrew@sorensengroup.com (or personal)
- Phone: 561-337-6371
```

**You get:**
- $15 credit (free)
- ~300 outbound calls (at $0.05/min)
- 1 free phone number

### Step 2: Get Credentials
After signup, grab:
- Account SID (starts with AC...)
- Auth Token (hidden, click to reveal)
- Phone number (buy free number in dashboard)

### Step 3: Configure OpenClaw
```bash
openclaw config patch plugins.entries.voice-call.config '{
  "provider": "twilio",
  "twilio": {
    "accountSid": "AC...",
    "authToken": "...",
    "fromNumber": "+1..."
  }
}'
```

### Step 4: Test Call
```bash
openclaw voicecall call --to "+15613376371" --message "Testing Twilio integration from Watson"
```

**This gets us operational in 5 minutes.**

---

## NEXT: FREE UNLIMITED CALLS (After $15 runs out)

### Option A: Vapi.ai (Easiest, Free Tier)

**Features:**
- 100 free minutes/month
- Modern voice AI (< 1 second latency)
- Built-in LLM, TTS, STT
- Web dashboard + API

**Setup:**
```bash
# Sign up: vapi.ai
# Get API key
# Test call via API:
curl -X POST https://api.vapi.ai/call \
  -H "Authorization: Bearer YOUR_KEY" \
  -d '{
    "phoneNumber": "+15613376371",
    "assistant": {
      "firstMessage": "Hi, this is Andrew from Sorensen Group. Do you have a minute?",
      "model": {
        "provider": "openai",
        "model": "gpt-4o-realtime"
      }
    }
  }'
```

**Cost after free tier:** $0.10/min (still cheaper than Twilio)

---

### Option B: Retell AI (Open Source, Self-Hosted)

**Why:** Unlimited free calls, full control, modern architecture

**Setup:**
```bash
# Clone repo
git clone https://github.com/RetellAI/retell-backend-node-demo
cd retell-backend-node-demo

# Install dependencies
npm install

# Configure (uses your Deepgram + OpenAI keys)
export DEEPGRAM_API_KEY="your_key"  # Free tier: 12K min/month
export OPENAI_API_KEY="your_key"

# Run
npm start
```

**Frontend (make calls):**
```bash
# Use Retell's web client or integrate with Twilio
# Incoming calls → Retell processes → AI responds
```

**Cost:** $0 (if using free tiers of Deepgram + OpenAI Whisper API)

---

### Option C: OpenAI Realtime API (Lowest Latency)

**Best for:** High-quality conversational AI

**Features:**
- Voice-to-voice (no STT/TTS lag)
- < 500ms response time
- Native function calling

**Cost:** $0.06/min input, $0.24/min output (~$0.30/min total)

**Setup:**
```python
import openai
from twilio.rest import Client

# Make call via Twilio
client = Client(account_sid, auth_token)
call = client.calls.create(
    to="+15613376371",
    from_=twilio_number,
    url="https://yourserver.com/voice"  # TwiML endpoint
)

# TwiML endpoint streams audio to OpenAI Realtime API
# OpenAI processes voice → responds in real-time
```

**Best balance:** Quality + cost + latency

---

### Option D: 100% Free Local (Whisper + Piper + Ollama)

**When to use:** After exhausting all free tiers, or for dev/testing

**Stack:**
- **Speech-to-Text:** Whisper.cpp (local, fast)
- **LLM:** Ollama qwen3.5:9b (local, free)
- **Text-to-Speech:** Piper (local, natural voice)
- **Call handling:** SIP.js + FreeSWITCH (open source PBX)

**Setup time:** 1-2 hours
**Cost:** $0
**Limitation:** Higher latency (~2-3 seconds response time)

---

## RECOMMENDED PATH

**Phase 1 (Now - Next 300 calls):**
✅ Use Twilio free trial ($15 credit)
✅ Integrate with OpenClaw voice-call plugin
✅ Test with FL business calls

**Phase 2 (After free trial):**
✅ Switch to Vapi.ai free tier (100 min/month)
✅ Or use Retell AI (self-hosted, unlimited)
✅ Or OpenAI Realtime API ($0.30/min, best quality)

**Phase 3 (Scale):**
✅ Build local stack (Whisper + Piper + Ollama)
✅ Zero marginal cost
✅ Unlimited calls

---

## WHAT TO DO RIGHT NOW

1. **Create Twilio account** (5 min) → you do this
2. **Get credentials** → paste them here
3. **I configure OpenClaw** (1 min)
4. **Test call to your phone** (verify it works)
5. **Start calling FL businesses** (tonight)

**Ready to start? Create Twilio account now:**
https://www.twilio.com/try-twilio
