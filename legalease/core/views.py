from django.shortcuts import render, redirect
import csv
import os
import pandas as pd
import plotly.express as px 
from plotly.offline import plot
from pandasai import PandasAI
from api.models import User, Expert, Docs
from api.serializers import UserSerializer
from hashlib import sha256
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from core.settings import EMAIL_HOST_USER
import random
import numpy as np
import plotly.graph_objects as go
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LogisticRegression
from functools import lru_cache

def index(request):
    if request.session.get('user_id'): return redirect(home)
    msg = {}
    msg["title"] = "Welcome"
    return render(request, 'index.html', msg)

def login(request):
    if request.session.get('user_id'):
        return redirect(home)
    msg = {}
    msg["title"] = "Login"
    msg["status"] = 1
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        hash = sha256(password.encode()).hexdigest()
        users = User.objects.filter(email=email)
        flg = 0
        for user in users:
            if user.password == hash:
                otp = str(random.randrange(1000,99999))
                otp_hash = str(sha256(otp.encode()).hexdigest())
                request.session['on_hold'] = user.id
                user.data = otp_hash
                user.save()
                flg = 1
                break
        if flg == 1:
            try:
                subject = "One-Time Password to Login to Your LegalEase Account"
                message = f"Hello {user.username} \n Your Verification OTP is : {otp}. \n Please use the OTP code to complete your login request.\n\n\n Best Regards,\n LegalEase"
                send_mail(subject, message, EMAIL_HOST_USER, [user.email], fail_silently=True)
                return redirect(email_verify)
            except:
                msg['status'] = 0
        else: msg['status'] = -1

    return render(request, 'login.html', msg)


def email_verify(request):
    if not request.session.get('on_hold'): return redirect(index)
    if request.session.get('user_id'): return redirect(home)
    user = User.objects.get(id=request.session['on_hold'])
    user_data = UserSerializer(user)
    msg = {}
    msg['username'] = user_data['username'].value
    msg['status'] = 1
    msg['title'] = 'Verify Email'
    if request.method == 'POST':
        otp = str(request.POST.get('otp'))
        hash = str(sha256(otp.encode()).hexdigest())
        if user_data['data'].value == hash:
            del request.session['on_hold']
            request.session['user_id'] = user_data['id'].value
            return redirect(index)
        msg['status'] = -1

    return render(request, 'emailverify.html', msg)
        

def register(request):
    if request.session.get('user_id'):
        return redirect(home)
    msg = {}
    msg["title"] = "Register"
    if request.method == 'POST':
        username, email, password = request.POST.get('username'), request.POST.get('email'), request.POST.get('password')
        hash = sha256(str(password).encode()).hexdigest()
        user = User(username=username, email=email, password=hash, data='')
        user.save()
        msg['status'] = 1
    return render(request, 'register.html', msg)


def logout(request):
    if request.session.get('user_id'):
        del request.session['user_id']
    return redirect(index)


# def home(request):
#     if not request.session.get('user_id'):
#         return redirect(index)
#     msg = {}
#     msg["title"] = "Dashboard"
#     return render(request, 'home.html',msg)

@lru_cache()
def home(request):
    if not request.session.get('user_id'): return redirect(index)
    msg = {"title": "Dashboard", "description": "This is the landing Page"}
    number_of_docs = len(Docs.objects.all())
    msg["number_of_docs"] = number_of_docs
    msg["number_of_domains"] = 5
    msg["number_of_languages_supported"] = 25
    # HR ratio pie chart
    # fig_hr_ratio = px.pie(
    #     df, values=[hr_male, hr_female], names=["HR Males", "HR Females"], height=250, title="HR"
    # )
    # pie_plot = fig_hr_ratio.to_html(full_html=False, include_plotlyjs=False)
    # msg["fig_hr_ratio"] = pie_plot
    
    # # R&D pie chart
    # fig_rd_ratio = px.pie(
    #     df, values=[rd_male, rd_female], names=["R&D Males", "R&D Females"], height=250, title="R&D"
    # )
    # pie_plot = fig_rd_ratio.to_html(full_html=False, include_plotlyjs=False)
    # msg["fig_rd_ratio"] = pie_plot
    
    # Sales pie chart
    # fig_sales_ratio = px.pie(
    #     df, values=[sales_male, sales_female], names=["Sales Males", "Sales Females"], height=250, title="Sales"
    # )
    # pie_plot = fig_sales_ratio.to_html(full_html=False, include_plotlyjs=False)
    # msg["fig_sales_ratio"] = pie_plot
    
    # Total attrition by gender
    # fig_total_attritionbygender = px.bar(
    #     attrition_counts, x="Gender", y="Count", color="Attrition", barmode='group', title="Total Attrition by Gender", height=500
    # )
    # bar_plot = fig_total_attritionbygender.to_html(full_html=False, include_plotlyjs=False)
    # msg["fig_total_attritionbygender"] = bar_plot

   
    return render(request, 'home.html', msg)


def generatedoc(request):
    if not request.session.get('user_id'): return redirect(index)
    msg = {}
    msg["status"] = -1
    if request.method == 'POST':
        domain = request.POST.get('domain')
        duration = request.POST.get('duration')
        jurisdiction = request.POST.get('jurisdiction')
        date = request.POST.get('date')
        party1 = request.POST.get('party1')
        party2 = request.POST.get('party2')
        import openai
        import os
        openai.api_key = os.getenv('api_key')
        # try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
            {"role": "user", "content": f"""Parties:
            - Party A: {party1}
            - Party B: {party2}
            Terms:
            - Effective Date: {date}
            - Duration: {duration}
            - Jurisdiction: {jurisdiction}

            {domain}:
            This {domain} ("{domain}") is entered into by Party A and Party B on the Effective Date. Generate a legal documentation for the above prompt."""}
            ]
        )
        text = response['choices'][0]['message']['content']
        msg["status"] = 1
        msg["text"] = text
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        my_pdf = canvas.Canvas('C:/Users/dhana/coding/Personal Projects/LegalEase/legalease/media/docs/newfile.pdf', pagesize=letter)
        my_pdf.setFont('Helvetica', 12)
        x,y = 100, 700
        paragraphs = text.split('\n\n')
        for paragraph in paragraphs:
            my_pdf.drawString(x,y, paragraph)
            y -= 20
        my_pdf.save()
        #pdf.output('C:/Users/dhana/coding/Personal Projects/LegalEase/legalease/media/docs/newfile.pdf', 'F')
        #my_pdf = Canvas("C:/Users/dhana/coding/Personal Projects/LegalEase/legalease/media/docs/newfile.pdf", pagesize = LETTER)  
        

    return render(request, 'generatedoc.html', msg)

def translation(request):
    msg = {}
    if request.method == 'POST':
        pdf_file = request.FILES.get('data')
        language_code = request.POST.get('language')
        translate(pdf_file, language_code)
        msg["status"] = 1    
    return render(request, 'translate.html', msg)

def expertlogin(request):
    msg = {"title": "Expert Login", "description": "This is the Expert Page"}
    if request.session.get('expert_id'):
        return redirect(experthome)
    if request.method == 'POST':
        email, password = request.POST.get('email'), request.POST.get('password')
        expert = Expert.objects.filter(email=email, password=password)
        if expert:
            request.session['expert_id'] = expert.id
            return redirect(experthome)
        else:
            msg['status'] = -1
    return render(request, 'expertlogin.html', msg)

def experthome(request):
    pass

def translate(file, target_language):
    from PyPDF2 import PdfReader
    from googletrans import Translator
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph
    from reportlab.lib.styles import getSampleStyleSheet
    from io import BytesIO

    def translate_text(text, target_language):
        translator = Translator()
        return translator.translate(text, dest=target_language).text

    pdf_file = file
    pdf_reader = PdfReader(open(pdf_file, "rb"))


    output_filename = "legalease/media/docs/translated.pdf"

    # Initialize ReportLab document
    output_buffer = BytesIO()
    doc = SimpleDocTemplate(output_buffer, pagesize=letter)

    # Define a style for the translated text
    styles = getSampleStyleSheet()
    style = styles["Normal"]

    translated_paragraphs = []

    # Loop through each page of the PDF
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text = page.extract_text()

        # Translate the entire page's text to the target language
        translated_text = translate_text(text, target_language)
        
        # Split the translated text into paragraphs
        translated_paragraphs.extend(translated_text.split('\n'))

    # Create Story for ReportLab
    story = []

    for paragraph in translated_paragraphs:
        paragraph = Paragraph(paragraph, style)
        story.append(paragraph)

    # Build the ReportLab PDF
    doc.build(story)

    with open(output_filename, 'wb') as output_file:
        output_file.write(output_buffer.getvalue())