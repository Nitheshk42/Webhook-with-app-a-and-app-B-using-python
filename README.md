# Secure Webhook Implementation: App-to-App Communication

A production-ready webhook system demonstrating secure inter-application communication using HMAC-SHA256 signature verification. This project teaches how real-world systems like GitHub, Stripe, and AWS communicate securely.

![Webhook Architecture](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![Security](https://img.shields.io/badge/Security-HMAC--SHA256-green?style=flat-square)
![Deployment](https://img.shields.io/badge/Deployment-Railway-0B0D0E?style=flat-square&logo=railway)

---

## 📖 Table of Contents

- [Overview](#overview)
- [For Beginners](#for-beginners)
- [For Intermediate Developers](#for-intermediate-developers)
- [For Enterprise](#for-enterprise)
- [Real-World Scenarios](#real-world-scenarios)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Security](#security)
- [Deployment](#deployment)

---

## Overview

This project demonstrates how **two independent applications communicate securely** in real-time using webhooks. When something happens in App B (sender), it automatically notifies App A (receiver) with cryptographically signed proof of authenticity.

**Key Concepts:**
- **Webhooks:** Event-driven communication via HTTP POST
- **Signatures:** HMAC-SHA256 hashing for authentication
- **Public URLs:** Railway deployment for internet-accessible endpoints

---

## For Beginners

### What is a Webhook?

Think of webhooks like **subscription notifications**:

```mermaid
graph LR
    A["📱 You Subscribe to News"] --> B["📰 Newspaper Office"]
    B --> C["📧 News Delivered to Your Door"]
    
    style A fill:#e1f5ff
    style B fill:#fff3e0
    style C fill:#f3e5f5
```

**Traditional way (you ask):**
- You call the newspaper office every morning asking "Any news today?"
- Wasteful - most calls return "No news"

**Webhook way (they tell you):**
- Newspaper sends you news automatically when something happens
- Efficient - you're only notified when relevant

### Real Example: GitHub Webhooks

When you push code to GitHub:
```
1. You: git push origin main
2. GitHub: "Something happened! Let me notify the webhook URL"
3. Your CI/CD Server: Receives notification → Runs tests automatically
4. You: See test results without checking manually
```

### How It Works (Step-by-Step)

```mermaid
sequenceDiagram
    participant User as User (Developer)
    participant AppB as App B<br/>(Sender)
    participant URL as Public URL
    participant AppA as App A<br/>(Receiver)
    
    User->>AppB: Types "user_created"
    AppB->>AppB: Create Event JSON
    AppB->>AppB: Generate HMAC Signature
    AppB->>URL: POST /webhook + Signature
    URL->>AppA: Forward Request
    AppA->>AppA: Verify Signature
    AppA->>AppA: Process Event
    AppA-->>User: Log: Event Received ✅
```

### Key Learning: Signatures Prove Identity

Imagine you receive a letter claiming to be from your bank:

**Without Signature (Insecure):**
```
Letter: "Dear Customer, send us $1000"
(Could be anyone!)
```

**With Signature (Secure):**
```
Letter: "Dear Customer, send us $1000"
Signature: A1B2C3D4E5 (only your bank knows how to make this)
You verify: Does signature match? YES → Trust the letter
```

Webhooks work the same way!

---

## For Intermediate Developers

### HMAC-SHA256: The Security Engine

**What it does:**
```
Secret Key + Event Data → HMAC Algorithm → Unique Signature
"my_secret_key_123" + '{"data":"hello"}' → a1b2c3d4e5f6...
```

**Why it's secure:**

1. **One-way function:** Can't reverse signature to get SECRET
2. **Deterministic:** Same input always produces same signature
3. **Tamper-proof:** Change even 1 character → completely different signature

```mermaid
graph TD
    A["Event Payload<br/>{'data':'hello'}"] --> B["+ Secret Key<br/>my_secret_key_123"]
    B --> C["HMAC-SHA256"]
    C --> D["Signature<br/>a1b2c3d4e5f6..."]
    
    E["Modified Payload<br/>{'data':'hacked'}"] --> F["+ Same Secret Key"]
    F --> G["HMAC-SHA256"]
    G --> H["Different Signature!<br/>f9e8d7c6b5a4..."]
    
    style D fill:#90ee90
    style H fill:#ffcccb
```

### Verification Flow

**App B (Sender):**
```
1. event_json = '{"action":"user_created","id":123}'
2. signature = HMAC-SHA256(SECRET, event_json)
3. POST to /webhook with Header: X-Signature=signature
```

**App A (Receiver):**
```
1. Receive: X-Signature header + request body
2. Calculate: expected = HMAC-SHA256(SECRET, received_body)
3. Compare: received_signature == expected?
   YES → Process event
   NO  → Reject (401 Unauthorized)
```

### Security Threat Scenarios

| Threat | Attack | Defense |
|--------|--------|---------|
| **Unauthorized access** | Attacker sends webhook to URL | Signature fails - needs SECRET |
| **Payload tampering** | Attacker modifies event data | Signature changes - detected |
| **Replay attacks** | Same event sent twice | Future: Add timestamp |
| **Man-in-the-middle** | Intercept and modify request | HTTPS + signature verification |

### Code Structure

```python
# app_a.py - Receiver
@app.route('/webhook', methods=['POST'])
def webhook():
    signature = request.headers.get('X-Signature')
    payload = request.get_data()
    
    # Verify
    expected = HMAC-SHA256(SECRET, payload)
    if signature != expected:
        return 401  # Reject
    
    process_event(request.get_json())
    return 200  # Accept
```

---

## For Enterprise

### Production Architecture

```mermaid
graph TB
    subgraph "On-Premise"
        AppB["App B<br/>(Event Producer)"]
    end
    
    subgraph "Cloud (Railway)"
        LB["Load Balancer"]
        AppA1["App A Instance 1"]
        AppA2["App A Instance 2"]
        Queue["Event Queue"]
        DB["Database"]
    end
    
    AppB -->|HTTPS + Signature| LB
    LB --> AppA1
    LB --> AppA2
    AppA1 --> Queue
    AppA2 --> Queue
    Queue --> DB
    
    style AppB fill:#fff3e0
    style LB fill:#e1f5ff
    style Queue fill:#f3e5f5
    style DB fill:#c8e6c9
```

### Compliance & Monitoring

**Security Standards:**
- ✅ TLS 1.2+ (HTTPS only)
- ✅ HMAC-SHA256 signature verification
- ✅ Audit logging of all requests
- ✅ Secret rotation every 90 days
- ✅ Rate limiting (100 req/min per IP)

**Monitoring Metrics:**
```
- Signature verification failures (alert: >5/min)
- Response latency (alert: >2s)
- Error rate (alert: >1%)
- Queue depth (alert: >1000)
```

### Scalability Considerations

1. **Asynchronous Processing**
   - Don't process webhooks synchronously
   - Queue events → process in background
   - Return 200 immediately

2. **Idempotency**
   - Track request IDs
   - Prevent duplicate processing
   - Handle retries safely

3. **Retry Strategy**
   - Exponential backoff: 1s, 2s, 4s, 8s, 16s
   - Max 5 retries
   - Dead letter queue for failures

---

## Real-World Scenarios

### Scenario 1: E-Commerce Order Processing

```mermaid
graph LR
    A["Customer Places Order<br/>on Website"] --> B["Order Service<br/>App B"]
    B -->|Webhook: order_created| C["Email Service<br/>App A"]
    C --> D["📧 Confirmation Email Sent"]
    
    style A fill:#fff3e0
    style B fill:#e1f5ff
    style C fill:#f3e5f5
    style D fill:#c8e6c9
```

**What happens:**
1. Customer buys item on website
2. Website (App B) creates order event
3. Website sends webhook to Email Service (App A)
4. Email Service receives verified event
5. Automatically sends confirmation email
6. Customer gets email within seconds

**Why webhooks?**
- No polling database (wasteful)
- Real-time notifications (fast)
- Decoupled services (flexible)

### Scenario 2: CI/CD Pipeline

```mermaid
graph LR
    A["Developer Pushes Code<br/>git push"] --> B["GitHub<br/>App B"]
    B -->|Webhook: push| C["Jenkins CI<br/>App A"]
    C --> D["🧪 Tests Run"]
    C --> E["📦 Build App"]
    C --> F["🚀 Deploy"]
    
    style A fill:#fff3e0
    style B fill:#e1f5ff
    style C fill:#f3e5f5
```

**What happens:**
1. Developer pushes code to GitHub
2. GitHub automatically sends webhook
3. Jenkins CI receives and verifies webhook
4. Tests run automatically
5. If tests pass → auto-deploy
6. Developer sees results without manual intervention

**Benefits:**
- Faster feedback loop
- No manual triggering
- Catches bugs immediately

### Scenario 3: Payment Processing

```mermaid
graph LR
    A["Customer Makes Payment<br/>Stripe"] --> B["Stripe<br/>App B"]
    B -->|Webhook: payment_success| C["Your App<br/>App A"]
    C --> D["Update Order Status"]
    C --> E["Send Receipt"]
    C --> F["Unlock Content"]
    
    style A fill:#fff3e0
    style B fill:#e1f5ff
    style C fill:#f3e5f5
```

**Why Stripe uses webhooks:**
- Immediate payment confirmation
- Update inventory in real-time
- Send receipts automatically
- All without polling

---

## Quick Start

### Prerequisites
```bash
- Python 3.8+
- pip
- Two terminal windows
```

### Installation

```bash
git clone <your-repo>
cd webhook-app
pip install -r requirements.txt
```

### Local Testing

**Terminal 1 - Start receiver:**
```bash
python app_a.py
# Output: Running on http://127.0.0.1:3000
```

**Terminal 2 - Start sender:**
```bash
python app_b.py
# Output: Enter change (or 'quit'):
```

**Type in Terminal 2:**
```
Enter change (or 'quit'): user_created
```

**See in Terminal 1:**
```
✅ Verified webhook from App B: {'action': 'user_input', 'data': 'user_created'}
```

### Test Security

```bash
python test_invalid.py
# Should show: 401 Unauthorized (signature rejected)
```

---

## Project Structure

```
webhook-app/
├── README.md                    # This file
├── app_a.py                     # Webhook receiver
├── app_b.py                     # Webhook sender
├── test_invalid.py              # Security test
├── requirements.txt             # Dependencies
├── Procfile                     # Railway deployment
└── docs/
    ├── ARCHITECTURE.md
    ├── SECURITY.md
    └── DEPLOYMENT.md
```

---

## Security

### ✅ What's Protected

- **Signature Verification:** HMAC-SHA256 proves authenticity
- **Payload Integrity:** Any change detected immediately
- **Secret Management:** Never transmitted over network
- **HTTPS:** All production traffic encrypted

### ⚠️ Threat Model

| Threat | Mitigation |
|--------|-----------|
| Unauthorized webhook | Signature fails |
| Modified payload | Hash mismatch detected |
| URL exposure | Without SECRET, can't create valid signature |
| Replay attacks | Future: Add timestamp validation |

### 🔒 Best Practices

```python
# ✅ DO
SECRET = os.getenv('WEBHOOK_SECRET')  # Environment variable
app.run(ssl_context='adhoc')           # HTTPS only

# ❌ DON'T
SECRET = "hardcoded_key"               # Exposed in git
app.run(debug=True)                    # Production mode
```

---

## Deployment

### Deploy to Railway

```bash
# 1. Push to GitHub
git add .
git commit -m "Production ready"
git push origin main

# 2. Connect to Railway
# Visit railway.app → Create Project → Deploy from GitHub

# 3. Set environment variables
# WEBHOOK_SECRET = your-production-secret

# 4. Get public URL
# https://webhook-app-production.up.railway.app
```

### Update App B for Production

```python
# Change from localhost to Railway URL
url = "https://webhook-app-production.up.railway.app/webhook"
```

---

## Learning Outcomes

After this project, you'll understand:

✅ How webhooks enable real-time event communication
✅ Why HMAC signatures are essential for security
✅ How to verify webhook authenticity in production
✅ How to deploy web applications to the cloud
✅ Real-world patterns used by GitHub, Stripe, AWS

---

## Resources

- [HMAC Specification](https://tools.ietf.org/html/rfc4868)
- [GitHub Webhook Security](https://docs.github.com/en/developers/webhooks-and-events/webhooks/securing-your-webhooks)
- [Stripe Webhook Best Practices](https://stripe.com/docs/webhooks)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

## Next Steps

1. Deploy both App A and App B to Railway
2. Add timestamp validation to prevent replay attacks
3. Implement webhook retry logic with exponential backoff
4. Add database persistence for received events
5. Build a dashboard to monitor webhook status

---

## Author

Created to teach secure webhook implementation for beginners to enterprise developers.

**Topics Covered:**
- Event-driven architecture
- Cryptographic authentication
- Cloud deployment
- Production best practices

---

## License

MIT License - Feel free to use for learning and projects.

---

**Last Updated:** June 2024 | **Status:** Production Ready
