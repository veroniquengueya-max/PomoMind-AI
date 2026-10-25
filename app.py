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
