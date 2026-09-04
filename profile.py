import json
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from pydantic import BaseModel, Field
try:
    from groq import Groq
except ImportError:
    Groq = None

# ------------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & STYLING
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Kishan Sharma | Interactive AI Portfolio",
    page_icon="🚀",
    layout="wide"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .company-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #0F172A;
        margin-top: 1.2rem;
    }
    .role-subtitle {
        font-size: 1.05rem;
        font-weight: 600;
        color: #334155;
    }
    .project-header {
        font-size: 1.05rem;
        font-weight: 600;
        color: #2563EB;
        margin-top: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 2. FULL CANDIDATE PROFILE DATA
# ------------------------------------------------------------------------------
PROFILE_DATA = {
    "name": "Kishan Sharma",
    "title": "Principal - Data & AI Engineer/Architect | Gen AI Solutions Architect | Forward Deployed Engineer",
    "contact": {
        "phone": "(224) 258-8971",
        "email": "kishansharma.sharma60@gmail.com",
        "location": "Chicago, IL",
        "linkedin": "https://linkedin.com/in/kishan-sharma-2b2663a6/"
    },
    "summary": "13.5 years' experience in Data & AI Engineering, Databricks Lakehouse Architecture, GenAI Solutions, LLM Code Agents, and Cloud Enterprise Data Platforms.",
    "awards": [
        "IMPACT Award (June 2025)",
        "Multiple MAKE IT HAPPEN Awards in last 2 years with Zurich Insurance",
        "Part of the $1.5B RFP won by TCS from Walgreens in 2020 for Global Operations",
        "Architect & key contributor saving ~$8M/year for Walgreens under Total Cost Optimization Program",
        "EMERGING GURU AWARD (January 2023) at annual Golden Gala awards for Training & Competency Building",
        "Winner of TCS Global Hackathon (July 2021)",
        "Multiple Star of the Quarter, Star of the Month, and Technical Excellence Awards"
    ],
    "skills_rated": [
        {"skill": "Databricks & Delta Lake", "rating": 9.5, "category": "Data Engineering", "level": "Expert (🔥 Hot)"},
        {"skill": "PySpark / Spark SQL", "rating": 9.5, "category": "Data Engineering", "level": "Expert (🔥 Hot)"},
        {"skill": "LangChain / LangGraph / N8N", "rating": 9.0, "category": "AI & GenAI", "level": "Expert (🔥 Hot)"},
        {"skill": "Unity Catalog & DLT", "rating": 9.0, "category": "Data Engineering", "level": "Expert (🔥 Hot)"},
        {"skill": "Python / Pydantic", "rating": 9.0, "category": "Core / Lang", "level": "Expert (🔥 Hot)"},
        {"skill": "RAG & Vector Search", "rating": 9.0, "category": "AI & GenAI", "level": "Expert (🔥 Hot)"},
        {"skill": "Azure Cloud (ADF, Synapse, ADLS)", "rating": 8.5, "category": "Cloud & DevOps", "level": "Advanced"},
        {"skill": "SQL & Data Modeling", "rating": 9.0, "category": "Core / Lang", "level": "Expert (🔥 Hot)"},
        {"skill": "Snowflake", "rating": 8.0, "category": "Data Engineering", "level": "Advanced"},
        {"skill": "dbt & DAB Frameworks", "rating": 8.5, "category": "Cloud & DevOps", "level": "Advanced"},
        {"skill": "Hadoop / Hive / Sqoop", "rating": 8.5, "category": "Legacy & Big Data", "level": "Advanced"},
        {"skill": "Kafka Streaming", "rating": 8.0, "category": "Data Engineering", "level": "Advanced"},
        {"skill": "Talend / SSIS ETL", "rating": 8.5, "category": "Legacy & Big Data", "level": "Advanced"}
    ],
    "experience": [
        {
            "company": "Zurich Insurance",
            "role": "Principal Data & AI Engineer/Architect",
            "period": "May 2024 - Current",
            "skills": "Databricks, PySpark, Spark, Unity Catalog, Delta Lake, Azure SQL, Azure Synapse, Azure Data Factory, Hadoop, Python, ETL, SQL, Kafka, DLT, DAB, Spark NLP, DBT, Langchain, VectorSearch, LLMs, Pydantic, Snowflake, SSIS, Pinecone",
            "projects": [
                {
                    "title": "SCS Bright Horizon (SCS - PCMI Migration)",
                    "highlights": [
                        "Developed a CODE Agent using LLMs and Databricks to automatically convert legacy SSIS packages and Stored Procedures into Databricks Python/PySpark code, now utilized across teams for automated code conversion.",
                        "Architected and implemented end-to-end Medallion Architecture pipelines, automated metadata sync pipelines, and operational checks-and-balances pipelines."
                    ]
                },
                {
                    "title": "TSP Telematics Business Line Data Architecture",
                    "highlights": [
                        "Partnered with TSP vendors to evaluate capabilities against enterprise requirements and designed telematics data architecture.",
                        "Engineered pipelines and executive dashboards for telematics data reconciliation and reporting."
                    ]
                },
                {
                    "title": "PDF RAG Search Engine & Document Intelligence",
                    "highlights": [
                        "Successfully deployed an enterprise RAG Chat solution over unstructured PDFs (Claims, Billing, Policy) using LangChain, Databricks, LLMs (OpenAI), and Vector Index."
                    ]
                },
                {
                    "title": "Guidewire Policy Center - CDA Enterprise Pipeline",
                    "highlights": [
                        "Architected, built, and deployed to production a critical pipeline processing 4,200+ daily tables with 80-90 minutes end-to-end runtime used across the organization for reporting and downstream applications."
                    ]
                },
                {
                    "title": "Claims Connect - AGG Limit Optimization",
                    "highlights": [
                        "Optimized PDF processing pipeline ingesting 120,000 daily PDFs within 15 minutes, drastically reducing runtime from 73 hours down to 1.5 hours."
                    ]
                },
                {
                    "title": "FMCSA Open-Data Web Ingestion Pipeline",
                    "highlights": [
                        "Built automated pipeline extracting external regulatory website data into Data Lake and curating key KPI layers, delivering ~$500K/year in operational cost savings."
                    ]
                },
                {
                    "title": "DAB, DBT & CI/CD Frameworks",
                    "highlights": [
                        "Helped establish DAB framework, DBT curation framework, automated DDL cleansing agent, and Azure DevOps CI/CD pipelines incorporating Databricks DLT Meta."
                    ]
                }
            ]
        },
        {
            "company": "Tiger Analytics",
            "role": "Lead Data Engineer / Data Architect",
            "period": "January 2024 - May 2024",
            "skills": "Databricks, PySpark, Spark, Unity Catalog, Delta Lake, Azure SQL, Azure Synapse, Azure Data Factory, Hadoop, Python, ETL, SQL, Kafka",
            "projects": [
                {
                    "title": "Real-Time Streaming & Enterprise Lakehouse Frameworks",
                    "highlights": [
                        "Engineered high-throughput real-time Kafka data streaming pipelines and downstream PySpark processors.",
                        "Designed complex data warehousing architectures, distributed cluster sizing models, capacity planning, and reusable engineering frameworks."
                    ]
                }
            ]
        },
        {
            "company": "Citizens Bank",
            "role": "Senior Data Engineer",
            "period": "September 2023 - January 2024",
            "skills": "Databricks, PySpark, Unity Catalog, Delta Lake, Spark, Python, Talend, EMR, Hadoop, SQL, Redshift, Java, S3, Kafka",
            "projects": [
                {
                    "title": "Data Control Center / AWS EMR to Databricks Migration",
                    "highlights": [
                        "Led AWS EMR to Databricks cloud modernization under the Data Control Center initiative.",
                        "Built custom REST APIs for automated job submission, source connections, data reads, and pipeline health monitoring.",
                        "Managed, mentored, and conducted code/architectural reviews for a team of 4-7 Data Engineers."
                    ]
                }
            ]
        },
        {
            "company": "Tata Consultancy Services (TCS) — The Home Depot",
            "role": "Computer Programmer / Lead Data Architect",
            "period": "April 2023 - August 2023",
            "skills": "Databricks, SAP BW, SQL, Python, PySpark, ADF, Snowflake, Bitbucket, GIT",
            "projects": [
                {
                    "title": "SAP BW Migration to Databricks & Logistics Data Warehouse",
                    "highlights": [
                        "Designed and built large-scale SAP BW migration pipelines into Databricks and Snowflake using PySpark and Azure Data Factory.",
                        "Created reusable pipeline frameworks ensuring automated logging, re-startability, and performance optimization."
                    ]
                }
            ]
        },
        {
            "company": "Tata Consultancy Services (TCS) — Walgreens Co.",
            "role": "Computer Programmer / Lead Developer / Architect",
            "period": "July 2016 - March 2023",
            "skills": "Databricks, Azure Synapse, Azure Data Lake, ADF, PySpark, Spark SQL, Python, HDFS, Sqoop, Talend, Abinitio, Datastage, Oracle, JMS, Hive",
            "projects": [
                {
                    "title": "LEAP - Cloud Modernization (On-Prem Hadoop to Azure/Databricks)",
                    "highlights": [
                        "Led transition of legacy on-prem Hadoop data to Azure ADLS and Databricks using PySpark, ADF, and PowerShell automation.",
                        "Built a Central Data Lineage repository using POM files/Python and developed a metadata-driven automated testing framework."
                    ]
                },
                {
                    "title": "Total Cost Optimization Program (Ab Initio / DataStage to Talend & PySpark)",
                    "highlights": [
                        "Migrated legacy Ab Initio and DataStage workloads to PySpark and Talend, directly enabling ~$8M/year in operational savings.",
                        "Created account-level Spark big data framework ensuring code re-usability, logging, and performance SLAs for store inventory jobs.",
                        "Led and mentored a team of 14-16 Data Engineers."
                    ]
                },
                {
                    "title": "Retail & Finance Transformation (Legacy to SAP)",
                    "highlights": [
                        "Built real-time messaging pipeline for processing Store Promotions and Markdowns using JMS, PySpark, and Talend Big Data.",
                        "Introduced PySpark optimizations to handle massive retail data tables (MARA, MARC, BDM) within strictly mandated SLAs."
                    ]
                }
            ]
        },
        {
            "company": "Tata Consultancy Services (TCS) — JD Williams",
            "role": "Developer",
            "period": "June 2015 - July 2016",
            "skills": "Talend, Hadoop, HDFS, Hive, Sqoop, SOA, SQL, GIT, TAC, Power BI",
            "projects": [
                {
                    "title": "Golden Customer (Single Customer View)",
                    "highlights": [
                        "Constructed large-scale Big Data pipelines using Talend, Hadoop, Hive, and Sqoop for Single Customer View analytics.",
                        "Authored complex SQL stored procedures and built executive Power BI dashboards for business stakeholders."
                    ]
                }
            ]
        },
        {
            "company": "Tata Consultancy Services (TCS) — ASDA Stores Limited",
            "role": "Developer",
            "period": "March 2013 - June 2015",
            "skills": "SSIS, SSAS (Multidimensional & Tabular), SSRS, Power BI, SQL, Control M, TFS",
            "projects": [
                {
                    "title": "Parcel Tracking System & Data Warehouse Management",
                    "highlights": [
                        "Engineered SSIS ETL packages, SOA Web Services, and SSAS multidimensional/tabular cubes using MDX/DAX.",
                        "Automated SSAS cube processing and automated report delivery, eliminating manual support intervention."
                    ]
                }
            ]
        }
    ]
}

# ------------------------------------------------------------------------------
# 3. LLM RESPONSE SCHEMA & INFERENCE FUNCTION
# ------------------------------------------------------------------------------
class MatchAnalysis(BaseModel):
    match_percentage: int = Field(description="Match score from 0 to 100 based on alignment.")
    executive_summary: str = Field(description="2-3 sentence overview explaining why the candidate fits this role.")
    matching_skills: list[str] = Field(description="Matching technical skills from JD.")
    skill_gaps_or_growth: list[str] = Field(description="Transferable areas or growth skills.")
    value_proposition: list[str] = Field(description="3 distinct bullet points detailing candidate impact.")

def analyze_job_match(job_description: str, api_key: str, model_name: str = "groq/compound") -> MatchAnalysis:
    if not Groq:
        raise ValueError("The 'groq' package is not installed. Please add 'groq' to requirements.txt.")
    
    if not api_key:
        raise ValueError("Groq API Key is missing. Please provide one in the sidebar or Streamlit Secrets.")

    client = Groq(api_key=api_key)

    prompt = f"""
    You are an executive technical talent recruiter evaluating candidate alignment.
    
    CANDIDATE PROFILE:
    Name: {PROFILE_DATA['name']}
    Title: {PROFILE_DATA['title']}
    Summary: {PROFILE_DATA['summary']}
    Awards: {json.dumps(PROFILE_DATA['awards'])}
    Skills: {json.dumps(PROFILE_DATA['skills_rated'])}
    Experience & Projects: {json.dumps(PROFILE_DATA['experience'])}
    
    JOB DESCRIPTION TO EVALUATE:
    {job_description[:4000]}
    
    Analyze alignment objectively and output strictly structured JSON adhering to key names:
    match_percentage (int), executive_summary (str), matching_skills (list of str), skill_gaps_or_growth (list of str), value_proposition (list of str).
    """

    # Model fallback list starting with groq/compound
    models_to_try = [
        model_name,
        "groq/compound",
        "groq/compound-mini",
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant"
    ]
    
    # Remove duplicates while preserving order
    seen = set()
    unique_models = [m for m in models_to_try if not (m in seen or seen.add(m))]

    last_exception = None

    for m in unique_models:
        try:
            response = client.chat.completions.create(
                model=m,
                messages=[
                    {"role": "system", "content": "You are an expert technical talent recruiter. Output strictly valid JSON matching the schema."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.2
            )
            return MatchAnalysis.model_validate_json(response.choices[0].message.content)
        except Exception as err:
            last_exception = err
            continue

    raise last_exception

# ------------------------------------------------------------------------------
# 4. UI NAVIGATION & SIDEBAR
# ------------------------------------------------------------------------------
st.sidebar.title(PROFILE_DATA['name'])
st.sidebar.caption(PROFILE_DATA['contact']['email'])
st.sidebar.markdown(f"📍 {PROFILE_DATA['contact']['location']} | 📞 {PROFILE_DATA['contact']['phone']}")
st.sidebar.markdown("---")

# Retrieve API key from secrets or user input
groq_key = st.secrets.get("GROQ_API_KEY", "")
if not groq_key:
    groq_key = st.sidebar.text_input("Groq API Key (Free @ groq.com):", type="password", help="Enter a free API key from console.groq.com to power the AI matcher.")

selected_model = st.sidebar.selectbox("LLM Model Engine", [
    "groq/compound",
    "groq/compound-mini",
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant"
])

st.sidebar.markdown("---")
nav_selection = st.sidebar.radio(
    "Navigate",
    ["🎯 AI Role Matcher", "📊 Skills & Competency Dashboard", "📜 Complete Resume"]
)

# ==============================================================================
# TAB 1: AI ROLE FIT MATCHER
# ==============================================================================
if nav_selection == "🎯 AI Role Matcher":
    st.markdown('<div class="main-header">AI-Powered Role Alignment Engine</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Paste any Job Description to compute candidate match percentage, core alignment, and tailored value proposition.</div>', unsafe_allow_html=True)

    preset_jds = {
        "Custom JD": "",
        "Principal Data Architect (Databricks / GenAI)": (
            "We are seeking a Principal Data Architect to lead enterprise GenAI and Lakehouse modernizations. "
            "Required skills: Databricks, PySpark, Unity Catalog, LLM Code Agents, RAG architecture, and Azure DevOps."
        ),
        "Forward Deployed AI Solutions Engineer": (
            "Seeking a hands-on AI Engineer to build LLM agents, code-translation engines, vector search pipelines, "
            "and work closely with business leaders to deploy scalable AI solutions into production."
        )
    }

    selected_preset = st.selectbox("Sample Job Descriptions:", list(preset_jds.keys()))
    default_text = preset_jds[selected_preset] if selected_preset != "Custom JD" else ""
    jd_input = st.text_area("Paste Job Description (JD):", value=default_text, height=200)

    if st.button("🚀 Analyze Alignment", type="primary"):
        if not jd_input.strip():
            st.warning("Please paste a Job Description first.")
        elif not groq_key:
            st.error("Missing API Key! Please enter a free Groq API key in the sidebar (or configure GROQ_API_KEY in Streamlit secrets).")
        else:
            with st.spinner("Evaluating alignment using Groq AI Cloud..."):
                try:
                    result = analyze_job_match(
                        jd_input, 
                        api_key=groq_key, 
                        model_name=selected_model
                    )
                    
                    st.markdown("---")
                    c1, c2 = st.columns([1, 2])
                    with c1:
                        st.metric("Overall Match", f"{result.match_percentage}%")
                        st.progress(result.match_percentage / 100)
                    with c2:
                        st.subheader("Executive Fit Summary")
                        st.write(result.executive_summary)

                    st.markdown("---")
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.markdown("### ✅ Direct Technical Matches")
                        for item in result.matching_skills:
                            st.markdown(f"- **{item}**")
                    with col_b:
                        st.markdown("### 🔄 Transferable / Growth Strengths")
                        for item in result.skill_gaps_or_growth:
                            st.markdown(f"- {item}")

                    st.markdown("---")
                    st.markdown("### 🌟 Key Candidate Value Proposition")
                    for pt in result.value_proposition:
                        st.markdown(f"• {pt}")

                except Exception as e:
                    st.error(f"Inference error: {str(e)}")

# ==============================================================================
# TAB 2: SKILLS & COMPETENCY DASHBOARD
# ==============================================================================
elif nav_selection == "📊 Skills & Competency Dashboard":
    st.markdown('<div class="main-header">Skills & Competency Heatmap Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Interactive technical competency matrix with hot/cold rating heatmaps.</div>', unsafe_allow_html=True)

    df_skills = pd.DataFrame(PROFILE_DATA['skills_rated'])
    df_skills = df_skills.sort_values(by="rating", ascending=True)

    # Key Metrics Banner
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Top Platform Skill", "9.5 / 10", "Databricks & PySpark")
    m2.metric("AI / Agentic Frameworks", "9.0 / 10", "LLMs, RAG & N8N")
    m3.metric("Cloud Platforms", "8.5 / 10", "Azure Synapse & ADF")
    m4.metric("Industry Experience", "13.5 Years", "Data & AI Scale")

    st.markdown("---")

    col_chart1, col_chart2 = st.columns([1.6, 1])

    # Horizontal Heatmap Bar Chart
    with col_chart1:
        st.markdown("### 🔥 Technical Proficiency Ratings")
        
        fig_bar = px.bar(
            df_skills,
            x="rating",
            y="skill",
            orientation="h",
            text="rating",
            color="rating",
            color_continuous_scale=[
                (0.0, "#3B82F6"),   # Cool Blue
                (0.5, "#F59E0B"),   # Warm Gold
                (1.0, "#EF4444")    # Hot Red
            ],
            labels={"rating": "Score (/10)", "skill": "Skill"},
            range_x=[0, 10]
        )
        fig_bar.update_traces(
            texttemplate='%{text:.1f} / 10',
            textposition='inside',
            insidetextanchor='end',
            textfont=dict(color='white', size=12)
        )
        fig_bar.update_layout(
            height=520,
            margin=dict(l=10, r=20, t=10, b=10),
            coloraxis_showscale=False,
            xaxis=dict(showgrid=True, gridcolor='#E2E8F0'),
            yaxis=dict(showgrid=False)
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # Radar / Spider Chart
    with col_chart2:
        st.markdown("### 🕸️ Domain Core Radar")
        
        domain_avg = df_skills.groupby("category")["rating"].mean().reset_index()
        
        fig_radar = go.Figure(data=go.Scatterpolar(
            r=domain_avg['rating'],
            theta=domain_avg['category'],
            fill='toself',
            fillcolor='rgba(239, 68, 68, 0.25)',
            line=dict(color='#EF4444', width=2),
            marker=dict(size=6, color='#EF4444')
        ))
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 10], gridcolor='#E2E8F0')
            ),
            showlegend=False,
            height=480,
            margin=dict(l=30, r=30, t=30, b=30)
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    st.markdown("---")

    # Categorized Progress Bars
    st.markdown("### 🛠️ Detailed Skill Breakdown")
    categories = df_skills['category'].unique()

    cols = st.columns(len(categories))
    for idx, cat in enumerate(sorted(categories)):
        with cols[idx]:
            st.markdown(f"#### **{cat}**")
            cat_df = df_skills[df_skills['category'] == cat].sort_values(by="rating", ascending=False)
            for _, row in cat_df.iterrows():
                st.write(f"**{row['skill']}** — `{row['rating']}/10`")
                st.progress(row['rating'] / 10.0)

# ==============================================================================
# TAB 3: COMPLETE RESUME (FULL PROJECT SUMMARIES UNDER EACH COMPANY)
# ==============================================================================
elif nav_selection == "📜 Complete Resume":
    st.markdown(f'<div class="main-header">{PROFILE_DATA["name"]}</div>', unsafe_allow_html=True)
    st.markdown(f'**{PROFILE_DATA["title"]}**')
    st.markdown(f'📍 {PROFILE_DATA["contact"]["location"]} | 📞 {PROFILE_DATA["contact"]["phone"]} | 📧 {PROFILE_DATA["contact"]["email"]} | 🔗 [LinkedIn Profile]({PROFILE_DATA["contact"]["linkedin"]})')
    
    st.write(PROFILE_DATA['summary'])

    st.markdown("---")
    st.markdown("### 🏆 Awards & Major Accomplishments")
    for award in PROFILE_DATA['awards']:
        st.markdown(f"- {award}")

    st.markdown("---")
    st.markdown("### 💼 Experience & Projects")

    for exp in PROFILE_DATA['experience']:
        st.markdown(f'<div class="company-title">{exp["company"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="role-subtitle">{exp["role"]} | 🗓️ {exp["period"]}</div>', unsafe_allow_html=True)
        st.markdown(f"**Tech Stack:** `{exp['skills']}`")

        st.markdown("##### **Projects & Key Deliverables:**")
        for proj in exp['projects']:
            st.markdown(f'<div class="project-header">📌 {proj["title"]}</div>', unsafe_allow_html=True)
            for h in proj['highlights']:
                st.markdown(f"  - {h}")
        st.markdown("---")
