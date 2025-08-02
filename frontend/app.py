import streamlit as st
import requests

# Enhanced page configuration with custom styling
st.set_page_config(
    page_title="CRM Chatbot Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Main container styling */
    .main > div {
        padding-top: 2rem;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 1rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
        color: white;
    }
    
    /* Chat input styling */
    .stTextInput > div > div > input {
        background-color: #f8f9fa;
        border: 2px solid #e9ecef;
        border-radius: 25px;
        padding: 0.75rem 1rem;
        font-size: 1rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
    }
    
    /* Lead card styling */
    .lead-card {
        background: #ffffff;
        border: 1px solid #e9ecef;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .lead-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    }
    
    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .status-converted {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    
    .status-interested {
        background-color: #cce7ff;
        color: #004085;
        border: 1px solid #99d6ff;
    }
    
    .status-contacted {
        background-color: #fff3cd;
        color: #856404;
        border: 1px solid #ffeaa7;
    }
    
    .status-new {
        background-color: #e2e3e5;
        color: #383d41;
        border: 1px solid #d6d8db;
    }
    
    .status-not-interested {
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f1b0b7;
    }
    
    /* Stats container */
    .stats-container {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Success message styling */
    .success-message {
        background: linear-gradient(90deg, #56ab2f 0%, #a8e6cf 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
        font-weight: 500;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
</style>
""", unsafe_allow_html=True)

# Enhanced header
st.markdown("""
<div class="main-header">
    <h1>CRM Chatbot Assistant</h1>
    <p style="margin: 0; font-size: 1.1rem; opacity: 0.9;">Ask me anything about your leads - I'm here to help!</p>
</div>
""", unsafe_allow_html=True)

# Sidebar with helpful information
with st.sidebar:
    st.markdown("### Quick Commands")
    st.markdown("""
                
    **City Queries:**
    - "Show leads from Delhi"
    - "Show me leads in Mumbai"
    - "Show leads from Bangalore"
    - "Show me leads in Noida"
    - "What are the cities of all leads?"

    **General Queries:**
    - "Show all leads"
    - "How many leads are there?"
    - "Interested leads"

    **Status Queries:**
    - "Show me converted leads"
    - "highest converted lead"

    """)
    
    st.markdown("---")
    st.markdown("### Pro Tips")
    st.info("Use natural language - I understand conversational queries!")
    st.success("Be specific for better results")
    st.warning("Ask for counts and statistics too!")

# Enhanced input section
st.markdown("### Chat with your CRM")
col1, col2 = st.columns([4, 1])

with col1:
    user_input = st.text_input("", placeholder="Type your question here... (e.g., 'Show me all leads from Mumbai')", label_visibility="collapsed")

with col2:
    search_button = st.button("Search", use_container_width=True)

# Function to get status badge HTML
def get_status_badge(status):
    status_lower = status.lower().replace(' ', '-')
    return f'<span class="status-badge status-{status_lower}">{status}</span>'

if user_input or search_button:
    if user_input:
        with st.spinner('Searching your CRM database...'):
            try:
                # Send request as JSON instead of params
                response = requests.post(
                    "https://crm-chatbot-production.up.railway.app/chat/"", 
                    json={"query": user_input},
                    headers={"Content-Type": "application/json"}
                )

                if response.status_code == 200:
                    try:
                        data = response.json()
                        
                        if "error" in data:
                            st.error(f"Error: {data['error']}")
                        elif "message" in data:
                            st.success(f"{data['message']}")
                            
                            # Display leads if available
                            if "leads" in data and data["leads"]:
                                st.write(f"Found {len(data['leads'])} leads:")
                                
                                for lead in data["leads"]:
                                    with st.container():
                                        st.markdown(f"""
                                        <div class="lead-card">
                                            <h4>{lead.get('name', 'N/A')}</h4>
                                            <p><strong>Email:</strong> {lead.get('email', 'N/A')}</p>
                                            <p><strong>Phone:</strong> {lead.get('phone', 'N/A')}</p>
                                            <p><strong>City:</strong> {lead.get('city', 'N/A')}</p>
                                            <p><strong>Company:</strong> {lead.get('company', 'N/A')}</p>
                                            <p><strong>Status:</strong> {get_status_badge(lead.get('status', 'Unknown'))}</p>
                                            <p><strong>Source:</strong> {lead.get('source', 'N/A')}</p>
                                            <p><strong>Notes:</strong> {lead.get('notes', 'N/A')}</p>
                                        </div>
                                        """, unsafe_allow_html=True)
                        else:
                            st.warning("Unexpected response format received from server.")
                            
                    except ValueError as json_error:
                        st.error(f"Failed to parse server response: {json_error}")
                        
                else:
                    st.error(f"Server returned status {response.status_code}")
                    try:
                        error_data = response.json()
                        if "detail" in error_data:
                            st.error(f"Error: {error_data['detail']}")
                    except:
                        st.error(f"Raw error: {response.text}")

            except requests.exceptions.ConnectionError:
                st.error("Connection Error: Could not connect to the backend server. Please ensure the server is running on http://localhost:8000")
            except requests.exceptions.Timeout:
                st.error("Timeout Error: The server took too long to respond.")
            except Exception as e:
                st.error(f"Error: Something went wrong: {e}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6c757d; padding: 2rem 0;">
    <p>Powered by Streamlit & FastAPI | Built for efficient CRM management</p>
</div>
""", unsafe_allow_html=True)
