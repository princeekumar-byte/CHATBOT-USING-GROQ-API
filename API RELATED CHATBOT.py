import streamlit as st
import json
from groq import Groq
from typing import List, Dict, Any

# --- 1. Configuration and Data ---

# NOTE: This code uses st.secrets to securely retrieve the API key.
# It requires a secrets.toml file locally or the secret set in the cloud.
try:
    # Use the specific key name for Groq
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("Groq API Key not found. Please ensure you have defined 'GROQ_API_KEY' in your secrets file.")
    st.stop()

# Initialize the Groq client
client = Groq(api_key=GROQ_API_KEY)
MODEL_NAME = "llama-3.1-8b-instant" # High-speed, high-quality model

# Internship Data (Embedded from my_data.json)
INTERNSHIP_DATA_JSON = """
[
  {
    "id": 1,
    "title": "AI Intern",
    "skills": "Python Machine Learning Data Analysis",
    "location": "Remote",
    "sector": "Tech"
  },
  {
    "id": 2,
    "title": "Web Dev Intern",
    "skills": "HTML CSS JavaScript React",
    "location": "Delhi",
    "sector": "Tech"
  },
  {
    "id": 3,
    "title": "Marketing Intern",
    "skills": "Communication Social Media Advertising",
    "location": "Remote",
    "sector": "Marketing"
  },
  {
    "id": 4,
    "title": "Data Science Intern",
    "skills": "Python R SQL Tableau PowerBI",
    "location": "Bangalore",
    "sector": "Tech"
  },
  {
    "id": 5,
    "title": "Software Engineer Intern",
    "skills": "Java C++ Python Git Docker",
    "location": "Hyderabad",
    "sector": "Tech"
  },
  {
    "id": 6,
    "title": "Product Manager Intern",
    "skills": "Agile Scrum JIRA Market-Research",
    "location": "Pune",
    "sector": "Tech"
  },
  {
    "id": 7,
    "title": "UX/UI Design Intern",
    "skills": "Figma Sketch Adobe-XD Wireframing",
    "location": "Mumbai",
    "sector": "Tech"
  },
  {
    "id": 8,
    "title": "Content Writer Intern",
    "skills": "SEO Copywriting Blogging WordPress",
    "location": "Remote",
    "sector": "Marketing"
  },
  {
    "id": 9,
    "title": "Graphic Design Intern",
    "skills": "Adobe-Illustrator Photoshop InDesign",
    "location": "Delhi",
    "sector": "Marketing"
  },
  {
    "id": 10,
    "title": "Financial Analyst Intern",
    "skills": "Excel Financial-Modeling Valuation",
    "location": "Mumbai",
    "sector": "Finance"
  },
  {
    "id": 11,
    "title": "Investment Banking Intern",
    "skills": "DCF LBO Mergers-Acquisitions",
    "location": "Bangalore",
    "sector": "Finance"
  },
  {
    "id": 12,
    "title": "Clinical Research Intern",
    "skills": "GCP Clinical-Trials Data-Management",
    "location": "Hyderabad",
    "sector": "Healthcare"
  },
  {
    "id": 13,
    "title": "Healthcare Administration Intern",
    "skills": "EMR HIPAA Medical-Billing",
    "location": "Pune",
    "sector": "Healthcare"
  },
  {
    "id": 14,
    "title": "EdTech Product Intern",
    "skills": "Moodle Canvas Blackboard",
    "location": "Bangalore",
    "sector": "Education"
  },
  {
    "id": 15,
    "title": "Curriculum Development Intern",
    "skills": "Instructional-Design Articulate-Storyline",
    "location": "Remote",
    "sector": "Education"
  },
  {
    "id": 16,
    "title": "E-commerce Operations Intern",
    "skills": "Shopify Magento WooCommerce",
    "location": "Delhi",
    "sector": "E-commerce"
  },
  {
    "id": 17,
    "title": "Supply Chain Intern",
    "skills": "SAP-SCM Oracle-SCM Logistics",
    "location": "Mumbai",
    "sector": "E-commerce"
  },
  {
    "id": 18,
    "title": "Journalism Intern",
    "skills": "AP-Style-Writing Fact-Checking Interviewing",
    "location": "Delhi",
    "sector": "Media"
  },
  {
    "id": 19,
    "title": "Video Production Intern",
    "skills": "Adobe-Premiere-Pro Final-Cut-Pro After-Effects",
    "location": "Mumbai",
    "sector": "Media"
  },
  {
    "id": 20,
    "title": "Cybersecurity Intern",
    "skills": "Networking Wireshark Penetration-Testing",
    "location": "Bangalore",
    "sector": "Tech"
  },
  {
    "id": 21,
    "title": "Cloud Computing Intern",
    "skills": "AWS Azure GCP Docker Kubernetes",
    "location": "Hyderabad",
    "sector": "Tech"
  },
  {
    "id": 22,
    "title": "SEO Intern",
    "skills": "Google-Analytics SEMrush Ahrefs",
    "location": "Remote",
    "sector": "Marketing"
  },
  {
    "id": 23,
    "title": "Social Media Marketing Intern",
    "skills": "Hootsuite Buffer Facebook-Ads Instagram-Marketing",
    "location": "Pune",
    "sector": "Marketing"
  },
  {
    "id": 24,
    "title": "Accounting Intern",
    "skills": "QuickBooks Tally ERP-Systems",
    "location": "Delhi",
    "sector": "Finance"
  },
  {
    "id": 25,
    "title": "Data Science Intern",
    "skills": "Python R SQL Tableau PowerBI",
    "location": "Chennai",
    "sector": "Tech"
  },
  {
    "id": 26,
    "title": "Software Engineer Intern",
    "skills": "Java C++ Python Git Docker",
    "location": "Kolkata",
    "sector": "Tech"
  },
  {
    "id": 27,
    "title": "Product Manager Intern",
    "skills": "Agile Scrum JIRA Market-Research",
    "location": "Gurgaon",
    "sector": "Tech"
  },
  {
    "id": 28,
    "title": "UX/UI Design Intern",
    "skills": "Figma Sketch Adobe-XD Wireframing",
    "location": "Noida",
    "sector": "Tech"
  },
  {
    "id": 29,
    "title": "Content Writer Intern",
    "skills": "SEO Copywriting Blogging WordPress",
    "location": "Chennai",
    "sector": "Marketing"
  },
  {
    "id": 30,
    "title": "Graphic Design Intern",
    "skills": "Adobe-Illustrator Photoshop InDesign",
    "location": "Kolkata",
    "sector": "Marketing"
  },
  {
    "id": 31,
    "title": "Financial Analyst Intern",
    "skills": "Excel Financial-Modeling Valuation",
    "location": "Gurgaon",
    "sector": "Finance"
  },
  {
    "id": 32,
    "title": "Investment Banking Intern",
    "skills": "DCF LBO Mergers-Acquisitions",
    "location": "Noida",
    "sector": "Finance"
  },
  {
    "id": 33,
    "title": "Clinical Research Intern",
    "skills": "GCP Clinical-Trials Data-Management",
    "location": "Chennai",
    "sector": "Healthcare"
  },
  {
    "id": 34,
    "title": "Healthcare Administration Intern",
    "skills": "EMR HIPAA Medical-Billing",
    "location": "Kolkata",
    "sector": "Healthcare"
  },
  {
    "id": 35,
    "title": "EdTech Product Intern",
    "skills": "Moodle Canvas Blackboard",
    "location": "Gurgaon",
    "sector": "Education"
  },
  {
    "id": 36,
    "title": "Curriculum Development Intern",
    "skills": "Instructional-Design Articulate-Storyline",
    "location": "Noida",
    "sector": "Education"
  },
  {
    "id": 37,
    "title": "E-commerce Operations Intern",
    "skills": "Shopify Magento WooCommerce",
    "location": "Chennai",
    "sector": "E-commerce"
  },
  {
    "id": 38,
    "title": "Supply Chain Intern",
    "skills": "SAP-SCM Oracle-SCM Logistics",
    "location": "Kolkata",
    "sector": "E-commerce"
  },
  {
    "id": 39,
    "title": "Journalism Intern",
    "skills": "AP-Style-Writing Fact-Checking Interviewing",
    "location": "Gurgaon",
    "sector": "Media"
  },
  {
    "id": 40,
    "title": "Video Production Intern",
    "skills": "Adobe-Premiere-Pro Final-Cut-Pro After-Effects",
    "location": "Noida",
    "sector": "Media"
  },
  {
    "id": 41,
    "title": "Cybersecurity Intern",
    "skills": "Networking Wireshark Penetration-Testing",
    "location": "Chennai",
    "sector": "Tech"
  },
  {
    "id": 42,
    "title": "Cloud Computing Intern",
    "skills": "AWS Azure GCP Docker Kubernetes",
    "location": "Kolkata",
    "sector": "Tech"
  },
  {
    "id": 43,
    "title": "SEO Intern",
    "skills": "Google-Analytics SEMrush Ahrefs",
    "location": "Gurgaon",
    "sector": "Marketing"
  },
  {
    "id": 44,
    "title": "Social Media Marketing Intern",
    "skills": "Hootsuite Buffer Facebook-Ads Instagram-Marketing",
    "location": "Noida",
    "sector": "Marketing"
  },
  {
    "id": 45,
    "title": "Accounting Intern",
    "skills": "QuickBooks Tally ERP-Systems",
    "location": "Chennai",
    "sector": "Finance"
  },
  {
    "id": 46,
    "title": "Data Science Intern",
    "skills": "Python R SQL Tableau PowerBI",
    "location": "Remote",
    "sector": "Tech"
  },
  {
    "id": 47,
    "title": "Software Engineer Intern",
    "skills": "Java C++ Python Git Docker",
    "location": "Remote",
    "sector": "Tech"
  },
  {
    "id": 48,
    "title": "Product Manager Intern",
    "skills": "Agile Scrum JIRA Market-Research",
    "location": "Remote",
    "sector": "Tech"
  },
  {
    "id": 49,
    "title": "UX/UI Design Intern",
    "skills": "Figma Sketch Adobe-XD Wireframing",
    "location": "Remote",
    "sector": "Tech"
  },
  {
    "id": 50,
    "title": "Content Writer Intern",
    "skills": "SEO Copywriting Blogging WordPress",
    "location": "Remote",
    "sector": "Marketing"
  }
]
"""
INTERNSHIP_DATA = json.loads(INTERNSHIP_DATA_JSON)


def get_system_instruction() -> str:
    """Creates the system instruction using the embedded internship data."""
    internship_data_string = json.dumps(INTERNSHIP_DATA, indent=2)

    return f"""
        You are the Internship Advisor Chatbot powered by Llama 3.1. Your primary role is to act as an expert search engine using the provided JSON dataset.

        **DATASET:**
        ---JSON START---
        {internship_data_string}
        ---JSON END---

        **INSTRUCTIONS:**
        1.  **Search Logic:** Analyze the user's query for keywords related to 'title', 'skills', 'location', or 'sector'. Identify all internship objects in the DATASET that match the criteria. Matches should be case-insensitive.
        2.  **Synthesis:** Synthesize a helpful, conversational response based on the findings.
        3.  **Formatting:** If matches are found:
            * List them clearly using a numbered or bulleted list.
            * Include the Title, Location, and Core Skills for each match.
        4.  **No Matches:** If no matches are found, inform the user and politely suggest alternative search terms (e.g., "Try searching for a different skill or location").
        5.  **Tone:** Maintain a friendly, professional, and helpful tone. Do not mention that you are an AI or that you are searching JSON.
    """


def get_groq_response(messages: List[Dict[str, str]]) -> str:
    """Calls the Groq API and handles the response."""
    try:
        chat_completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "system", "content": get_system_instruction()}] + messages,
            temperature=0.2,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        # Provide a clear error message if the API call fails
        return (
            f"API Error: An error occurred while contacting Groq. This is usually due to an "
            f"invalid or expired API key, or running out of free usage.\n\n"
            f"Details: {e}"
        )

# --- 4. Streamlit App Layout and Logic ---

def main_app():
    st.set_page_config(
        page_title="Internship Advisor Chatbot",
        page_icon="🤖",
        layout="centered"
    )

    st.title("🤖 Groq Internship Advisor Chatbot")
    st.caption("Powered by Llama 3.1 8B (Groq).")

    # Initialize chat history in session state
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {
                "role": "assistant",
                "content": (
                    "Hello! I am your **Groq Internship Advisor**. I have access to 50 internship postings.\n\n"
                    "Ask me to find openings based on **Skills**, **Location**, or **Sector**.\n"
                    "Example: 'I need a Data Science internship in Bangalore' or 'Remote marketing jobs.'"
                )
            }
        ]

    # Display chat messages
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Handle user input
    if prompt := st.chat_input("Ask me about internships..."):
        # 1. Add user message to history
        st.session_state["messages"].append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # 2. Prepare message list for Groq (only user/assistant history)
        api_messages = [
            {"role": "user" if msg["role"] == "user" else "assistant", "content": msg["content"]}
            for msg in st.session_state["messages"]
        ]

        # 3. Call the model
        with st.chat_message("assistant"):
            with st.spinner("Processing request via Groq..."):
                full_response = get_groq_response(api_messages)

            # 4. Display the response
            st.markdown(full_response)
        
        # 5. Add assistant message to history
        st.session_state["messages"].append({"role": "assistant", "content": full_response})


if __name__ == "__main__":
    main_app()