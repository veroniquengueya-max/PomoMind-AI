import streamlit as st
import os
import time
import hashlib
import io
import base64
import random
import pypdf  # type: ignore
from PIL import Image as PILImage, ImageDraw, ImageFont

# ==============================================================================
# 🛰️ CONFIGURATION DES INFRASTRUCTURES SPONSORS OFFICIELLES (CONFORME RÈGLEMENT)
# ==============================================================================
demo_mode = True 

PRIMARY_AI_PROVIDER = "Meterless Nightshift AI"
ACTIVE_METERLESS_ENGINE = "Meterless Scout Intent Engine (V3)"
DATA_LAYER_INFRASTRUCTURE = "Zetaris Decentralized Data Harness"
HARDWARE_ACCELERATION = "NVIDIA Cloud Inference Architecture"

API_KEY_SECURE = os.environ.get("METERLESS_NIGHTSHIFT_KEY", "MOCK_CAMPUS_KEY_2026")

st.set_page_config(
    page_title="PomoMind AI - ICT University",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded"
)

FR = st.sidebar.toggle("🇫🇷 Mode Français / English Mode", value=True, key="global_language_toggle")

# ==============================================================================
# 🛡️ COFFRE-FORT CRYPTOGRAPHIQUE DE LA CTO (LOCAL STORAGE DB)
# ==============================================================================
DB_FILE = "utilisateurs_db.txt"
nom_cache_public = "cache_cours_public.txt"

def encoder_role_secret(role):
    if role == "prof":
        return "SECURE_NODE_FACULTY_AM4"
    return "SECURE_NODE_STUDENT_X99"

def decoder_role_secret(token_secret):
    if "FACULTY" in token_secret:
        return "prof"
    return "eleve"

def charger_base_donnees_locales():
    comptes = {}
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            for ligne in f:
                if "::" in ligne:
                    u, h_p, r_secret = ligne.strip().split("::")
                    comptes[u] = {"password_hash": h_p, "role": decoder_role_secret(r_secret)}
    return comptes

def sauvegarder_compte_local(username, password_hash, role):
    role_chiffre = encoder_role_secret(role)
    with open(DB_FILE, "a", encoding="utf-8") as f:
        f.write(f"{username}::{password_hash}::{role_chiffre}\n")

# Initialisation de la mémoire d'état persistante
st.session_state["comptes_utilisateurs"] = charger_base_donnees_locales()

if "user_role_actif" not in st.session_state: st.session_state["user_role_actif"] = None
if "capsule_sessions_aujourdhui" not in st.session_state: st.session_state["capsule_sessions_aujourdhui"] = 0
if "session_initialisee" not in st.session_state: st.session_state["session_initialisee"] = False
if "xp" not in st.session_state: st.session_state.xp = 0
if "pomodoro_termine" not in st.session_state: st.session_state["pomodoro_termine"] = False
if "chrono_en_cours" not in st.session_state: st.session_state["chrono_en_cours"] = False
if "buddy_energy" not in st.session_state: st.session_state["buddy_energy"] = 80
if "buddy_joy" not in st.session_state: st.session_state["buddy_joy"] = 70
if "buddy_status" not in st.session_state: st.session_state["buddy_status"] = "⚡ Prêt à coder !" if FR else "⚡ Ready to code!"
if "buddy_animation" not in st.session_state: st.session_state["buddy_animation"] = "buddy-float"
if "capsule_countdown_seconds" not in st.session_state: st.session_state["capsule_countdown_seconds"] = 1200  
if "capsule_timer_running" not in st.session_state: st.session_state["capsule_timer_running"] = False
if "capsule_audio_unlocked" not in st.session_state: st.session_state["capsule_audio_unlocked"] = False
if "pomodoro_cycles_completed" not in st.session_state: st.session_state["pomodoro_cycles_completed"] = 0
if "pomodoro_current_phase" not in st.session_state: st.session_state["pomodoro_current_phase"] = "focus"  
if "pomodoro_lock_active" not in st.session_state: st.session_state["pomodoro_lock_active"] = False
if "planning_personnalise" not in st.session_state: st.session_state["planning_personnalise"] = []
if "username" not in st.session_state: st.session_state["username"] = ""
if "carousel_disc_idx" not in st.session_state: st.session_state["carousel_disc_idx"] = 0
if "carousel_stress_idx" not in st.session_state: st.session_state["carousel_stress_idx"] = 0
if "carousel_leader_idx" not in st.session_state: st.session_state["carousel_leader_idx"] = 0
if "chat_messages" not in st.session_state: st.session_state["chat_messages"] = []

def calculer_empreinte_sha256(texte_brut):
    try:
        return hashlib.sha256(texte_brut.encode('utf-8')).hexdigest()
    except Exception:
        return "e3b0c44298fc1c149afbDcJHrrHSgvFpsYxqb6g97uaQTd2kE31rPUeDZTeDsjVq"

def extraire_texte_pdf(fichier_pdf):
    try:
        lecteur = pypdf.PdfReader(fichier_pdf)
        texte_complet = ""
        for page in lecteur.pages:
            texte_page = page.extract_text()
            if texte_page: texte_complet += texte_page + "\n"
        return texte_complet.strip()
    except Exception:
        return ""

def generer_concepts_feynman_dynamiques(texte_cours, titre_matiere):
    if not texte_cours:
        return "CONCEPT 1 : Introduction Générale\nEXPLICATION : Cours d'excellence universitaire."
    lignes = [l.strip() for l in texte_cours.split("\n") if len(l.strip()) > 30]
    concepts = []
    for i in range(min(3, len(lignes))):
        concept_titre = f"CONCEPT {i+1} : " + lignes[i][:50] + "..."
        concept_expl = f"EXPLICATION : <b>Explication Feynman :</b> {lignes[i]} Nous appliquons ici une simplification par métaphore pour ancrer la logique."
        concepts.append(f"{concept_titre}\n{concept_expl}")
    return "\n---\n".join(concepts)

# ==============================================================================
# 🦅 COEUR DE SÉCURITÉ : CONFIGURATION DE L'AUTHENTIFICATION SÉCURISÉE
# ==============================================================================
if not st.session_state["session_initialisee"]:
    st.markdown(f"""<div style="text-align:center; margin-bottom:30px;"><h1 style="color:#00f0ff; font-family:sans-serif; font-size:42px;">🦅 POMOMIND AI</h1><p style="color:rgba(255,255,255,0.6);">{"Écosystème d'Étude Multi-Agent Universitaire Sécurisé Core 2026" if FR else "Secure University Multi-Agent Study Ecosystem Core 2026"}</p></div>""", unsafe_allow_html=True)
    tab_se_connecter, tab_s_inscrire = st.tabs(["🔐 Connexion / Login", "📝 Inscription / Register"])
    
    with tab_se_connecter:
        with st.form("form_login_core"):
            login_user = st.text_input("🎯 Identifiant (Username) :", placeholder="ex: veronique_cto").strip()
            login_pass = st.text_input("🔒 Mot de passe / Password :", type="password")
            univ_node = st.selectbox("🏫 Connected Campus Node :", ["The ICT University (Yaoundé)"])
            if st.form_submit_button("🚀 Connexion sécurisée" if FR else "🚀 Secure Login", use_container_width=True):
                st.session_state["comptes_utilisateurs"] = charger_base_donnees_locales()
                if login_user in st.session_state["comptes_utilisateurs"] and calculer_empreinte_sha256(login_pass) == st.session_state["comptes_utilisateurs"][login_user]["password_hash"]:
                    st.session_state["username"] = login_user
                    st.session_state["univ_selectionnee"] = univ_node
                    st.session_state["user_role_actif"] = st.session_state["comptes_utilisateurs"][login_user]["role"]
                    st.session_state["session_initialisee"] = True
                    st.rerun()
                else: st.error("🚨 Identifiants invalides." if FR else "🚨 Invalid credentials.")
    with tab_s_inscrire:
        with st.form("form_registration_core"):
            reg_user = st.text_input("🎯 Identifiant unique (Username) :", placeholder="ex: veronique_cto").strip()
            reg_pass = st.text_input("🔒 Mot de passe / Password :", type="password")
            reg_role = st.selectbox("🎭 Type de profil :", ["Student (Étudiant)", "Professor (Enseignant)"])
            prof_secret_key = st.text_input("🔑 Code Secret Enseignant :", type="password")
            if st.form_submit_button("💾 Enregistrer et Entrer" if FR else "💾 Register and Enter", use_container_width=True):
                if "Enseignant" in reg_role and prof_secret_key != "PROF2026": st.error("🚨 Code Professeur Invalide." if FR else "🚨 Invalid Faculty Secret Key.")
                else:
                    role_defini = "prof" if "Enseignant" in reg_role else "eleve"
                    sauvegarder_compte_local(reg_user, calculer_empreinte_sha256(reg_pass), role_defini)
                    st.session_state["username"] = reg_user
                    st.session_state["user_role_actif"] = role_defini
                    st.session_state["session_initialisee"] = True
                    st.rerun()
    st.stop()

# ==============================================================================
# 🤖 INTERFACE DE LA SIDEBAR UNIFIÉE ET DE SES COMPOSANTS INTERNES
# ==============================================================================
with st.sidebar:
    style_robot_expressif = """
    <style>
    @keyframes robotHover {
        0% { transform: translateY(0px); filter: drop-shadow(0 0 5px #00f0ff); }
        50% { transform: translateY(-8px); filter: drop-shadow(0 0 15px #00f0ff); }
        100% { transform: translateY(0px); filter: drop-shadow(0 0 5px #00f0ff); }
    }
    .robot-chassis { width: 50px; height: 44px; background-color: #1e1b4b; border: 3px solid #00f0ff; border-radius: 10px; position: relative; display: inline-block; margin: 15px auto; animation: robotHover 2.5s infinite ease-in-out; }
    .robot-visor { position: absolute; width: 34px; height: 6px; top: 12px; left: 5px; background-color: #ff007f; border-radius: 2px; }
    .readable-buddy-bubble { background-color: #ffffff !important; border: 4px solid #111116 !important; border-radius: 12px; padding: 12px; text-align: center; color:#111116; font-family: monospace; font-weight: bold; }
    </style>
    """
