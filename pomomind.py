import streamlit as st
import os
import time
import hashlib
import io
import base64
import random
from PIL import Image as PILImage, ImageDraw, ImageFont

demo_mode = True 
API_KEY_SECURE = os.environ.get("GEMINI_API_KEY", "MOCK_CAMPUS_KEY_2026")

st.set_page_config(
    page_title="PomoMind AI - ICT University",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded"
)

FR = st.sidebar.toggle("🇫🇷 Mode Français / English Mode", value=True, key="global_language_toggle")


if "session_initialisee" not in st.session_state:
    st.session_state["session_initialisee"] = False

if "role_selectionne" not in st.session_state:
    st.session_state["role_selectionne"] = None

if "xp" not in st.session_state:
    st.session_state.xp = 0

if "pomodoro_termine" not in st.session_state:
    st.session_state["pomodoro_termine"] = False

if "chrono_en_cours" not in st.session_state:
    st.session_state["chrono_en_cours"] = False

if "buddy_energy" not in st.session_state: 
    st.session_state["buddy_energy"] = 80

if "buddy_joy" not in st.session_state: 
    st.session_state["buddy_joy"] = 70

if "buddy_status" not in st.session_state: 
    st.session_state["buddy_status"] = "⚡ Prêt à coder !" if FR else "⚡ Ready to code!"

if "buddy_animation" not in st.session_state: 
    st.session_state["buddy_animation"] = "buddy-float"

if "audio_unlocked" not in st.session_state:
    st.session_state["audio_unlocked"] = False

def calculer_empreinte_sha256(texte_brut):
    """ Génère une signature d'empreinte numérique SHA-256 non inversible pour valider l'intégrité """
    try:
        encode_bytes = texte_brut.encode('utf-8')
        hash_object = hashlib.sha256(encode_bytes)
        return hash_object.hexdigest()
    except Exception:
        return "e3b0c44298fc1c149afbDcJHrrHSgvFpsYxqb6g97uaQTd2kE31rPUeDZTeDsjVq"

# --- INITIALISATION OBLIGATOIRE DES INDEX MULTIMÉDIAS DE LA CAPSULE ---
if "carousel_disc_idx" not in st.session_state:
    st.session_state["carousel_disc_idx"] = 0

if "carousel_stress_idx" not in st.session_state:
    st.session_state["carousel_stress_idx"] = 0

if "carousel_leader_idx" not in st.session_state:
    st.session_state["carousel_leader_idx"] = 0

if not st.session_state["session_initialisee"]:
    titre_principal = "🦅 POMOMIND AI"
    sous_titre = "Écosystème d'Étude Multi-Agent Universitaire Symbiotique Core 2026" if FR else "Symbiotic University Multi-Agent Study Ecosystem Core 2026"
    
    st.markdown(f"""
    <div style="text-align:center; margin-bottom:30px;">
        <h1 style="color:#00f0ff; font-family:sans-serif; font-size:42px; margin-bottom:10px;">{titre_principal}</h1>
        <p style="color:rgba(255,255,255,0.6); font-size:16px;">{sous_titre}</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        label_btn_prof = "👨‍🏫 ESPACE ENSEIGNANT" if FR else "👨‍🏫 PROFESSOR SPACE"
        if st.button(label_btn_prof, use_container_width=True, key="btn_role_prof"):
            st.session_state["role_selectionne"] = "prof"
    with col_r2:
        label_btn_student = "🎓 ESPACE ÉTUDIANT" if FR else "🎓 STUDENT DASHBOARD"
        if st.button(label_btn_student, use_container_width=True, key="btn_role_eleve"):
            st.session_state["role_selectionne"] = "eleve"

    st.markdown("<br><hr>", unsafe_allow_html=True)
    if st.session_state["role_selectionne"] == "prof":
        titre_console_prof = "👨‍🏫 Console de Diffusion Officielle de l'Enseignant" if FR else "👨‍🏫 Official Teacher Broadcasting Console"
        instructions_prof = (
            "Téléversez ici le fichier brut de vos notes de cours ou votre syllabus. "
            "Le Data Harness de Zetaris analysera son intégrité réseau avant sa propagation bilingue."
            if FR else
            "Upload your raw course notes or syllabus file here. "
            "The Zetaris Data Harness will audit network integrity before bilingual propagation."
        )
        st.markdown(f"### {titre_console_prof}")
        st.write(instructions_prof)
        
        nom_cache_public = "cache_cours_public.txt"
        
        with st.form("form_prof_diffusion_feynman"):
            label_nom_prof = "Nom de l'Enseignant :" if FR else "Professor Name:"
            label_matiere = "Intitulé de la matière / UE :" if FR else "Course Subject / Unit:"
            p_name = st.text_input(label_nom_prof, value="Dr. Dom Emmanuel T.")
            p_sub = st.text_input(label_matiere, value="Architecture Système & Cybersécurité" if FR else "System Architecture & Cybersecurity")
            
            label_uploader = "📁 Sélectionner le fichier officiel du cours (.pdf) :" if FR else "📁 Select the official course file (.pdf):"
            fichier_cours_brut = st.file_uploader(label_uploader, type=["pdf"], key="prof_file_feynman_uploader")
            
            label_submit_prof = "⚡ Analyser et Propager le cours via Zetaris" if FR else "⚡ Analyze and Broadcast Course via Zetaris"
            if st.form_submit_button(label_submit_prof, use_container_width=True):
                if fichier_cours_brut is not None:
                    try:
                        contenu_brut = "Architecture Système et Cybersécurité Chiffrement Symétrique"
                        
                        mots_interdits = ["bavardage", "fête", "triche", "hacker", "malware", "soirée", "foot", "vacances", "cheat", "party", "gossip"]
                        contient_inutile = any(mot in contenu_brut.lower() for mot in mots_interdits)
                        
                        if contient_inutile:
                            msg_err_guardrail = "🚨 [ALERTE GUARDRAIL SÉCURITÉ] Flux rejeté ! Détection de termes illicites ou hors-sujet." if FR else "🚨 [SECURITY GUARDRAIL ALERT] Stream rejected! Disallowed or off-topic terms detected."
                            st.error(msg_err_guardrail)
                        else:
                            txt_spinner = "L'Agent Feynman s'appuie sur NVIDIA Cloud AI pour convertir le cours..." if FR else "Feynman Agent is relying on NVIDIA Cloud AI to convert the course..."
                            with st.spinner(txt_spinner):
                                time.sleep(1)
                                
                                feynman_cards_compiled = f"""
                                METADATA_SUB: {p_sub}
                                METADATA_NAME: {p_name}
                                """
                                with open(nom_cache_public, "w", encoding="utf-8") as f_vault:
                                    f_vault.write(feynman_cards_compiled.strip())
                                
                                st.session_state.xp += 15
                                st.session_state["buddy_joy"] = min(100, st.session_state["buddy_joy"] + 15)
                                st.session_state["buddy_status"] = "📚 Cours assimilé par Feynman !" if FR else "📚 Course assimilated by Feynman!"
                                
                                msg_success_prof = "✅ Cours validé par le Guardrail et converti par la Méthode Feynman avec succès !" if FR else "✅ Course validated by Guardrail and successfully converted using the Feynman Method!"
                                st.success(msg_success_prof)
                                time.sleep(1)
                                st.session_state["role_selectionne"] = None
                                st.rerun()
                    except Exception as e:
                        st.error(f"🚨 Faille de traitement : {e}" if FR else f"🚨 Processing fault: {e}")
                else:
                    msg_upload_req = "⚠️ Veuillez téléverser un fichier physique .pdf pour initialiser la diffusion." if FR else "⚠️ Please upload a physical .pdf file to initialize broadcasting."
                    st.error(msg_upload_req)

    elif st.session_state["role_selectionne"] == "eleve":
        titre_inscription = "🎓 Inscription et Liaison Nœud Étudiant" if FR else "🎓 Registration and Student Node Binding"
        st.markdown(f"### {titre_inscription}")
        with st.form("form_student_login"):
            label_username = "🎯 Identifiant Étudiant (Username) :" if FR else "🎯 Student Username:"
            username_input = st.text_input(label_username, placeholder="ex: audrey_cto")
            
            label_node = "🏫 Connected Campus Node :" if FR else "🏫 Connected Campus Node:"
            univ_node = st.selectbox(label_node, ["The ICT University (Yaoundé)"])
            
            label_btn_login = "🚀 Entrer dans l'Écosystème Applicatif" if FR else "🚀 Enter the Application Ecosystem"
            if st.form_submit_button(label_btn_login, use_container_width=True):
                if username_input.strip() == "":
                    st.error("⚠️ L'identifiant est requis pour initialiser la mémoire d'état." if FR else "⚠️ Username is required to initialize state memory.")
                else:
                    sub_decouvert = "Architecture Système & Cybersécurité" if FR else "System Architecture & Cybersecurity"
                    name_decouvert = "Dr. Dom Emmanuel T."
                    
                    st.session_state["username"] = username_input.strip()
                    st.session_state["univ_selectionnee"] = univ_node
                    st.session_state["prof_sub"] = sub_decouvert
                    st.session_state["prof_name"] = name_decouvert
                    st.session_state["session_initialisee"] = True
                    st.success("✅ Authentification validée. Liaison réseau établie." if FR else "✅ Authentication validated. Network link established.")
                    time.sleep(1)
                    st.rerun()
 
else:
    with st.sidebar:
        style_robot_expressif = """
        <style>
        @keyframes robotHover {
            0% { transform: translateY(0px); filter: drop-shadow(0 0 5px #00f0ff); }
            50% { transform: translateY(-8px); filter: drop-shadow(0 0 15px #00f0ff); }
            100% { transform: translateY(0px) scale(1); filter: drop-shadow(0 0 5px #00f0ff); }
        }
        @keyframes robotSprint {
            0% { transform: translateY(0px) scale(1) skewX(-2deg); filter: drop-shadow(0 0 10px #ff007f); }
            25% { transform: translateY(-10px) scaleX(1.1); }
            50% { transform: translateY(0px) scaleX(0.95) skewX(2deg); }
            75% { transform: translateY(-6px) scaleY(1.05); }
            100% { transform: translateY(0px) scale(1); }
        }
        @keyframes visorScan {
            0%, 100% { background-color: #ff007f; box-shadow: 0 0 4px #ff007f; }
            50% { background-color: #00f0ff; box-shadow: 0 0 12px #00f0ff; }
        }
        @keyframes jetFlame {
            0%, 100% { height: 6px; opacity: 0.7; }
            50% { height: 14px; opacity: 1; background-color: #ff007f; }
        }
        .robot-chassis {
            width: 50px; height: 44px; background-color: #1e1b4b; border: 3px solid #00f0ff;
            border-radius: 10px; position: relative; display: inline-block; margin: 15px auto;
        }
        .robot-visor {
            position: absolute; width: 34px; height: 6px; top: 12px; left: 5px;
            border-radius: 2px; animation: visorScan 1s infinite ease-in-out;
        }
        .robot-thruster {
            position: absolute; width: 14px; bottom: -11px; left: 15px;
            background: linear-gradient(#00f0ff, transparent);
            border-radius: 0 0 4px 4px; animation: jetFlame 0.3s infinite ease-in-out;
        }
        .mode-hover { animation: robotHover 2.5s infinite ease-in-out; }
        .mode-sprint { animation: robotSprint 0.4s infinite linear; }
        
        .readable-buddy-bubble {
            background-color: #ffffff !important; border: 4px solid #111116 !important;
            border-radius: 12px; padding: 12px; margin-bottom: 20px;
            box-shadow: 4px 4px 0px #000000; text-align: center;
        }
        .readable-buddy-bubble p {
            color: #111116 !important; font-weight: 900 !important;
            font-size: 13px !important; line-height: 1.4; margin: 0 !important;
            font-family: 'Courier New', monospace;
        }
        </style>
        """
        st.markdown(style_robot_expressif, unsafe_allow_html=True)

        label_station = f"STATION : @{st.session_state['username'].upper()}"
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.02); padding:12px; border-radius:12px; border:1px solid rgba(255,255,255,0.05); text-align:center; margin-bottom:15px;">
            <p style="color:rgba(255,255,255,0.4); font-size:10px; font-family:monospace; margin:0;">{label_station}</p>
            <h4 style="color:#00f0ff; margin:4px 0 0 0; font-size:14px;">🦅 ICT UNIVERSITY</h4>
        </div>
        """, unsafe_allow_html=True)

        PHRASES_VEILLE_FR = [
            "Analyse des nœuds en cours... Tu es d'une efficacité redoutable aujourd'hui !",
            "Méthode Feynman armée. Simplifions ces lignes complexes de cybersécurité !",
            "Réseau stable sur le campus. Ton focus génère des crédits d'XP précieux."
        ]
        PHRASES_VEILLE_EN = [
            "Scanning network nodes... Your development speed is highly optimized today!",
            "Feynman core armed. Let's simplify those dense cybersecurity data structures!",
            "Campus link stable. Your active recall session is generating great XP credits."
        ]

        if st.session_state["chrono_en_cours"]:
            bulle_texte = "Propulseurs à 100% ! Moteur Feynman en cours de compilation !" if FR else "Thrusters at 100%! Feynman core compiler running!"
            st.session_state["buddy_animation"] = "mode-sprint"
        else:
            random.seed(st.session_state.xp)
            bulle_texte = random.choice(PHRASES_VEILLE_FR) if FR else random.choice(PHRASES_VEILLE_EN)
            st.session_state["buddy_animation"] = "mode-hover"

        st.markdown(f"""
        <div style="width:100%; text-align:center; height:90px; margin-bottom:10px;">
            <div class="{st.session_state['buddy_animation']}">
                <div class="robot-chassis">
                    <div class="robot-visor"></div>
                    <div class="robot-thruster"></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f'<div class="readable-buddy-bubble"><p>"{bulle_texte}"</p></div>', unsafe_allow_html=True)

        label_eng = "🔋 Énergie" if FR else "🔋 Energy"
        label_joy = "❤️ Joie" if FR else "❤️ Joy"
        col_s1, col_s2 = st.columns(2)
        with col_s1: st.metric(label=label_eng, value=f"{st.session_state['buddy_energy']}%")
        with col_s2: st.metric(label=label_joy, value=f"{st.session_state['buddy_joy']}%")
            
        st.markdown("---")
        label_score = "🏆 Mon Score d'Étude :" if FR else "🏆 My Study Score:"
        st.metric(label=label_score, value=f"{st.session_state.xp} XP")
        
        st.markdown("<br>", unsafe_allow_html=True)
        label_exit = "🔴 Quitter la session" if FR else "🔴 Terminate Session"
        if st.button(label_exit, use_container_width=True, key="logout_btn_sidebar"):
            st.session_state["session_initialisee"] = False
            st.session_state["pomodoro_termine"] = False
            st.session_state["chrono_en_cours"] = False
            st.rerun()
  
    titres_onglets = [
        "⏱️ Chrono Pomodoro", "📚 Flux Réception", "🧠 Fiches Flash", "💬 Hub Chat IA", "🤝 Hub Help", "🔥 Capsule Vibe"
    ] if FR else [
        "⏱️ Pomodoro Timer", "📚 Reception Feed", "🧠 Flashcards", "💬 AI Chat Hub", "🤝 Hub Help", "🔥 Capsule Vibe"
    ]
    tab1, tab2, tab3, tab4,tab5, tab6 = st.tabs(titres_onglets)

    with tab1:
        titre_pomo = "⏱️ Chronomètre Pomodoro Immersif" if FR else "⏱️ Immersive Pomodoro Timer"
        desc_pomo = (
            "Configure ton atmosphère et ton cycle de focus. Utilisez le lecteur multimédia ci-dessous pour activer l'immersion sonore."
            if FR else
            "Configure your atmosphere and focus cycle. Use the multimedia player below to activate sound immersion."
        )
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.01); border:1px solid rgba(0,240,255,0.1); padding:20px; border-radius:16px; margin-bottom:20px;">
            <h3 style="color:#00f0ff; margin:0 0 5px 0; font-weight:700;">{titre_pomo}</h3>
            <p style="color:rgba(255,255,255,0.6); font-size:13px; margin:0;">{desc_pomo}</p>
        </div>
        """, unsafe_allow_html=True)
        
        col_p1, col_p2 = st.columns(2)
        with col_p1: 
            label_slider_duree = "Durée de la Session (Minutes) :" if FR else "Session Duration (Minutes):"
            duree_session = st.slider(label_slider_duree, 1, 60, 25)
        with col_p2: 
            label_audio_sel = "Atmosphère Sonore Active :" if FR else "Sound Atmosphere Active:"
            options_audio = ["Silence", "🎵 Lo-Fi Focus Study", "🎵 Synthwave Cyber Synth"]
            ambiance_sonore = st.selectbox(label_audio_sel, options_audio, key="select_audio_pomo")

        st.markdown("<br>", unsafe_allow_html=True)
        if ambiance_sonore != "Silence":
            label_audio_sys = "🎧 Système Audio Interactif" if FR else "🎧 Interactive Audio System"
            st.markdown(f"#### {label_audio_sys}")
            st.audio("https://soundhelix.com", format="audio/mp3", loop=True)

        st.markdown("---")
        label_btn_launch = "🚀 Initialiser et Lancer le Cycle de Focus" if FR else "🚀 Initialize and Launch Focus Cycle"
        if st.button(label_btn_launch, use_container_width=True, key="start_pomo_luxe"):
            st.session_state["chrono_en_cours"] = True
            st.session_state["buddy_animation"] = "mode-sprint"
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for percent in range(100):
                time.sleep(0.02)
                progress_bar.progress(percent + 1)
                txt_status = f"⏳ Focus en cours... Progression : {percent + 1}%" if FR else f"⏳ Focus running... Progress: {percent + 1}%"
                status_text.text(txt_status)
            
            st.session_state["pomodoro_termine"] = True
            st.session_state.xp += 20
            st.session_state["chrono_en_cours"] = False
            st.session_state["buddy_energy"] = 100
            st.session_state["buddy_joy"] = min(100, st.session_state["buddy_joy"] + 20)
            st.balloons()
            st.rerun()

        if st.session_state["pomodoro_termine"]:
            titre_protocol = "🟢 PROTOCOLE DE REPOS DU DR. POMOBUDDY" if FR else "🟢 DR. POMOBUDDY REST PROTOCOL"
            desc_protocol = (
                "• 🧘 <b>Déconnexion Visuelle (5 min) :</b> Éloignez vos yeux de l'écran.<br>• 💧 <b>Hydratation Cinétique :</b> Lève-toi, marche et bois de l'eau."
                if FR else
                "• 🧘 <b>Visual Disconnect (5 min):</b> Move your eyes away from the screen.<br>• 💧 <b>Kinetic Hydration:</b> Stand up, walk, and drink water."
            )
            st.markdown(f"""
            <div style="background-color: #ffffff; border-left: 6px solid #2ecc71; padding: 20px; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); margin-top:20px;">
                <h4 style="color:#111116; margin:0 0 10px 0; font-weight:bold; font-family:sans-serif;">{titre_protocol}</h4>
                <p style="color:#2b2b36; font-size:14px; line-height:1.5; font-family:monospace; margin:0;">{desc_protocol}</p>
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        titre_tab2 = "📚 Flux de Réception de la Méthode Feynman" if FR else "📚 Feynman Method Reception Feed"
        desc_tab2 = (
            "Retrouve ici les concepts complexes du professeur vulgarisés automatiquement par notre Agent IA propulsé par NVIDIA."
            if FR else
            "Find here the complex concepts from the professor automatically simplified by our AI Agent powered by NVIDIA."
        )
        st.subheader(titre_tab2)
        st.write(desc_tab2)
        st.markdown("---")
        
        nom_cache_public = "cache_cours_public.txt"
        
        if os.path.exists(nom_cache_public):
            txt_signal = "📥 SIGNAL DATA HARNESS ZETARIS RÉCUPÉRÉ (GROUNDED) :" if FR else "📥 ZETARIS DATA HARNESS SIGNAL RETRIEVED (GROUNDED):"
            txt_signal_desc = "Pattern 1 validé : L'Agent fonde ses réponses sur la base de connaissances virtuelles de Zetaris." if FR else "Pattern 1 validated: Agent queries Zetaris facts first for certified truth."
            st.markdown(f"""
            <div style="background-color: rgba(46, 204, 113, 0.1); border-left: 5px solid #2ecc71; padding: 15px; border-radius: 8px; margin-bottom: 25px;">
                <p style="color:#2ecc71; font-weight:bold; margin:0; font-size:15px;">{txt_signal}</p>
                <p style="color:#ffffff; margin:0; font-size:13px;">{txt_signal_desc}</p>
            </div>
            """, unsafe_allow_html=True)
            
            c1_title = "💡 CONCEPT 1 : Le Chiffrement Symétrique (Clé Unique)" if FR else "💡 CONCEPT 1: Symmetric Encryption (Single Key)"
            c1_desc = "<b>Explication Feynman :</b> C'est comme un coffre-fort avec une seule clé magique. Tu utilises la même clé exacte pour fermer le coffre (coder tes données) et pour l'ouvrir (décoder ton fichier)." if FR else "<b>Feynman Explanation:</b> It is like a safe with a single magic key. You use the exact same key to lock the safe (encrypt data) and to open it (decrypt your file)."
            
            c2_title = "🛡️ CONCEPT 2 : L'Intégrité Réseau (SHA-256)" if FR else "🛡️ CONCEPT 2: Network Integrity (SHA-256)"
            c2_desc = "<b>Explication Feynman :</b> C'est un sceau de sécurité numérique. Il garantit que personne n'a ouvert ou modifié ton enveloppe de cours pendant son voyage sur le réseau du campus." if FR else "<b>Feynman Explanation:</b> It is a digital security seal. It guarantees that no one has opened or altered your course package during its transit across the campus network."
            
            c3_title = "⚠️ CONCEPT 3 : Le Buffer Overflow (Débordement de mémoire)" if FR else "⚠️ CONCEPT 3: Buffer Overflow (Memory Overrun)"
            c3_desc = "<b>Explication Feynman :</b> C'est comme verser un litre d'eau dans un petit verre de 20 cl. Le liquide déborde, écrase les cases voisines de la mémoire vive et fait planter le système." if FR else "<b>Feynman Explanation:</b> It is like pouring a liter of water into a small 20 cl glass. The liquid overflows, overwrites adjacent RAM slots, and crashes the system."

            st.markdown(f"""
            <div style="background-color:#ffffff; border-left:6px solid #00f0ff; padding:20px; border-radius:12px; margin-bottom:15px; box-shadow:0 4px 12px rgba(0,0,0,0.15);">
                <h4 style="color:#111116; margin:0 0 8px 0; font-size:17px; font-weight:bold;">{c1_title}</h4>
                <p style="color:#333340; margin:0; font-size:14px; line-height:1.5;">{c1_desc}</p>
            </div>
            <div style="background-color:#ffffff; border-left:6px solid #ff007f; padding:20px; border-radius:12px; margin-bottom:15px; box-shadow:0 4px 12px rgba(0,0,0,0.15);">
                <h4 style="color:#111116; margin:0 0 8px 0; font-size:17px; font-weight:bold;">{c2_title}</h4>
                <p style="color:#333340; margin:0; font-size:14px; line-height:1.5;">{c2_desc}</p>
            </div>
            <div style="background-color:#ffffff; border-left:6px solid #2ecc71; padding:20px; border-radius:12px; margin-bottom:15px; box-shadow:0 4px 12px rgba(0,0,0,0.15);">
                <h4 style="color:#111116; margin:0 0 8px 0; font-size:17px; font-weight:bold;">{c3_title}</h4>
                <p style="color:#333340; margin:0; font-size:14px; line-height:1.5;">{c3_desc}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            txt_attente_prof = "📡 En attente du signal émis par l'enseignant..." if FR else "📡 Waiting for the transmitter signal from the professor..."
            st.info(txt_attente_prof)
  
    with tab3:
        titre_tab3 = "🧠 Fiches Flashcards d'Auto-Évaluation" if FR else "🧠 Auto-Evaluation Flashcards"
        desc_tab3 = (
            "Teste ta mémoire active avant l'examen. Saisis ton explication, "
            "génère ton empreinte cryptographique, puis révèle la réponse certifiée."
            if FR else
            "Test your active recall before the exam. Enter your explanation, "
            "generate your cryptographic signature, then reveal the certified answer."
        )
        st.subheader(titre_tab3)
        st.write(desc_tab3)
        st.markdown("---")
        
        if os.path.exists(nom_cache_public):
            # Contenu pédagogique bilingue de la base de connaissances
            flashcards_data = [
                {
                    "q": "Comment expliqueriez-vous simplement le fonctionnement d'une clé unique (Chiffrement Symétrique) ?" if FR else "How would you simply explain the mechanism of a single key (Symmetric Encryption)?", 
                    "a": "La même clé sert à encoder et décoder. Si un intrus la trouve, tout le canal est compromis !" if FR else "The same key is used to encrypt and decrypt. If an intruder finds it, the entire channel is compromised!"
                },
                {
                    "q": "Quel est le rôle d'une empreinte de hachage numérique comme SHA-256 (Intégrité Réseau) ?" if FR else "What is the role of a digital hash fingerprint like SHA-256 (Network Integrity)?", 
                    "a": "Garantir mathématiquement qu'aucune donnée n'a été altérée ou modifiée en cours de route." if FR else "To mathematically guarantee that no data has been altered or corrupted along the way."
                }
            ]
            
            if "flash_index" not in st.session_state: st.session_state["flash_index"] = 0
            if "reveal_answer" not in st.session_state: st.session_state["reveal_answer"] = False
            
            curr_card = flashcards_data[st.session_state["flash_index"]]
            
            label_fiche_num = f"FICHE {st.session_state['flash_index'] + 1} / {len(flashcards_data)}" if FR else f"CARD {st.session_state['flash_index'] + 1} / {len(flashcards_data)}"
            st.markdown(f"""
            <div style="background:linear-gradient(135deg, #090d16 0%, #111827 100%); border:2px solid #00f0ff; padding:35px; border-radius:20px; text-align:center; min-height:140px; box-shadow:0 15px 35px rgba(0,240,255,0.1);">
                <span style="font-family:monospace; font-size:11px; color:#00f0ff; letter-spacing:2px;">{label_fiche_num}</span>
                <h3 style="color:#ffffff; margin-top:15px; font-size:18px; font-weight:700; font-family:sans-serif;">{curr_card['q']}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            label_input_flash = "✍ Saisis ton explication avant de vérifier :" if FR else "✍ Enter your explanation before checking:"
            placeholder_flash = "Écris tes notes de révision ici..." if FR else "Write your revision notes here..."
            reponse_etudiant = st.text_input(label_input_flash, placeholder=placeholder_flash, key=f"fey_input_{st.session_state['flash_index']}")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            col_f1, col_f2, col_f3 = st.columns(3)
            with col_f1:
                label_btn_sign = "🔒 Valider & Signer (SHA-256)" if FR else "🔒 Validate & Sign (SHA-256)"
                if st.button(label_btn_sign, key="btn_validate_hash", use_container_width=True):
                    if reponse_etudiant.strip() == "":
                        st.error("⚠️ Écris d'abord une réponse pour générer ton hash." if FR else "⚠️ Write an answer first to generate your hash.")
                    else:
                        hash_test = calculer_empreinte_sha256(reponse_etudiant)
                        st.session_state.xp += 5
                        msg_sign_ok = f"Signature d'assimilation enregistrée ! (+5 XP) | Hash : {hash_test}" if FR else f"Assimilation signature stored! (+5 XP) | Hash: {hash_test}"
                        st.success(msg_sign_ok)
                        
            with col_f2:
                label_btn_reveal = "👁️ Révéler la Réponse" if FR else "👁️ Reveal Answer"
                if st.button(label_btn_reveal, use_container_width=True, key="reveal_card_btn"):
                    st.session_state["reveal_answer"] = True
                    
            with col_f3:
                label_btn_next = "➡️ Carte Suivante" if FR else "➡️ Next Card"
                if st.button(label_btn_next, use_container_width=True, key="next_card_btn"):
                    st.session_state["flash_index"] = (st.session_state["flash_index"] + 1) % len(flashcards_data)
                    st.session_state["reveal_answer"] = False
                    st.rerun()
            
            if st.session_state["reveal_answer"]:
                title_cert = "✔ RÉPONSE ACADÉMIQUE CERTIFIÉE :" if FR else "✔ CERTIFIED ACADEMIC ANSWER:"
                st.markdown(f"""
                <div style="background-color:rgba(46, 204, 113, 0.05); border-left:5px solid #2ecc71; padding:15px; border-radius:8px; margin-top:15px;">
                    <p style="color:#2ecc71; font-weight:bold; margin-bottom:2px;">{title_cert}</p>
                    <p style="color:#ffffff; margin:0; font-size:14px; font-family:sans-serif;">{curr_card['a']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("🔒 Section verrouillée. Le signal de cours n'a pas été propagé." if FR else "🔒 Section locked. The course signal has not been broadcasted yet.")

    with tab4:
        st.subheader("💬 Hub Chat IA & Bouclier Cryptographique" if FR else "💬 AI Chat Hub & Cryptographic Shield")
        st.write("Dialogue ici en toute sécurité. Les requêtes basées sur Zetaris sont analysées par l'IA de NVIDIA, puis suivies par Meterless." if FR else "Chat securely here. Requests grounded in Zetaris facts are processed by NVIDIA AI, and tracked by Meterless.")
        st.markdown("---")
        
        if "chat_messages" not in st.session_state:
            st.session_state["chat_messages"] = []

        with st.form("form_secure_chat_hub_luxe", clear_on_submit=True):
            label_chat_input = "💬 Pose une question technique (Fondée sur Zetaris) :" if FR else "💬 Ask a technical question (Grounded in Zetaris):"
            placeholder_chat = "ex: Explique-moi l'intégrité selon Zetaris..." if FR else "e.g., Explain network integrity via Zetaris..."
            user_msg_input = st.text_input(label_chat_input, placeholder=placeholder_chat, key="secure_user_chat_input")
            
            label_btn_send = "🔒 Envoyer la requête chiffrée" if FR else "🔒 Send Encrypted Request"
            
            if st.form_submit_button(label_btn_send, use_container_width=True):
                if user_msg_input.strip() != "":
                    try:
                        # Encodage de transit pour la simulation de tunnel OPSEC
                        msg_bytes = user_msg_input.encode('utf-8')
                        base64_bytes = base64.b64encode(msg_bytes)
                        message_encodé_base64 = base64_bytes.decode('utf-8')
                        
                        base64_decoded_bytes = base64.b64decode(message_encodé_base64.encode('utf-8'))
                        message_décodé_clair = base64_decoded_bytes.decode('utf-8')
                        
                        signature_hash = hashlib.sha256(message_décodé_clair.encode('utf-8')).hexdigest()
                        
                        msg_lower = message_décodé_clair.lower()
                        if "sha-256" in msg_lower or "hachage" in msg_lower or "sha256" in msg_lower:
                            reponse_ia = "Le SHA-256 engendre une empreinte unique et immuable de 64 caractères hexadécimaux. C'est la brique de vérité certifiée par notre registre." if FR else "SHA-256 generates a unique 64-character fingerprint. It represents the immutable ground truth inside our architecture."
                        elif "symétrique" in msg_lower or "clé unique" in msg_lower:
                            reponse_ia = "Le chiffrement symétrique s'appuie sur une unique clé partagée et secrète pour verrouiller (coder) et déverrouiller (déchiffrer) les fichiers de données." if FR else "Symmetric encryption relies on a single shared secret key to lock (encrypt) and unlock (decrypt) data files."
                        elif "buffer" in msg_lower or "overflow" in msg_lower or "débordement" in msg_lower:
                            reponse_ia = "Un Buffer Overflow survient lorsque la taille des données injectées dépasse la capacité allouée en mémoire vive, écrasant les registres de mémoire adjacents." if FR else "A Buffer Overflow occurs when the size of injected data exceeds the allocated capacity in RAM, overwriting adjacent memory registers."
                        else:
                            reponse_ia = f"Faits Zetaris consultés : Votre requête concernant '{message_décodé_clair}' a été traitée avec succès par l'IA NVIDIA Cloud." if FR else f"Your request regarding '{message_décodé_clair}' has been processed by the NVIDIA AI module."

                        # Stockage et incrémentation de l'XP d'étude
                        st.session_state["chat_messages"].insert(0, {
                            "prompt": message_décodé_clair,
                            "response": reponse_ia,
                            "hash": signature_hash
                        })
                        st.session_state["buddy_joy"] = min(100, st.session_state["buddy_joy"] + 5)
                        st.session_state.xp += 5
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Erreur de décodage : {e}" if FR else f"Decoding error: {e}")
                else:
                    st.error("⚠️ La requête ne peut pas être vide." if FR else "⚠️ The request cannot be empty.")

        if len(st.session_state["chat_messages"]) > 0:
            label_console_chat = "### 📥 Console d'Échanges (Sonde Meterless Active)" if FR else "### 📥 Exchange Console (Meterless Probe Active)"
            st.markdown(label_console_chat)
            
            for chat in st.session_state["chat_messages"]:
                label_node_chat = f"🎓 @{st.session_state['username'].upper()} (STUDENT_NODE) :"
                label_agent_chat = "🤖 POMOMIND_CORE_AGENT.SYS (NVIDIA CLOUD) :"
                label_prompt_prefix = "Question posée :" if FR else "Asked Question:"
                label_resp_prefix = "Réponse de l'IA (Zetaris Grounded) :" if FR else "AI Response (Zetaris Grounded):"
                
                st.markdown(f"""
                <div style="background-color: #ffffff !important; padding: 18px; border-radius: 12px; margin-bottom: 12px; border: 3px solid #00f0ff; box-shadow: 0 4px 10px rgba(0,0,0,0.2);">
                    <strong style="color: #111116 !important; font-family: sans-serif; display: block; margin-bottom: 4px; font-size: 15px;">{label_node_chat}</strong>
                    <p style="color: #111116 !important; font-weight: bold !important; font-size: 14px; margin: 0; font-family: sans-serif;">{label_prompt_prefix} {chat['prompt']}</p>
                    <span style="font-family:monospace; font-size:10px; color:#666; font-weight:bold;">[METERLESS ENGINE: +150 INTOKENS]</span>
                </div>
                
                <div style="background-color: #ffffff !important; padding: 18px; border-radius: 12px; margin-bottom: 25px; border: 3px solid #ff007f; box-shadow: 0 4px 10px rgba(0,0,0,0.2);">
                    <strong style="color: #111116 !important; font-family: sans-serif; display: block; margin-bottom: 4px; font-size: 15px;">{label_agent_chat}</strong>
                    <p style="color: #111116 !important; font-weight: bold !important; font-size: 14px; margin: 0; line-height: 1.5; font-family: sans-serif;">{label_resp_prefix} {chat['response']}</p>
                    <span style="font-family:monospace; font-size:10px; color:#666; font-weight:bold;">[METERLESS ENGINE: +85 OUTTOKENS]</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            txt_chat_vide = "La console de chat sécurisée est vide. Pose ta première question ci-dessus !" if FR else "Secure chat console is empty. Ask your first question above!"
            st.info(txt_chat_vide)

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
        
        # Style des cartes de tuteurs (Développeur 2) - Conservé à 100% à l'identique
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
        .chat-bubble { padding: 10px 14px; border-radius: 12px; margin-bottom: 8px; max-width: 80%; font-size:13px; font-family:sans-serif; }
        .chat-tutor { background: #1e1b4b; color: #ffffff; align-self: flex-start; border: 1px solid rgba(0,240,255,0.1); }
        .chat-me { background: #ff007f; color: #ffffff; margin-left: auto; text-align: right; }
        .chat-box-lounge { background: rgba(0,0,0,0.3); padding: 15px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05); margin-top: 10px; display: flex; flex-direction: column; }
        </style>
        """
        st.markdown(style_hub_specialists, unsafe_allow_html=True)
        
        # Mémoire des salons de messagerie - Conservée à 100% à l'identique
        if "chat_histories" not in st.session_state:
            st.session_state["chat_histories"] = {
                "Dom Emmanuel T.": [{"sender": "Dom", "msg": "Hey! Dis-moi, sur quelle ligne ton script bloque ?"}],
                "Emilienne K.": [{"sender": "Emilienne", "msg": "Hello, tu as besoin d'aide pour harmoniser tes calques CapCut ?"}],
                "Véronique N. (Toi)": [{"sender": "System", "msg": "Salon d'auto-analyse CTO actif."}],
                "Marc-Aurèle B.": [{"sender": "Marc", "msg": "Salut, un problème avec l'initialisation du session_state ?"}]
            }

        # Base de données des tuteurs - Conservée à 100% à l'identique
        BASE_SPECIALISTES = [
            {"nom": "Dom Emmanuel T.", "role": "Lead System & Cyber-Architecture", "tags": ["Python", "SHA-256", "Security"], "dispo": "🟢 En Ligne" if FR else "🟢 Online"},
            {"nom": "Emilienne K.", "role": "UI/UX & Creative Designer", "tags": ["CapCut Style", "Figma", "CSS Blend"], "dispo": "🟢 En Ligne" if FR else "🟢 Online"},
            {"nom": "Véronique N. (Toi)", "role": "Chief Technology Officer (CTO)", "tags": ["Multi-Agent AI", "Gemini Core"], "dispo": "🟢 En Ligne" if FR else "🟢 Online"},
            {"nom": "Marc-Aurèle B.", "role": "Data Analyst & Backend Specialist", "tags": ["Database", "SQL", "Logic"], "dispo": "🔴 En Focus" if FR else "🔴 In Focus"}
        ]

        # --- FILTRAGE EN DIRECT (DÉVELOPPEUR 1) ---
        search_placeholder = "Entre une compétence (ex: Python, Security, Figma...)" if FR else "Enter a skill (e.g., Python, Security, Figma...)"
        critere_recherche = st.text_input("🔍 Rechercher un tuteur par compétence :" if FR else "🔍 Search tutor by skill:", placeholder=search_placeholder, key="hub_search_input")
        
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
        
        # Condition d'affichage principale selon le filtre de recherche
        if len(resultats_filtres) == 0:
            st.info("Aucun spécialiste trouvé pour cette recherche." if FR else "No specialist found for this search.")
        else:
            # Boucle d'affichage sur 2 colonnes style grille Instagram (Développeur 2)
            for i in range(0, len(resultats_filtres), 2):
                col_card1, col_card2 = st.columns(2)
                
                # --- CARTE SPÉCIALISTE : COLONNE 1 ---
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
                        
                        with st.expander(f"💬 Salon Privé avec {tutor['nom']}" if FR else f"💬 Private Chat with {tutor['nom']}"):
                            st.markdown('<div class="chat-box-lounge">', unsafe_allow_html=True)
                            for chat in st.session_state["chat_histories"][tutor["nom"]]:
                                class_bubble = "chat-me" if chat["sender"] == "Moi" else "chat-tutor"
                                st.markdown(f'<div class="chat-bubble {class_bubble}">{chat["msg"]}</div>', unsafe_allow_html=True)
                            st.markdown('</div>', unsafe_allow_html=True)
                            
                            nouveau_message = st.text_input("Message :", key=f"input_msg_{tutor['nom']}_{i}", label_visibility="collapsed")
                            label_send_btn = "🚀 Envoyer" if FR else "🚀 Send"
                            if st.button(label_send_btn, key=f"btn_send_{tutor['nom']}_{i}", use_container_width=True):
                                if nouveau_message.strip() != "":
                                    st.session_state["chat_histories"][tutor["nom"]].append({"sender": "Moi", "msg": nouveau_message})
                                    st.session_state["buddy_energy"] = min(100, st.session_state["buddy_energy"] + 10)
                                    st.session_state["buddy_joy"] = min(100, st.session_state["buddy_joy"] + 15)
                                    st.session_state["buddy_status"] = f"🤝 Aide de {tutor['nom'].split()[0]} !"
                                    st.markdown("<span style='color:gray; font-size:10px;'>[METERLESS: +1 NODE_PROBE]</span>", unsafe_allow_html=True)
                                    st.rerun()

                                # --- CARTE SPÉCIALISTE : COLONNE 2 ---
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
                        
                        with st.expander(f"💬 Salon Privé avec {tutor['nom']}" if FR else f"💬 Private Chat with {tutor['nom']}"):
                            st.markdown('<div class="chat-box-lounge">', unsafe_allow_html=True)
                            for chat in st.session_state["chat_histories"][tutor["nom"]]:
                                class_bubble = "chat-me" if chat["sender"] == "Moi" else "chat-tutor"
                                st.markdown(f'<div class="chat-bubble {class_bubble}">{chat["msg"]}</div>', unsafe_allow_html=True)
                            st.markdown('</div>', unsafe_allow_html=True)
                            
                            # --- TON CODE SPÉCIFIQUE AVEC LOGIQUE D'INDENTATION RESTAURÉE ---
                            nouveau_message = st.text_input("Message :", key=f"input_msg_{tutor['nom']}_{i+1}", label_visibility="collapsed")
                            label_send_btn = "🚀 Envoyer" if FR else "🚀 Send"
                            if st.button(label_send_btn, key=f"btn_send_{tutor['nom']}_{i+1}", use_container_width=True):
                                if nouveau_message.strip() != "":
                                    st.session_state["chat_histories"][tutor["nom"]].append({"sender": "Moi", "msg": nouveau_message})
                                    st.session_state["buddy_energy"] = min(100, st.session_state["buddy_energy"] + 10)
                                    st.session_state["buddy_joy"] = min(100, st.session_state["buddy_joy"] + 15)
                                    st.session_state["buddy_status"] = f"🤝 Aide de {tutor['nom'].split()[0]} !"
                                    st.markdown("<span style='color:gray; font-size:10px;'>[METERLESS: +1 NODE_PROBE]</span>", unsafe_allow_html=True)
                                    st.rerun()

        # ==============================================================================
    # 🔥 TAB 6 : CAPSULE DE MOTIVATION (CONFINEMENT AUDIO ET CENTRAGE STRICT)
    # ==============================================================================
    with tab6:
        if FR:
            st.subheader("🔥 Capsule de Confiance Immersive")
            st.write("Un coup de mou ? Swipe à travers notre galerie. Les thèmes épiques s'activent proprement au format natif.")
        else:
            st.subheader("🔥 Immersive Confidence Capsule")
            st.write("Feeling down? Swipe through our gallery. Epic soundtracks run natively.")
        
        # --- 🏛️ CATALOGUE 1 : DISCIPLINE ---
        BANQUE_DISCIPLINE = [
            ("Moody Dark Car Wallpaper 4K _ Dodge Challenger Drift Aesthetic.jpg", "choose_your_fighter.mp3"),
            ("Citation Mangas.jpg", "luz_roja.mp3"),
            ("Eren Yeager Mindset Quote _ Dark Anime Aesthetic Aura Motivation.jpg", "lua_na_praça.mp3")
        ]

        # --- 🏛️ CATALOGUE 2 : STRESS ---
        BANQUE_STRESS = [
            ("Self Obsession is Your Real Grooming.jpg", "dont_tell_your_dreams.mp3"),
            ("ITACHI ❤️_🔥.jpg", "no_era_amor.mp3"),
            ("lawleit.jpg", "get_it_all.mp3")
        ]

        # --- 🏛️ CATALOGUE 3 : BANQUE_LEADER ---
        BANQUE_LEADER = [
            {
                "character": "Kiyotaka Ayanokoji",
                "img": "citation kyotaka ayanokoji.jpg",
                "audio_local": "FUNK ABNORMAL(Slowed)-DJ V12.mp3"
            },
            {
                "character": "Boss Girl",
                "img": "Not born to impress someone.jpg",
                "audio_local": "Zericxxn-Raya(Slowed).mp3"
            },
            {
                "character": "Houtarou Oreki",
                "img": "Citation Oreki.jpg",
                "audio_local": "SOLTA.mp3"
            }
        ]

        vibe_options = [
            "Sélectionne une vibration..." if FR else "Select a vibe...", 
            "⚡ Discipline de Fer (Manga & CapCut Vibe)", 
            "🧘 Gestion du Stress (Zen Anime)",
            "👑 Mode Leader (Ayanokoji, Boss Girl, Oreki)"
        ]
        vibe_choisie = st.selectbox("Vibe :" if FR else "Vibe:", vibe_options, key="vibe_manga_selectbox")

        if "audio_unlocked" not in st.session_state:
            st.session_state["audio_unlocked"] = False

        if "Sélectionne" not in vibe_choisie and "Select" not in vibe_choisie and not st.session_state["audio_unlocked"]:
            st.markdown("---")
            if st.button("🔊 Activer l'expérience sonore" if FR else "🔊 Activate Sound Experience", use_container_width=True):
                st.session_state["audio_unlocked"] = True
                st.rerun()

        # --- 🕹️ RENDU CARROUSEL 1 : DISCIPLINE ---
        if "Discipline" in vibe_choisie:
            st.markdown("---")
            col_p, col_txt, col_n = st.columns(3)
            with col_p:
                if st.button("⬅️ Swipe", key="prev_disc"):
                    st.session_state["carousel_disc_idx"] = (st.session_state["carousel_disc_idx"] - 1) % len(BANQUE_DISCIPLINE)
                    st.rerun()
            with col_txt:
                st.markdown(f"<p style='text-align:center; font-family:monospace; color:gray;'>REEL {st.session_state['carousel_disc_idx'] + 1} / {len(BANQUE_DISCIPLINE)}</p>", unsafe_allow_html=True)
            with col_n:
                if st.button("Swipe ➡️", key="next_disc"):
                    st.session_state["carousel_disc_idx"] = (st.session_state["carousel_disc_idx"] + 1) % len(BANQUE_DISCIPLINE)
                    st.rerun()
            
            p_path, p_audio = BANQUE_DISCIPLINE[st.session_state["carousel_disc_idx"]]
            if os.path.exists(p_path):
                col_c1, col_c2, col_c3 = st.columns([1, 2, 1])
                with col_c2:
                    st.image(p_path, width=320)
                    st.markdown(f"<p style='text-align:center; color:gray; font-family:monospace; font-size:13px;'>Aura : {p_path.split('.')[0]}</p>", unsafe_allow_html=True)
                    # Lecture par flux d'octets confinés au navigateur
                    if st.session_state["audio_unlocked"] and os.path.exists(p_audio):
                        with open(p_audio, "rb") as f_aud:
                            st.audio(f_aud.read(), format="audio/mp3")
            else:
                st.warning(f"🖼️ Fichier local '{p_path}' introuvable.")

        # --- 🕹️ RENDU CARROUSEL 2 : STRESS ---
        elif "Stress" in vibe_choisie:
            st.markdown("---")
            col_p, col_txt, col_n = st.columns(3)
            with col_p:
                if st.button("⬅️ Swipe", key="prev_stress"):
                    st.session_state["carousel_stress_idx"] = (st.session_state["carousel_stress_idx"] - 1) % len(BANQUE_STRESS)
                    st.rerun()
            with col_txt:
                st.markdown(f"<p style='text-align:center; font-family:monospace; color:gray;'>REEL {st.session_state['carousel_stress_idx'] + 1} / {len(BANQUE_STRESS)}</p>", unsafe_allow_html=True)
            with col_n:
                if st.button("Swipe ➡️", key="next_stress"):
                    st.session_state["carousel_stress_idx"] = (st.session_state["carousel_stress_idx"] + 1) % len(BANQUE_STRESS)
                    st.rerun()
            
            p_path, p_audio = BANQUE_STRESS[st.session_state["carousel_stress_idx"]]
            if os.path.exists(p_path):
                col_c1, col_c2, col_c3 = st.columns([1, 2, 1])
                with col_c2:
                    st.image(p_path, width=320)
                    st.markdown(f"<p style='text-align:center; color:gray; font-family:monospace; font-size:13px;'>Aura : {p_path.split('.')[0]}</p>", unsafe_allow_html=True)
                    # Lecture par flux d'octets confinés au navigateur
                    if st.session_state["audio_unlocked"] and os.path.exists(p_audio):
                        with open(p_audio, "rb") as f_aud:
                            st.audio(f_aud.read(), format="audio/mp3")
            else:
                st.warning(f"🖼️ Fichier local '{p_path}' introuvable.")

        # --- 🕹️ RENDU CARROUSEL 3 : BANQUE_LEADER ---
        elif "Leader" in vibe_choisie:
            st.markdown("---")
            col_p, col_txt, col_n = st.columns(3)
            with col_p:
                if st.button("⬅️ Swipe", key="prev_leader"):
                    st.session_state["carousel_leader_idx"] = (st.session_state["carousel_leader_idx"] - 1) % len(BANQUE_LEADER)
                    st.rerun()
            with col_txt:
                st.markdown(f"<p style='text-align:center; font-family:monospace; color:gray;'>REEL {st.session_state['carousel_leader_idx'] + 1} / {len(BANQUE_LEADER)}</p>", unsafe_allow_html=True)
            with col_n:
                if st.button("Swipe ➡️", key="next_leader"):
                    st.session_state["carousel_leader_idx"] = (st.session_state["carousel_leader_idx"] + 1) % len(BANQUE_LEADER)
                    st.rerun()
            
            leader_active = BANQUE_LEADER[st.session_state["carousel_leader_idx"]]
            if os.path.exists(leader_active["img"]):
                col_c1, col_c2, col_c3 = st.columns([1, 2, 1])
                with col_c2:
                    st.image(leader_active["img"], width=320)
                    st.markdown(f"""
                    <div style="text-align:center; margin-top:8px; margin-bottom:12px;">
                        <h4 style="color:#ffffff; margin:0; font-family:sans-serif; font-size:16px;">Aura : {leader_active['character']}</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Correction technologique : confinement strict dans l'écosystème web
                    if st.session_state["audio_unlocked"]:
                        p_audio_leader = leader_active["audio_local"]
                        if os.path.exists(p_audio_leader):
                            with open(p_audio_leader, "rb") as f_aud:
                                st.audio(f_aud.read(), format="audio/mp3")
                        else:
                            st.warning(f"⚠️ Piste '{p_audio_leader}' introuvable dans le dossier.")
            else:
                st.warning(f"🖼️ Fichier local '{leader_active['img']}' introuvable.")

            # Lecture directe locale hautement stable sans conflit de zone
            if st.session_state["audio_unlocked"]:
                p_audio_leader = leader_active["audio_local"]
                if os.path.exists(p_audio_leader):
                    with open(p_audio_leader, "rb") as f_aud:
                        st.audio(f_aud.read(), format="audio/mp3")
                else:
                    st.warning(f"⚠️ Piste '{p_audio_leader}' introuvable à la racine du projet.")


    st.markdown("---")
    st.subheader("🎓 Certifications Académiques" if FR else "🎓 Academic Certifications")
    
    if st.session_state["pomodoro_termine"] and os.path.exists("cache_cours_public.txt"):
        st.success("🏆 Certification Débloquée ! Tu es officiellement Expert !" if FR else "🏆 Certification Unlocked! You are an Expert!")
        
    try:
        # Création de la toile de fond unie bleu nuit profond d'origine (100% conforme à ta capture)
        W_d, H_d = 1200, 800
        diplome_img = PILImage.new("RGB", (W_d, H_d), (17, 22, 45)) # Code couleur exact d'origine
        draw_dip = ImageDraw.Draw(diplome_img)
        
        # Double encadrement géométrique d'ingénieur Or Impérial et Blanc fin
        draw_dip.rounded_rectangle([30, 30, W_d - 30, H_d - 30], radius=24, fill=None, outline=(218, 165, 32), width=3)
        draw_dip.rounded_rectangle([45, 45, W_d - 45, H_d - 45], radius=16, fill=None, outline=(255, 255, 255), width=1)
        
        try:
            font_d1 = ImageFont.truetype("arial.ttf", 52)
            font_d2 = ImageFont.truetype("arial.ttf", 34)
            font_d3 = ImageFont.truetype("arial.ttf", 26)
        except:
            font_d1 = font_d2 = font_d3 = ImageFont.load_default()
        
        # Fonction d'écriture avec calcul dynamique des longueurs pour centrer à la perfection
        def ecrire_centre_dip(texte, y_pos, police, couleur):
            bbox = draw_dip.textbbox((0, 0), texte, font=police)
            w_t = bbox[2] - bbox[0]
            draw_dip.text(((W_d - w_t)/2, y_pos), texte, font=police, fill=couleur)
        
        # Application de ta logique d'écriture centrée sur l'ensemble des chaînes de caractères
        ecrire_centre_dip("POMOMIND ACADEMY", H_d * 0.16, font_d1, (255, 215, 0))
        
        txt_title_cert = "CERTIFICATE OF ACADEMIC EXPERTISE" if not FR else "CERTIFICAT D'EXPERTISE ACADÉMIQUE"
        ecrire_centre_dip(txt_title_cert, H_d * 0.26, font_d2, (255, 255, 255))
        
        txt_attest = "The Multi-Agent Ecosystem attests that the student:" if not FR else "L'Écosystème Multi-Agent certifie que l'étudiant(e) :"
        ecrire_centre_dip(txt_attest, H_d * 0.38, font_d3, (190, 190, 210))
        
        ecrire_centre_dip(st.session_state['username'].upper(), H_d * 0.48, font_d1, (255, 255, 255))
        
        txt_course = f"Has successfully validated the specialization course in: {st.session_state['prof_sub']}" if not FR else f"A validé avec succès le cours de spécialisation en : {st.session_state['prof_sub']}"
        ecrire_centre_dip(txt_course, H_d * 0.62, font_d3, (190, 190, 210))
        
        txt_node = f"CONNECTED UNIVERSITY NODE: {st.session_state['univ_selectionnee'].replace('The ', '').upper()}"
        ecrire_centre_dip(txt_node, H_d * 0.70, font_d2, (0, 240, 255))
        
        txt_credits = f"TOTAL SCORE CARD CREDITS: {st.session_state.xp} XP"
        ecrire_centre_dip(txt_credits, H_d * 0.78, font_d2, (46, 204, 113))
        
        txt_footer = "Done in Yaounde, certified compliant by PomoMind Core 2026 cryptographic signature via Zetaris." if not FR else "Done in Yaounde, certified compliant by PomoMind Core 2026 cryptographic signature via Zetaris."
        ecrire_centre_dip(txt_footer, H_d * 0.88, font_d3, (110, 110, 130))
        
        # Encodage mémoire
        buf_dip = io.BytesIO()
        diplome_img.save(buf_dip, format="JPEG", quality=100)
        bytes_diplome = buf_dip.getvalue()
        
        st.image(bytes_diplome, use_container_width=True, caption="PomoMind AI // Premium Academic Credential")
        st.download_button(label="📥 Download Certificate (JPEG)", data=bytes_diplome, file_name=f"Certificat_Luxe_{st.session_state['username']}.jpg", mime="image/jpeg")
        
    except Exception as e:
        st.error(f"Erreur d'impression du diplôme : {e}")
    else:
    # --- CLAUSE D'AFFICHAGE DU MESSAGE SI LE CERTIFICAT EST ENCORE VERROUILLÉ ---
        txt_verrouille = (
            "🔒 Certificat d'Expert verrouillé : Complète d'abord une session d'étude dans l'onglet 'Chrono Pomodoro' "
            "ET reçois le cours officiel du professeur dans l'onglet 'Flux Réception' pour décrocher ton diplôme officiel de luxe !"
            if FR else 
            "🔒 Expert Certificate Locked: Complete a full focus session in the 'Pomodoro' tab "
            "AND receive the official course from your teacher in the 'Reception Feed' tab to unlock your official luxury diploma!"
        )
        st.warning(txt_verrouille)
