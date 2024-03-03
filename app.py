import streamlit as st
from mashup import *

def send_mail(to, filename):
    from dotenv import load_dotenv
    load_dotenv()
    email_address = os.getenv("EMAIL_ADDRESS") 
    email_password = os.getenv('EMAIL_PASSWORD')  
    # create email
    msg = MIMEMultipart()
    msg['Subject'] = "Mashup File"
    msg['From'] = email_address
    msg['To'] = to 

    with open(filename,'rb') as file:
        # Attach the file with filename to the email
        msg.attach(MIMEApplication(file.read(), Name='mashup.zip'))
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)
    


def main():
    st.title("Mashup")

    # Singer Name
    singer_name = st.text_input("Singer Name")

    # Number of Videos
    num_videos = st.number_input("Number of Videos", min_value=0, step=1)

    # Duration of Videos
    video_duration = st.number_input("Duration of Videos (in seconds)", min_value=0, step=1)

    # Email ID
    email_id = st.text_input("Email ID")

    # Submit Button
    if st.button("Submit"):
        # Process the form data
        process_form_data(singer_name, num_videos, video_duration, email_id)

def process_form_data(singer_name, num_videos, video_duration, email_id):
    # Process the form data here
    # You can perform any required operations with the input values
    # For example, you can store the data in a database or send an email
    # mashup_generator(singer_name, num_videos, video_duration, "mashup.mp3")
    # Print the form data
    st.write("Singer Name:", singer_name)
    st.write("Number of Videos:", num_videos)
    st.write("Duration of Videos:", video_duration, "minutes")
    st.write("Email ID:", email_id)
    # print "Emailed Successfully"
    mashup_generator(singer_name, num_videos, video_duration, "mashup.mp3")
    with zipfile.ZipFile("mashup.zip", 'w') as zipf:
        zipf.write("mashup.mp3", arcname="mashup.mp3")
    
    send_mail(email_id, "mashup.zip")
    st.write("Emailed Successfully to {}".format(email_id))


if __name__ == "__main__":
    main()