from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
import base64
import io
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#taking content, giving to the model , based on some prompt
def get_gemini_response(input,pdf_content,prompt):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    #convert the pdf to image
    if uploaded_file is not None:
        images=pdf2image.convert_from_bytes(uploaded_file.read())
        first_page=images[0]

        #convert to bytes?
        img_byte_arr=io.BytesIO()
        first_page.save(img_byte_arr,format='JPEG')
        img_byte_arr=img_byte_arr.getvalue()

        pdf_parts=[
            {
                "mime_type":"image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode() #encode to base64
            }
        ]

        return pdf_parts
    else:
        raise FileNotFoundError("No File Uploaded")
    
# streamlit app

st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text=st.text_area("Job Description: ", key="input")
uploaded_file=st.file_uploader("Upload your resue(PDF)..",type=["pdf"])


if uploaded_file is not None:
    st.write("Pdf Uploaded Successfully")

submit1=st.button("Tell Me About the Resume")
# submit3=st.button("How Can I Improvise my Skills")   can be added
submit2=st.button("Percentage Match")

input_prompt1="""
You are an experienced Technical Human Resource Manager, your task is to review the provided resume agaianst the job description
.Please share your professional evaluation on whether the candidate's profile aligns with the role.
Highlight the strengths and the weakness of the applicant in relation to specified job requirements.
"""

input_prompt2="""
You are an skilled ATS(Application Tracking System) scanner witha deep understanding od data science and ATS functionality,
your task is to evaluate the resume against the provided job description. Give me the percentage match
if the resume matches the job description. First the output should come as percentage and then keywords missing
and last final thoughts.

"""

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.write("Please Upload a Resume")

elif submit2:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt2, pdf_content, input_text)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.write("Please Upload a Resume")





