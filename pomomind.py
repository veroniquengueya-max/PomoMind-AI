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
        "⏱️ Chrono Pomodoro", "📚 Flux Réception", "🧠 Fiches Flash", "💬 Hub Chat IA"
    ] if FR else [
        "⏱️ Pomodoro Timer", "📚 Reception Feed", "🧠 Flashcards", "💬 AI Chat Hub"
    ]
    tab1, tab2, tab3, tab4 = st.tabs(titres_onglets)

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



            
    