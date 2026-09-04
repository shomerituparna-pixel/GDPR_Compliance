# 🔐 GDPR Compliance Analyser

An AI-powered Retrieval-Augmented Generation (RAG) application that analyses privacy documents against relevant provisions of the General Data Protection Regulation (GDPR).

The application combines PDF text extraction, semantic search, a FAISS vector index, a GDPR knowledge base, a Hugging Face-hosted language model, and a Streamlit interface to generate a structured GDPR compliance assessment.

> **Status: Version 1.0 — Working MVP**

---

## 📌 Project Overview

Privacy policies and other data-protection documents can be lengthy and difficult to review manually against GDPR requirements.

This project explores how Retrieval-Augmented Generation (RAG) can be used to support GDPR document analysis.

Instead of asking a language model to assess a document using only its general knowledge, the application first retrieves relevant GDPR content from a domain-specific knowledge base and provides that content as context to the model.

The application then generates a structured compliance assessment containing:

- Compliance score
- Overall risk level
- Summary
- Potential compliance issues
- Relevant GDPR articles
- Recommendations
- Identified strengths

The application provides a Streamlit-based interface for uploading and analysing privacy documents.

This project is intended for educational, research, and portfolio purposes and is **not a substitute for professional legal advice**.

---

## 🎯 Objective

The objective of this project is to build a practical RAG-based application that demonstrates how AI can be combined with a domain-specific knowledge base to analyse regulatory documents.

The system focuses on three key areas:

1. **Document processing** — extracting text from uploaded PDF documents.

2. **Knowledge retrieval** — finding relevant GDPR content using semantic search.

3. **AI analysis** — using the retrieved GDPR content to generate a structured compliance assessment.

---

## 🏗️ Application Architecture

```text
                  Uploaded PDF
                       │
                       ▼
              ┌─────────────────┐
              │  PDF Extraction │
              │     PyPDF2      │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Semantic Search │
              │      FAISS      │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Relevant GDPR   │
              │    Content      │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │    Qwen3-8B     │
              │ Hugging Face    │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Compliance      │
              │ Assessment      │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │    Streamlit    │
              │       UI        │
              └─────────────────┘
```

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| **Python** | Application development |
| **Streamlit** | Interactive web interface |
| **PyPDF2** | PDF text extraction |
| **FAISS** | Vector similarity search and retrieval |
| **Hugging Face** | LLM inference |
| **Qwen3-8B** | Language model used for compliance analysis |
| **python-dotenv** | Environment variable management |
| **Git/GitHub** | Version control |

---

## 📁 Project Structure

```text
GDPR_Compliance/
│
├── analysis/
│   ├── compliance_checker.py
│   ├── document_parser.py
│   └── llm.py
│
├── data/
│   ├── EU_AI_ACT.pdf
│   ├── GDPR.pdf
│   ├── gdpr.txt
│   ├── gdpr_chunks.json
│   └── gdpr_index.faiss
│
├── rag/
│   ├── build_gdpr_index.py
│   ├── chunk_gdpr.py
│   ├── extract_text.py
│   ├── inspect_chunks.py
│   ├── inspect_raw_text.py
│   └── semantic_search.py
│
├── app.py
├── config.py
├── sample_privacy_policy_gdpr_test.pdf
├── test_models.py
├── test_token.py
├── README.md
└── .gitignore
```

### Key Components

- **`app.py`** — Streamlit application and user interface.
- **`analysis/document_parser.py`** — Extracts text from uploaded PDF documents.
- **`analysis/compliance_checker.py`** — Retrieves relevant GDPR context and performs the compliance analysis using the language model.
- **`analysis/llm.py`** — Contains LLM-related functionality.
- **`rag/semantic_search.py`** — Performs semantic search against the GDPR knowledge base.
- **`rag/build_gdpr_index.py`** — Builds the FAISS vector index used for retrieval.
- **`rag/chunk_gdpr.py`** — Processes GDPR content into chunks for retrieval.
- **`data/GDPR.pdf`** — GDPR source document used as part of the knowledge base.
- **`data/gdpr.txt`** — Extracted GDPR text.
- **`data/gdpr_chunks.json`** — Processed GDPR chunks used by the RAG pipeline.
- **`data/gdpr_index.faiss`** — FAISS vector index used for semantic retrieval.
- **`sample_privacy_policy_gdpr_test.pdf`** — Synthetic privacy policy used to test the application.
- **`test_models.py`** and **`test_token.py`** — Development and testing scripts used during model and authentication setup.

---

## 🔄 How the Application Works

The Version 1.0 workflow can be summarised as:

```text
1. User uploads a privacy document
              ↓
2. PDF text is extracted
              ↓
3. Document text is used for semantic retrieval
              ↓
4. Relevant GDPR content is retrieved from FAISS
              ↓
5. Retrieved GDPR content is added to the LLM prompt
              ↓
6. Qwen3-8B analyses the document
              ↓
7. Structured compliance assessment is generated
              ↓
8. Results are displayed through Streamlit
```

The key idea is that the language model receives relevant GDPR content as context before performing the compliance analysis.

---

## 🚀 Key Features

### 📄 PDF Document Processing

The application accepts PDF documents and extracts their text using PyPDF2.

### 🔎 Semantic GDPR Retrieval

The system searches the GDPR knowledge base for content that is semantically relevant to the uploaded privacy document.

### 📚 Retrieval-Augmented Generation

Retrieved GDPR content is provided to the language model as contextual information for the compliance analysis.

### 🤖 AI-Powered Analysis

Qwen3-8B is used to analyse the uploaded document against the retrieved GDPR content.

### 📊 Structured Compliance Assessment

The application generates:

- Compliance score
- Risk level
- Summary
- Potential compliance issues
- Relevant GDPR articles
- Recommendations
- Identified strengths

### 🖥️ Streamlit Interface

The analysis is exposed through a simple interactive web interface, allowing users to upload a document and review the generated assessment.

---

## 🧪 Testing

A synthetic privacy policy is included in the repository:

```text
sample_privacy_policy_gdpr_test.pdf
```

This document provides a reproducible test case for the Version 1.0 application.

The test document contains a mixture of privacy-policy statements that allow the analyser to identify potential compliance gaps as well as areas of strength.

### Test Workflow

```text
Start Streamlit
      ↓
Upload sample privacy policy
      ↓
Run GDPR analysis
      ↓
Extract document text
      ↓
Retrieve relevant GDPR content
      ↓
Run LLM analysis
      ↓
Display compliance assessment
```

---

## 📊 Output

The application generates a structured compliance assessment containing:

- **Compliance Score**
- **Risk Level**
- **Summary**
- **Compliance Issues**
- **Relevant GDPR Articles**
- **Recommendations**
- **Strengths**

The underlying LLM response follows a structured format similar to:

```json
{
  "compliance_score": 40,
  "risk_level": "High",
  "summary": "...",
  "issues": [
    {
      "article": "Article 13(2)(b)",
      "severity": "High",
      "issue": "...",
      "recommendation": "..."
    }
  ],
  "strengths": [
    "..."
  ]
}
```

The Streamlit interface presents this information in a more user-friendly format.

---

## ⚠️ Current Limitations

Version 1.0 is a working MVP and currently has several limitations:

- The semantic retrieval approach operates at the document level.
- The compliance score is AI-generated and has not been legally validated.
- Findings are not consistently linked to the exact passage in the uploaded document that triggered the finding.
- PDF documents are the primary supported input format.
- AI-generated results may contain errors or omissions.
- Results should be reviewed by a qualified GDPR or legal professional before being used for real compliance decisions.

---

## 🔮 Future Improvements

Future versions of the project may explore:

- Section-level document analysis
- More granular GDPR Article mapping
- Evidence extraction from uploaded documents
- Requirement-to-evidence mapping
- Improved risk scoring
- Enhanced compliance dashboards
- Downloadable compliance reports
- Support for additional document formats
- Automated evaluation and testing

---

## ⚖️ Disclaimer

This project is intended for educational, research, and portfolio purposes.

It does not provide legal advice and should not be used as a substitute for review by a qualified GDPR or legal professional.

AI-generated results may contain errors or omissions.

---

## 📌 Project Status

**Version 1.0 — Working MVP**

The core GDPR RAG pipeline and Streamlit application are functional.

The current version demonstrates:

- PDF document processing
- GDPR knowledge retrieval
- FAISS-based semantic search
- RAG-based LLM analysis
- Structured compliance assessment
- Streamlit-based presentation of results