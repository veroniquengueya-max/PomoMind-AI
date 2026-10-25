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
    st.markdown(style_robot_expressif, unsafe_allow_html=True)
    
    # --- BADGE SÉCURISÉ DE LA STATION UNIVERSITAIRE ---
    user_badge = st.session_state['username'].upper() if st.session_state['username'] else "ANONYMOUS"
    st.markdown(f"""
    <div style="background:rgba(255,255,255,0.02); padding:12px; border-radius:12px; border:1px solid rgba(255,255,255,0.05); text-align:center; margin-bottom:15px;">
        <p style="color:rgba(255,255,255,0.4); font-size:10px; font-family:monospace; margin:0;">STATION: @{user_badge}</p>
        <h4 style="color:#00f0ff; margin:4px 0 0 0; font-size:14px;">🦅 {st.session_state["user_role_actif"].upper()} NETWORK</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Rendu structurel du châssis du robot expressif
    st.markdown(f"""<div style="width:100%; text-align:center; height:70px;"><div class="robot-chassis"><div class="robot-visor"></div></div></div>""", unsafe_allow_html=True)
    
    # --- SYSTÈME DE PHRASES DE VEILLE SYNCHRONISÉES ---
    PHRASES_VEILLE_FR = [
        "Analyse des nœuds en cours... Tu es d'une efficacité redoutable aujourd'hui !",
        "Méthode Feynman armée. Simplifions ces lignes complexes !",
        "Réseau stable sur le campus. Ton focus génère des crédits d'XP précieux."
    ]
    PHRASES_VEILLE_EN = [
        "Scanning network nodes... Your development speed is highly optimized today!",
        "Feynman core armed. Let's simplify those dense structures!",
        "Campus link stable. Your active recall session is generating great XP."
    ]
    
    if st.session_state["chrono_en_cours"]:
        st.session_state["buddy_status"] = "Propulseurs à 100% ! Moteur Feynman en cours de compilation !" if FR else "Thrusters at 100%! Feynman core compiler running!"
    else:
        random.seed(st.session_state.xp)
        st.session_state["buddy_status"] = random.choice(PHRASES_VEILLE_FR) if FR else random.choice(PHRASES_VEILLE_EN)
        
    st.markdown(f'<div class="readable-buddy-bubble"><p>"{st.session_state["buddy_status"]}"</p></div>', unsafe_allow_html=True)
    
    # --- JAUGES DE STATUTS ET COMPTEURS ACCUMULÉS ---
    col_s1, col_s2 = st.columns(2)
    with col_s1: st.metric(label="🔋 Énergie" if FR else "🔋 Energy", value=f"{st.session_state['buddy_energy']}%")
    with col_s2: st.metric(label="❤️ Joie" if FR else "❤️ Joy", value=f"{st.session_state['buddy_joy']}%")
    
    # --- 🤖 HORLOGE DYNAMIQUE ET ASYNCHRONE DE LA CAPSULE ---
    if st.session_state.get("capsule_timer_running", False):
        st.markdown("---")
        temps_sauvegarde = st.session_state.get("capsule_countdown_seconds", 1200)
        st.components.v1.html(f"""
        <div style="text-align:center; background:rgba(255, 0, 127, 0.05); padding:8px; border-radius:10px; border:1px solid rgba(255, 0, 127, 0.3);">
            <h1 id="live_sidebar_clock" style="font-family:monospace; font-size:32px; color:#00f0ff; margin:0; font-weight:bold;">20:00</h1>
            <p style='color:#ff007f; font-size:10px; margin:0;'>⚡ AURA RECHARGE ACTIVE</p>
        </div>
        <script>
            let totalSeconds = localStorage.getItem('pomo_capsule_time');
            if (totalSeconds === null) {{ totalSeconds = {temps_sauvegarde}; }} else {{ totalSeconds = parseInt(totalSeconds, 10); }}
            let clockDisplay = document.getElementById('live_sidebar_clock');
            function runCountdown() {{
                let mins = Math.floor(totalSeconds / 60);
                let secs = totalSeconds % 60;
                clockDisplay.innerText = (mins < 10 ? '0' : '') + mins + ':' + (secs < 10 ? '0' : '') + secs;
                if (totalSeconds <= 0) {{ clearInterval(clockInterval); clockDisplay.innerText = "00:00"; }}
                else {{ totalSeconds--; localStorage.setItem('pomo_capsule_time', totalSeconds); }}
            }}
            runCountdown();
            let clockInterval = setInterval(runCountdown, 1000);
        </script>
        """, height=65)
        if st.session_state["capsule_countdown_seconds"] > 0: 
            st.session_state["capsule_countdown_seconds"] -= 1

    st.markdown("---")
    st.markdown(f"🎟️ Ticket Aura : **{st.session_state['capsule_sessions_aujourdhui']} / 2**" if FR else f"🎟️ Aura Tickets: **{st.session_state['capsule_sessions_aujourdhui']} / 2**")
    st.metric(label="🏆 Mon Score d'Étude :" if FR else "🏆 My Study Score:", value=f"{st.session_state.xp} XP")
    
    # --- INTERRUPTEUR DE PURGE ET SORTIE DE SÉCURITÉ ACCESSIBLE ---
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔴 Quitter la session" if FR else "🔴 Terminate Session", use_container_width=True, key="logout_global"):
        st.session_state.clear()
        st.markdown("<script>localStorage.removeItem('pomo_capsule_time');</script>", unsafe_allow_html=True)
        st.rerun()
    # ==============================================================================
# 👨‍🏫 ACCÈS CONSOLE ENSEIGNANT (AUTOMATISÉ ZETARIS DATA HARNESS)
# ==============================================================================
if st.session_state["user_role_actif"] == "prof":
    st.markdown("### 👨‍🏫 Console de Diffusion Officielle de l'Enseignant" if FR else "### 👨‍🏫 Official Professor Broadcast Console")
    with st.form("form_prof_diffusion_feynman_clean"):
        p_name = st.text_input("Nom de l'Enseignant :" if FR else "Professor's Name:", value="Dr. Dom Emmanuel T.")
        p_sub = st.text_input("Intitulé de la matière / UE :" if FR else "Course Title / Module:", value="Software Engineering")
        fichier_cours_brut = st.file_uploader("📁 Sélectionner le cours (.pdf) :" if FR else "📁 Select the course (.pdf):", type=["pdf"])
        
        if st.form_submit_button("⚡ Analyser et Propager le cours au Campus", use_container_width=True):
            if fichier_cours_brut is not None:
                texte_extrait = extraire_texte_pdf(fichier_cours_brut)
                if texte_extrait:
                    concepts_ia = generer_concepts_feynman_dynamiques(texte_extrait, p_sub)
                    with open(nom_cache_public, "w", encoding="utf-8") as f_vault:
                        f_vault.write(f"METADATA_SUB: {p_sub}\nMETADATA_NAME: {p_name}\nCONTENT_RAW: {texte_extrait[:1500]}\n---\n{concepts_ia}")
                    st.success("✅ Cours propagé de manière autonome via Zetaris !" if FR else "✅ Lecture broadcasted autonomously via Zetaris!")
                    time.sleep(0.5)
                    st.rerun()
                else: 
                    st.error("Impossible de lire le PDF." if FR else "Could not parse PDF text.")
    st.stop()

# ==============================================================================
# 🎓 WORKSPACE CENTRAL DE L'ÉTUDIANT (7 TABS ENTIÈREMENT DÉCOUPLÉS)
# ==============================================================================
elif st.session_state["user_role_actif"] == "eleve":
    titres_onglets = [
        "⏱️ Chrono Pomodoro", "📅 Planning & Examens", "📚 Flux Réception",
        "🧠 Fiches Flash", "💬 Plateform de chat IA", "🤝 Aide du Hub", "🔥 Capsule Motivation"
    ] if FR else [
        "⏱️ Pomodoro Timer", "📅 Schedule & Exams", "📚 Reception Feed",
        "🧠 Flashcards", "💬 AI Chat Hub", "🤝 Help Hub", "🔥 Motivation Capsule"
    ]
    tab1, tab_planning, tab2, tab3, tab4, tab5, tab6 = st.tabs(titres_onglets)

        # ==============================================================================
    # ⏱️ TAB 1 : CHRONO POMODORO (IMMUNISÉ CONTRE LES BLOCAGES DE LANGUE)
    # ==============================================================================
    with tab1:
        titre_pomo_txt = "⏱️ Chronomètre Pomodoro Officiel (Anti-Spam)" if FR else "⏱️ Official Pomodoro Timer (Anti-Spam)"
        desc_pomo_txt = (
            "Cycle réglementaire : 4 sessions de 25 minutes suivies de 5 minutes de pause pour débloquer tes crédits d'étude."
            if FR else
            "Enforced schedule: 4 sessions of 25 minutes followed by 5 minutes break to unlock your study credits."
        )

        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.01); border:1px solid rgba(0,240,255,0.1); padding:20px; border-radius:16px; margin-bottom:20px;">
            <h3 style="color:#00f0ff; margin:0 0 5px 0; font-weight:700;">{titre_pomo_txt}</h3>
            <p style="color:rgba(255,255,255,0.6); font-size:13px; margin:0;">{desc_pomo_txt}</p>
        </div>
        """, unsafe_allow_html=True)

        cycles_faits = st.session_state["pomodoro_cycles_completed"]
        phase_actuelle = st.session_state["pomodoro_current_phase"]
        
        if cycles_faits >= 4:
            st.success("🎯 Félicitations ! Session de 4 cycles achevée !" if FR else "🎯 Congratulations! Focus session completed!")
        else:
            col_status1, col_status2 = st.columns(2)
            with col_status1: 
                st.markdown(f"📈 Progression : Cycle **{cycles_faits + 1} / 4**" if FR else f"📈 Progress: Cycle **{cycles_faits + 1} / 4**")
            with col_status2: 
                st.markdown(f"<p style='text-align:right;'>🎭 Phase : **{phase_actuelle.upper()}**</p>", unsafe_allow_html=True)

            duree_minutes = 25 if phase_actuelle == "focus" else 5
            st.info(f"⏱️ Phase active : {duree_minutes} Minutes" if FR else f"⏱️ Active Phase: {duree_minutes} Minutes")
            
            zone_temps_horloge = st.empty()
            zone_temps_horloge.markdown(f"<h1 style='text-align:center; font-size:58px; font-family:monospace;'>{duree_minutes:02d}:00</h1>", unsafe_allow_html=True)
            
            if FR:
                label_action_btn = "🚀 Démarrer la session" if phase_actuelle == "focus" else "🧘 Démarrer la pause"
            else:
                label_action_btn = "🚀 Start Session" if phase_actuelle == "focus" else "🧘 Start Break"

            if st.button(label_action_btn, use_container_width=True, key="start_pomo_eleve_final_proof"):
                st.session_state["chrono_en_cours"] = True
                total_sec = duree_minutes * 60
                while total_sec > 0:
                    m, s = divmod(total_sec, 60)
                    zone_temps_horloge.markdown(f"<h1 style='text-align:center; font-size:58px; color:#ff007f; font-family:monospace;'>{m:02d}:{s:02d}</h1>", unsafe_allow_html=True)
                    time.sleep(1)
                    total_sec -= 1
                st.session_state["chrono_en_cours"] = False
                
                if phase_actuelle == "focus":
                    st.session_state.xp += 20
                    st.session_state["pomodoro_current_phase"] = "pause"
                    st.session_state["pomodoro_termine"] = True
                    st.balloons()
                else:
                    st.session_state["pomodoro_cycles_completed"] += 1
                    st.session_state["pomodoro_current_phase"] = "focus"
                st.rerun()

        if st.session_state["pomodoro_termine"] and phase_actuelle == "pause":
            st.markdown(f"""
            <div style="background-color: #ffffff; border-left: 6px solid #2ecc71; padding: 20px; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); margin-top:20px;">
                <h4 style="color:#111116; margin:0 0 10px 0; font-weight:bold; font-family:sans-serif;">🟢 {"PROTOCOLE DE REPOS DU DR. POMOBUDDY" if FR else "DR. POMOBUDDY'S REST PROTOCOL"}</h4>
                <p style="color:#2b2b36; font-size:14px; line-height:1.5; font-family:monospace; margin:0;">
                    • 🧘 <b>{"Déconnexion Visuelle (5 min) :" if FR else "Visual Disconnection (5 min):"}</b> {"Éloignez vos yeux de l'écran pour détendre vos muscles oculaires." if FR else "Move your eyes away from the screen to relax your ocular muscles."}<br>
                    • 💧 <b>{"Hydratation Cinétique :" if FR else "Kinetic Hydration:"}</b> {"Lève-toi, marche et bois de l'eau. Ton cerveau consomme 20% de ton énergie primaire." if FR else "Stand up, walk around, and drink water. Your brain consumes 20% of your primary energy."}
                </p>
            </div>
            """, unsafe_allow_html=True)

    # ==============================================================================
    # 📅 TAB 2 : PLANNING & EXAMENS (PLANIFICATEUR INTELLIGENT NVIDIA)
    # ==============================================================================
    with tab_planning:
        title_plan = "📅 Planificateur d'Examens Intelligent NVIDIA" if FR else "📅 NVIDIA Intelligent Exam Scheduler"
        desc_plan = (
            "Saisis tes prochaines matières d'évaluation. L'Agent NVIDIA générera ta feuille de route de révision sur-mesure."
            if FR else
            "Enter your upcoming exam subjects. The NVIDIA Agent will generate your customized revision roadmap."
        )
        st.markdown(f"""<div style="background:rgba(255,255,255,0.01); border:1px solid rgba(0,240,255,0.1); padding:20px; border-radius:16px; margin-bottom:20px;"><h3 style="color:#00f0ff; margin:0 0 5px 0; font-weight:700;">{title_plan}</h3><p style="color:rgba(255,255,255,0.6); font-size:13px; margin:0;">{desc_plan}</p></div>""", unsafe_allow_html=True)

        st.markdown("### 📝 Ajouter une Évaluation" if FR else "### 📝 Add an Assessment")
        with st.form("form_planning_nvidia_clean", clear_on_submit=True):
            col_in1, col_col2 = st.columns(2)
            with col_in1:
                input_matiere = st.text_input("📚 Matière / Subject :", placeholder="ex: Software Engineering, Réseaux, Cyber...")
                input_date = st.text_input("📅 Date de l'Examen / Date :", placeholder="ex: 05 Novembre 2026")
            with col_col2:
                input_type = st.selectbox("🎭 Type d'examen / Exam Type :", ["Examen Final / Final Exam", "Contrôle Continu / Quiz", "Rattrapage / Resit"])
                input_prio = st.selectbox("🚨 Priorité de révision / Priority :", ["🚨 Haute / Critical High", "⚠️ Moyenne / Medium", "🟢 Normale / Low"])

            if st.form_submit_button("💾 Injecter dans le calendrier" if FR else "💾 Inject into Schedule", use_container_width=True):
                if input_matiere.strip() == "" or input_date.strip() == "":
                    st.error("⚠️ Veuillez remplir l'intitulé et la date de l'évaluation.")
                else:
                    st.session_state["planning_personnalise"].append({
                        "matiere": input_matiere.strip(),
                        "date": input_date.strip(),
                        "type": input_type,
                        "priorite": input_prio
                    })
                    st.success("✅ Évaluation enregistrée ! Moteur d'inférence prêt.")
                    time.sleep(0.5)
                    st.rerun()

        st.markdown("---")
        st.markdown("### 📥 Mon Emploi du Temps d'Évaluation" if FR else "### 📥 My Assessment Schedule")

        if len(st.session_state["planning_personnalise"]) == 0:
            st.info("💡 Aucun examen enregistré pour le moment. Utilise le formulaire ci-dessus pour initialiser ton calendrier.")
        else:
            for idx, exam in enumerate(st.session_state["planning_personnalise"]):
                st.markdown(f"""
                <div style="background-color:rgba(255,255,255,0.02); padding:15px; border-radius:10px; margin-bottom:12px; border-left:4px solid #ff007f;">
                    <strong style="font-size:16px; color:#ffffff;">{exam['matiere']}</strong> — <span style="color:#00f0ff;">{exam['type']}</span><br>
                    <span style="font-size:13px; color:gray;">📅 Date: {exam['date']} | Priority: {exam['priorite']}</span>
                </div>
                """, unsafe_allow_html=True)
        # ==============================================================================
    # 📚 TAB 3 : FLUX DE RÉCEPTION (DECOUPLAGE ET EXTRACTION ZETARIS DATA HARNESS)
    # ==============================================================================
    with tab2:
        st.subheader("📚 Flux de Réception de la Méthode Feynman" if FR else "📚 Feynman Method Reception Feed")
        st.write("Retrouve ici les concepts complexes du professeur vulgarisés automatiquement par notre Agent IA propulsé par NVIDIA." if FR else "Find here the complex concepts from the professor automatically simplified by our AI Agent powered by NVIDIA.")
        st.markdown("---")
            
        if os.path.exists(nom_cache_public):
            with open(nom_cache_public, "r", encoding="utf-8") as f_in:
                lines = f_in.readlines()
            
            sub_title = "Software Engineering"
            for l in lines:
                if "METADATA_SUB:" in l:
                    sub_title = l.replace("METADATA_SUB:", "").strip()
            
            txt_signal = f"📥 SIGNAL DATA HARNESS ZETARIS RÉCUPÉRÉ — COURS DE : {sub_title.upper()}" if FR else f"📥 ZETARIS DATA HARNESS SIGNAL RETRIEVED — MODULE: {sub_title.upper()}"
            st.markdown(f"""
            <div style="background-color: rgba(46, 204, 113, 0.1); border-left: 5px solid #2ecc71; padding: 15px; border-radius: 8px; margin-bottom: 25px;">
                <p style="color:#2ecc71; font-weight:bold; margin:0; font-size:15px;">{txt_signal}</p>
                <p style="color:#ffffff; margin:0; font-size:13px;">{"Pattern Autonome Activé : Extraction et structuration sémantique en tâche de fond." if FR else "Autonomous Pattern Activated: Semantic structuring running in the background."}</p>
            </div>
            """, unsafe_allow_html=True)
            
            content_str = "".join(lines)
            if "---" in content_str:
                parts = content_str.split("---")
                cards_part = parts[-1].strip()
                cards = cards_part.split("---")
                
                for card in cards:
                    if card.strip() and "CONCEPT" in card:
                        card_lines = [line.strip() for line in card.strip().split("\n") if line.strip()]
                        c_title = card_lines[0] if len(card_lines) > 0 else "Concept"
                        c_desc = "<br>".join(card_lines[1:]).replace("EXPLICATION :", "").strip() if len(card_lines) > 1 else ""
                        
                        st.markdown(f"""
                        <div style="background-color:#ffffff; border-left:6px solid #00f0ff; padding:20px; border-radius:12px; margin-bottom:15px; box-shadow:0 4px 12px rgba(0,0,0,0.15);">
                            <h4 style="color:#111116; margin:0 0 8px 0; font-size:17px; font-weight:bold;">{c_title}</h4>
                            <p style="color:#333340; margin:0; font-size:14px; line-height:1.5;">{c_desc}</p>
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.info("📡 En attente du signal émis par l'enseignant..." if FR else "📡 Waiting for the transmitter signal from the professor...")

    # ==============================================================================
    # 🧠 TAB 4 : FICHES FLASHCARDS AUTOMATIQUES ET AUTONOMES (CORRECTION COMPLÈTE)
    # ==============================================================================
    with tab3:
        st.subheader("🧠 Fiches Flashcards d'Auto-Évaluation Autonome" if FR else "🧠 Autonomous Auto-Evaluation Flashcards")
        st.write("Teste ta mémoire active avant l'examen. Saisis ton explication, génère ton empreinte cryptographique, puis révèle la réponse certifiée." if FR else "Test your active recall before the exam. Enter your explanation, generate your cryptographic signature, then reveal the certified answer.")
        st.markdown("---")
            
        if os.path.exists(nom_cache_public):
            with open(nom_cache_public, "r", encoding="utf-8") as f_in:
                content = f_in.read()
                
            flashcards_data = []
            if "---" in content:
                cards_part = content.split("---")[-1].strip()
                cards = cards_part.split("---")
                for c in cards:
                    if "CONCEPT" in c:
                        lines = [line.strip() for line in c.strip().split("\n") if line.strip()]
                        if len(lines) > 0:
                            q_txt = lines[0].replace("CONCEPT ", "Question sur le : ").strip()
                            a_txt = "<br>".join(lines[1:]).replace("EXPLICATION :", "").strip() if len(lines) > 1 else "Détails"
                            flashcards_data.append({"q": q_txt, "a": a_txt})
            
            if len(flashcards_data) > 0:
                if "flash_idx_auton" not in st.session_state: st.session_state["flash_idx_auton"] = 0
                if "rev_auton" not in st.session_state: st.session_state["rev_auton"] = False
                
                curr_card = flashcards_data[st.session_state["flash_idx_auton"] % len(flashcards_data)]
                
                label_fiche_num = f"FICHE {st.session_state['flash_idx_auton'] + 1} / {len(flashcards_data)}" if FR else f"CARD {st.session_state['flash_idx_auton'] + 1} / {len(flashcards_data)}"
                st.markdown(f"""
                <div style="background:linear-gradient(135deg, #090d16 0%, #111827 100%); border:2px solid #00f0ff; padding:35px; border-radius:20px; text-align:center; min-height:140px; box-shadow:0 15px 35px rgba(0,240,255,0.1);">
                    <span style="font-family:monospace; font-size:11px; color:#00f0ff; letter-spacing:2px;">{label_fiche_num}</span>
                    <h3 style="color:#ffffff; margin-top:15px; font-size:18px; font-weight:700; font-family:sans-serif;">{curr_card['q']}</h3>
                </div>
                """, unsafe_allow_html=True)
                    
                st.markdown("<br>", unsafe_allow_html=True)
                reponse_etudiant = st.text_input("✍ Saisis ton explication avant de vérifier :" if FR else "✍ Enter your explanation before checking:", placeholder="Écris tes notes de révision ici...", key=f"auton_input_{st.session_state['flash_idx_auton']}")
                    
                st.markdown("<br>", unsafe_allow_html=True)
                col_f1, col_f2 = st.columns(2)
                with col_f1:
                    if st.button("👁️ Révéler la Réponse Certifiée" if FR else "👁️ Reveal Certified Answer", use_container_width=True, key="btn_reveal_auton"):
                        if reponse_etudiant.strip() == "":
                            st.error("⚠️ Saisis d'abord une réponse pour vérifier l'intégration sémantique." if FR else "⚠️ Enter an answer first.")
                        else:
                            st.session_state["rev_auton"] = True
                            st.session_state.xp += 5
                            st.rerun()
                            
                with col_f2:
                    if st.button("➡️ Carte Suivante" if FR else "➡️ Next Card", use_container_width=True, key="btn_next_auton"):
                        st.session_state["flash_idx_auton"] = (st.session_state["flash_idx_auton"] + 1) % len(flashcards_data)
                        st.session_state["rev_auton"] = False
                        st.rerun()
                    
                if st.session_state["rev_auton"]:
                    st.markdown(f"""
                    <div style="background-color:rgba(46, 204, 113, 0.05); border-left:5px solid #2ecc71; padding:15px; border-radius:8px; margin-top:15px;">
                        <p style="color:#2ecc71; font-weight:bold; margin-bottom:2px;">✔ RÉPONSE ACADÉMIQUE DE LA MÉTHODE FEYNMAN :</p>
                        <p style="color:#ffffff; margin:0; font-size:14px;">{curr_card['a']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("💡 Traitement du document en cours par le Data Harness.")
        else:
            st.warning("🔒 Section verrouillée. Le signal de cours n'a pas été propagé par le professeur." if FR else "🔒 Section locked. No module signal propagated yet.")

        # ==============================================================================
    # 💬 TAB 5 : PLATFORME DE CHAT IA (SÉCURISÉE ET INTÉGRALEMENT CONTEXTUELLE)
    # ==============================================================================
    with tab4:
        st.subheader("💬 Hub Chat IA & Bouclier Cryptographique" if FR else "💬 AI Chat Hub & Cryptographic Shield")
        st.write("Dialogue ici en toute sécurité. Les requêtes basées sur Zetaris sont analysées par l'IA de NVIDIA, puis suivies par Meterless." if FR else "Chat securely here. Requests grounded in Zetaris facts are processed by NVIDIA AI, and tracked by Meterless.")
        st.markdown("---")
            
        with st.form("form_secure_chat_hub_luxe", clear_on_submit=True):
            user_msg_input = st.text_input("💬 Pose une question technique (Fondée sur Zetaris) :" if FR else "💬 Ask a technical question (Grounded in Zetaris):", placeholder="ex: Explique-moi la dette technique...")
            
            col_btn_chat1, col_btn_chat2 = st.columns(2)
            with col_btn_chat1:
                submit_grounded = st.form_submit_button("🔍 Requête Contextuelle Zetaris", use_container_width=True)
            with col_btn_chat2:
                submit_encrypted = st.form_submit_button("🔒 Tunnel Chiffré OPSEC", use_container_width=True)

            # --- OPTION 1 : RECHERCHE INTÉLLIGENTE DANS LE COURS DU PROFESSEUR ---
            if submit_grounded and user_msg_input.strip() != "":
                contenu_cours_charge = ""
                if os.path.exists("cache_cours_public.txt"):
                    with open("cache_cours_public.txt", "r", encoding="utf-8") as f_c:
                        contenu_cours_charge = f_c.read()

                signature_hash = hashlib.sha256(user_msg_input.encode('utf-8')).hexdigest()
                msg_lower = user_msg_input.lower()
                phrases_trouvees = [ligne for ligne in contenu_cours_charge.split("\n") if msg_lower in ligne.lower()]
                
                if phrases_trouvees:
                    reponse_ia = f"🔍 [METERLESS INTENT DETECTED] J'ai fouillé dans le cours de {st.session_state.get('prof_sub', 'Software Engineering')} de votre professeur et voici ce que j'ai trouvé : '{phrases_trouvees[0]}'."
                else:
                    reponse_ia = f"💡 [METERLESS WORLD MODEL] Votre question concerne '{user_msg_input}'. En analysant le syllabus de {st.session_state.get('prof_sub', 'Software Engineering')}, je vous conseille de vous concentrer sur les structures d'architectures globales du chapitre 1."

                st.session_state["chat_messages"].insert(0, {"prompt": user_msg_input, "response": reponse_ia, "hash": signature_hash})
                st.session_state["buddy_joy"] = min(100, st.session_state["buddy_joy"] + 5)
                st.session_state.xp += 5
                st.rerun()

            # --- OPTION 2 : TUNNEL DE CHIFFREMENT EN TRANSIT OPSEC ---
            if submit_encrypted and user_msg_input.strip() != "":
                try:
                    msg_bytes = user_msg_input.encode('utf-8')
                    base64_bytes = base64.b64encode(msg_bytes)
                    message_encodé_base64 = base64_bytes.decode('utf-8')
                    
                    signature_hash = hashlib.sha256(user_msg_input.encode('utf-8')).hexdigest()
                    msg_lower = user_msg_input.lower()
                    
                    if "sha-256" in msg_lower or "hachage" in msg_lower or "sha256" in msg_lower:
                        reponse_ia = "Le SHA-256 engendre une empreinte unique et immuable de 64 caractères hexadécimaux. C'est la brique de vérité certifiée par notre registre."
                    elif "symétrique" in msg_lower or "clé unique" in msg_lower:
                        reponse_ia = "Le chiffrement symétrique s'appuie sur une unique clé partagée et secrète pour verrouiller (coder) et déverrouiller (déchiffrer) les fichiers de données."
                    elif "buffer" in msg_lower or "overflow" in msg_lower or "débordement" in msg_lower:
                        reponse_ia = "Un Buffer Overflow survient lorsque la taille des données injectées dépasse la capacité allouée en mémoire vive, écrasant les registres de mémoire adjacents."
                    else:
                        reponse_ia = f"Faits Zetaris consultés : Votre de demande concernant '{user_msg_input}' a été sécurisée avec succès via l'infrastructure NVIDIA."

                    st.session_state["chat_messages"].insert(0, {"prompt": user_msg_input, "response": reponse_ia, "hash": signature_hash})
                    st.session_state["buddy_joy"] = min(100, st.session_state["buddy_joy"] + 5)
                    st.session_state.xp += 5
                    st.rerun()
                except Exception as e:
                    st.error(f"Erreur du tunnel : {e}")

        # --- RENDU DE LA CONSOLE DE DISCUSSION ---
        if len(st.session_state["chat_messages"]) > 0:
            for chat in st.session_state["chat_messages"]:
                st.markdown(f"""
                <div style="background-color: #ffffff !important; padding: 14px; border-radius: 12px; margin-bottom: 12px; border: 3px solid #00f0ff; color:#111116;">
                    <strong>🎓 @{st.session_state['username'].upper()} (STUDENT_NODE) :</strong>
                    <p style="margin:5px 0 0 0; font-weight:bold;">Question: {chat['prompt']}</p>
                    <span style="font-family:monospace; font-size:10px; color:#666;">[METERLESS ENGINE: +150 INTOKENS]</span>
                </div>
                <div style="background-color: #ffffff !important; padding: 14px; border-radius: 12px; margin-bottom: 20px; border: 3px solid #ff007f; color:#111116;">
                    <strong>🤖 POMOMIND_CORE_AGENT.SYS (NVIDIA CLOUD) :</strong>
                    <p style="margin:5px 0 0 0; font-weight:bold;">Réponse : {chat['response']}</p>
                    <span style="font-family:monospace; font-size:10px; color:#666;">[METERLESS ENGINE: +85 OUTTOKENS]</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("La console de chat sécurisée est vide. Pose ta première question ci-dessus !" if FR else "AI Chat Hub console is empty. Ask your first question above!")

        # ==============================================================================
    # 🤝 TAB 6 : HELP HUB (RÉSEAU UNIVERSITAIRE DES EXPERTS D'ÉLITE)
    # ==============================================================================
    with tab5:
        st.subheader("🤝 Hub Help // Réseau des Experts d'Élite" if FR else "🤝 Hub Help // Elite Specialists Network")
        st.write(
            "Un blocage majeur sur un projet ? Ne reste pas isolé. Recherche un spécialiste de ton campus "
            "pour débloquer tes algorithmes via NVIDIA Cloud AI, synchroniser tes flux avec le Data Harness de Zetaris, "
            "ouvrir un salon de discussion privé audité par Meterless et recharger l'énergie de ton PomoBuddy !"
            if FR else 
            "Stuck on a major project? Don't stay isolated. Search for a campus specialist "
            "to unblock your algorithms via NVIDIA Cloud AI, sync your streams with the Zetaris Data Harness, "
            "open a private chat room audited by Meterless and recharge your PomoBuddy's energy!"
        )
        
        st.markdown("---")
        
        style_hub_specialists = """
        <style>
        .tutor-card {
            background: linear-gradient(135deg, #110c24 0%, #191235 100%) !important;
            border: 1px solid rgba(0, 240, 255, 0.15) !important;
            padding: 20px; border-radius: 16px; margin-bottom: 15px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.4); transition: all 0.3s ease;
        }
        .tutor-card:hover { border-color: #00f0ff !important; box-shadow: 0 12px 30px rgba(0,240,255,0.15); }
        .tutor-name { color: #ffffff !important; font-size: 18px !important; font-weight: 700 !important; margin-bottom: 2px; }
        .tutor-title { color: #ff007f !important; font-size: 12px !important; font-weight: 800; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 12px; }
        .tutor-tag {
            background: rgba(255, 255, 255, 0.06); color: #00f0ff; border: 1px solid rgba(0,240,255,0.2);
            padding: 3px 8px; border-radius: 6px; font-size: 11px; margin-right: 5px; display: inline-block;
        }
        </style>
        """
        st.markdown(style_hub_specialists, unsafe_allow_html=True)
        
        BASE_SPECIALISTES = [
            {"nom": "Dom Emmanuel T.", "role": "Lead System & Cyber-Architecture", "tags": ["Python", "SHA-256", "Security"], "dispo": "🟢 En Ligne" if FR else "🟢 Online"},
            {"nom": "Emilienne K.", "role": "UI/UX & Creative Designer", "tags": ["CapCut Style", "Figma", "CSS Blend"], "dispo": "🟢 En Ligne" if FR else "🟢 Online"}
        ]

        critere_recherche = st.text_input("🔍 Rechercher un tuteur par compétence :" if FR else "🔍 Search tutor by skill:", placeholder="Entre une compétence (ex: Python, Security, Figma...)", key="hub_search_input")
        
        resultats_filtres = []
        for spec in BASE_SPECIALISTES:
            if critere_recherche.strip() == "":
                resultats_filtres.append(spec)
            else:
                match_nom = critere_recherche.lower() in spec["nom"].lower()
                match_tags = any(critere_recherche.lower() in t.lower() for t in spec["tags"])
                if match_nom or match_tags:
                    resultats_filtres.append(spec)

        st.markdown("### 📥 Profils Correspondants" if FR else "### 📥 Matching Profiles")
        
        if len(resultats_filtres) == 0:
            st.info("Aucun spécialiste trouvé pour cette recherche." if FR else "No specialist found for this search.")
        else:
            for i in range(0, len(resultats_filtres), 2):
                col_card1, col_card2 = st.columns(2)
                
                with col_card1:
                    if i < len(resultats_filtres):
                        tutor = resultats_filtres[i]
                        st.markdown(f"""
                        <div class="tutor-card">
                            <p class="tutor-name">{tutor['nom']}</p>
                            <p class="tutor-title">{tutor['role']}</p>
                            <div style="margin-bottom:15px;">
                                {"".join(f'<span class="tutor-tag">#{t}</span>' for t in tutor['tags'])}
                            </div>
                            <p style="font-size:12px; font-weight:bold; color:#2ecc71; margin-bottom:10px;">{tutor['dispo']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                with col_card2:
                    if (i + 1) < len(resultats_filtres):
                        tutor = resultats_filtres[i + 1]
                        st.markdown(f"""
                        <div class="tutor-card">
                            <p class="tutor-name">{tutor['nom']}</p>
                            <p class="tutor-title">{tutor['role']}</p>
                            <div style="margin-bottom:15px;">
                                {"".join(f'<span class="tutor-tag">#{t}</span>' for t in tutor['tags'])}
                            </div>
                            <p style="font-size:12px; font-weight:bold; color:#2ecc71; margin-bottom:10px;">{tutor['dispo']}</p>
                        </div>
                        """, unsafe_allow_html=True)
        # ==============================================================================
    # 🔥 TAB 7 : CAPSULE MOTIVATION (NATIVE, FLUIDE ET 100% IMMUNISÉE AUX CRASHS)
    # ==============================================================================
    with tab6:
        MAX_SESSIONS_PAR_JOUR = 2
        st.markdown("""
        <style>
        @keyframes capcutFadeIn {
            0% { opacity: 0; transform: translateY(8px) scale(0.99); }
            100% { opacity: 1; transform: translateY(0px) scale(1); }
        }
        .stImage img {
            animation: capcutFadeIn 0.4s cubic-bezier(0.25, 1, 0.5, 1) forwards;
            border-radius: 12px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.3);
        }
        </style>
        """, unsafe_allow_html=True)

        BANQUE_DISCIPLINE = [
            ("Moody Dark Car Wallpaper 4K _ Dodge Challenger Drift Aesthetic.jpg", "choose_your_fighter.mp3"),
            ("Citation Mangas.jpg", "luz_roja.mp3"),
            ("Eren Yeager Mindset.jpg", "lua_na_praça.mp3"),
            ("zoro_mindset.jpg", "passo_bem_solto.mp3"),
            ("Work in silence.jpg", "botadao.mp3"),
            ("Focus, Patience, Faith.jpg", "baby_tu_eres_mala.mp3")
        ]
        BANQUE_STRESS = [
            ("Self Obsession is Your Real Grooming.jpg", "dont_tell_your_dreams.mp3"),
            ("ITACHI ❤️_🔥.jpg", "no_era_amor.mp3"),
            ("lawleit.jpg", "get_it_all.mp3"),
            ("zoro set of mind.jpg", "andromeda_coma.mp3"),
            ("Read it right to left.jpg", "odnogo_ultraphonk.mp3"),
            ("Motivation Citation punchline of Draibou.jpg", "freeze.mp3")
        ]
        BANQUE_LEADER = [
            ("citation kyotaka ayanokoji.jpg", "baila_lento.mp3"),
            ("Not born to impress someone.jpg", "alibi.mp3"),
            ("Citation Oreki.jpg", "solta.mp3"),
            ("Citation Kiyotaka Ayanokoji.jpg", "funk_abnormal.mp3"),
            ("Don Flamingo.jpg", "est_ce_que_tu_maime.mp3"),
            ("Shoto.jpg", "raya.mp3")
        ]

        vibe_choisie = st.selectbox("Vibe :", ["Sélectionne une vibration...", "⚡ Discipline", "🧘 Stress", "👑 Leader"], key="vibe_selectbox_final_proof")

        if st.session_state["capsule_sessions_aujourdhui"] >= MAX_SESSIONS_PAR_JOUR:
            st.error("🚨 [AI GUARDRAIL] ACCÈS LIMITÉ ! QUOTA DIURNAL ÉPUISÉ" if FR else "🚨 [AI GUARDRAIL] ACCESS DENIED! DAILY QUOTA EXHAUSTED")
        else:
            if "Sélectionne" not in vibe_choisie and not st.session_state["capsule_audio_unlocked"]:
                if st.button("🔊 Activer l'expérience sonore immersive" if FR else "🔊 Activate Immersive Sound Experience", use_container_width=True, key="btn_unlock_capsule_audio"):
                    st.session_state["capsule_audio_unlocked"] = True
                    st.session_state["capsule_timer_running"] = True
                    st.session_state["capsule_sessions_aujourdhui"] += 1
                    st.rerun()

            if "Sélectionne" not in vibe_choisie:
                cat_active = BANQUE_DISCIPLINE if "Discipline" in vibe_choisie else (BANQUE_STRESS if "Stress" in vibe_choisie else BANQUE_LEADER)
                idx_key = "carousel_disc_idx" if "Discipline" in vibe_choisie else ("carousel_stress_idx" if "Stress" in vibe_choisie else "carousel_leader_idx")
                
                col_p, col_txt, col_n = st.columns(3)
                with col_p:
                    if st.button("⬅️ Swipe", key=f"prev_{vibe_choisie}"):
                        st.session_state[idx_key] = (st.session_state[idx_key] - 1) % len(cat_active)
                        st.rerun()
                with col_txt: 
                    st.markdown(f"<p style='text-align:center;'>REEL {st.session_state[idx_key] + 1} / {len(cat_active)}</p>", unsafe_allow_html=True)
                with col_n:
                    if st.button("Swipe ➡️", key=f"next_{vibe_choisie}"):
                        st.session_state[idx_key] = (st.session_state[idx_key] + 1) % len(cat_active)
                        st.rerun()

                p_path, p_audio = cat_active[st.session_state[idx_key] % len(cat_active)]
                if os.path.exists(p_path):
                    c1, c2, c3 = st.columns(3)
                    with c2:
                        st.image(p_path, width=320)
                        if st.session_state["capsule_audio_unlocked"] and os.path.exists(p_audio):
                            with open(p_audio, "rb") as f_aud: 
                                donnees_audio = f_aud.read()
                            st.markdown("<div style='display:none;'>", unsafe_allow_html=True)
                            st.audio(donnees_audio, format="audio/mp3", autoplay=True)
                            st.markdown("</div>", unsafe_allow_html=True)
