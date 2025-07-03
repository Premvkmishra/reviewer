import streamlit as st
import httpx
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000/api")

st.title("AI Code Review")

code = st.text_area("Paste your code here", height=300)
language = st.selectbox("Select language (optional)", ["None", "Python", "JavaScript", "Java", "C++"])
if st.button("Analyze"):
    if not code:
        st.error("Please enter some code")
    else:
        with st.spinner("Analyzing..."):
            try:
                response = httpx.post(
                    f"{BACKEND_URL}/analyze",
                    json={"code": code, "language": language if language != "None" else None},
                    timeout=30
                )
                response.raise_for_status()
                feedback = response.json()["markdown_feedback"]
                st.markdown(feedback)
            except Exception as e:
                st.error(f"Error: {str(e)}")

st.markdown("---")
st.write("For GitHub PR integration, configure a webhook pointing to `<your-domain>/api/webhook`")

# --- PR Review Section ---
st.header("Review a GitHub Pull Request")
pr_url = st.text_input("Enter GitHub PR URL (e.g., https://github.com/owner/repo/pull/123)")
if st.button("Review PR"):
    if not pr_url:
        st.error("Please enter a PR URL")
    else:
        with st.spinner("Reviewing PR..."):
            try:
                response = httpx.post(
                    f"{BACKEND_URL}/review-pr",
                    json={"pr_url": pr_url},
                    timeout=60
                )
                response.raise_for_status()
                feedback = response.json()["markdown_feedback"]
                st.markdown(feedback)
            except Exception as e:
                st.error(f"Error: {str(e)}")
