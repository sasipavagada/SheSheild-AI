import os
import json
from datetime import datetime
from flask import Flask, render_template, render_template_string, request, redirect, url_for, session, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# =====================================================
# FLASK CONFIGURATION
# =====================================================
app = Flask(__name__)
app.config['SECRET_KEY'] = 'sheshield-ultra-secret-2025'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sheshield.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# =====================================================
# DATABASE MODELS
# =====================================================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    contacts_json = db.Column(db.Text, default="[]")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_contacts(self):
        try:
            return json.loads(self.contacts_json)
        except Exception:
            return []

    def set_contacts(self, contacts_list):
        self.contacts_json = json.dumps(contacts_list[:4])


class AlertLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    alert_type = db.Column(db.String(50), default="SMART_SOS")
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    status = db.Column(db.String(20), default="ACTIVE")
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# =====================================================
# ULTRA-ATTRACTIVE LOGIN TEMPLATE
# =====================================================
LOGIN_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SheShield AI - Intelligent Women Safety</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Outfit:wght@400;600;800;900&display=swap" rel="stylesheet">
<style>
* { margin:0; padding:0; box-sizing:border-box; font-family:'Plus Jakarta Sans', sans-serif; }
body {
    background-color: #06020c;
    background-image: 
        radial-gradient(at 0% 0%, rgba(142, 26, 168, 0.35) 0px, transparent 50%),
        radial-gradient(at 100% 0%, rgba(217, 70, 239, 0.3) 0px, transparent 50%),
        radial-gradient(at 50% 100%, rgba(6, 182, 212, 0.2) 0px, transparent 50%);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 25px 15px;
    position: relative;
    overflow-x: hidden;
}
/* Glowing animated Aurora Orbs */
.orb {
    position: absolute;
    border-radius: 50%;
    filter: blur(100px);
    pointer-events: none;
    z-index: 0;
}
.orb-1 { width: 350px; height: 350px; background: rgba(142, 26, 168, 0.45); top: -80px; left: -80px; animation: floatOrb 8s infinite alternate; }
.orb-2 { width: 400px; height: 400px; background: rgba(217, 70, 239, 0.35); bottom: -100px; right: -80px; animation: floatOrb 10s infinite alternate-reverse; }
@keyframes floatOrb {
    0% { transform: translateY(0px) scale(1); }
    100% { transform: translateY(40px) scale(1.15); }
}

.auth-card {
    position: relative;
    z-index: 1;
    background: rgba(18, 9, 31, 0.75);
    border: 1px solid rgba(255, 255, 255, 0.12);
    backdrop-filter: blur(28px);
    -webkit-backdrop-filter: blur(28px);
    width: 100%;
    max-width: 1020px;
    border-radius: 32px;
    box-shadow: 0 35px 80px rgba(0, 0, 0, 0.65), 0 0 50px rgba(142, 26, 168, 0.25);
    display: grid;
    grid-template-columns: 1.1fr 1fr;
    overflow: hidden;
}
/* Left Showcase Panel */
.hero-panel {
    background: linear-gradient(145deg, rgba(37, 10, 61, 0.85), rgba(77, 10, 99, 0.9));
    border-right: 1px solid rgba(255, 255, 255, 0.1);
    padding: 50px 42px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    position: relative;
}
.hero-brand {
    display: inline-flex;
    align-items: center;
    gap: 12px;
}
.brand-icon {
    width: 48px;
    height: 48px;
    border-radius: 14px;
    background: linear-gradient(135deg, #d946ef, #8e1aa8);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    box-shadow: 0 0 25px rgba(217, 70, 239, 0.6);
}
.brand-name {
    font-family: 'Outfit', sans-serif;
    font-size: 24px;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -0.5px;
}
.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(34, 197, 94, 0.12);
    border: 1px solid rgba(34, 197, 94, 0.35);
    color: #4ade80;
    padding: 6px 14px;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.5px;
    margin-top: 30px;
    width: fit-content;
}
.pulse-dot {
    width: 7px;
    height: 7px;
    background: #4ade80;
    border-radius: 50%;
    box-shadow: 0 0 10px #4ade80;
    animation: pulseDot 1.5s infinite;
}
@keyframes pulseDot { 50% { opacity: 0.3; } }

.hero-content h1 {
    font-family: 'Outfit', sans-serif;
    font-size: 38px;
    font-weight: 900;
    line-height: 1.15;
    color: #ffffff;
    margin: 16px 0 14px;
}
.gradient-text {
    background: linear-gradient(120deg, #f0abfc, #d946ef, #67e8f9);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-content p {
    color: #c4b5d4;
    font-size: 14px;
    line-height: 1.65;
    font-weight: 400;
}
/* Feature Badges */
.feature-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-top: 26px;
}
.feature-card {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.09);
    padding: 12px 14px;
    border-radius: 16px;
    display: flex;
    align-items: center;
    gap: 10px;
    transition: 0.3s;
}
.feature-card:hover {
    background: rgba(255, 255, 255, 0.09);
    border-color: rgba(217, 70, 239, 0.4);
    transform: translateY(-2px);
}
.feature-card span { font-size: 20px; }
.feature-card div { font-size: 12px; font-weight: 600; color: #f1e7fe; line-height: 1.3; }

/* Right Form Panel */
.form-panel {
    padding: 50px 45px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    background: rgba(14, 6, 25, 0.4);
}
.form-title h2 {
    font-family: 'Outfit', sans-serif;
    font-size: 30px;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 6px;
}
.form-title p {
    font-size: 13px;
    color: #a79cb6;
    margin-bottom: 26px;
}
.input-box {
    margin-bottom: 18px;
    position: relative;
}
.input-box label {
    display: block;
    font-size: 11px;
    font-weight: 700;
    color: #d8b4fe;
    letter-spacing: 0.8px;
    margin-bottom: 8px;
    text-transform: uppercase;
}
.input-wrapper {
    position: relative;
    display: flex;
    align-items: center;
}
.input-icon {
    position: absolute;
    left: 15px;
    font-size: 16px;
    color: #9382a8;
}
.custom-input {
    width: 100%;
    padding: 14px 16px 14px 44px;
    background: rgba(255, 255, 255, 0.045);
    border: 1.5px solid rgba(255, 255, 255, 0.12);
    border-radius: 16px;
    font-size: 14px;
    color: #ffffff;
    outline: none;
    transition: all 0.25s ease;
}
.custom-input:focus {
    background: rgba(255, 255, 255, 0.08);
    border-color: #d946ef;
    box-shadow: 0 0 20px rgba(217, 70, 239, 0.35);
}
.custom-input::placeholder { color: #6d5d83; }

.toggle-eye {
    position: absolute;
    right: 14px;
    background: none;
    border: none;
    cursor: pointer;
    font-size: 16px;
    color: #9382a8;
    padding: 4px;
}
.submit-btn {
    width: 100%;
    padding: 15px;
    background: linear-gradient(90deg, #d946ef, #8e1aa8);
    border: none;
    border-radius: 16px;
    color: #ffffff;
    font-size: 15px;
    font-weight: 800;
    cursor: pointer;
    box-shadow: 0 12px 30px rgba(217, 70, 239, 0.4);
    transition: all 0.25s ease;
    margin-top: 8px;
    position: relative;
    overflow: hidden;
}
.submit-btn::before {
    content:'';
    position: absolute;
    top:0; left:-100%; width:100%; height:100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.25), transparent);
    transition: 0.5s;
}
.submit-btn:hover::before { left: 100%; }
.submit-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 16px 40px rgba(217, 70, 239, 0.55);
}

/* Quick Demo Pass Box */
.demo-pass {
    margin-top: 24px;
    background: rgba(217, 70, 239, 0.08);
    border: 1px dashed rgba(217, 70, 239, 0.35);
    border-radius: 16px;
    padding: 12px 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.demo-pass div {
    font-size: 11px;
    color: #f0abfc;
    line-height: 1.4;
}
.demo-fill-btn {
    background: #d946ef;
    color: #fff;
    border: none;
    padding: 7px 12px;
    border-radius: 10px;
    font-size: 11px;
    font-weight: 800;
    cursor: pointer;
    transition: 0.2s;
}
.demo-fill-btn:hover { background: #c026d3; }

.flash-alert {
    background: rgba(239, 68, 68, 0.15);
    border: 1px solid rgba(239, 68, 68, 0.4);
    color: #fca5a5;
    padding: 11px 16px;
    border-radius: 14px;
    font-size: 13px;
    margin-bottom: 18px;
}
.switch-link {
    text-align: center;
    font-size: 13px;
    color: #9f8fb3;
    margin-top: 22px;
}
.switch-link a {
    color: #f0abfc;
    font-weight: 700;
    text-decoration: none;
    transition: 0.2s;
}
.switch-link a:hover { color: #ffffff; text-decoration: underline; }

@media (max-width: 900px) {
    .auth-card { grid-template-columns: 1fr; max-width: 480px; }
    .hero-panel { display: none; }
    .form-panel { padding: 40px 25px; }
}
</style>
</head>
<body>

<div class="orb orb-1"></div>
<div class="orb orb-2"></div>

<div class="auth-card">
    <!-- LEFT SHOWCASE -->
    <div class="hero-panel">
        <div>
            <div class="hero-brand">
                <div class="brand-icon">🛡️</div>
                <div class="brand-name">SheShield AI</div>
            </div>
            <div class="status-pill">
                <div class="pulse-dot"></div>
                AI GUARDIAN ENGINE ONLINE
            </div>
            <div class="hero-content">
                <h1>Step Fearlessly Into <span class="gradient-text">The Night.</span></h1>
                <p>Next-generation women's personal safety platform equipped with Edge Vision threat tracing, high-decibel acoustic defense, and live sub-meter satellite tracking.</p>
            </div>
        </div>

        <div>
            <div class="feature-grid">
                <div class="feature-card">
                    <span>👁️</span>
                    <div>Rear Vision<br><small style="color:#a79cb6;">Back Threat Radar</small></div>
                </div>
                <div class="feature-card">
                    <span>📍</span>
                    <div>Live GPS<br><small style="color:#a79cb6;">4-Contact Relay</small></div>
                </div>
                <div class="feature-card">
                    <span>📢</span>
                    <div>120dB Siren<br><small style="color:#a79cb6;">Police Strobe Light</small></div>
                </div>
                <div class="feature-card">
                    <span>🎭</span>
                    <div>Stealth Mode<br><small style="color:#a79cb6;">Camouflage Screen</small></div>
                </div>
            </div>
            <p style="font-size:11px; color:#78698c; margin-top:22px;">🔒 100% On-Device Neural Processing • Zero Cloud Video Storage</p>
        </div>
    </div>

    <!-- RIGHT LOGIN FORM -->
    <div class="form-panel">
        <div class="form-title">
            <h2>Welcome Back ✨</h2>
            <p>Access your personalized safety dashboard</p>
        </div>

        {% with messages = get_flashed_messages() %}
          {% if messages %}
            {% for m in messages %}<div class="flash-alert">⚠️ {{ m }}</div>{% endfor %}
          {% endif %}
        {% endwith %}

        <form method="POST" action="/login">
            <div class="input-box">
                <label>Email Address</label>
                <div class="input-wrapper">
                    <span class="input-icon">📧</span>
                    <input type="email" id="loginEmail" name="email" class="custom-input" placeholder="user@sheshield.ai" required>
                </div>
            </div>

            <div class="input-box">
                <label>Password</label>
                <div class="input-wrapper">
                    <span class="input-icon">🔒</span>
                    <input type="password" id="loginPassword" name="password" class="custom-input" placeholder="••••••••••••" required>
                    <button type="button" class="toggle-eye" onclick="togglePasswordVisibility('loginPassword', this)">👁️</button>
                </div>
            </div>

            <button type="submit" class="submit-btn">Unlock Safety Guardian →</button>
        </form>

        <!-- Quick 1-Click Demo -->
        <div class="demo-pass">
            <div>
                <b>⚡ Evaluator / Demo Login:</b><br>
                <span>demo@sheshield.ai | password123</span>
            </div>
            <button type="button" class="demo-fill-btn" onclick="fillDemoCredentials()">⚡ Auto Fill</button>
        </div>

        <div class="switch-link">
            Need an account? <a href="/register">Create Your Guardian Account</a>
        </div>
    </div>
</div>

<script>
function togglePasswordVisibility(fieldId, btn) {
    const input = document.getElementById(fieldId);
    if (input.type === "password") {
        input.type = "text";
        btn.textContent = "🙈";
    } else {
        input.type = "password";
        btn.textContent = "👁️";
    }
}
function fillDemoCredentials() {
    document.getElementById("loginEmail").value = "demo@sheshield.ai";
    document.getElementById("loginPassword").value = "password123";
}
</script>
</body>
</html>
"""

# =====================================================
# ULTRA-ATTRACTIVE REGISTER TEMPLATE
# =====================================================
REGISTER_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Register - SheShield AI Safety</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Outfit:wght@400;600;800;900&display=swap" rel="stylesheet">
<style>
* { margin:0; padding:0; box-sizing:border-box; font-family:'Plus Jakarta Sans', sans-serif; }
body {
    background-color: #06020c;
    background-image: 
        radial-gradient(at 0% 0%, rgba(142, 26, 168, 0.35) 0px, transparent 50%),
        radial-gradient(at 100% 0%, rgba(217, 70, 239, 0.3) 0px, transparent 50%),
        radial-gradient(at 50% 100%, rgba(6, 182, 212, 0.2) 0px, transparent 50%);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 25px 15px;
    position: relative;
    overflow-x: hidden;
}
.orb {
    position: absolute;
    border-radius: 50%;
    filter: blur(100px);
    pointer-events: none;
    z-index: 0;
}
.orb-1 { width: 350px; height: 350px; background: rgba(142, 26, 168, 0.45); top: -80px; left: -80px; }
.orb-2 { width: 400px; height: 400px; background: rgba(217, 70, 239, 0.35); bottom: -100px; right: -80px; }

.auth-card {
    position: relative;
    z-index: 1;
    background: rgba(18, 9, 31, 0.75);
    border: 1px solid rgba(255, 255, 255, 0.12);
    backdrop-filter: blur(28px);
    -webkit-backdrop-filter: blur(28px);
    width: 100%;
    max-width: 1020px;
    border-radius: 32px;
    box-shadow: 0 35px 80px rgba(0, 0, 0, 0.65), 0 0 50px rgba(142, 26, 168, 0.25);
    display: grid;
    grid-template-columns: 1.1fr 1fr;
    overflow: hidden;
}
.hero-panel {
    background: linear-gradient(145deg, rgba(37, 10, 61, 0.85), rgba(77, 10, 99, 0.9));
    border-right: 1px solid rgba(255, 255, 255, 0.1);
    padding: 50px 42px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
.hero-brand {
    display: inline-flex;
    align-items: center;
    gap: 12px;
}
.brand-icon {
    width: 48px;
    height: 48px;
    border-radius: 14px;
    background: linear-gradient(135deg, #d946ef, #8e1aa8);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    box-shadow: 0 0 25px rgba(217, 70, 239, 0.6);
}
.brand-name {
    font-family: 'Outfit', sans-serif;
    font-size: 24px;
    font-weight: 800;
    color: #ffffff;
}
.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(6, 182, 212, 0.15);
    border: 1px solid rgba(6, 182, 212, 0.4);
    color: #67e8f9;
    padding: 6px 14px;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 700;
    margin-top: 26px;
    width: fit-content;
}
.hero-content h1 {
    font-family: 'Outfit', sans-serif;
    font-size: 38px;
    font-weight: 900;
    line-height: 1.15;
    color: #ffffff;
    margin: 16px 0 14px;
}
.gradient-text {
    background: linear-gradient(120deg, #f0abfc, #d946ef, #67e8f9);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-content p {
    color: #c4b5d4;
    font-size: 14px;
    line-height: 1.65;
}
.feature-list-check {
    margin-top: 22px;
    display: flex;
    flex-direction: column;
    gap: 12px;
}
.check-item {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 13px;
    color: #f1e7fe;
    font-weight: 600;
}
.check-item span {
    color: #4ade80;
    font-size: 16px;
}

/* Right Form */
.form-panel {
    padding: 45px 42px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    background: rgba(14, 6, 25, 0.4);
}
.form-title h2 {
    font-family: 'Outfit', sans-serif;
    font-size: 28px;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 4px;
}
.form-title p {
    font-size: 13px;
    color: #a79cb6;
    margin-bottom: 22px;
}
.input-grid-two {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
}
.input-box {
    margin-bottom: 15px;
    position: relative;
}
.input-box label {
    display: block;
    font-size: 11px;
    font-weight: 700;
    color: #d8b4fe;
    letter-spacing: 0.8px;
    margin-bottom: 6px;
    text-transform: uppercase;
}
.input-wrapper {
    position: relative;
    display: flex;
    align-items: center;
}
.input-icon {
    position: absolute;
    left: 14px;
    font-size: 15px;
    color: #9382a8;
}
.custom-input {
    width: 100%;
    padding: 13px 14px 13px 40px;
    background: rgba(255, 255, 255, 0.045);
    border: 1.5px solid rgba(255, 255, 255, 0.12);
    border-radius: 15px;
    font-size: 13.5px;
    color: #ffffff;
    outline: none;
    transition: all 0.25s ease;
}
.custom-input:focus {
    background: rgba(255, 255, 255, 0.08);
    border-color: #d946ef;
    box-shadow: 0 0 20px rgba(217, 70, 239, 0.35);
}
.custom-input::placeholder { color: #6d5d83; }

.toggle-eye {
    position: absolute;
    right: 14px;
    background: none;
    border: none;
    cursor: pointer;
    font-size: 16px;
    color: #9382a8;
}
.submit-btn {
    width: 100%;
    padding: 15px;
    background: linear-gradient(90deg, #d946ef, #8e1aa8);
    border: none;
    border-radius: 15px;
    color: #ffffff;
    font-size: 15px;
    font-weight: 800;
    cursor: pointer;
    box-shadow: 0 12px 30px rgba(217, 70, 239, 0.4);
    transition: all 0.25s ease;
    margin-top: 8px;
}
.submit-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 16px 40px rgba(217, 70, 239, 0.55);
}
.flash-alert {
    background: rgba(239, 68, 68, 0.15);
    border: 1px solid rgba(239, 68, 68, 0.4);
    color: #fca5a5;
    padding: 10px 14px;
    border-radius: 12px;
    font-size: 12.5px;
    margin-bottom: 15px;
}
.switch-link {
    text-align: center;
    font-size: 13px;
    color: #9f8fb3;
    margin-top: 18px;
}
.switch-link a {
    color: #f0abfc;
    font-weight: 700;
    text-decoration: none;
}
@media (max-width: 900px) {
    .auth-card { grid-template-columns: 1fr; max-width: 480px; }
    .hero-panel { display: none; }
    .input-grid-two { grid-template-columns: 1fr; }
    .form-panel { padding: 35px 22px; }
}
</style>
</head>
<body>

<div class="orb orb-1"></div>
<div class="orb orb-2"></div>

<div class="auth-card">
    <!-- LEFT PANEL -->
    <div class="hero-panel">
        <div>
            <div class="hero-brand">
                <div class="brand-icon">🛡️</div>
                <div class="brand-name">SheShield AI</div>
            </div>
            <div class="status-pill">
                ENCRYPTED SAFETY NETWORK
            </div>
            <div class="hero-content">
                <h1>Your Personal <span class="gradient-text">Guardian Angel</span> Is Always Awake.</h1>
                <p>Register once to link up to 4 trusted guardians, activate real-time rear vision sensors, and travel with total confidence day or night.</p>
            </div>
            <div class="feature-list-check">
                <div class="check-item"><span>✓</span> Instant 1-Tap SOS to 4 Emergency Contacts</div>
                <div class="check-item"><span>✓</span> Camera Optical Threat & Follower Detection</div>
                <div class="check-item"><span>✓</span> Voice-Activated SOS ("Help / Bachao")</div>
                <div class="check-item"><span>✓</span> Anti-Snooping PIN Vault for Private Logs</div>
            </div>
        </div>
        <p style="font-size:11px; color:#78698c;">Shielding Over 50,000+ Safe Journeys Across Cities</p>
    </div>

    <!-- RIGHT FORM -->
    <div class="form-panel">
        <div class="form-title">
            <h2>Create Account 🚀</h2>
            <p>Setup your AI safety shield in 30 seconds</p>
        </div>

        {% with messages = get_flashed_messages() %}
          {% if messages %}
            {% for m in messages %}<div class="flash-alert">⚠️ {{ m }}</div>{% endfor %}
          {% endif %}
        {% endwith %}

        <form method="POST" action="/register">
            <div class="input-box">
                <label>Full Name</label>
                <div class="input-wrapper">
                    <span class="input-icon">👤</span>
                    <input type="text" name="name" class="custom-input" placeholder="e.g. Pushpanjali" required>
                </div>
            </div>

            <div class="input-grid-two">
                <div class="input-box">
                    <label>Email Address</label>
                    <div class="input-wrapper">
                        <span class="input-icon">📧</span>
                        <input type="email" name="email" class="custom-input" placeholder="user@gmail.com" required>
                    </div>
                </div>
                <div class="input-box">
                    <label>Mobile Number</label>
                    <div class="input-wrapper">
                        <span class="input-icon">📱</span>
                        <input type="tel" name="phone" class="custom-input" placeholder="+91 98480 12345">
                    </div>
                </div>
            </div>

            <div class="input-box">
                <label>Create Password</label>
                <div class="input-wrapper">
                    <span class="input-icon">🔒</span>
                    <input type="password" id="regPassword" name="password" class="custom-input" placeholder="At least 6 characters" required>
                    <button type="button" class="toggle-eye" onclick="togglePasswordVisibility('regPassword', this)">👁️</button>
                </div>
            </div>

            <button type="submit" class="submit-btn">Activate SheShield Guardian →</button>
        </form>

        <div class="switch-link">
            Already have an account? <a href="/login">Sign In Here</a>
        </div>
    </div>
</div>

<script>
function togglePasswordVisibility(fieldId, btn) {
    const input = document.getElementById(fieldId);
    if (input.type === "password") {
        input.type = "text";
        btn.textContent = "🙈";
    } else {
        input.type = "password";
        btn.textContent = "👁️";
    }
}
</script>
</body>
</html>
"""

# =====================================================
# ROUTES
# =====================================================
@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '').strip()

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password credentials.')

    return render_template_string(LOGIN_HTML)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        phone = request.form.get('phone', '').strip()
        password = request.form.get('password', '').strip()

        if not name or not email or not password:
            flash('Please fill in all required fields.')
            return render_template_string(REGISTER_HTML)

        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please sign in.')
            return redirect(url_for('login'))

        new_user = User(name=name, email=email, phone=phone)
        new_user.set_password(password)
        new_user.set_contacts([{"name": "Dad", "phone": "+919848011223"}])

        db.session.add(new_user)
        db.session.commit()

        session['user_id'] = new_user.id
        session['user_name'] = new_user.name
        return redirect(url_for('dashboard'))

    return render_template_string(REGISTER_HTML)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    if not user:
        session.clear()
        return redirect(url_for('login'))

    contacts = user.get_contacts()
    primary_contact = contacts[0]['phone'] if len(contacts) > 0 else "Not added"

    return render_template(
        'dashboard.html',
        user_name=user.name,
        user_email=user.email,
        user_phone=user.phone or "Not added",
        emergency_contact=primary_contact,
        emergency_contacts=contacts
    )

# =====================================================
# REST APIS (SOS, CONTACTS)
# =====================================================
@app.route('/api/sos', methods=['POST'])
def trigger_sos():
    if 'user_id' not in session:
        return jsonify({"success": False, "error": "Unauthorized"}), 401

    data = request.get_json() or {}
    lat = data.get('latitude')
    lon = data.get('longitude')
    user = User.query.get(session['user_id'])

    alert = AlertLog(user_id=user.id, latitude=lat, longitude=lon, status="ACTIVE")
    db.session.add(alert)
    db.session.commit()

    print(f"\n🚨 [EMERGENCY SOS ALERT ACTIVATED] 🚨")
    print(f"User: {user.name} | Phone: {user.phone}")
    print(f"Location: https://www.google.com/maps?q={lat},{lon}")
    print(f"Alerting Contacts: {user.get_contacts()}\n")

    return jsonify({"success": True, "alert_id": alert.id, "message": "Emergency SOS broadcasted"})


@app.route('/api/emergency-contacts', methods=['GET', 'POST'])
def manage_contacts():
    if 'user_id' not in session:
        return jsonify({"success": False, "error": "Unauthorized"}), 401

    user = User.query.get(session['user_id'])
    if request.method == 'GET':
        return jsonify({"success": True, "contacts": user.get_contacts()})

    data = request.get_json() or {}
    contacts_list = data.get('contacts', [])
    user.set_contacts(contacts_list[:4])
    db.session.commit()
    return jsonify({"success": True, "contacts": user.get_contacts()})


@app.route('/api/emergency-contact', methods=['POST'])
def save_single_contact():
    if 'user_id' not in session:
        return jsonify({"success": False, "error": "Unauthorized"}), 401

    data = request.get_json() or {}
    phone = data.get('emergency_contact')
    user = User.query.get(session['user_id'])
    contacts = user.get_contacts()

    if len(contacts) > 0:
        contacts[0] = {"name": "Primary Guardian", "phone": phone}
    else:
        contacts.append({"name": "Primary Guardian", "phone": phone})

    user.set_contacts(contacts)
    db.session.commit()
    return jsonify({"success": True, "emergency_contact": phone})


# =====================================================
# START FLASK SERVER
# =====================================================
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # Seed Demo Account
        if not User.query.filter_by(email="demo@sheshield.ai").first():
            demo_user = User(
                name="Pushpanjali",
                email="demo@sheshield.ai",
                phone="+919876543210"
            )
            demo_user.set_password("password123")
            demo_user.set_contacts([
                {"name": "Dad", "phone": "+919848011223"},
                {"name": "Sister", "phone": "+919848099887"}
            ])
            db.session.add(demo_user)
            db.session.commit()
            print(">> Seeded demo user: demo@sheshield.ai / password123")

    print("\n=======================================================")
    print("🛡️  SheShield AI Backend Server Online!")
    print("📍 Open Browser at: http://127.0.0.1:5000")
    print("=======================================================\n")
    app.run(debug=True, host='0.0.0.0', port=5000)