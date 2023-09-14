from django.shortcuts import render, redirect
import csv
import os
import pandas as pd
import plotly.express as px 
from plotly.offline import plot
from pandasai import PandasAI
from api.models import User
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
    msg['title'] = 'Login'
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
    data = []
    # with open('static/HR.csv', mode='r') as file:
    #     csvfile = csv.reader(file)
    #     for ind, lines in enumerate(csvfile):
    #         if ind != 0:
    #             inddata = {
    #                 "Name": lines[1],
    #                 "Hired": lines[2],
    #                 "Previous CTC": lines[3],
    #                 "Gender": lines[8],
    #                 "Domain": lines[9],
    #                 "Experience": lines[5]
    #             }
    #             data.append(inddata)

    #print(data)
    df = pd.read_csv('static/HR.csv')
    # Calculate Total Employees
    total_emp = df[df.columns[0]].count()
    msg["total_emp"] = total_emp
    
    
    #Calculate Gender Ratio
    gender_counts = df['Gender'].value_counts()
    count_male = gender_counts['Male']
    count_female = gender_counts['Female']
   
    # Total Attrition
    attrition = df['Attrition'].value_counts()['Yes']
    msg["attrition"] = attrition
    attrition_counts = df.groupby(['Gender', 'Attrition']).size().reset_index(name='Count')
    male_attrition = attrition_counts.loc[3, "Count"]
    female_attrition = attrition_counts.loc[1, "Count"]
    # Attrition Ratio
    attrition_ratio = format(((male_attrition+female_attrition)/total_emp)*100, ".3f")
    msg["attrition_ratio"] = attrition_ratio
    
    # Department wise male and Female count
    counts = df.groupby(['Department', 'Gender'])['Gender'].count()
    hr_male, hr_female = counts["HR"]["Male"], counts["HR"]["Female"]
    rd_male, rd_female = counts["R&D"]["Male"], counts["R&D"]["Female"]
    sales_male, sales_female = counts["Sales"]["Male"], counts["Sales"]["Female"]
    
    
    
    
    # Summary stats
    msg["summary_stats"] = df.describe()
    
    # Gender ratio pie chart
    fig_gender_ratio = px.pie(
        df, values=[count_male, count_female], names=["Male", "Female"], height=500, title="Gender Ratio"
    )
    pie_plot = fig_gender_ratio.to_html(full_html=False, include_plotlyjs=False)
    msg["fig_gender_ratio"] = pie_plot
    
    # HR ratio pie chart
    fig_hr_ratio = px.pie(
        df, values=[hr_male, hr_female], names=["HR Males", "HR Females"], height=250, title="HR"
    )
    pie_plot = fig_hr_ratio.to_html(full_html=False, include_plotlyjs=False)
    msg["fig_hr_ratio"] = pie_plot
    
    # R&D pie chart
    fig_rd_ratio = px.pie(
        df, values=[rd_male, rd_female], names=["R&D Males", "R&D Females"], height=250, title="R&D"
    )
    pie_plot = fig_rd_ratio.to_html(full_html=False, include_plotlyjs=False)
    msg["fig_rd_ratio"] = pie_plot
    
    # Sales pie chart
    fig_sales_ratio = px.pie(
        df, values=[sales_male, sales_female], names=["Sales Males", "Sales Females"], height=250, title="Sales"
    )
    pie_plot = fig_sales_ratio.to_html(full_html=False, include_plotlyjs=False)
    msg["fig_sales_ratio"] = pie_plot
    
    # Total attrition by gender
    fig_total_attritionbygender = px.bar(
        attrition_counts, x="Gender", y="Count", color="Attrition", barmode='group', title="Total Attrition by Gender", height=500
    )
    bar_plot = fig_total_attritionbygender.to_html(full_html=False, include_plotlyjs=False)
    msg["fig_total_attritionbygender"] = bar_plot

    #Box Plot
    fig_pay_gap = px.box(df, x='Gender', y='Monthly Income', title='Salary Distribution by Gender', height=500)
    box_plot = fig_pay_gap.to_html(full_html=False, include_plotlyjs=False)
    msg["fig_pay_gap"] = box_plot
    

    # Group the data by job role and gender, and calculate the count
    job_role_by_gender = df.groupby(['Job Role', 'Gender']).size().unstack()
    # Reset the index to convert 'Job Role' to a regular column
    job_role_by_gender = job_role_by_gender.reset_index()
    # Melt the dataframe to create separate columns for male and female counts
    job_role_by_gender = job_role_by_gender.melt(id_vars='Job Role', value_vars=['Male', 'Female'],
                                             var_name='Gender', value_name='Count')
    # Create a count plot
    fig_job_distribution = px.bar(job_role_by_gender, x='Count', y='Job Role', color='Gender', orientation='h',
             title='Gender Distribution by Job Role', labels={'Count': 'Count', 'Job Role': 'Job Role'})
    bar_plot = fig_job_distribution.to_html(full_html=False, include_plotlyjs=False)
    msg["fig_job_distribution"] = bar_plot

    # Group the data by job satisfaction status and gender, and calculate the count
    promotion_by_gender = df.groupby(['Job Satisfaction Status', 'Gender']).size().unstack()
    # Reset the index to convert 'Job Satisfaction Status' to a regular column
    promotion_by_gender = promotion_by_gender.reset_index()
    # Melt the dataframe to create separate columns for male and female counts
    promotion_by_gender = promotion_by_gender.melt(id_vars='Job Satisfaction Status', value_vars=['Male', 'Female'],
                                               var_name='Gender', value_name='Count')
    # Create a count plot
    fig_promotion_distribution = px.bar(promotion_by_gender, x='Count', y='Job Satisfaction Status', color='Gender', orientation='h',
             title='Promotion Status by Gender', labels={'Count': 'Count', 'Job Satisfaction Status': 'Job Satisfaction Status'})
    bar_plot = fig_promotion_distribution.to_html(full_html=False, include_plotlyjs=False)
    msg["fig_promotion_distribution"] = bar_plot

    
    X = df["Monthly Income"].values.reshape(-1, 1)
    x_range = np.linspace(X.min(), X.max(), 100)

    # Model #1
    knn_dist = KNeighborsRegressor(10, weights='distance')
    knn_dist.fit(X, df["Years At Company"])
    y_dist = knn_dist.predict(x_range.reshape(-1, 1))

    # Model #2
    knn_uni = KNeighborsRegressor(10, weights='uniform')
    knn_uni.fit(X, df["Years At Company"])
    y_uni = knn_uni.predict(x_range.reshape(-1, 1))

    fig = px.scatter(df, x='Monthly Income', y='Years At Company', color='Gender', title="Gender wise KNN Clustering", opacity=0.65)
    fig.add_traces(go.Scatter(x=x_range, y=y_uni, name='Weights: Uniform'))
    fig.add_traces(go.Scatter(x=x_range, y=y_dist, name='Weights: Distance'))
    knnplot = fig.to_html(full_html=True, include_plotlyjs=False)
    msg["knnplot"] = knnplot
    
    # 3D Scatter Plot
    fig = px.scatter_3d(df[1:100], x='Years At Company', y='Monthly Income', z='Total Working Years', color='Gender')
    fig.update_layout(
        scene=dict(
            xaxis_title='Years At Company',
            yaxis_title='Monthly Income',
            zaxis_title='Total Working Years',
        ),
        title='Gender Diversity Hiring Imbalances',
    )
    scatter3d_plot = fig.to_html(full_html=True, include_plotlyjs=False)
    msg["scatter3dplot"] = scatter3d_plot
    
    # Logistic Regression Model
    X = df[['Age', 'Monthly Income']][1:200]
    y = df['Department'][1:200]
    # Encode the target variable if it contains string values
    from sklearn.preprocessing import LabelEncoder
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y)

    # Fit a logistic regression model
    model = LogisticRegression()
    model.fit(X, y)

    # Generate grid points to create a decision boundary plot
    x1_min, x1_max = X['Age'].min() - 1, X['Age'].max() + 1
    x2_min, x2_max = X['Monthly Income'].min() - 1, X['Monthly Income'].max() + 1
    xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, 0.1), np.arange(x2_min, x2_max, 100))
    Z = model.predict(np.c_[xx1.ravel(), xx2.ravel()])
    Z = Z.reshape(xx1.shape)

    # Create a scatter plot of the data points
    fig = go.Figure(data=go.Scatter(x=X['Age'], y=X['Monthly Income'], mode='markers', marker=dict(color=y)))

    # Add a contour plot for the decision boundary
    fig.add_trace(go.Contour(x=xx1[0], y=xx2[:, 0], z=Z, colorscale='Viridis', showscale=False, opacity=0.8))

    # Customize the plot layout
    fig.update_layout(
        title="Logistic Regression Decision Boundary",
        xaxis_title="Age",
        yaxis_title="Monthly Income",
    )
    logistic_plot = fig.to_html(full_html=True, include_plotlyjs=False)
    msg["logisticplot"] = logistic_plot
    

    
    
    # fig_scatter = px.scatter(
    #     df, x="Experience", y="Previous CTC", color="Gender", height=500, hover_data=["Name"], title="Scatter Plot"
    # )
    # fig_pie = px.pie(
    #     df.loc[1:30], values="Experience", names="Gender", height=250, title="Pie Chart"
    # )
    
    
    # scatter_plot = fig_scatter.to_html(full_html=True, include_plotlyjs=False)
    
    
    # msg["scatterplot"] = scatter_plot
    
    
    return render(request, 'historical.html', msg)


def prompt(request):
    if not request.session.get('user_id'): return redirect(index)
    msg = {}
    prompt = None
    msg["prompt"] = prompt
    imported_data = None
    if request.method == 'POST':
        button = False
        prompt = request.POST.get('prompt')
        
        csv_file = request.FILES.get('data')
        
        if csv_file:
            imported_data = pd.read_csv(csv_file)
            imported_data.to_csv('media/data.csv')
            #print(imported_data.describe())
            button = True
        
        if prompt:
            imported_data = pd.read_csv('media/data.csv')
            from pandasai.llm.openai import OpenAI
            from dotenv import load_dotenv
            load_dotenv()
            api_key = os.getenv('api_key')
            llm = OpenAI(api_token=api_key)
            pandas_ai = PandasAI(llm)
            response = pandas_ai.run(imported_data, prompt=prompt)
            print(response, type(response))
            msg["prompt"] = response
        msg['button'] = button
        msg["imported_data"] = imported_data.loc[0:9]
    return render(request, 'prompt.html', msg)
    

def custom(request):
    msg = {}
    import_form = True
    changed = False
    if request.method == 'POST':
        csv_file = request.FILES.get('data')
        #num_rows = request.POST.get('num_rows')
        #imported_data = None
        #button = False
        #edit = False
        if csv_file:
            imported_data = pd.read_csv(csv_file)
            imported_data.drop(columns=imported_data.columns[0], axis=1, inplace=True)
            imported_data.to_csv('static/HR.csv')
            button = True
            return redirect(home)
        # elif num_rows:
        #     num_rows = int(num_rows)
        #     df = pd.read_csv('static/HR.csv')
        #     columns = list(df.columns)
        #     columns.pop(0)
        #     num_columns = len(columns)
        #     # data = [request.POST.getlist(f'data[{i}]') for i in range(num_rows)]
        #     data = []
        #     for i in range(num_rows):
        #         lst = request.POST.getlist(f'data[{i}]')
        #         lst.pop(0)
        #         data.append(lst)
        #     imported_data = pd.DataFrame(data, columns=columns)
        #     imported_data.to_csv('media/custom.csv')
        #     changed=True
        #     button=True
        # else:
        #     imported_data = pd.read_csv('media/custom.csv')
        #     edit = True
        #     import_form = False
        # msg['imported_data'] = imported_data   
        # msg['button'] = button
        # msg['edit'] = edit
        # msg['changed'] = changed
    msg['import_form'] = import_form      
    return render(request, 'custom.html', msg)