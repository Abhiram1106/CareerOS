"""Distinct resume personas for discrimination testing.

Each persona has:
  - ``text``: full plain-text resume (what ``analyze_ats`` and the matcher see)
  - ``sections``: structured sections matching what the parser would extract from
    the text — rich enough to exercise section-based scorers meaningfully.
  - ``label``: short human tag
  - ``tier``: coarse expected quality band ("strong" | "mid" | "weak")

Section content intentionally mirrors the full text slices so the two code
paths (text analyzer vs section heuristics) receive consistent, realistic input.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Persona:
    label: str
    tier: str
    text: str
    sections: list[dict]


def _sections(**named: str) -> list[dict]:
    return [
        {"section_name": name, "content_json": {"raw": raw}}
        for name, raw in named.items()
    ]


STRONG_FULLSTACK = Persona(
    label="strong_fullstack",
    tier="strong",
    text="""RAHUL SHARMA
rahul.sharma@gmail.com | +91 9876543210 | linkedin.com/in/rahulsharma | github.com/rahuls
Bengaluru, India

SUMMARY
Final-year CSE student focused on backend systems and distributed infrastructure.
Seeking SDE roles at product-first companies.

EDUCATION
B.Tech Computer Science, NIT Trichy, Aug 2021 - May 2025, CGPA 8.4/10

EXPERIENCE
Software Engineering Intern, Razorpay, Jun 2024 - Aug 2024
- Built a payment reconciliation service in Python and FastAPI, reducing manual effort by 60%
- Optimized SQL queries on PostgreSQL, cut p95 latency by 40%
- Deployed microservices on Docker and Kubernetes serving 2M requests/day
- Integrated Redis caching layer, improved API throughput by 35%

Teaching Assistant, NIT Trichy, Jan 2024 - May 2024
- Mentored 120 students in Data Structures and Algorithms
- Designed 15 coding problems used in semester exams
- Led weekly doubt sessions improving batch average by 12%

PROJECTS
Distributed Cache — Implemented an LRU cache in Go with Redis backing, handled 10k req/s.
Benchmarked against Memcached, achieved 20% lower p99 latency.

Churn ML Pipeline — Developed a churn prediction model using PyTorch and pandas, 87% accuracy.
Deployed on AWS Lambda with a FastAPI inference wrapper serving 500 req/min.

SKILLS
Python, FastAPI, SQL, PostgreSQL, Docker, Kubernetes, Go, PyTorch, pandas, React, TypeScript, Git, Redis, AWS
""",
    sections=_sections(
        header="rahul.sharma@gmail.com | +91 9876543210 | linkedin.com/in/rahulsharma | github.com/rahuls | Bengaluru",
        summary=(
            "Final-year CSE student focused on backend systems and distributed infrastructure. "
            "Seeking SDE roles at product-first companies."
        ),
        education="B.Tech Computer Science, NIT Trichy, Aug 2021 - May 2025, CGPA 8.4/10",
        experience=(
            "Software Engineering Intern, Razorpay, Jun 2024 - Aug 2024\n"
            "- Built a payment reconciliation service in Python and FastAPI, reducing manual effort by 60%\n"
            "- Optimized SQL queries on PostgreSQL, cut p95 latency by 40%\n"
            "- Deployed microservices on Docker and Kubernetes serving 2M requests/day\n"
            "- Integrated Redis caching layer, improved API throughput by 35%\n"
            "Teaching Assistant, NIT Trichy, Jan 2024 - May 2024\n"
            "- Mentored 120 students in Data Structures and Algorithms\n"
            "- Designed 15 coding problems used in semester exams\n"
            "- Led weekly doubt sessions improving batch average by 12%"
        ),
        projects=(
            "Distributed Cache — Implemented an LRU cache in Go with Redis backing, handled 10k req/s. "
            "Benchmarked against Memcached, achieved 20% lower p99 latency.\n"
            "Churn ML Pipeline — Developed a churn prediction model using PyTorch and pandas, 87% accuracy. "
            "Deployed on AWS Lambda with FastAPI inference wrapper serving 500 req/min."
        ),
        skills="Python, FastAPI, SQL, PostgreSQL, Docker, Kubernetes, Go, PyTorch, pandas, React, TypeScript, Git, Redis, AWS",
    ),
)

STRONG_DATA = Persona(
    label="strong_data",
    tier="strong",
    text="""PRIYA NAIR
priya.nair@outlook.com | +91 9123456780 | linkedin.com/in/priyanair | github.com/priyanair
Hyderabad, India

SUMMARY
Data-focused engineer with applied ML internships and competition wins.
Published 2 papers at inter-college AI symposium.

EDUCATION
B.Tech Information Technology, IIIT Hyderabad, May 2021 - May 2025, CGPA 9.1/10

EXPERIENCE
Machine Learning Intern, Swiggy, May 2024 - Jul 2024
- Engineered a demand-forecasting model in Python, improved forecast accuracy by 18%
- Automated feature pipelines with pandas and Airflow, reduced runtime by 3x
- Analyzed 50M order rows in SQL to surface delivery bottlenecks
- Reduced model retraining cost by 40% via incremental learning

Data Science Intern, Analytics Firm, Dec 2023 - Feb 2024
- Built customer segmentation pipeline with scikit-learn KMeans, 5 clusters
- Designed Tableau dashboards used by 12 business stakeholders
- Optimized ETL jobs cutting daily report latency by 25%

PROJECTS
Recommender System — Designed collaborative-filtering in TensorFlow, served 5k users, 0.89 NDCG.
NLP Classifier — Built a resume-section classifier with scikit-learn, 92% F1 on 10k samples.

ACHIEVEMENTS
Smart India Hackathon 2024 finalist — AI for Agriculture track.
Published paper on transfer learning at NIT AI Symposium 2024.

SKILLS
Python, TensorFlow, scikit-learn, pandas, numpy, SQL, Airflow, AWS, Git, Tableau, Keras
""",
    sections=_sections(
        header="priya.nair@outlook.com | +91 9123456780 | linkedin.com/in/priyanair | github.com/priyanair | Hyderabad",
        summary=(
            "Data-focused engineer with applied ML internships and competition wins. "
            "Published 2 papers at inter-college AI symposium."
        ),
        education="B.Tech Information Technology, IIIT Hyderabad, May 2021 - May 2025, CGPA 9.1/10",
        experience=(
            "Machine Learning Intern, Swiggy, May 2024 - Jul 2024\n"
            "- Engineered a demand-forecasting model in Python, improved forecast accuracy by 18%\n"
            "- Automated feature pipelines with pandas and Airflow, reduced runtime by 3x\n"
            "- Analyzed 50M order rows in SQL to surface delivery bottlenecks\n"
            "- Reduced model retraining cost by 40% via incremental learning\n"
            "Data Science Intern, Analytics Firm, Dec 2023 - Feb 2024\n"
            "- Built customer segmentation pipeline with scikit-learn KMeans, 5 clusters\n"
            "- Designed Tableau dashboards used by 12 business stakeholders\n"
            "- Optimized ETL jobs cutting daily report latency by 25%"
        ),
        projects=(
            "Recommender System — Designed collaborative-filtering in TensorFlow, served 5k users, 0.89 NDCG.\n"
            "NLP Classifier — Built a resume-section classifier with scikit-learn, 92% F1 on 10k samples."
        ),
        achievements=(
            "Smart India Hackathon 2024 finalist — AI for Agriculture track. "
            "Published paper on transfer learning at NIT AI Symposium 2024."
        ),
        skills="Python, TensorFlow, scikit-learn, pandas, numpy, SQL, Airflow, AWS, Git, Tableau, Keras",
    ),
)

MID_AVERAGE = Persona(
    label="mid_average",
    tier="mid",
    text="""ANITA RAO
anita.rao@gmail.com | +91 9988776655
Pune, India

EDUCATION
B.E. Computer Engineering, Pune University, Jun 2020 - May 2024, CGPA 7.2

EXPERIENCE
Web Development Intern, Local Startup, Jan 2023 - Jun 2023
- Worked on the company website using HTML and CSS
- Helped the team fix 10 bugs across 3 sprints
- Updated content pages for the marketing team

PROJECTS
College Portal — Made a student portal using Java and MySQL for 200 students.

SKILLS
Java, HTML, CSS, MySQL, C
""",
    sections=_sections(
        header="anita.rao@gmail.com | +91 9988776655 | Pune",
        education="B.E. Computer Engineering, Pune University, Jun 2020 - May 2024, CGPA 7.2",
        experience=(
            "Web Development Intern, Local Startup, Jan 2023 - Jun 2023\n"
            "- Worked on the company website using HTML and CSS\n"
            "- Helped the team fix 10 bugs across 3 sprints\n"
            "- Updated content pages for the marketing team"
        ),
        projects="College Portal — Made a student portal using Java and MySQL for 200 students.",
        skills="Java, HTML, CSS, MySQL, C",
    ),
)

MID_NOMETRICS = Persona(
    label="mid_nometrics",
    tier="mid",
    text="""KARTHIK V
karthik.v@gmail.com | +91 9001122334 | github.com/karthikv
Chennai

EDUCATION
B.Tech ECE, Anna University, Jun 2021 - May 2025

EXPERIENCE
Intern, TechServ Pvt Ltd, May 2024 - Jul 2024
- Developed internal tools using Python and Flask
- Created API documentation for the REST endpoints
- Implemented a few features for the admin dashboard
- Collaborated with frontend team on integration

PROJECTS
IoT Dashboard — Built a sensor dashboard with Flask and SQLite for monitoring 5 devices.

SKILLS
Python, Flask, SQLite, Git, Linux, REST API
""",
    sections=_sections(
        header="karthik.v@gmail.com | +91 9001122334 | github.com/karthikv | Chennai",
        education="B.Tech ECE, Anna University, Jun 2021 - May 2025",
        experience=(
            "Intern, TechServ Pvt Ltd, May 2024 - Jul 2024\n"
            "- Developed internal tools using Python and Flask\n"
            "- Created API documentation for the REST endpoints\n"
            "- Implemented a few features for the admin dashboard\n"
            "- Collaborated with frontend team on integration"
        ),
        projects="IoT Dashboard — Built a sensor dashboard with Flask and SQLite for monitoring 5 devices.",
        skills="Python, Flask, SQLite, Git, Linux, REST API",
    ),
)

WEAK_SPARSE = Persona(
    label="weak_sparse",
    tier="weak",
    text="""Amit
amit123@gmail.com
I did some coursework in python. Looking for a job. Studied computer science.
Know basics of programming and html.
""",
    sections=_sections(
        summary="I did some coursework in python. Looking for a job. Studied computer science.",
        skills="python, html",
    ),
)

WEAK_NOCONTACT = Persona(
    label="weak_nocontact",
    tier="weak",
    text="""Resume
Studied B.Sc. Did a project once. Interested in software.
Hobbies: cricket, music.
""",
    sections=_sections(
        summary="Studied B.Sc. Did a project once. Interested in software.",
    ),
)

WEAK_WALLOFTEXT = Persona(
    label="weak_walloftext",
    tier="weak",
    text=(
        "SOMEONE\nsomeone@mail.com\n"
        "I have good communication skills and am a team player. I am a quick learner. "
        "I have done many things in college and worked hard on assignments. "
        "I am self-motivated and eager to learn. I am passionate about technology. "
        "I am a hard working person who is dedicated and motivated. "
        "I have good communication skills and am eager to learn new things. " * 2
    ),
    sections=_sections(
        summary=(
            "I have good communication skills and am a team player. I am a quick learner. "
            "I have done many things in college and worked hard on assignments. "
            "I am self-motivated and eager to learn. I am passionate about technology. "
            "I am a hard working person who is dedicated and motivated."
        ),
    ),
)


ALL_PERSONAS: list[Persona] = [
    STRONG_FULLSTACK,
    STRONG_DATA,
    MID_AVERAGE,
    MID_NOMETRICS,
    WEAK_SPARSE,
    WEAK_NOCONTACT,
    WEAK_WALLOFTEXT,
]

SAMPLE_JD = """Software Engineer - Backend
We are hiring a backend software engineer to build scalable services.

Required Skills:
- Python
- SQL
- REST API
- Docker

Eligibility:
- Minimum CGPA 7.0
- No active backlogs
- Graduating 2025
"""
