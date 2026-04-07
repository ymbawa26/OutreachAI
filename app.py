import streamlit as st
import pandas as pd
import time
from ai_engine import mock_ai_generate, send_mock_email

st.set_page_config(page_title="OutreachAI", page_icon="✉️", layout="wide")

st.title("✉️ OutreachAI: Personalized Mass Emailer")
st.markdown("Easily turn generic outreach into personalized 1-on-1 messages, powered by AI.")

# 1. Sidebar for Template
st.sidebar.header("1. Your Base Template")
base_subject = st.sidebar.text_input("Subject Line", "Checking in on your progress!")
base_template = st.sidebar.text_area(
    "What is the main message?", 
    "Please let me know if you need to schedule office hours. Best, Ms. Teacher",
    height=300
)

# 2. Main Area for File Upload
st.header("2. Upload Your Students Data")
uploaded_file = st.file_uploader("Upload CSV (must contain columns: Name, Email, Class, Recent Grade, Personal Note)", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("### Preview of Uploaded Data")
    st.dataframe(df.head())
    
    # Check for required columns
    required_cols = ["Name", "Email", "Class", "Recent Grade", "Personal Note"]
    if all(col in df.columns for col in required_cols):
        
        st.header("3. Generate Emails")
        if st.button("🚀 Generate Personalized Emails"):
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            generated_emails = []
            
            for index, row in df.iterrows():
                # Update progress
                progress = (index + 1) / len(df)
                progress_bar.progress(progress)
                status_text.text(f"Generating email for {row['Name']}...")
                
                # Mock AI Generation
                email_body = mock_ai_generate(
                    name=row["Name"],
                    class_name=row["Class"],
                    grade=str(row["Recent Grade"]),
                    note=row["Personal Note"],
                    base_template=base_template
                )
                generated_emails.append(email_body)
                
            status_text.text("Finished generating emails!")
            
            # Save emails back to dataframe
            df["Generated_Email"] = generated_emails
            
            # Add a 'Select' column for checkboxes, initialized to True
            df.insert(0, "Select", True)
            
            # Store in session state so it doesn't disappear
            st.session_state["final_df"] = df
    else:
        st.error(f"Missing required columns! Ensure your CSV has: {', '.join(required_cols)}")

# Display finalized emails if they exist
if "final_df" in st.session_state:
    st.header("4. Review & Select Emails to Send")
    final_df = st.session_state["final_df"]
    
    # Use interactive data editor
    st.write("Uncheck any student you do NOT want to email.")
    
    # Make editor interactive for the 'Select' column
    edited_df = st.data_editor(
        final_df,
        column_config={
            "Select": st.column_config.CheckboxColumn("Send?", default=True)
        },
        disabled=["Name", "Email", "Class", "Recent Grade", "Personal Note", "Generated_Email"],
        hide_index=True,
        use_container_width=True
    )
    
    st.session_state["edited_df"] = edited_df

    st.header("5. Finalize")
    col1, col2 = st.columns(2)
    
    with col1:
        # Download option
        csv = edited_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download All Emails as CSV",
            data=csv,
            file_name="personalized_emails_output.csv",
            mime="text/csv",
        )
        
    with col2:
        if st.button("📨 Send Selected Emails NOW!"):
            selected_rows = edited_df[edited_df["Select"] == True]
            num_selected = len(selected_rows)
            
            if num_selected == 0:
                st.warning("No students selected!")
            else:
                progress_bar_send = st.progress(0)
                status_text_send = st.empty()
                
                for idx, (index, row) in enumerate(selected_rows.iterrows()):
                    progress = (idx + 1) / num_selected
                    progress_bar_send.progress(progress)
                    status_text_send.text(f"Sending to {row['Name']} ({row['Email']})...")
                    
                    # Call our mock send function
                    send_mock_email(row['Email'], base_subject, row['Generated_Email'])
                    
                st.success(f"Successfully sent {num_selected} emails!")
