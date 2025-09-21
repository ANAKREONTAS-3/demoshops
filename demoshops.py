import streamlit as st
from openai import OpenAI

# Παίρνουμε το API key από τα secrets
api_key = st.secrets["OPENAI_API_KEY"]

# Δημιουργούμε τον client
client = OpenAI(api_key=api_key)

# ----------------- Εφαρμογή -----------------
st.set_page_config(page_title="Eshop Demo Tool", page_icon="🛒", layout="centered")

st.title("🛍️ Eshop Demo Tool")
st.write("Δώσε το προϊόν σου και πάρε έτοιμα κείμενα για το e-shop και τα social media σου.")

# Input από χρήστη
product_name = st.text_input("🔑 Όνομα προϊόντος:")
keywords = st.text_input("📌 Λέξεις-κλειδιά (προαιρετικά):")

if st.button("Δημιουργία"):
    if not product_name.strip():
        st.warning("⚠️ Δώσε όνομα προϊόντος για να συνεχίσουμε.")
    else:
        with st.spinner("✍️ Δημιουργία κειμένων..."):

            # Περιγραφή προϊόντος
            desc = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Είσαι ειδικός στη δημιουργία ελκυστικών περιγραφών προϊόντων για e-shop."},
                    {"role": "user", "content": f"Φτιάξε μια περιγραφή για το προϊόν '{product_name}' με βάση αυτές τις λέξεις-κλειδιά: {keywords}"}
                ]
            )

            # Hashtags
            tags = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Είσαι ειδικός στα social media."},
                    {"role": "user", "content": f"Δώσε μου hashtags για το προϊόν '{product_name}' στο Facebook, Instagram και TikTok."}
                ]
            )

            # Caption για social media
            caption = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Είσαι ειδικός στο μάρκετινγκ και γράφεις έξυπνα captions για social media."},
                    {"role": "user", "content": f"Γράψε ένα σύντομο caption για το προϊόν '{product_name}'."}
                ]
            )

        # Αποτελέσματα
        st.subheader("📝 Περιγραφή προϊόντος")
        st.write(desc.choices[0].message.content.strip())

        st.subheader("🏷️ Hashtags")
        st.write(tags.choices[0].message.content.strip())

        st.subheader("💬 Social Media Caption")
        st.write(caption.choices[0].message.content.strip())