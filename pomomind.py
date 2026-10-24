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

# --- TRACKER DE SESSIONS QUOTIDIENNES ANTI-INSTAGRAM ---
if "capsule_sessions_aujourdhui" not in st.session_state:
    st.session_state["capsule_sessions_aujourdhui"] = 0

if "capsule_chrono_actif" not in st.session_state:
    st.session_state["capsule_chrono_actif"] = False

# --- INITIALISATION DE LA SÉCURITÉ ET DES CYCLES DU CHRONO POMODORO ---
if "pomodoro_cycles_completed" not in st.session_state:
    st.session_state["pomodoro_cycles_completed"] = 0

if "pomodoro_current_phase" not in st.session_state:
    st.session_state["pomodoro_current_phase"] = "focus"  # Options : "focus" ou "pause"

if "pomodoro_lock_active" not in st.session_state:
    st.session_state["pomodoro_lock_active"] = False

# --- BASE DE DONNÉES SÉCURISÉE EN MÉMOIRE (SIMULATION EN TRANSIT) ---
if "comptes_utilisateurs" not in st.session_state:
    st.session_state["comptes_utilisateurs"] = {}  # Stockage : {username: hash_password}

if "user_role_actif" not in st.session_state:
    st.session_state["user_role_actif"] = None

# --- MÉMOIRE DE L'EMPLOI DU TEMPS INTÉLLIGENT NVIDIA ---
if "planning_personnalise" not in st.session_state:
    st.session_state["planning_personnalise"] = []

# ==============================================================================
# 🦅 COEUR DE SÉCURITÉ : SYSTÈME D'AUTHENTIFICATION CRYPTOGRAPHIQUE DOUBLE ONGLÈTE
# ==============================================================================
if not st.session_state["session_initialisee"]:
    st.markdown(f"""
    <div style="text-align:center; margin-bottom:30px;">
        <h1 style="color:#00f0ff; font-family:sans-serif; font-size:42px; margin-bottom:10px;">🦅 POMOMIND AI</h1>
        <p style="color:rgba(255,255,255,0.6); font-size:16px;">
            {"Écosystème d'Étude Multi-Agent Universitaire Sécurisé Core 2026" if FR else "Secure University Multi-Agent Study Ecosystem Core 2026"}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Création des deux onglets distincts sur une même ligne d'état
    tab_se_connecter, tab_s_inscrire = st.tabs(["🔐 Connexion / Login", "📝 Inscription / Register"])
    
    # --- ONGLÈTE 1 : FORMULAIRE DE CONNEXION ÉTANCHE ---
    with tab_se_connecter:
        st.markdown("### 🔐 Accéder à mon Espace Privé" if FR else "### 🔐 Access My Private Space")
        with st.form("form_login_core"):
            login_user = st.text_input("🎯 Identifiant (Username) :", placeholder="ex: veronique_cto", key="login_username_input").strip()
            login_pass = st.text_input("🔒 Mot de passe / Password :", type="password", key="login_password_input")
            univ_node = st.selectbox("🏫 Connected Campus Node :", ["The ICT University (Yaoundé)"])
            
            if st.form_submit_button("🚀 Connexion sécurisée" if FR else "🚀 Secure Login", use_container_width=True):
                if login_user == "" or login_pass == "":
                    st.error("⚠️ Saisis ton identifiant et ton mot de passe." if FR else "⚠️ Enter your username and password.")
                elif login_user not in st.session_state["comptes_utilisateurs"]:
                    st.error("❌ Identifiant inconnu sur ce nœud universitaire." if FR else "❌ Unknown username on this university node.")
                else:
                    hash_tentative = calculer_empreinte_sha256(login_pass)
                    compte_valide = st.session_state["comptes_utilisateurs"][login_user]
                    
                    if hash_tentative == compte_valide["password_hash"]:
                        st.session_state["username"] = login_user
                        st.session_state["univ_selectionnee"] = univ_node
                        st.session_state["user_role_actif"] = compte_valide["role"]
                        
                        sub_decouvert = "Informatique Générale"
                        name_decouvert = "Professeur Titulaire"
                        if os.path.exists("cache_cours_public.txt"):
                            with open("cache_cours_public.txt", "r", encoding="utf-8") as f_in:
                                for l in f_in.readlines():
                                    if "METADATA_SUB:" in l: sub_decouvert = l.replace("METADATA_SUB:", "").strip()
                                    if "METADATA_NAME:" in l: name_decouvert = l.replace("METADATA_NAME:", "").strip()
                        
                        st.session_state["prof_sub"] = sub_decouvert
                        st.session_state["prof_name"] = name_decouvert
                        st.session_state["session_initialisee"] = True
                        st.success("✅ Authentification cryptographique validée. Redirection..." if FR else "✅ Cryptographic authentication validated. Redirecting...")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("🚨 Mot de passe incorrect ! Alerte Guardrail Sécurité." if FR else "🚨 Incorrect password! Security Guardrail Alert.")

    # --- ONGLÈTE 2 : FORMULAIRE D'INSCRIPTION AVEC AUTO-LOGIN COMPRIS ---
    with tab_s_inscrire:
        st.markdown("### 📝 Créer un compte unique" if FR else "### 📝 Create a Unique Account")
        with st.form("form_registration_core"):
            reg_user = st.text_input("🎯 Identifiant unique (Username) :", placeholder="ex: veronique_cto", key="reg_username_input").strip()
            reg_pass = st.text_input("🔒 Mot de passe / Password :", type="password", key="reg_password_input")
            reg_role = st.selectbox("🎭 Type de profil / Profile Type :", ["Student (Étudiant / Adulte)", "Professor (Enseignant)"])
            prof_secret_key = st.text_input("🔑 Code Secret Enseignant (Laisser vide si étudiant) :", type="password")
            
            if st.form_submit_button("💾 Enregistrer et Entrer" if FR else "💾 Register and Enter", use_container_width=True):
                if reg_user == "" or reg_pass == "":
                    st.error("⚠️ Tous les champs sont obligatoires." if FR else "⚠️ All fields are required.")
                elif reg_user in st.session_state["comptes_utilisateurs"]:
                    st.error("🚨 Cet identifiant existe déjà." if FR else "🚨 This username already exists.")
                elif "Professor" in reg_role and prof_secret_key != "PROF2026":
                    st.error("🚨 Code Secret Enseignant invalide !" if FR else "🚨 Invalid Professor Secret Code!")
                else:
                    hash_secure = calculer_empreinte_sha256(reg_pass)
                    role_defini = "prof" if "Professor" in reg_role else "eleve"
                    
                    st.session_state["comptes_utilisateurs"][reg_user] = {
                        "password_hash": hash_secure,
                        "role": role_defini
                    }
                    
                    st.session_state["username"] = reg_user
                    st.session_state["univ_selectionnee"] = "The ICT University (Yaoundé)"
                    st.session_state["user_role_actif"] = role_defini
                    st.session_state["prof_sub"] = "Architecture Système & Cybersécurité" if FR else "System Architecture & Cybersecurity"
                    st.session_state["prof_name"] = "Dr. Dom Emmanuel T."
                    st.session_state["session_initialisee"] = True
                    st.success("🎯 Compte créé et connecté automatiquement ! Redirection..." if FR else "🎯 Account created and auto-logged in! Redirecting...")
                    time.sleep(1)
                    st.rerun()
            else:
                    st.error("🚨 Mot de passe incorrect ! Alerte Guardrail Sécurité." if FR else "🚨 Incorrect password! Security Guardrail Alert.")
            # ==============================================================================
    # 🦅 COEUR DE SÉCURITÉ : COMMUTATEUR ET REDIRECTION ÉTANCHE DES RÔLES (PARTIE C)
    # ==============================================================================
    st.markdown("<br><hr>", unsafe_allow_html=True)

    # Redirection automatique et hermétique selon le privilège validé par le Guardrail
    if st.session_state["user_role_actif"] == "prof":
        st.markdown("### 👨‍🏫 Console de Diffusion Officielle de l'Enseignant" if FR else "### 👨‍🏫 Official Professor Broadcast Console")
        st.write(
            "Téléversez ici le fichier brut de vos notes de cours ou votre syllabus. L'écosystème Zetaris et NVIDIA analysera son intégrité avant de le propager au campus."
            if FR else
            "Upload the raw file of your lecture notes or syllabus here. The Zetaris and NVIDIA ecosystem will analyze its integrity before broadcasting it to the campus."
        )
        
        nom_cache_public = "cache_cours_public.txt"
        
        with st.form("form_prof_diffusion_feynman"):
            label_pname = "Nom de l'Enseignant :" if FR else "Professor's Name:"
            label_psub = "Intitulé de la matière / UE :" if FR else "Course Title / Module:"
            p_name = st.text_input(label_pname, value="Dr. Dom Emmanuel T.")
            p_sub = st.text_input(label_psub, value="Architecture Système & Cybersécurité" if FR else "System Architecture & Cybersecurity")
            
            label_uploader = "📁 Sélectionner le fichier officiel du cours (.pdf) :" if FR else "📁 Select the official course file (.pdf):"
            fichier_cours_brut = st.file_uploader(label_uploader, type=["pdf"], key="prof_file_feynman_uploader")
            
            label_submit_prof = "⚡ Analyser et Propager le cours au Campus" if FR else "⚡ Analyze and Broadcast Course to Campus"
            if st.form_submit_button(label_submit_prof, use_container_width=True):
                if fichier_cours_brut is not None:
                    try:
                        contenu_brut = fichier_cours_brut.read().decode("utf-8", errors="ignore")
                        
                        mots_interdits = ["bavardage", "fête", "triche", "hacker", "malware", "soirée", "foot", "vacances"]
                        contient_inutile = any(mot in contenu_brut.lower() for mot in mots_interdits)
                        
                        if contenu_brut.strip() == "":
                            st.error("⚠️ Erreur réseau : Le fichier téléversé est totalement vide." if FR else "⚠️ Network Error: The uploaded file is completely empty.")
                        elif contient_inutile:
                            st.error("🚨 [ALERTE GUARDRAIL SÉCURITÉ] Flux rejeté ! Détection de termes illicites compromettant l'intégrité du campus." if FR else "🚨 [SECURITY GUARDRAIL ALERT] Stream rejected! Detection of illicit terms compromising campus integrity.")
                        else:
                            txt_spinner = "L'Agent Feynman propulsé par NVIDIA analyse le syllabus..." if FR else "The Feynman Agent powered by NVIDIA is analyzing the syllabus..."
                            with st.spinner(txt_spinner):
                                time.sleep(1.5)  # Simulation du temps de calcul de l'inférence NVIDIA
                                
                                # --- MOTEUR GÉNÉRATIF CONTEXTUEL NVIDIA (ALGORITHME D'ADAPTATION DE L'AURA) ---
                                matiere_lower = p_sub.lower()
                                
                                if "cyber" in matiere_lower or "sécurité" in matiere_lower or "security" in matiere_lower:
                                    concepts_generes = f"""
                                    CONCEPT 1 : Le Chiffrement Symétrique (Verrouillage à clé unique) | Symmetric Encryption
                                    EXPLICATION : {"C'est comme un coffre-fort avec une seule clé magique. Tu utilises la même clé exacte pour fermer le coffre (coder tes données) et pour l'ouvrir (décoder ton fichier). Tout le monde doit cacher cette clé !" if FR else "It's like a safe with a single magic key. You use the exact same key to lock the safe (encrypt data) and open it (decrypt file). Everyone must hide this key!"}
                                    ---
                                    CONCEPT 2 : L'Intégrité Réseau (Le cachet de cire numérique) | Network Integrity
                                    EXPLICATION : {"C'est la certitude absolue que personne n'a ouvert ou modifié ton enveloppe de cours pendant son voyage sur le réseau du campus. C'est validé de manière mathématique par la fonction SHA-256." if FR else "It is the absolute certainty that no one opened or altered your lecture envelope during its transit over the campus network. It is mathematically validated by the SHA-256 function."}
                                    ---
                                    CONCEPT 3 : Le Buffer Overflow (Le débordement de mémoire) | Buffer Overflow
                                    EXPLICATION : {"C'est l'équivalent de verser un litre d'eau dans un petit verre de 20 cl. Le liquide déborde partout : les données en trop écrasent les cases voisines de la mémoire vive et font planter le système." if FR else "It is the equivalent of pouring a liter of water into a small 20 cl glass. The liquid overflows everywhere: the excess data overwrites adjacent memory cells in RAM and crashes the system."}
                                    """
                                elif "réseau" in matiere_lower or "network" in matiere_lower or "proto" in matiere_lower:
                                    concepts_generes = f"""
                                    CONCEPT 1 : Le Routage IP (Le facteur du Net) | IP Routing
                                    EXPLICATION : {"C'est comme un facteur à moto dans les rues de Yaoundé. Il regarde l'adresse écrite sur l'enveloppe de ton paquet de données et cherche le chemin le plus rapide de carrefour en carrefour pour le livrer sans le perdre." if FR else "It's like a mailman on a motorcycle in the streets of Yaounde. He looks at the address written on your data packet envelope and finds the fastest path from intersection to intersection to deliver it without losing it."}
                                    ---
                                    CONCEPT 2 : Le Commutateur (Switch) vs Routeur | Switch vs Router
                                    EXPLICATION : {"Le Switch est le chef de classe : il distribue les papiers uniquement aux élèves à l'intérieur de la salle. Le Routeur, lui, est le gardien du portail du campus : il prend ton courrier et l'envoie vers l'extérieur, dans une autre école." if FR else "The Switch is the classroom monitor: it distributes papers only to students inside the room. The Router is the campus gatekeeper: it takes your mail and sends it outside to another school."}
                                    ---
                                    CONCEPT 3 : La Bande Passante (L'Avenue Kennedy aux heures de pointe) | Bandwidth
                                    EXPLICATION : {"C'est la largeur de l'autoroute numérique. Si l'avenue est étroite et qu'il y a trop de voitures (de données) en même temps, tout le monde est bloqué dans les embouteillages et ton cours met du temps à se charger." if FR else "It's the width of the digital highway. If the avenue is narrow and there are too many cars (data) at the same time, everyone gets stuck in traffic jams and your lecture takes time to load."}
                                    """
                                else:
                                    # Plan de secours sémantique universel s'il s'agit d'une autre matière tapée par le prof
                                    concepts_generes = f"""
                                    CONCEPT 1 : L'Abstraction Sémantique (La caricature simplifiée) | Semantic Abstraction
                                    EXPLICATION : {"C'est l'art de dessiner uniquement les contours importants d'un problème complexe pour le comprendre d'un seul coup d'œil, sans se perdre dans les micro-détails techniques." if FR else "It's the art of drawing only the important outlines of a complex problem to understand it at a single glance, without getting lost in technical micro-details."}
                                    ---
                                    CONCEPT 2 : Algorithme (La recette du Ndolé) | Algorithm Execution
                                    EXPLICATION : {"Un algorithme n'est pas magique : c'est une suite d'instructions strictes et ordonnées, comme les étapes de préparation d'un plat. Si tu inverses l'ordre des ingrédients, le résultat final est gâté." if FR else "An algorithm isn't magic: it's a sequence of strict, ordered instructions, like the steps to prepare a dish. If you reverse the order of ingredients, the final result is ruined."}
                                    ---
                                    CONCEPT 3 : La Base de Données (Le grand registre du secrétariat) | Database Storage
                                    EXPLICATION : {"C'est un entrepôt virtuel ultra-ordonné où chaque information possède sa propre étagère numérotée. Au lieu de fouiller tout le campus, l'IA sait exactement dans quelle case piocher en une milliseconde." if FR else "It's an ultra-organized virtual warehouse where every piece of information has its own numbered shelf. Instead of searching the whole campus, the AI knows exactly which cell to pick from in a millisecond."}
                                    """

                                # Compilation et écriture dans le coffre-fort de données Zetaris
                                feynman_cards_compiled = f"""
                                METADATA_SUB: {p_sub}
                                METADATA_NAME: {p_name}
                                ---
                                {concepts_generes.strip()}
                                """
                                with open(nom_cache_public, "w", encoding="utf-8") as f_vault:
                                    f_vault.write(feynman_cards_compiled.strip())
                                st.session_state.xp += 15
                                st.session_state["buddy_joy"] = min(100, st.session_state["buddy_joy"] + 15)
                                st.session_state["buddy_status"] = "📚 Cours assimilé par Feynman !" if FR else "📚 Course assimilated by Feynman!"
                                
                                st.success("✅ Cours validé par le Guardrail et converti par la Méthode Feynman avec succès !" if FR else "✅ Course validated by the Guardrail and successfully converted by the Feynman Method!")
                                time.sleep(1)
                                # Déconnexion automatique pour libérer le terminal sécurisé
                                st.session_state["session_initialisee"] = False
                                st.session_state["user_role_actif"] = None
                                st.rerun()
                    except Exception as e:
                        st.error(f"🚨 Faille de traitement du fichier : {e}" if FR else f"🚨 File processing failure: {e}")
                else:
                    st.error("⚠️ Veuillez téléverser un fichier physique .pdf pour initialiser la diffusion." if FR else "⚠️ Please upload a physical .pdf file to initialize broadcasting.")

    elif st.session_state["user_role_actif"] == "eleve":
        # Le code laisse ici le flux s'écouler naturellement vers tes 7 onglets d'étudiants (Pomodoro, Planning...)
        pass

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
        "⏱️ Chrono Pomodoro", "📅 Planning & Examens", "📚 Flux Réception", 
        "🧠 Fiches Flash", "💬 Hub Chat IA", "🤝 Hub Help", "🔥 Capsule Motivation"
    ] if FR else [
        "⏱️ Pomodoro Timer", "📅 Schedule & Exams", "📚 Reception Feed", 
        "🧠 Flashcards", "💬 AI Chat Hub", "🤝 Hub Help", "🔥 Motivation Capsule"
    ]
    tab1, tab_planning, tab2, tab3, tab4, tab5, tab6 = st.tabs(titres_onglets)


    with tab1:
        st.markdown("""
        <div style="background:rgba(255,255,255,0.01); border:1px solid rgba(0,240,255,0.1); padding:20px; border-radius:16px; margin-bottom:20px;">
            <h3 style="color:#00f0ff; margin:0 0 5px 0; font-weight:700;">⏱️ Chronomètre Pomodoro Officiel (Anti-Spam)</h3>
            <p style="color:rgba(255,255,255,0.6); font-size:13px; margin:0;">Cycle réglementaire : 4 sessions de 25 minutes suivies de 5 minutes de pause pour débloquer tes crédits d'étude.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Affichage graphique de l'état actuel des 4 cycles
        cycles_faits = st.session_state["pomodoro_cycles_completed"]
        phase_actuelle = st.session_state["pomodoro_current_phase"]
        
        if cycles_faits >= 4:
            st.success("🎯 Félicitations ! Tu as complété la session maximale de 4 cycles d'étude avec succès !" if FR else "🎯 Congratulations! You have successfully completed the maximum session of 4 study cycles!")
        else:
            col_status1, col_status2 = st.columns(2)
            with col_status1:
                label_cycle_txt = f"📈 Progression : Cycle **{cycles_faits + 1} / 4**" if FR else f"📈 Progress: Cycle **{cycles_faits + 1} / 4**"
                st.markdown(label_cycle_txt)
            with col_status2:
                label_phase_txt = f"🎭 Phase active : **{phase_actuelle.upper()}**"
                st.markdown(f"<p style='text-align:right;'>{label_phase_txt}</p>", unsafe_allow_html=True)

        col_p1, col_p2 = st.columns(2)
        with col_p1: 
            # Fixation stricte de la durée selon la phase réglementaire (Pas de slider tricheur)
            if phase_actuelle == "focus":
                duree_minutes = 25
                label_duree_active = "⏱️ Temps de Focus Imposé : 25 Minutes" if FR else "⏱️ Enforced Focus Time: 25 Minutes"
            else:
                duree_minutes = 5
                label_duree_active = "🧘 Temps de Pause Imposé : 5 Minutes" if FR else "🧘 Enforced Break Time: 5 Minutes"
            st.info(label_duree_active)
            
        with col_p2: 
            options_audio = ["Silence", "🎵 no_friends", "🎵 mockingbird"]
            ambiance_sonore = st.selectbox("Atmosphère Sonore Active :" if FR else "Sound Atmosphere:", options_audio, key="select_audio_pomo")

        st.markdown("<br>", unsafe_allow_html=True)
        if ambiance_sonore != "Silence":
            track_file = "no_friends.mp3" if "no_friends" in ambiance_sonore else "mockingbird.mp3"
            if os.path.exists(track_file):
                with open(track_file, "rb") as f_audio:
                    st.audio(f_audio.read(), format="audio/mp3", loop=True)
            else:
                st.audio("https://soundhelix.com", format="audio/mp3", loop=True)

        st.markdown("---")
                # --- ⏳ ZONE D'AFFICHAGE DU COMPTE À REBOURS NUMÉRIQUE ---
        zone_temps_horloge = st.empty()
        status_action_text = st.empty()
        
        # Formatage initial de l'horloge au repos
        zone_temps_horloge.markdown(f"""
        <div style="text-align:center; margin:20px 0;">
            <h1 style="font-family:monospace; font-size:68px; color:#00f0ff; margin:0;">{duree_minutes:02d}:00</h1>
        </div>
        """, unsafe_allow_html=True)

        # Désactivation du bouton si les 4 cycles sont terminés ou si le chrono tourne déjà
        bouton_desactive = st.session_state["pomodoro_lock_active"] or st.session_state["pomodoro_cycles_completed"] >= 4
        
        label_action_btn = (
            "🚀 Démarrer la session" if phase_actuelle == "focus" else "🧘 Démarrer la pause"
        ) if FR else (
            "🚀 Start Session" if phase_actuelle == "focus" else "🧘 Start Break"
        )
        
        if st.button(label_action_btn, use_container_width=True, key="action_pomo_cycle_core", disabled=bouton_desactive):
            st.session_state["chrono_en_cours"] = True
            st.session_state["pomodoro_lock_active"] = True
            st.session_state["buddy_animation"] = "mode-sprint"
            
            # Conversion stricte de la durée réelle en secondes pour le décrément
            # (Pour ta démo de soutenance rapide, tu peux diviser par 60 si tu veux accélérer le test)
            total_secondes = duree_minutes * 60
            
            # --- BOUCLE TECHNIQUE DU COMPTE À REBOURS STRICT ---
            while total_secondes > 0:
                mins, secs = divmod(total_secondes, 60)
                zone_temps_horloge.markdown(f"""
                <div style="text-align:center; margin:20px 0;">
                    <h1 style="font-family:monospace; font-size:68px; color:#ff007f; margin:0;">{mins:02d}:{secs:02d}</h1>
                </div>
                """, unsafe_allow_html=True)
                
                txt_animation_status = (
                    f"⏳ Focus en cours (Cycle {cycles_faits + 1}/4)... Ne quitte pas l'onglet !" 
                    if phase_actuelle == "focus" else 
                    f"🧘 Pause active... Respire profondément et relâche la tension."
                ) if FR else (
                    f"⏳ Focus active (Cycle {cycles_faits + 1}/4)... Stay on this tab!" 
                    if phase_actuelle == "focus" else 
                    f"🧘 Break active... Breathe deeply and relax."
                )
                status_action_text.text(txt_animation_status)
                
                time.sleep(1)
                total_secondes -= 1
                        # --- 🏁 ACTIONS ET DISTRIBUTION DES CRÉDITS EN FIN DE CYCLE STREAK ---
            st.session_state["chrono_en_cours"] = False
            st.session_state["pomodoro_lock_active"] = False
            
            if phase_actuelle == "focus":
                # Fin des 25 minutes de travail : attribution des points
                st.session_state.xp += 20
                st.session_state["buddy_energy"] = max(0, st.session_state["buddy_energy"] - 25)
                st.session_state["buddy_joy"] = min(100, st.session_state["buddy_joy"] + 15)
                st.session_state["buddy_status"] = "🧠 Session de 25 min validée ! (+20 XP)" if FR else "🧠 25 min Session validated! (+20 XP)"
                
                # Bascule automatique vers la phase de repos réglementaire
                st.session_state["pomodoro_current_phase"] = "pause"
                st.session_state["pomodoro_termine"] = True
                
                st.balloons()
            else:
                # Fin des 5 minutes de pause : régénération du Tamagotchi
                st.session_state["buddy_energy"] = 100
                st.session_state["buddy_joy"] = min(100, st.session_state["buddy_joy"] + 20)
                st.session_state["buddy_status"] = "🧘 Pause terminée ! Prêt pour le focus." if FR else "🧘 Break over! Ready for focus."
                
                # Validation officielle du cycle complet et retour au focus
                st.session_state["pomodoro_cycles_completed"] += 1
                st.session_state["pomodoro_current_phase"] = "focus"
                
                # Message vocal ou sonore de fin de pause
                st.markdown("#### 🔊 Message Vocal de ton Coach (Fin de session) :")
                if os.path.exists("coach_break.mp3"):
                    with open("coach_break.mp3", "rb") as f_break:
                        st.audio(f_break.read(), format="audio/mp3", autoplay=True)
                else:
                    st.audio("https://soundhelix.com", format="audio/mp3", autoplay=True)
            
            st.rerun()

        # Affichage du protocole d'hygiène de vie d'origine si une session vient d'aboutir
        if st.session_state["pomodoro_termine"] and phase_actuelle == "pause":
            if FR:
                st.markdown("""
            <div style="background-color: #ffffff; border-left: 6px solid #2ecc71; padding: 20px; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); margin-top:20px;">
                <h4 style="color:#111116; margin:0 0 10px 0; font-weight:bold; font-family:sans-serif;">🟢 PROTOCOLE DE REPOS DU DR. POMOBUDDY</h4>
                <p style="color:#2b2b36; font-size:14px; line-height:1.5; font-family:monospace; margin:0;">
                    • 🧘 <b>Déconnexion Visuelle (5 min) :</b> Éloignez vos yeux de l'écran pour détendre vos muscles oculaires.<br>
                    • 💧 <b>Hydratation Cinétique :</b> Lève-toi, marche et bois de l'eau. Ton cerveau consomme 20% de ton énergie primaire.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style="background-color: #ffffff !important; border-left: 6px solid #2ecc71 !important; padding: 20px; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); margin-top:20px;">
                    <h4 style="color:#111116 !important; margin:0 0 10px 0; font-weight:bold; font-family:sans-serif;">🟢 DR. POMOBUDDY'S REST PROTOCOL</h4>
                    <p style="color:#2b2b36 !important; font-size:14px; line-height:1.5; font-family:monospace; margin:0;">
                        • 🧘 <b>Visual Disconnection (5 min):</b> Move your eyes away from the screen to relax your ocular muscles.<br>
                        • 💧 <b>Kinetic Hydration:</b> Stand up, walk around, and drink water. Your brain consumes 20% of your primary energy.
                    </p>
                </div>
                """, unsafe_allow_html=True)
      
    with tab_planning:
        title_plan = "📅 Planificateur d'Examens Intelligent NVIDIA" if FR else "📅 NVIDIA Intelligent Exam Scheduler"
        desc_plan = (
            "Saisis tes prochaines matières d'évaluation. L'Agent NVIDIA générera ta feuille de route de révision sur-mesure."
            if FR else
            "Enter your upcoming exam subjects. The NVIDIA Agent will generate your customized revision roadmap."
        )
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.01); border:1px solid rgba(0,240,255,0.1); padding:20px; border-radius:16px; margin-bottom:20px;">
            <h3 style="color:#00f0ff; margin:0 0 5px 0; font-weight:700;">{title_plan}</h3>
            <p style="color:rgba(255,255,255,0.6); font-size:13px; margin:0;">{desc_plan}</p>
        </div>
        """, unsafe_allow_html=True)

        # --- FORMULAIRE D'AJOUT DYNAMIQUE D'ÉVALUATION ---
        st.markdown("### 📝 Ajouter une Évaluation" if FR else "### 📝 Add an Assessment")
        with st.form("form_ajout_planning_nvidia", clear_on_submit=True):
            col_in1, col_col2 = st.columns(2)
            with col_in1:
                input_matiere = st.text_input("📚 Intitulé de la matière / Subject :", placeholder="ex: Algorithme, Réseaux, Cyber...")
                input_date = st.text_input("📅 Date de l'examen / Date :", placeholder="ex: 04 Novembre 2026")
            with col_col2:
                input_type = st.selectbox("🎭 Type d'examen / Exam Type :", ["Examen Final / Final Exam", "Contrôle Continu / Quiz", "Rattrapage / Resit"])
                input_prio = st.selectbox("🚨 Priorité de révision / Priority :", ["🚨 Haute / Critical High", "⚠️ Moyenne / Medium", "🟢 Normale / Low"])

            if st.form_submit_button("💾 Injecter dans la Matrice NVIDIA" if FR else "💾 Inject into NVIDIA Matrix", use_container_width=True):
                if input_matiere.strip() == "" or input_date.strip() == "":
                    st.error("⚠️ Veuillez remplir l'intitulé et la date de l'évaluation." if FR else "⚠️ Please enter the subject title and the exam date.")
                else:
                    # Ajout direct dans l'état de session persistant
                    st.session_state["planning_personnalise"].append({
                        "matiere": input_matiere.strip(),
                        "date": input_date.strip(),
                        "type": input_type,
                        "priorite": input_prio
                    })
                    st.success("✅ Évaluation enregistrée ! Moteur d'inférence prêt." if FR else "✅ Assessment registered! Inference engine ready.")
                    time.sleep(0.5)
                    st.rerun()

        
        st.markdown("---")
        st.markdown("### 📥 Mon Emploi du Temps d'Évaluation" if FR else "### 📥 My Assessment Schedule")

        # Affichage dynamique des examens saisis par l'étudiant
        if len(st.session_state["planning_personnalise"]) == 0:
            st.info("💡 Aucun examen enregistré pour le moment. Utilise le formulaire ci-dessus pour initialiser ton calendrier." if FR else "💡 No exams registered yet. Use the form above to initialize your schedule.")
        else:
            for idx, exam in enumerate(st.session_state["planning_personnalise"]):
                label_date_txt = "Date :" if FR else "Date:"
                label_prio_txt = "Priorité :" if FR else "Priority:"
                
                st.markdown(f"""
                <div style="background-color:rgba(255,255,255,0.02); padding:15px; border-radius:10px; margin-bottom:12px; border-left:4px solid #ff007f;">
                    <strong style="font-size:16px; color:#ffffff;">{exam['matiere']}</strong> — <span style="color:#00f0ff;">{exam['type']}</span><br>
                    <span style="font-size:13px; color:gray;">📅 {label_date_txt} {exam['date']} | {label_prio_txt} {exam['priorite']}</span>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("### 🧠 Conseiller de Révision Stratégique NVIDIA AI" if FR else "### 🧠 NVIDIA AI Strategic Revision Advisor")

            # Récupération dynamique de la liste des matières saisies pour le sélecteur de conseils
            liste_choix = [e["matiere"] for e in st.session_state["planning_personnalise"]]
            
            label_select = "🎯 Choisis la matière à analyser par NVIDIA AI :" if FR else "🎯 Select the subject for NVIDIA AI analysis:"
            choix_matiere = st.selectbox(label_select, liste_choix, key="sb_planning_custom_advisor")

            if choix_matiere:
                matiere_lower = choix_matiere.lower()
                
                # --- ALGORITHME D'INFÉRENCE SÉMANTIQUE DE NVIDIA AI ---
                if "cyber" in matiere_lower or "sécurité" in matiere_lower or "crypt" in matiere_lower:
                    guide_titre = f"🛡️ [NVIDIA INFERENCE] Feuille de Route : {choix_matiere}"
                    guide_etapes = [
                        "**Étape 1 (Focus Pomodoro) :** Bloque 25 minutes sur les algorithmes cryptographiques asymétriques et symétriques." if FR else "**Step 1 (Pomodoro Focus):** Spend 25 minutes on asymmetric and symmetric cryptographic algorithms.",
                        "**Étape 2 (Vérification Active) :** Génère un hash SHA-256 dans l'onglet Fiches Flash pour comprendre le principe d'intégrité." if FR else "**Step 2 (Active Verification):** Generate a SHA-256 hash in the Flashcards tab to understand the principle of integrity.",
                        "**Étape 3 (AI Guardrail) :** Simule une attaque par débordement de tampon dans le Hub Chat IA pour analyser les réponses du bouclier." if FR else "**Step 3 (AI Guardrail):** Simulate a buffer overflow attack in the AI Chat Hub to analyze the shield's responses."
                    ]
                    conseil_coach = "💡 *Dr. PomoBuddy :* La sécurité exige de la rigueur. Utilise 2 cycles de 25 minutes d'étude pure sans aucune distraction." if FR else "💡 *Dr. PomoBuddy:* Security requires rigor. Use 2 cycles of 25 minutes of pure study without any distraction."
                
                elif "réseau" in matiere_lower or "net" in matiere_lower or "rout" in matiere_lower:
                    guide_titre = f"🌐 [NVIDIA INFERENCE] Feuille de Route : {choix_matiere}"
                    guide_etapes = [
                        "**Étape 1 (Focus Pomodoro) :** Consacre 25 minutes à réviser le modèle OSI et l'encapsulation des paquets IP." if FR else "**Step 1 (Pomodoro Focus):** Spend 25 minutes reviewing the OSI model and IP packet encapsulation.",
                        "**Étape 2 (Feynman) :** Explique la différence entre un commutateur et un routeur à l'aide d'une métaphore simple (chef de classe vs gardien)." if FR else "**Step 2 (Feynman):** Explain the difference between a switch and a router using a simple metaphor (class monitor vs gatekeeper).",
                        "**Étape 3 (Zetaris Integration) :** Synchronise tes connaissances sur la topologie réseau avec le flux diffusé par ton professeur." if FR else "**Step 3 (Zetaris Integration):** Sync your network topology knowledge with the stream broadcast by your professor."
                    ]
                    conseil_coach = "💡 *Dr. PomoBuddy :* Les réseaux se comprennent par le schéma. Dessine l'architecture pendant tes 5 minutes de pause." if FR else "💡 *Dr. PomoBuddy:* Networks are understood through diagrams. Draw the architecture during your 5-minute breaks."
                
                else:
                    # Générateur de plan universel intelligent adaptatif si la matière est inconnue
                    guide_titre = f"🧠 [NVIDIA INFERENCE] Feuille de Route Personnalisée : {choix_matiere}"
                    guide_etapes = [
                        "**Étape 1 (Focus Pomodoro) :** Isole les concepts fondamentaux de cette matière pendant une session de 25 minutes sans tricher." if FR else "**Step 1 (Pomodoro Focus):** Isolate the core concepts of this subject during a strict 25-minute session without cheating.",
                        "**Étape 2 (Déconstruction) :** Rédige une fiche explicative vulgarisée. Si un enfant de 10 ans ne peut pas la comprendre, réduis la complexité." if FR else "**Step 2 (Deconstruction):** Write a simplified explanatory card. If a 10-year-old cannot understand it, reduce the complexity.",
                        "**Étape 3 (Recall Actif) :** Teste ta mémoire en fermant tes notes et en écrivant les définitions clés sous forme de hachage." if FR else "**Step 3 (Active Recall):** Test your memory by closing your notes and writing key definitions as a cryptographic signature."
                    ]
                    conseil_coach = "💡 *Dr. PomoBuddy :* NVIDIA AI a généré ce plan adaptatif. Atteins les 100 XP d'étude pour débloquer ton diplôme officiel !" if FR else "💡 *Dr. PomoBuddy:* NVIDIA AI generated this adaptive plan. Reach 100 study XP to unlock your official diploma!"

                # Rendu graphique haut de gamme de la feuille de route
                st.markdown(f"""
                <div style="background:rgba(0, 240, 255, 0.03); border:1px solid rgba(0, 240, 255, 0.2); padding:20px; border-radius:12px; margin-top:15px;">
                    <h4 style="color:#00f0ff; margin-top:0; font-family:sans-serif;">{guide_titre}</h4>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                for etape in guide_etapes:
                    st.markdown(f"- {etape}")
                    
                st.markdown("---")
                st.info(conseil_coach)

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
    # 🔥 TAB 6 : CAPSULE DE MOTIVATION (PARTIE A CORRIGÉE - ORDRE DE COMPILATION OK)
    # ==============================================================================
        # ==============================================================================
    # 🔥 TAB 6 : CAPSULE DE MOTIVATION (PARTIE A - HORLOGE & SÉLECTEUR UNIQUE)
    # ==============================================================================
    with tab6:
        # Durée réglementaire d'une recharge d'Aura : 20 minutes
        DUREE_CAPSULE_MINUTES = 20
        MAX_SESSIONS_PAR_JOUR = 2

        # --- 🏛️ LES DICTIONNAIRES DE PRODUCTION FORMAT TUPLE ---
        BANQUE_DISCIPLINE = [
            ("Moody Dark Car Wallpaper 4K _ Dodge Challenger Drift Aesthetic.jpg", "choose_your_fighter.mp3"),
            ("Citation Mangas.jpg", "luz_roja.mp3"),
            ("Eren Yeager Mindset Quote _ Dark Anime Aesthetic Aura Motivation.jpg", "lua_na_praça.mp3")
        ]

        # S'assure que la banque de stress contient bien tes 3 éléments d'origine
        BANQUE_STRESS = [
            ("Self Obsession is Your Real Grooming.jpg", "dont_tell_your_dreams.mp3"),
            ("ITACHI ❤️_🔥.jpg", "no_era_amor.mp3"),
            ("lawleit.jpg", "get_it_all.mp3")
        ]

        # Format Tuple unifié pour la banque Leader comme demandé
        BANQUE_LEADER = [
            ("citation kyotaka ayanokoji.jpg", "baila_lento.mp3"),
            ("Not born to impress someone.jpg", "raya.mp3"),
            ("Citation Oreki.jpg", "solta.mp3")
        ]

        # --- 🎯 LE SÉLECTEUR DE VIBE UNIQUE AVEC CLÉ PROPRE ---
        vibe_options = [
            "Sélectionne une vibration..." if FR else "Select a vibe...", 
            "⚡ Discipline", 
            "🧘 Stress", 
            "👑 Leader"
        ]
        vibe_choisie = st.selectbox("Vibe :", vibe_options, key="vibe_manga_selectbox_unique")
        zone_audio_dynamique = st.empty()

        # --- ⏳ PROTECTION ET REFRESH DE L'ONGLET ---
        if "ancienne_vibe_check" not in st.session_state:
            st.session_state["ancienne_vibe_check"] = vibe_choisie

        if vibe_choisie != st.session_state["ancienne_vibe_check"]:
            st.session_state["capsule_chrono_actif"] = False
            st.session_state["ancienne_vibe_check"] = vibe_choisie

        # --- CONDITION 1 : LE QUOTA QUOTIDIEN EST ATTEINT ---
        if st.session_state["capsule_sessions_aujourdhui"] >= MAX_SESSIONS_PAR_JOUR:
            st.error("🚨 [AI GUARDRAIL] ACCÈS LIMITÉ ! QUOTA QUOTIDIEN ÉPUISÉ" if FR else "🚨 [AI GUARDRAIL] ACCESS DENIED! DAILY QUOTA EXHAUSTED")
            st.warning(
                "Tu as atteint la limite maximale de 2 sessions de motivation par jour. L'effet 'Instagram Junior' est bloqué "
                "pour préserver tes neurones. Retourne étudier dans l'onglet Chrono !"
                if FR else
                "You have reached the maximum limit of 2 motivation sessions per day. The 'Instagram Junior' effect is blocked "
                "to protect your focus. Go back to study in the Chrono tab!"
            )
            if st.button("⏱️ Reprendre l'Étude Réglementaire" if FR else "⏱️ Resume Enforced Study", use_container_width=True):
                st.rerun()

        # --- CONDITION 2 : ACCÈS AUTORISÉ ➔ COMPTEUR & RECHARGE ---
        else:
            col_cap_info1, col_cap_info2 = st.columns(2)
            with col_cap_info1:
                st.markdown(f"🎟️ Sessions consommées : **{st.session_state['capsule_sessions_aujourdhui']} / {MAX_SESSIONS_PAR_JOUR}**" if FR else f"🎟️ Daily Sessions used: **{st.session_state['capsule_sessions_aujourdhui']} / {MAX_SESSIONS_PAR_JOUR}**")
            with col_cap_info2:
                st.markdown(f"<p style='text-align:right; color:#ff007f;'>⏱️ Temps par recharge : 20:00</p>", unsafe_allow_html=True)

            zone_horloge_capsule = st.empty()
            
            if not st.session_state["capsule_chrono_actif"]:
                zone_horloge_capsule.markdown(f"""
                <div style="text-align:center; margin:15px 0;">
                    <h1 style="font-family:monospace; font-size:52px; color:#ff007f; margin:0;">20:00</h1>
                </div>
                """, unsafe_allow_html=True)

                label_start_cap = "🔊 Allumer le Moteur d'Aura" if FR else "🔊 Ignite Aura Engine"
                if st.button(label_start_cap, use_container_width=True, key="btn_declencher_timer_capsule"):
                    st.session_state["capsule_chrono_actif"] = True
                    st.session_state["capsule_sessions_aujourdhui"] += 1
                    
                    total_sec_capsule = DUREE_CAPSULE_MINUTES * 60
                    
                    while total_sec_capsule > 0 and st.session_state["capsule_chrono_actif"]:
                        c_mins, c_secs = divmod(total_sec_capsule, 60)
                        zone_horloge_capsule.markdown(f"""
                        <div style="text-align:center; margin:15px 0;">
                            <h1 style="font-family:monospace; font-size:52px; color:#00f0ff; margin:0;">{c_mins:02d}:{c_secs:02d}</h1>
                        </div>
                        """, unsafe_allow_html=True)
                        time.sleep(1)
                        total_sec_capsule -= 1
                    
                    st.session_state["capsule_chrono_actif"] = False
                    st.rerun()

            if FR:
                st.subheader("🔥 Capsule de Confiance Immersive")
            else:
                st.subheader("🔥 Immersive Confidence Capsule")

       
                # --- 🕹️ RENDU CARROUSEL 1 : DISCIPLINE ---
        if "Discipline" in vibe_choisie or "Iron" in vibe_choisie:
            st.markdown("---")
            if "carousel_disc_idx" not in st.session_state: 
                st.session_state["carousel_disc_idx"] = 0
            
            col_p, col_txt, col_n = st.columns(3)
            with col_p:
                if st.button("⬅️ Swipe", key="prev_disc"):
                    st.session_state["carousel_disc_idx"] = (st.session_state["carousel_disc_idx"] - 1) % len(BANQUE_DISCIPLINE)
                    st.rerun()
            with col_txt:
                st.markdown(f"<p style='text-align:center; font-family:monospace; color:rgba(255,255,255,0.4); margin-top:8px;'>REEL {st.session_state['carousel_disc_idx'] + 1} / {len(BANQUE_DISCIPLINE)}</p>", unsafe_allow_html=True)
            with col_n:
                if st.button("Swipe ➡️", key="next_disc"):
                    st.session_state["carousel_disc_idx"] = (st.session_state["carousel_disc_idx"] + 1) % len(BANQUE_DISCIPLINE)
                    st.rerun()
            
            curr_idx = st.session_state["carousel_disc_idx"]
            p_path, p_audio = BANQUE_DISCIPLINE[curr_idx]
            
            if os.path.exists(p_path):
                with open(p_path, "rb") as img_file: 
                    b64_img = base64.b64encode(img_file.read()).decode()
                st.markdown(f"""
                <div style="width:100%; text-align:center; margin-top:10px;">
                    <img src="data:image/jpeg;base64,{b64_img}" style="width:100%; max-width:380px; border-radius:16px; border:none !important; box-shadow:none !important;">
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning(f"🖼️ Fichier local '{p_path}' introuvable.")

            if st.session_state["audio_unlocked"]:
                player_id = f"audio_node_disc_{curr_idx}_{int(time.time())}"
                audio_src = f"data:audio/mp3;base64,{base64.b64encode(open(p_audio, 'rb').read()).decode()}" if os.path.exists(p_audio) else "https://soundhelix.com"
                
                zone_audio_dynamique.markdown(f"""
                <audio id="{player_id}" autoplay><source src="{audio_src}" type="audio/mp3"></audio>
                <script>
                var pInst = document.getElementById("{player_id}");
                if(pInst) {{
                    pInst.volume = 0.50;
                    setTimeout(function() {{ pInst.pause(); pInst.src=''; }}, 30000);
                }}
                </script>
                """, unsafe_allow_html=True)

                # --- 🕹️ RENDU CARROUSEL 2 : STRESS ---
        elif "Stress" in vibe_choisie or "Management" in vibe_choisie:
            st.markdown("---")
            if "carousel_stress_idx" not in st.session_state: 
                st.session_state["carousel_stress_idx"] = 0
            
            col_p, col_txt, col_n = st.columns(3)
            with col_p:
                if st.button("⬅️ Swipe", key="prev_stress"): 
                    st.session_state["carousel_stress_idx"] = (st.session_state["carousel_stress_idx"] - 1) % len(BANQUE_STRESS)
                    st.rerun()
            with col_txt:
                st.markdown(f"<p style='text-align:center; font-family:monospace; color:rgba(255,255,255,0.4); margin-top:8px;'>REEL {st.session_state['carousel_stress_idx'] + 1} / {len(BANQUE_STRESS)}</p>", unsafe_allow_html=True)
            with col_n:
                if st.button("Swipe ➡️", key="next_stress"):
                    st.session_state["carousel_stress_idx"] = (st.session_state["carousel_stress_idx"] + 1) % len(BANQUE_STRESS)
                    st.rerun()
            
            curr_idx = st.session_state["carousel_stress_idx"]
            p_path, p_audio = BANQUE_STRESS[curr_idx]
            
            if os.path.exists(p_path):
                with open(p_path, "rb") as img_file: 
                    b64_img = base64.b64encode(img_file.read()).decode()
                st.markdown(f"""
                <div style="width:100%; text-align:center; margin-top:10px;">
                    <img src="data:image/jpeg;base64,{b64_img}" style="width:100%; max-width:380px; border-radius:16px; border:none !important; box-shadow:none !important;">
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning(f"🖼️ Fichier local '{p_path}' introuvable.")

            if st.session_state["audio_unlocked"]:
                player_id = f"audio_node_stress_{curr_idx}_{int(time.time())}"
                audio_src = f"data:audio/mp3;base64,{base64.b64encode(open(p_audio, 'rb').read()).decode()}" if os.path.exists(p_audio) else "https://soundhelix.com"
                
                zone_audio_dynamique.markdown(f"""
                <audio id="{player_id}" autoplay><source src="{audio_src}" type="audio/mp3"></audio>
                <script>
                var pInst = document.getElementById("{player_id}");
                if(pInst) {{
                    pInst.volume = 0.50;
                    setTimeout(function() {{ pInst.pause(); pInst.src=''; }}, 30000);
                }}
                </script>
                """, unsafe_allow_html=True)

                # --- 🕹️ RENDU CARROUSEL 3 : BANQUE_LEADER (TAILLE COMPACTE & VRAI FADE-IN CAPCUT) ---
        elif "Leader" in vibe_choisie or "👑" in vibe_choisie:
            st.markdown("---")
            if "carousel_leader_idx" not in st.session_state: 
                st.session_state["carousel_leader_idx"] = 0
            
            # Injection de l'animation CapCut Style : transition fluide, zoom léger et fondu entrant
            style_fade_entrant = """
            <style>
            @keyframes phonkFadeIn {
                0% { opacity: 0; transform: translateY(15px) scale(0.96); filter: brightness(1.3); }
                100% { opacity: 1; transform: translateY(0px) scale(1); filter: brightness(1); }
            }
            .phonk-image-container {
                text-align: center;
                width: 100%;
                margin: 0 auto;
            }
            .phonk-image-animated {
                animation: phonkFadeIn 0.5s cubic-bezier(0.25, 1, 0.5, 1) forwards;
                width: 320px !important; /* Taille compacte stricte d'origine demandée */
                height: auto;
                border-radius: 12px;
                box-shadow: 0 10px 25px rgba(0,0,0,0.5);
            }
            </style>
            """
            st.markdown(style_fade_entrant, unsafe_allow_html=True)

            col_p, col_txt, col_n = st.columns(3)
            with col_p:
                if st.button("⬅️ Swipe", key="prev_leader"):
                    st.session_state["carousel_leader_idx"] = (st.session_state["carousel_leader_idx"] - 1) % len(BANQUE_LEADER)
                    st.rerun()
            with col_txt:
                st.markdown(f"<p style='text-align:center; font-family:monospace; color:rgba(255,255,255,0.4); margin-top:8px;'>REEL {st.session_state['carousel_leader_idx'] + 1} / {len(BANQUE_LEADER)}</p>", unsafe_allow_html=True)
            with col_n:
                if st.button("Swipe ➡️", key="next_leader"):
                    st.session_state["carousel_leader_idx"] = (st.session_state["carousel_leader_idx"] + 1) % len(BANQUE_LEADER)
                    st.rerun()
            
            curr_idx = st.session_state["carousel_leader_idx"]
            p_path, p_audio = BANQUE_LEADER[curr_idx]
            
            if os.path.exists(p_path):
                with open(p_path, "rb") as img_file: 
                    b64_img = base64.b64encode(img_file.read()).decode()
                
                # Rendu HTML pur : force le navigateur à exécuter l'effet sans blocage de Streamlit
                st.markdown(f"""
                <div class="phonk-image-container">
                    <img src="data:image/jpeg;base64,{b64_img}" class="phonk-image-animated">
                    <h4 style="color:#00f0ff; margin-top:15px; font-family:sans-serif; font-weight:bold; font-size:16px;">
                        Aura : {p_path.split('.')[0]}
                    </h4>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning(f"🖼️ Fichier local '{p_path}' introuvable.")
            if st.session_state["audio_unlocked"]:
                player_id = f"audio_node_leader_{curr_idx}_{int(time.time())}"
                audio_src = f"data:audio/mp3;base64,{base64.b64encode(open(p_audio, 'rb').read()).decode()}" if os.path.exists(p_audio) else "https://soundhelix.com"
                
                zone_audio_dynamique.markdown(f"""
                <audio id="{player_id}" autoplay><source src="{audio_src}" type="audio/mp3"></audio>
                <script>
                var pInst = document.getElementById("{player_id}");
                if(pInst) {{
                    pInst.volume = 0.50;
                    setTimeout(function() {{ pInst.pause(); pInst.src=''; }}, 30000);
                }}
                </script>
                """, unsafe_allow_html=True)
        # ==============================================================================
    # 🎓 CERTIFICATION FINALE : VALIDE LE DIPLÔME DE LUXE À PARTIR DE 100 XP
    # ==============================================================================
    st.markdown("---")
    st.subheader("🎓 Certifications Académiques" if FR else "🎓 Academic Certifications")
    
    # CONDITION STRICTE : L'étudiant doit avoir complété un cycle ET posséder au moins 100 XP
    if st.session_state["pomodoro_termine"] and os.path.exists("cache_cours_public.txt") and st.session_state.xp >= 200:
        st.success("🏆 Certification Débloquée ! Tu es officiellement Expert !" if FR else "🏆 Certification Unlocked! You are an Expert!")
        
        try:
            # Création de la toile de fond unie bleu nuit profond d'origine
            W_d, H_d = 1200, 800
            diplome_img = PILImage.new("RGB", (W_d, H_d), (17, 22, 45)) 
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
            
            # Application des chaînes de texte exactes de ton design d'origine
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
            
            txt_footer = "Done in Yaounde, certified compliant by PomoMind Core 2026 cryptographic signature via Zetaris."
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
        # MESSAGE D'ERREUR INTERACTIF EN CAS DE CRÉDITS D'XP INSUFFISANTS
        if st.session_state.xp < 200:
            xp_manquant = 200 - st.session_state.xp
            txt_verrouille = (
                f"🔒 **Certificat d'Expert verrouillé (Niveau insuffisant) :** Tu possèdes actuellement **{st.session_state.xp} XP**. "
                f"Il te manque encore **{xp_manquant} XP** pour atteindre le seuil d'excellence académique de 200 XP ! "
                f"Effectue des sessions Pomodoro (+20 XP), valide des fiches ou dialogue avec le Hub IA pour accumuler tes crédits. 🎯"
                if FR else 
                f"🔒 **Expert Certificate Locked (Insufficient Level):** You currently have **{st.session_state.xp} XP**. "
                f"You need **{xp_manquant} more XP** to reach the 200 XP academic excellence threshold! "
                f"Run Pomodoro sessions (+20 XP), sign flashcards, or engage with the AI Hub to earn credits. 🎯"
            )
        else:
            txt_verrouille = (
                "🔒 **Certificat d'Expert verrouillé :** Complète d'abord une session d'étude dans l'onglet 'Chrono Pomodoro' "
                "ET reçois le cours officiel du professeur dans l'onglet 'Flux Réception' pour valider ton parcours !"
                if FR else 
                "🔒 **Expert Certificate Locked:** Complete a full focus session in the 'Pomodoro' tab "
                "AND receive the official course from your teacher in the 'Reception Feed' tab to validate your path!"
            )
        st.warning(txt_verrouille)
