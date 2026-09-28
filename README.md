# AI Rashed — Secure Backend (ধাপ ১)

Android অ্যাপ কখনো AI provider-এর সাথে সরাসরি কথা বলবে না:

    Android অ্যাপ → এই সার্ভার (API key শুধু এখানে) → OpenAI → সার্ভার → অ্যাপ

> **অবস্থা:** কোড ও অফলাইন টেস্ট তৈরি এবং পাস (৩২/৩২)। কিন্তু **আসল AI দিয়ে কিছুই এখনো যাচাই হয়নি** — কারণ যাচাই করতে আপনার নিজের key লাগবে। নিচের "লাইভ টেস্ট" ধাপ শেষ না হওয়া পর্যন্ত কোনো ফিচারকে "working" ধরবেন না।

---

## ১. কোন API key লাগবে (মোট ১টি AI key)

| Key | কী কাজে | কোথা থেকে নেবেন |
|---|---|---|
| **OpenAI API key** | Chat, ছবি বোঝা, PDF/ফাইল বোঝা, ছবি তৈরি, ছবি এডিট — সব | platform.openai.com → API keys |

Anthropic (Claude) key **আর লাগে না**। শুধু `OPENAI_API_KEY` (আর অ্যাপ-সার্ভার টোকেন `APP_TOKENS`) থাকলেই সার্ভার পুরো চলে।
OpenAI-র GPT Image মডেল ব্যবহারে আপনার OpenAI অ্যাকাউন্টে **API Organization Verification** লাগতে পারে (OpenAI ডক অনুযায়ী)। না করা থাকলে ছবি তৈরির সময় `provider_auth_error` আসবে।
OpenAI ড্যাশবোর্ডে **মাসিক খরচের সীমা (spend limit)** বেঁধে রাখুন। ব্যালেন্স/কোটা শেষ হলে সার্ভার `quota_exceeded` error দেবে।

## ২. কোন সুবিধা কোন provider/model দিয়ে হবে

| সুবিধা | Endpoint | Provider / API | Model (ডিফল্ট) |
|---|---|---|---|
| Real AI chat | `POST /v1/chat` | OpenAI Responses API | `gpt-4o` |
| ছবি বোঝা (image understanding) | `POST /v1/chat` + image attachment | OpenAI Responses API (`input_image`) | `gpt-4o` |
| PDF / টেক্সট ফাইল বোঝা | `POST /v1/chat` + attachment | OpenAI Responses API (`input_file`) | `gpt-4o` |
| ছবি তৈরি | `POST /v1/images/generate` | OpenAI Image API | `gpt-image-2` |
| ছবি এডিট | `POST /v1/images/edit` | OpenAI Image API | `gpt-image-2` |
| কোন সুবিধা চালু আছে | `GET /health` | — | — |

### Model ID কীভাবে যাচাই করা হয়েছে
- **`gpt-4o`** — OpenAI-র অফিসিয়াল ফাইল/PDF ইনপুট ডকে ছবি ও PDF সাপোর্টকারী (vision) model হিসেবে উল্লেখ আছে (developers.openai.com/api/docs/guides/file-inputs)। ⚠️ তবে OpenAI নিজে এখন নতুন GPT-5.6 পরিবার (`gpt-5.6-*`) সুপারিশ করছে, এবং deprecations পেজে `gpt-4o`-র কিছু পুরোনো snapshot (যেমন `gpt-4o-2024-05-13`, শাটডাউন ২০২৬-১০-২৩) আছে। সাধারণ `gpt-4o` নামের জন্য আমি কোনো ঘোষিত শাটডাউন তারিখ পাইনি, কিন্তু এটা বদলাতে পারে। আপনি চাইলে `.env`-এ `CHAT_MODEL` বদলে নতুন model দিতে পারেন (vision + PDF সাপোর্ট থাকতে হবে) — কোড বদলাতে হবে না। বদলানোর পর `check_models.py` ও `live_check.py` আবার চালান।
- **`gpt-image-2`** — OpenAI-র অফিসিয়াল Models ডকে (developers.openai.com/api/docs/models/gpt-image-2) তালিকাভুক্ত: তাদের state-of-the-art ছবি মডেল, generation ও editing দুটোই সাপোর্ট করে। এজন্য তৈরি ও এডিট দুটোতেই একই model ব্যবহার হচ্ছে।
- ⚠️ **সতর্কতা:** OpenAI-র model নাম দ্রুত বদলায়, এবং কোন model আপনার অ্যাকাউন্টে খোলা তা verification-এর ওপর নির্ভর করে। তাই **নিজের key দিয়ে `scripts/check_models.py` চালিয়ে নিশ্চিত হোন** (নিচে)।
- **অপশনাল:** `CHAT_PROVIDER=anthropic` দিলে Chat আবার Claude (`claude-sonnet-5`) দিয়ে চলবে; তখন `ANTHROPIC_API_KEY` লাগবে। ডিফল্টে এটা বন্ধ, দরকার নেই।

## ৩. Environment variable-এর নাম

| নাম | দরকার | মন্তব্য |
|---|---|---|
| `OPENAI_API_KEY` | ✅ | Chat, ছবি বোঝা, PDF, ছবি তৈরি/এডিট |
| `APP_TOKENS` | ✅ | অ্যাপ↔সার্ভার গোপন টোকেন (কমা দিয়ে একাধিক)। না থাকলে সার্ভার সব `/v1/*` বন্ধ রাখে |
| `CHAT_PROVIDER` | ঐচ্ছিক | ডিফল্ট `openai` |
| `IMAGE_PROVIDER` | ঐচ্ছিক | ডিফল্ট `openai` |
| `CHAT_MODEL` | ঐচ্ছিক | ডিফল্ট `gpt-4o` |
| `IMAGE_GENERATE_MODEL` | ঐচ্ছিক | ডিফল্ট `gpt-image-2` |
| `IMAGE_EDIT_MODEL` | ঐচ্ছিক | ডিফল্ট `gpt-image-2` |
| `RATE_LIMIT_PER_MIN` | ঐচ্ছিক | ডিফল্ট 20 |
| `MAX_OUTPUT_TOKENS` | ঐচ্ছিক | ডিফল্ট 4096 |
| `ANTHROPIC_API_KEY` | ঐচ্ছিক | শুধু `CHAT_PROVIDER=anthropic` করলে |

## ৪. নিজে নিরাপদে secret কনফিগার করার নিয়ম

**নিয়ম ১: কোনো key কখনো চ্যাটে, ইমেইলে, স্ক্রিনশটে বা কোডে দেবেন না।** (আমাকেও নয়।)

**লোকাল কম্পিউটারে:**
1. এই ফোল্ডারে গিয়ে ফাইল কপি করুন: `cp .env.example .env` (Windows: `copy .env.example .env`)
2. `.env` ফাইলটি নিজের টেক্সট এডিটরে খুলে `=` এর পরে নিজের key দুটো বসান, সেভ করুন।
3. `APP_TOKENS`-এর জন্য এই কমান্ডের ফলাফল বসান:
   `python -c "import secrets;print(secrets.token_urlsafe(32))"`
4. `.env` ইতিমধ্যে `.gitignore`-এ আছে, তাই git-এ উঠবে না।

**অনলাইন সার্ভারে (Render/Railway ইত্যাদি):** `.env` ফাইল আপলোড করবেন না। প্ল্যাটফর্মের **Environment Variables** পেজে একই নামে মান বসান। Start command: `gunicorn run:app`। শুধু HTTPS ব্যবহার করুন।

**key ফাঁস হলে:** সাথে সাথে ওই provider-এর ড্যাশবোর্ডে key মুছে নতুন বানান, তারপর `.env`/প্ল্যাটফর্মে বদলান।

## ৫. লাইভ টেস্ট — ধাপে ধাপে

```
pip install -r requirements.txt

# ধাপ ক: model ID আপনার অ্যাকাউন্টে আছে কি না (key স্ক্রিনে ছাপা হয় না)
python scripts/check_models.py

# ধাপ খ: সার্ভার চালু করুন (টার্মিনাল ১) — চলতে থাকবে
python run.py

# ধাপ গ: আসল AI টেস্ট (টার্মিনাল ২, একই ফোল্ডারে)
BASE_URL=http://localhost:5000 python scripts/live_check.py
```
Windows PowerShell-এ ধাপ গ: `$env:BASE_URL="http://localhost:5000"; python scripts/live_check.py`

`live_check.py` আপনার নির্ধারিত টেস্টগুলো চালায়: 2+2, "হ্যালো", বাংলাদেশের রাজধানী (বাংলা ও English), follow-up context, ছবি তৈরি, ছবি বোঝা, ছবি এডিট, ভুল টোকেন ও খালি বার্তার error। প্রতিটির ফল `PASS/FAIL/SKIP`। সব SKIP হলে সেটা **সফল ধরা হয় না** (exit code 2)। ছবি তৈরি/এডিটের ফল `generated_sample.png` ও `edited_sample.png` ফাইলে সেভ হয় — নিজের চোখে দেখে নিশ্চিত হোন। PDF টেস্ট করতে: `PDF_PATH=/আপনার/ফাইল.pdf` যোগ করুন।

ফলাফল (শুধু PASS/FAIL লাইনগুলো, key ছাড়া) আমাকে পাঠালে পরের ধাপ ঠিক করব।

## ৬. অফলাইন টেস্ট (key ছাড়াই চলে)
`python tests/test_backend.py` — ৩২টি টেস্ট: auth, rate limit, ফাইল যাচাই, provider-এর সব ধরনের ব্যর্থতা (timeout, 429, ব্যালেন্স শেষ, 5xx, ভুল key, model নেই, খালি উত্তর, refusal), provider বদলানোর যোগ্যতা, এবং project audit (কোডে localhost/পুরোনো endpoint/key নেই)। এগুলো *নকল network লেয়ার* ব্যবহার করে — এগুলো আসল AI টেস্ট নয়।

## ৭. Provider বদলানো
`app/providers/base.py`-তে `ChatProvider` ও `ImageProvider` চুক্তি আছে। নতুন provider (যেমন অন্য কোনো ছবি সার্ভিস) যোগ করতে: একটি class লিখুন → `app/providers/__init__.py`-র `CHAT_PROVIDERS` / `IMAGE_PROVIDERS`-এ নাম বসান → `.env`-এ `CHAT_PROVIDER` / `IMAGE_PROVIDER` বদলান। routes, validation বা Android অ্যাপে কোনো পরিবর্তন লাগে না।

## ৮. API সংক্ষেপে (Android-এর জন্য)
সব `/v1/*` অনুরোধে header: `Authorization: Bearer <APP_TOKEN>`

- **Chat:** `{"messages":[{"role":"user","content":"...","attachments":[{"mime":"image/png","name":"a.png","data":"<base64>"}]}]}` → `{"reply","model","usage","truncated"}`। আগের সব message পাঠালে context কাজ করে। Attachment: PNG/JPEG/GIF/WebP, PDF, text/plain, text/markdown, text/csv।
- **ছবি তৈরি:** `{"prompt":"...","size":"1024x1024"}` (size ঐচ্ছিক) → `{"image_base64","mime","model"}`
- **ছবি এডিট:** multipart — `image` (PNG/JPEG/WebP) + `prompt`
- **Error:** সবসময় `{"error":{"code","message","retryable"}}`। Codes: invalid_request 400 · unauthorized 401 · too_large 413 · unsupported_type 415 · rate_limited 429 · content_blocked 400 · not_configured 503 · provider_auth_error 503 · model_unavailable 503 · network_error 502 · upstream_error 502 · empty_response 502 · image_generation_failed 502 · timeout 504

## ৯. নিরাপত্তা — সৎ অবস্থা
- ✅ API key শুধু সার্ভারের environment-এ; কোডে কোনো key/localhost/পুরোনো endpoint নেই (টেস্টে স্বয়ংক্রিয় যাচাই); `.env.example`-এ কোনো মান নেই।
- ✅ সার্ভারে টোকেন কনফিগার না থাকলে সব endpoint বন্ধ (secure by default)।
- ✅ ফাইলের আসল ধরন (magic bytes), সাইজ, সংখ্যা যাচাই; error-এ কোনো secret বা thinking-এর লেখা বেরোয় না।
- ⚠️ `APP_TOKEN` অ্যাপে রাখলে APK খুলে বের করা সম্ভব। এটা শুধু এলোমেলো ট্রাফিক আটকায়। প্রকৃত ব্যবহারকারী আলাদা করতে পরে লগইন (যেমন Firebase Auth) লাগবে।
- ⚠️ Rate limit সার্ভারের মেমোরিতে (একটি instance-এর জন্য); একাধিক instance-এ Redis লাগবে। Proxy-র পেছনে চালালে client IP সঠিকভাবে পেতে proxy সেটিং লাগতে পারে।

## ১০. Render-এ deploy করা

দুটো ফাইল আছে:
- **`render.yaml`** — Render Blueprint। Render ড্যাশবোর্ডে "New +" → "Blueprint" বেছে এই প্রজেক্ট দিন। Build ও start command এমনিই সেট হয়ে যাবে।
- **`Procfile`** — Blueprint ছাড়া সাধারণ Web Service বানালে Render নিজে থেকেই এটা পড়ে start command বুঝে নেয়।

**Build command:** `pip install -r requirements.txt`
**Start command:** `gunicorn run:app` (`run.py`-র `app` অবজেক্ট, যেটা `create_app()` থেকে তৈরি)

কোনো পদ্ধতিতেই `render.yaml`/`Procfile`-এ কোনো key নেই। Deploy করার পর Render ড্যাশবোর্ডে **Environment** ট্যাবে গিয়ে সেকশন ৩-এর ভেরিয়েবলগুলো (`OPENAI_API_KEY`, `APP_TOKENS` ইত্যাদি) নিজে বসান — এগুলো কখনো repo/zip-এ যাবে না। বসানোর পর Render নিজে থেকে redeploy করবে।

Deploy হওয়ার পর যাচাই: আপনার Render URL দিয়ে `BASE_URL=https://আপনার-অ্যাপ.onrender.com python scripts/live_check.py` চালান (সেকশন ৫)।

⚠️ Render-এর Free/Starter প্ল্যানে নিষ্ক্রিয় থাকলে সার্ভার ঘুমিয়ে পড়তে পারে (প্রথম অনুরোধে কিছুটা দেরি হবে) — এটা কোডের বাগ নয়, প্ল্যানের সীমা।

## এখনো নেই (ইচ্ছাকৃত)
Streaming, লগইন, conversation সেভ, voice, web search।
