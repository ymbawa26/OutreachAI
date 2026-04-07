import pandas as pd
import time

def mock_ai_generate(name, class_name, grade, note, base_template):
    """
    This is a MOCK function to simulate an LLM.
    In the final version, this will call the OpenAI API using the commented code below.
    """
    time.sleep(0.5) # Simulate API latency
    
    # We simulate the LLM injecting the context smoothly
    personalized_greeting = f"Hi {name},\n\nI hope you're having a good week!"
    
    context_builder = f"I'm reaching out regarding your progress in {class_name}. I saw that your recent grade is a {grade}. "
    
    if "A" in grade:
        context_builder += f"Fantastic job! I specifically noticed that you {note}."
    elif "B" in grade:
        context_builder += f"You're doing well! I wanted to mention that you {note}."
    else:
        context_builder += f"Don't get discouraged! I know you are {note}."
    
    # Merge with user's base template
    final_email = f"{personalized_greeting}\n\n{context_builder}\n\n{base_template}"
    
    return final_email

# --- REAL OPENAI CODE (commented out for template sharing without keys) ---
# import openai
# openai.api_key = "YOUR_API_KEY"
# def real_ai_generate(name, class_name, grade, note, base_template):
#     prompt = f"Write an email to {name} who is in {class_name}. Their grade is {grade}. Note about them: {note}.\nUse this template as a base: {base_template}"
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[{"role": "system", "content": "You are a helpful and supportive teacher."},
#                   {"role": "user", "content": prompt}],
#         temperature=0.7
#     )
#     return response.choices[0].message['content']

def process_students(csv_path, base_template):
    print(f"Loading students from {csv_path}...")
    df = pd.read_csv(csv_path)
    
    generated_emails = []
    
    print("\n--- Generating Emails ---\n")
    for index, row in df.iterrows():
        name = row['Name']
        class_name = row['Class']
        grade = str(row['Recent Grade'])
        note = row['Personal Note']
        
        print(f"Processing: {name} ({class_name})")
        
        # Here we use the mock AI. Replace with real_ai_generate later.
        email = mock_ai_generate(name, class_name, grade, note, base_template)
        
        generated_emails.append(email)
        
        # Print output for testing
        print("======== EMAIL PREVIEW ========")
        print(email)
        print("===============================\n")
        
    df['Generated_Email'] = generated_emails
    return df

def send_mock_email(to_email, subject, body):
    """
    Simulates sending an email via SMTP.
    In the real version, you'd use smtplib and email.mime modules.
    """
    print(f"Connecting to SMTP server...")
    time.sleep(0.3)
    print(f"Sending email to: {to_email}")
    print(f"Subject: {subject}")
    print(f"Body snippet: {body[:30]}...")
    time.sleep(0.5)
    print("Sent successfully!\n")
    return True

if __name__ == "__main__":
    # Test script execution
    template = "Please let me know if you need to schedule office hours. Best, Ms. Teacher"
    process_students("sample_students.csv", template)
    print("Done!")
