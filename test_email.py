import pandas as pd
from ai_engine import mock_ai_generate, send_real_email

sender_email = "yazanbawaqna@gmail.com"
sender_password = "tecnmtjxfetkmicy"
base_template = "This is a test from the OutreachAI platform. Hope you are well!"
base_subject = "Checking in on your progress! [OutreachAI Test]"

print("Loading test data...")
df = pd.read_csv("sample_students.csv")

for index, row in df.iterrows():
    print(f"Generating for {row['Name']}...")
    email_body = mock_ai_generate(
        name=row["Name"],
        class_name=row["Class"],
        grade=str(row["Recent Grade"]),
        note=row["Personal Note"],
        base_template=base_template
    )
    
    print(f"Sending to {row['Email']}...")
    success, message = send_real_email(
        sender_email, 
        sender_password, 
        row['Email'], 
        base_subject, 
        email_body
    )
    
    if success:
        print(f"SUCCESS: Email sent to {row['Email']}\n")
    else:
        print(f"FAILED: Email to {row['Email']} failed. Error: {message}\n")
