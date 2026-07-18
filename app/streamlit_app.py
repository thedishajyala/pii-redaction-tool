import streamlit as st
import os
import sys
import tempfile

# Add src to sys.path so we can import our pipeline
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from main import run_pipeline

st.set_page_config(page_title="PII Redaction Tool", layout="centered")

st.markdown("""
<style>
/* Clean up UI to match user requests */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.title("Hybrid PII Redaction Tool for DOCX")
st.markdown("Detects and redacts PII using Regex + Microsoft Presidio")
st.divider()

uploaded_file = st.file_uploader("Upload Document", type=["docx"], label_visibility="collapsed")

if uploaded_file is not None:
    st.divider()
    
    if st.button("Redact Document", type="primary"):
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "input.docx")
            output_path = os.path.join(tmpdir, "redacted.docx")
            
            with open(input_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.markdown("### Pipeline")
            with st.status("Processing Document...", expanded=True) as status:
                st.write("✓ Regex Detection")
                st.write("✓ Presidio Detection")
                st.write("✓ Deterministic Replacement")
                
                try:
                    metrics, duration = run_pipeline(input_path, output_path)
                    status.update(label="Redaction Complete!", state="complete", expanded=False)
                    
                    st.divider()
                    st.markdown("### Processing Summary")
                    st.write("")
                    
                    if metrics:
                        for entity, count in sorted(metrics.items()):
                            # Display format: "Email           12"
                            st.text(f"{entity.capitalize().ljust(15)} {count}")
                    else:
                        st.text("No PII detected.")
                        
                    st.write("")
                    st.text(f"Processing Time: {duration:.1f} s")
                    
                    st.divider()
                    
                    with open(output_path, "rb") as f:
                        file_data = f.read()
                        
                    st.download_button(
                        label="Download Redacted DOCX",
                        data=file_data,
                        file_name="redacted_" + uploaded_file.name,
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                except Exception as e:
                    status.update(label="Error during processing", state="error")
                    st.error(f"An error occurred: {str(e)}")
