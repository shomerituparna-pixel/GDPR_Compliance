import json
import tempfile
import os

import streamlit as st

from analysis.document_parser import extract_pdf_text
from analysis.compliance_checker import analyze_document


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="GDPR Compliance Analyser",
    page_icon="🔐",
    layout="wide",
)


# --------------------------------------------------
# Helper functions
# --------------------------------------------------

def parse_llm_response(response):
    """
    Convert the LLM response into a Python dictionary.

    The model is instructed to return JSON, but sometimes
    LLMs wrap JSON inside ```json ... ``` markdown.
    This function handles both cases.
    """

    if not response:
        return None

    response = response.strip()

    # Remove markdown code fences if present
    if response.startswith("```json"):
        response = response[7:]

    elif response.startswith("```"):
        response = response[3:]

    if response.endswith("```"):
        response = response[:-3]

    response = response.strip()

    try:
        return json.loads(response)
    except json.JSONDecodeError:
        return None


def display_severity(severity):
    """
    Return a visual indicator for the severity level.
    """

    severity = str(severity).upper()

    if severity == "HIGH":
        return "🔴 HIGH"

    if severity == "MEDIUM":
        return "🟠 MEDIUM"

    if severity == "LOW":
        return "🟢 LOW"

    return f"⚪ {severity}"


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("🔐 GDPR Compliance Analyser")

st.markdown(
    """
    **AI-powered GDPR document analysis using Retrieval-Augmented Generation (RAG).**

    Upload a document and the system will analyse it against relevant GDPR
    provisions retrieved from the GDPR knowledge base.
    """
)

st.divider()


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.header("About")

    st.markdown(
        """
        This tool uses:

        - 📄 PDF document extraction
        - 🔎 Semantic search
        - 🧠 FAISS vector search
        - 🤖 Hugging Face LLM
        - ⚖️ GDPR knowledge base
        - 📊 AI-generated compliance assessment
        """
    )

    st.divider()

    st.caption(
        "This tool is for educational and analytical purposes "
        "and should not be treated as legal advice."
    )


# --------------------------------------------------
# File upload
# --------------------------------------------------

st.subheader("1. Upload your document")

uploaded_file = st.file_uploader(
    "Upload a PDF document to analyse",
    type=["pdf"],
    help="Upload a privacy policy, data processing agreement, "
         "employee data policy, or other document containing "
         "personal-data processing information.",
)


# --------------------------------------------------
# Analyse button
# --------------------------------------------------

if uploaded_file is not None:

    st.success(f"Document uploaded: {uploaded_file.name}")

    st.subheader("2. Analyse document")

    analyse_button = st.button(
        "🔎 Analyse for GDPR Compliance",
        type="primary",
        use_container_width=True,
    )

    if analyse_button:

        # ----------------------------------------------
        # Save uploaded PDF temporarily
        # ----------------------------------------------

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_file:

            temp_file.write(uploaded_file.getbuffer())
            temp_path = temp_file.name

        try:

            # ------------------------------------------
            # Extract document text
            # ------------------------------------------

            with st.spinner("📄 Extracting document text..."):

                document_text = extract_pdf_text(temp_path)

            if not document_text.strip():

                st.error(
                    "No text could be extracted from this PDF. "
                    "Please make sure the PDF contains selectable text."
                )

                st.stop()

            # ------------------------------------------
            # Show document statistics
            # ------------------------------------------

            st.subheader("Document Information")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Characters",
                    f"{len(document_text):,}"
                )

            with col2:
                st.metric(
                    "Words",
                    f"{len(document_text.split()):,}"
                )

            with col3:
                st.metric(
                    "Document Type",
                    "PDF"
                )

            # ------------------------------------------
            # Run compliance analysis
            # ------------------------------------------

            with st.spinner(
                "🤖 Analysing document against GDPR requirements..."
            ):

                result = analyze_document(
                    document_text
                )

            # ------------------------------------------
            # Parse LLM response
            # ------------------------------------------

            analysis = parse_llm_response(result)

            if analysis is None:

                st.error(
                    "The AI returned a response that could not be "
                    "interpreted as JSON."
                )

                st.subheader("Raw AI Response")

                st.code(
                    result,
                    language="text"
                )

                st.stop()

            # ------------------------------------------
            # Compliance overview
            # ------------------------------------------

            st.divider()

            st.header("📊 Compliance Overview")

            score = analysis.get(
                "compliance_score",
                "N/A"
            )

            risk_level = analysis.get(
                "risk_level",
                "N/A"
            )

            summary = analysis.get(
                "summary",
                "No summary provided."
            )

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Compliance Score",
                    f"{score}%"
                    if isinstance(score, (int, float))
                    else score
                )

            with col2:

                st.metric(
                    "Overall Risk",
                    str(risk_level).upper()
                )

            st.markdown("### Summary")

            st.write(summary)

            # ------------------------------------------
            # Issues
            # ------------------------------------------

            issues = analysis.get(
                "issues",
                []
            )

            st.divider()

            st.header(
                f"⚠️ Compliance Findings ({len(issues)})"
            )

            if not issues:

                st.success(
                    "No compliance issues were identified "
                    "by the analysis."
                )

            else:

                for index, issue in enumerate(
                    issues,
                    start=1
                ):

                    article = issue.get(
                        "article",
                        "Not specified"
                    )

                    severity = issue.get(
                        "severity",
                        "Not specified"
                    )

                    issue_text = issue.get(
                        "issue",
                        "No issue description provided."
                    )

                    recommendation = issue.get(
                        "recommendation",
                        "No recommendation provided."
                    )

                    with st.expander(
                        f"{display_severity(severity)} — "
                        f"{article}"
                    ):

                        st.markdown(
                            "### Issue"
                        )

                        st.write(issue_text)

                        st.markdown(
                            "### GDPR Article"
                        )

                        st.info(article)

                        st.markdown(
                            "### Recommendation"
                        )

                        st.write(recommendation)

            # ------------------------------------------
            # Strengths
            # ------------------------------------------

            strengths = analysis.get(
                "strengths",
                []
            )

            st.divider()

            st.header("✅ Strengths")

            if strengths:

                for strength in strengths:

                    st.markdown(
                        f"- {strength}"
                    )

            else:

                st.info(
                    "No specific strengths were identified."
                )

            # ------------------------------------------
            # Raw JSON
            # ------------------------------------------

            with st.expander(
                "🔍 View raw analysis JSON"
            ):

                st.json(analysis)

        except Exception as e:

            st.error(
                "An error occurred while analysing the document."
            )

            st.exception(e)

        finally:

            # ------------------------------------------
            # Remove temporary file
            # ------------------------------------------

            if os.path.exists(temp_path):
                os.remove(temp_path)