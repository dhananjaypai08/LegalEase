# DiversifyNow
## 👨‍💻👩‍💻 Explore the ever evolving dynamics of inlcusive Hiring

<p align="center">
    Developing a web-based Diversity Analytics Dashboard to empower Corporate Services with insights and predictive tools for improving gender diversity hiring, utilizing historical data, demand prediction, real-time tracking, and data visualization.
    <br />
    <a href="https://github.com/dhananjaypai08/diversifiedHiring/issues">Report Bug</a>
    <br />
  <a href="https://github.com/dhananjaypai08/diversifiedHiring">Project Link</a>
 </p>
 
 ## ✍️ Table of Contents
- [Project Breakdown](#project-breakdown)
- [About the Project](#about-the-project)
  - [Built With](#built-with)
- [Getting Started](#getting-started)
  - [Installation](#installation)
- [Usage](#usage)
- [Contributions](#contributions)

## 🔨 Project Breakdown 
- Two factor authentication. Login Authentication + OTP verification via email service.
- Analyze historic as well as live(Imported) data to identify trends and patterns related to diversity. Track diversity in applicants for each position and hiring ratios at every stage of the hiring process.
- Visualize vendor graphs depicting trends in positions filled with diverse candidates.
- <strong>USP: Chat with Datat</strong> managers can import any dataset and chat with the Data. For example: Plot a graph/chart against this vs this, recommend the potential candidates based on given condition
- Enable real-time tracking of diversity ratios.
- Generate graphical representations to visualize the rise/fall in demand and supply based on bands and BUs.
- Highlight diversity ratio gaps on the BU map for better visibility and understanding.

## 💻 About The Project
The problem statement revolves around corporate services, 
which is facing a challenge in achieving a balanced gender diversity ratio within their firm. Currently, the company has a men to women ratio of 73:27, indicating a significant gender imbalance. 
Despite their efforts to hire more gender-diverse talent, the company has struggled to make significant progress, mainly due to a lack of supporting data.

To address this issue, AlwaysFirst is seeking an intelligent solution that can help them create and analyze data to improve their diversity ratio. One potential solution presented is "BuildTogether," which is described as a dashboard of diversity and inclusion (D&I) metrics. 
This dashboard aims to enable managers to remain accountable for reaching the company's D&I goals.

### 🔧 Built With
- Frontend:
  - HTML
  - Bootstrap
  - CSS
  - Jinja2
- Backend: 
  - Django
  - MongoDB
  - Django Rest Framework
    - Serializers
  - Plotly
  - Dash
  - PandasAI
  - Scikit-learn


## 🚀 Getting Started
To get a local copy up and running follow these simple steps.

### 🔨 Installation
1. Clone the repo

```sh
git clone https://github.com/dhananjaypai08/diversifiedHiring/
```

2. Create a Virtual Environment and activate

```sh
python3 -m venv [your_environment_name]
.\[your_environment_name]\Scripts\activate
```
<strong>Make sure in your .env file you enter your own OpenAI api key.</strong>

3. Installing dependencies and requirements

Terminal 1
```sh
cd diversifynow
pip3 install -r requirements.txt
```

4. Running the APP
```sh
python3 manage.py runserver
```

Terminal 2
```sh
cd filteringdash
pip3 install -r requirements.txt
```

 Running the APP
```sh
python3 main.py
```


Database migrations
```sh
python3 manage.py makemigrations
python3 manage.py migrate
```

## 🧠 Usage
Built version:
- Python v3.10.5
- Django v4.0.1

creation of the Diversity Analytics Dashboard for Corporate Services represents a significant step forward in addressing gender diversity imbalances within the organization. By harnessing the power of historical data analysis, demand prediction, and real-time tracking, the dashboard offers a comprehensive solution to identify trends, patterns, and areas of improvement in the hiring process. This project not only equips key stakeholders with the tools to make informed decisions, but also promotes a more inclusive and diverse workforce by providing actionable insights and visualizations. As the company strives for greater gender diversity, the dashboard stands as a testament to the potential of data-driven approaches in fostering positive change within the corporate landscape.

## 🤠 Contributions 
Open for contributions. Just clone and follow the installation. Make changes and raise a PR detailing about the changes made.

## 🏃♂️ Future Plans
- Switching from Monolithic architecture to Microservice Architecture
- Making custom modifications to the imported dataset. Just like any other dataset editor
- Feature to save edited snapshots of your dataset
- For containers to interact with each other we will require a container orchestration tool(kubernetes)

Elevating gender diversity at AlwaysFirst through data-driven insights.
