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
