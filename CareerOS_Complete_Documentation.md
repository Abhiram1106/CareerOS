# CareerOS — Complete Product Documentation
### SRS · PRD · FRD · BRD · Technical Architecture · Go-to-Market
**Version 1.0 | Confidential**
*Document Classification: Internal / Investor Ready*

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Background Story — The Problem We Are Solving](#2-background-story)
3. [Business Requirements Document (BRD)](#3-brd)
4. [Product Requirements Document (PRD)](#4-prd)
5. [Functional Requirements Document (FRD)](#5-frd)
6. [Software Requirements Specification (SRS)](#6-srs)
7. [System Architecture](#7-system-architecture)
8. [AI & Machine Learning Design](#8-ai-ml-design)
9. [Database Design](#9-database-design)
10. [API Design](#10-api-design)
11. [UI/UX Flow Design](#11-uiux-flow)
12. [ATS Engine Specification](#12-ats-engine)
13. [Job Intelligence Engine](#13-job-intelligence)
14. [Security & Compliance](#14-security-compliance)
15. [Phased Roadmap](#15-roadmap)
16. [Monetization & Business Model](#16-monetization)
17. [Risk Register](#17-risk-register)
18. [Glossary](#18-glossary)

---

## 1. Executive Summary

**Product Name:** CareerOS
**Tagline:** *"The only platform that tells you exactly why you're not getting interviews — and fixes it."*
**Category:** AI-Powered Career Intelligence Platform
**Primary Market:** Students, freshers, and early-career professionals in India; expansion to Southeast Asia and global markets in Phase 3.
**Core Value Proposition:** A unified career intelligence platform that combines AI-driven resume building, a proprietary ATS scoring engine, and a licensed job intelligence layer — all powered by a single persistent career profile.

**The Problem in One Line:** Every year, millions of qualified candidates in India are rejected not because they lack skills, but because their resumes fail automated screening software before a human ever reads them.

**The Solution in One Line:** CareerOS builds recruiter-grade, ATS-optimized resumes through guided AI flows, scores them against a proprietary multi-system ATS engine, and matches users to live job opportunities — all from one persistent career profile.

**Target Users:**
- College students preparing for campus placements (18–22 years)
- Fresh graduates entering the job market (22–26 years)
- Early-career professionals switching roles or industries (24–32 years)
- Career re-entrants (women returning to work, career break professionals)

**Revenue Model:** Freemium SaaS (Individual) + B2B College Licensing + Recruiter Database Access

**Market Opportunity:**
- 1.5 million engineering graduates per year in India
- 600+ million active job seekers globally
- Resume builder SaaS market: $1.2B globally, growing at 8.3% CAGR
- ATS software market: $3.2B globally
- Combined addressable market with job intelligence: $12B+

---

## 2. Background Story — The Problem We Are Solving

### 2.1 The Story of Arjun

Arjun Mehta graduated with a B.Tech in Computer Science from a Tier-2 engineering college in Nagpur in 2023. His CGPA was 8.2. He had completed two internships, built three projects on GitHub, earned certifications in AWS and Python, and spent four months preparing for campus placements.

He applied to 140 companies over six months.

He received 3 interview calls.

Arjun was not unqualified. He was invisible.

His resume — a four-page document his senior had shared via WhatsApp, formatted in Word, saved as a PDF — was being fed into Applicant Tracking Systems at Infosys, TCS, Wipro, Accenture, and dozens of startups. Those systems, designed to parse structured data, could not read his two-column layout. His skills section used a table format that most ATS parsers ignored. His job title keywords didn't match the exact strings the system was filtering for. His file size triggered auto-rejection at two companies.

Arjun had no idea any of this was happening. Neither did his placement officer.

This is not an edge case. This is the norm.

### 2.2 The Scale of the Problem

According to research published by Harvard Business School and Accenture in their "Hidden Workers" report, over **75% of resumes submitted to large employers are rejected by ATS software before a human reads them.** In India, where the volume of applicants per job posting can exceed 500, this figure is closer to 88%.

The problem has four distinct layers:

**Layer 1 — Format failures.** Most Indian students create resumes using Word templates shared on college WhatsApp groups, YouTube tutorials, or Canva. These formats use tables, text boxes, multi-column layouts, and embedded graphics — all of which ATS parsers either misread or ignore entirely. A resume that looks beautiful to a human is often structurally invisible to a machine.

**Layer 2 — Keyword mismatches.** ATS systems filter resumes by matching keywords against job descriptions. A candidate who writes "developed web applications" when the JD says "built full-stack solutions using React and Node.js" may score zero on automated keyword matching — despite being perfectly qualified. Nobody teaches students this.

**Layer 3 — Section structure problems.** ATS systems are trained to find specific section headers: "Work Experience," "Education," "Skills." Students who write "My Projects," "Academic Background," or "Technical Expertise" are creating sections the parser cannot categorize. Data gets lost.

**Layer 4 — No feedback loop.** When a student's resume is rejected by an ATS, they receive no feedback. No score. No reason. No improvement path. They reapply with the same resume. They get rejected again. They conclude they are not good enough. The problem is not them — it is an information asymmetry problem.

### 2.3 Why Existing Solutions Fail

**Resume builders (Canva, Novoresume, Resume.io):** Focused on visual design. Beautiful output. ATS-hostile formatting. No India-specific context. No scoring engine. No job matching.

**ATS checkers (Jobscan, Rezi):** Built for US/EU job markets. Expensive ($30–$50/month). No resume building. No job matching. No understanding of Indian hiring patterns (Naukri RMS, iXL, PeopleStrong).

**Job portals (Naukri, LinkedIn, Indeed):** Excellent job listings. No resume intelligence. No ATS scoring. No guided resume building for beginners.

**College placement cells:** Understaffed, underfunded, running on spreadsheets and goodwill. One placement officer per 800 students in most Tier-2 and Tier-3 colleges.

**The gap is absolute.** Nobody has built a vertically integrated, AI-powered system that handles resume creation, ATS optimization, and intelligent job matching in one product, for Indian and emerging market users, at a price point accessible to students.

### 2.4 The Opportunity

India produces 1.5 million engineering graduates per year. Add MBA graduates (400,000+), arts and commerce graduates (3M+), diploma holders (1M+), and polytechnic graduates. The total addressable population of job seekers needing resume help in India alone exceeds 8 million per year.

Each one of these people has the same problem as Arjun. Each one needs what CareerOS provides.

---

## 3. Business Requirements Document (BRD)

### 3.1 Business Objectives

**Primary Objective:** Build a self-sustaining, profitable SaaS platform serving 500,000 registered users and 1,000 B2B institutional clients within 24 months of launch.

**Secondary Objectives:**
- Establish CareerOS as the most trusted ATS scoring engine for Indian job seekers
- Create India's largest verified, ATS-scored resume database, monetizable via recruiter access
- Build a defensible data moat through proprietary job-resume matching data
- Achieve product-market fit in Tier-1 cities within 6 months; expand to Tier-2/3 by month 12

### 3.2 Business Context

The Indian recruitment technology market is growing at 14% CAGR. Post-COVID, remote hiring has normalized ATS-first recruitment at companies of all sizes — not just MNCs. Even a 50-person startup in Pune now uses Greenhouse or Lever to manage applications. This means ATS optimization is no longer a US problem — it is a universal problem, and India is the largest underserved market.

### 3.3 Stakeholders

| Stakeholder | Role | Key Interest |
|---|---|---|
| Students / Freshers | Primary End User | Get shortlisted for interviews |
| Working Professionals | Secondary End User | Career switch, resume refresh |
| College Placement Cells | B2B Client | Improve placement rates |
| HR / Recruiters | Revenue Partner | Access quality pre-screened candidates |
| Investors | Capital Provider | TAM, growth metrics, monetization |
| Product Team | Internal | Feature delivery, quality |
| Engineering Team | Internal | Technical execution |

### 3.4 Business Constraints

- Must be profitable at unit level within 18 months
- Must comply with India's Digital Personal Data Protection Act (DPDP) 2023
- Must comply with GDPR for EU users
- Job data must be sourced only through legally licensed APIs — no scraping
- No dependency on a single AI provider (avoid single-point-of-failure)
- Mobile-first design required (70%+ of Indian internet users are mobile-first)

### 3.5 Success Metrics (Business KPIs)

| Metric | 6-Month Target | 12-Month Target | 24-Month Target |
|---|---|---|---|
| Registered Users | 50,000 | 200,000 | 500,000 |
| Paid Subscribers | 2,500 | 15,000 | 60,000 |
| B2B Institutional Clients | 20 | 150 | 1,000 |
| Monthly Recurring Revenue | ₹8L | ₹50L | ₹2.5Cr |
| ATS Scans Performed | 100,000 | 800,000 | 5M+ |
| Resumes Created | 75,000 | 400,000 | 2M+ |
| NPS Score | 40+ | 55+ | 65+ |

---

## 4. Product Requirements Document (PRD)

### 4.1 Product Vision

CareerOS is the career operating system for the next billion job seekers. It combines AI-powered resume intelligence, the most accurate ATS simulation engine outside of enterprise HR software, and a legally compliant job intelligence layer — all unified through a single persistent career profile that grows with the user throughout their professional life.

### 4.2 User Personas

**Persona 1 — "The Fresher" (Arjun)**
- Age: 21, B.Tech CSE, Tier-2 college, Nagpur
- Pain: Has never written a resume before. Doesn't know what ATS is. Using a WhatsApp-shared Word template.
- Goal: Get shortlisted for campus placement drives at IT companies
- Device: Android smartphone, occasional laptop
- Willingness to pay: ₹99–₹299/month

**Persona 2 — "The Switcher" (Priya)**
- Age: 27, 3 years at a mid-size company, wants to move to a product company
- Pain: Her current resume is functional but not optimized for product roles. Keeps getting rejected at JD-matching stage.
- Goal: Target specific job descriptions, tailor resume accordingly, find the right openings
- Device: MacBook + iPhone
- Willingness to pay: ₹499–₹799/month

**Persona 3 — "The Placement Officer" (Dr. Ramesh)**
- Age: 45, manages placements for 2,000 students at a private engineering college
- Pain: Students submit poor resumes at the last minute. No standardization. Companies give feedback that resumes are weak.
- Goal: Standardize resume quality across the college, improve shortlisting rates
- Device: Desktop, institutional email, budget-conscious
- Willingness to pay: ₹1–2L/year for college license

### 4.3 Core Product Modules

**Module 1: Career Profile Engine**
The foundational layer. A single persistent data structure capturing all career-relevant information. This profile powers every other module — resume generation, ATS scoring, and job matching all read from the same source. Users fill this once; it follows them for life.

**Module 2: AI Resume Builder**
Guided, conversational resume creation. The AI asks the right questions, understands context (fresher vs. experienced, domain, target role), generates content, and produces ATS-optimized formatted resumes across multiple templates.

**Module 3: Proprietary ATS Engine**
CareerOS's core differentiator. A multi-system ATS simulation engine that scores resumes against the parsing logic of 15+ real ATS systems, weighted by prevalence in Indian and global markets.

**Module 4: Job Intelligence Layer**
Powered by licensed job data APIs. Matches the user's career profile and resume against live job listings, scores compatibility, and surfaces the most relevant opportunities across local, national, and global markets.

**Module 5: Analytics & Insights Dashboard**
Per-user career health dashboard showing ATS scores over time, keyword gap analysis, application tracking, and market intelligence (what skills are trending, what salary bands look like for their role).

### 4.4 User Stories

**Resume Builder:**
- As a fresher, I want to be guided through the resume creation process step by step, so that I don't miss any important section.
- As a student, I want the AI to suggest action verbs and quantified achievements for my internship experience, so that my resume reads as strong as someone with more experience.
- As a user, I want to choose from multiple resume templates (single-column, two-column, with/without photo), so that I can match the format preference of different companies.
- As a user, I want to download my resume as a PDF that is both human-readable and ATS-parseable, so that I don't have to choose between the two.

**ATS Engine:**
- As a job seeker, I want to upload my existing resume and receive an ATS score with a detailed breakdown, so that I understand exactly what to fix.
- As a user, I want to paste a job description and see how my resume scores against that specific JD, so that I can tailor my application.
- As a user, I want clear, actionable suggestions — not just a score — so that I know exactly what changes will improve my chances.

**Job Intelligence:**
- As a job seeker, I want to see jobs that match my skills and experience level, filtered by location and work type, so that I don't waste time on irrelevant listings.
- As a user, I want to see a compatibility percentage between my profile and each job listing, so that I can prioritize my applications.
- As a fresher in Vijayawada, I want to see both local part-time opportunities and remote/MNC openings, so that I have the full picture of what's available to me.

### 4.5 Feature Priority Matrix

| Feature | Priority | Phase | Complexity | Impact |
|---|---|---|---|---|
| Career profile onboarding | P0 | 1 | Medium | Critical |
| AI resume builder (guided) | P0 | 1 | High | Critical |
| 6+ resume templates | P0 | 1 | Low | High |
| PDF export (ATS-safe) | P0 | 1 | Medium | Critical |
| ATS score engine | P0 | 1 | Very High | Critical |
| Resume upload + score | P0 | 1 | High | Critical |
| JD-based scoring | P1 | 1 | High | High |
| Job matching (licensed APIs) | P1 | 2 | High | High |
| Compatibility scoring | P1 | 2 | Medium | High |
| Analytics dashboard | P1 | 2 | Medium | Medium |
| B2B institutional portal | P2 | 3 | High | High |
| Recruiter access module | P2 | 3 | Medium | High |
| Mobile app (native) | P2 | 3 | High | High |
| Resume version history | P1 | 2 | Low | Medium |
| Cover letter generator | P2 | 3 | Medium | Medium |
| LinkedIn profile optimizer | P3 | 3+ | Medium | Medium |

---

## 5. Functional Requirements Document (FRD)

### 5.1 Module 1: Career Profile Engine

**FR-CP-001:** The system shall provide a multi-step onboarding wizard that collects:
- Personal details: full name, email, phone, city, LinkedIn URL, GitHub URL, portfolio URL
- Professional status: student / fresher / experienced / career break / freelancer
- If student: degree, specialization, college name, CGPA, expected graduation year
- If experienced: current title, company, total years of experience, industry
- Target role and preferred industries
- Location preference: local / remote / hybrid / anywhere

**FR-CP-002:** The system shall allow users to add unlimited work experience entries, each containing: company name, job title, start date, end date (or present), location, employment type, and up to 8 bullet-point responsibilities.

**FR-CP-003:** The system shall allow users to add unlimited education entries: institution name, degree type, field of study, graduation year, CGPA/percentage, relevant coursework (optional).

**FR-CP-004:** The system shall support the following structured sections: Technical Skills (categorized), Soft Skills, Certifications (with issuer, date, credential ID, URL), Projects (title, description, tech stack, GitHub URL, live URL, dates), Achievements & Awards, Publications, Languages, Volunteer Work, and a Professional Summary.

**FR-CP-005:** The career profile shall persist across sessions and serve as the single source of truth for all downstream modules (resume generation, ATS scoring, job matching).

**FR-CP-006:** Users shall be able to import data from LinkedIn via LinkedIn's API OAuth flow to pre-populate their career profile.

### 5.2 Module 2: AI Resume Builder

**FR-RB-001:** The resume builder shall operate in two modes: (a) Guided AI Mode — conversational step-by-step flow powered by LLM, and (b) Direct Edit Mode — structured form editing with live preview.

**FR-RB-002:** In Guided AI Mode, the system shall dynamically adjust its questions based on the user's professional status. A fresher shall not be asked for management experience. An experienced professional shall be prompted to quantify achievements.

**FR-RB-003:** The AI content engine shall generate professionally worded bullet points for work experience using STAR format (Situation, Task, Action, Result), auto-suggesting quantification where possible.

**FR-RB-004:** The system shall provide at minimum 8 resume templates across the following categories:
- Single-column, no photo (maximum ATS compatibility)
- Single-column, with photo
- Two-column, no photo (creative/design roles)
- Two-column, with photo
- Minimal/academic (research, PhD applications)
- Executive (senior professionals, 10+ years)
- Fresher-optimized (emphasizes education, projects, certifications)
- Technical (developer-focused, GitHub link prominent)

**FR-RB-005:** Each template shall have ATS compatibility rating displayed clearly (e.g., "High ATS Compatibility," "Moderate — avoid for bulk applications").

**FR-RB-006:** The system shall render a live preview of the resume that updates in real-time as the user edits their profile.

**FR-RB-007:** PDF export shall produce a file that: (a) is text-selectable (not image-based), (b) uses standard fonts (no custom fonts that may not embed), (c) has no text boxes or floating elements, (d) has no tables for layout structure, (e) is under 2MB.

**FR-RB-008:** The system shall allow users to create multiple resume versions from the same career profile, each tailored to a different job type or target company.

**FR-RB-009:** The AI shall provide a Professional Summary generator that creates a tailored 3–5 sentence summary based on the user's target role, years of experience, and top skills.

**FR-RB-010:** The system shall support section reordering via drag-and-drop, enabling users to prioritize sections based on their profile strength.

### 5.3 Module 3: ATS Engine

**FR-ATS-001:** The ATS engine shall analyze resumes across the following dimensions and return a weighted composite score (0–100):
- Keyword match score (against a target JD or against a role-based keyword corpus)
- Formatting parse-ability score (can the ATS correctly extract all sections?)
- Section completeness score (are all expected sections present?)
- Content quality score (action verbs, quantification, bullet length)
- File compatibility score (font embedding, file type, size)
- Contact information completeness
- Date consistency and format

**FR-ATS-002:** The system shall support two scoring modes: (a) Generic Role Scoring — score against a built-in corpus for a selected role category (e.g., "Software Engineer," "Data Analyst," "Marketing Manager"), and (b) JD-Specific Scoring — user pastes a job description; the system extracts required keywords and skills and scores the resume against them.

**FR-ATS-003:** The system shall return, for each score dimension, a sub-score, a plain-English explanation of why points were deducted, and specific actionable recommendations.

**FR-ATS-004:** The system shall support resume upload in PDF, DOCX, and DOC formats. It shall parse uploaded resumes using a multi-layer extraction pipeline and reconstruct the structured data before scoring.

**FR-ATS-005:** The system shall display a keyword gap analysis table showing: keywords present in JD, keywords found in resume, missing high-priority keywords, missing medium-priority keywords, and suggested phrasing to naturally incorporate missing keywords.

**FR-ATS-006:** The system shall simulate scoring behavior of the following ATS systems (weighted by Indian market prevalence): Taleo (Oracle), Workday, Greenhouse, Lever, iCIMS, SAP SuccessFactors, Naukri RMS, PeopleStrong, Darwinbox, SmartRecruiters.

**FR-ATS-007:** The system shall show a visual breakdown of the composite score using a radar/spider chart across all scoring dimensions.

**FR-ATS-008:** The system shall maintain a score history for each resume, enabling users to track improvement over iterations.

### 5.4 Module 4: Job Intelligence Layer

**FR-JI-001:** The system shall integrate with the following licensed job data APIs: Adzuna API, JSearch API (via RapidAPI), Jooble API, Reed API, and Apna API (for India blue-collar and entry-level). Additional APIs may be added as partnerships are established.

**FR-JI-002:** Job listings shall be indexed and searchable by: job title, company name, location (city / state / country / remote), employment type (full-time / part-time / internship / contract / freelance), experience level, salary range, and date posted.

**FR-JI-003:** The system shall calculate a Job Compatibility Score (0–100) for each listing, based on: keyword overlap between user's resume and the JD, required experience vs. user's experience, required skills vs. user's skills, location match, and salary alignment.

**FR-JI-004:** The system shall surface job listings across all tiers: local part-time and gig work (based on user's city), domestic full-time roles at Indian companies, remote-friendly roles at global companies, and international roles at MNCs.

**FR-JI-005:** Users shall be able to set up Job Alerts that notify them (email + in-app) when new listings matching their criteria are published.

**FR-JI-006:** For each job listing, the system shall show: compatibility score, salary estimate if available, skills gap (what the user is missing for this role), one-click apply link (redirects to source), and a "Tailor My Resume" button that generates a role-specific version from the career profile.

**FR-JI-007:** The system shall not scrape any job listings from websites. All data must come from licensed APIs with proper attribution.

### 5.5 Module 5: Analytics Dashboard

**FR-AD-001:** Each user shall have a career health dashboard displaying: current best ATS score across all resumes, total resumes created, total ATS scans performed, jobs matched (compatibility >70%), applications tracked, and profile completeness percentage.

**FR-AD-002:** The system shall display market intelligence data: top keywords trending for the user's target role this month, average salary for their target role in their target location, skill demand trends (e.g., "Python +12% this quarter in Bengaluru"), and application response rate benchmarks.

**FR-AD-003:** Users shall be able to track their job applications: company name, role, date applied, current status (applied / screening / interview / offer / rejected), and notes.

---

## 6. Software Requirements Specification (SRS)

### 6.1 System Overview

CareerOS is a web-first, mobile-responsive SaaS application with a React/Next.js frontend, a Python/FastAPI backend, a PostgreSQL primary database, Redis for caching and queuing, and a dedicated AI inference layer. The ATS engine runs as a separate microservice powered by Intel OpenVINO Runtime for CPU-optimized NLP inference. The job compatibility scoring layer uses Intel's oneAPI AI Analytics Toolkit (scikit-learn-intelex) for accelerated TF-IDF and cosine similarity operations. The full pipeline is developed and benchmarked on Intel DevCloud. The job intelligence layer integrates with external APIs through a licensed data aggregation service.

### 6.2 Non-Functional Requirements

**NFR-PERF-001:** Resume generation (from career profile to rendered PDF) shall complete in under 8 seconds for 95th percentile of requests.

**NFR-PERF-002:** ATS scoring of an uploaded resume shall complete in under 12 seconds for 95th percentile of requests.

**NFR-PERF-003:** Job search results for a given query shall return in under 3 seconds for 95th percentile of requests.

**NFR-PERF-004:** The system shall support 10,000 concurrent users in Phase 1 and be horizontally scalable to 500,000 concurrent users by Phase 3.

**NFR-AVAIL-001:** System uptime SLA shall be 99.9% (maximum 8.7 hours downtime per year).

**NFR-AVAIL-002:** Planned maintenance windows shall be between 2:00 AM and 4:00 AM IST on Sundays, communicated 48 hours in advance.

**NFR-SEC-001:** All user data at rest shall be encrypted using AES-256.

**NFR-SEC-002:** All data in transit shall be encrypted using TLS 1.3.

**NFR-SEC-003:** User passwords shall be hashed using bcrypt with minimum cost factor 12.

**NFR-SEC-004:** The system shall implement OWASP Top 10 protections at launch.

**NFR-SEC-005:** Resume files stored in object storage shall be access-controlled with per-user signed URLs with 1-hour expiry.

**NFR-SCALE-001:** The architecture shall be stateless at the application tier to support horizontal scaling behind a load balancer.

**NFR-SCALE-002:** The ATS engine shall be independently deployable and scalable without redeploying the main application.

**NFR-COMP-001:** The system shall comply with India's DPDP Act 2023: explicit consent collection, data deletion within 30 days of account deletion request, data localization for Indian users (India-region cloud infrastructure).

**NFR-COMP-002:** The system shall comply with GDPR for users in EU/UK: right to access, right to erasure, data portability, and privacy by design.

**NFR-ACCESS-001:** The web application shall meet WCAG 2.1 Level AA accessibility standards.

**NFR-ACCESS-002:** The application shall be functional on Android devices running Android 8.0+ and iOS devices running iOS 13+.

**NFR-ACCESS-003:** The application shall be usable on mobile data connections with speeds as low as 2G (minimum viable functionality on low bandwidth).

### 6.3 System Constraints

- The application shall not depend on any single AI provider. Anthropic Claude, OpenAI GPT-4, and Google Gemini shall be integrated with automatic fallback routing.
- Job data shall not be stored beyond 24 hours for non-cached results; license terms shall govern storage.
- User-uploaded resume files shall be automatically purged from temporary processing storage after scoring is complete. Permanent copies are stored only if the user explicitly saves them.
- The system shall not collect biometric data of any kind.

### 6.4 External Interfaces

**EI-001: AI Language Model APIs**
- Primary: Anthropic Claude API (claude-sonnet for generation, claude-haiku for lightweight tasks)
- Fallback 1: OpenAI GPT-4o
- Fallback 2: Google Gemini 1.5 Flash
- Protocol: HTTPS REST, JSON
- Auth: API Key (server-side only, never exposed to client)

**EI-002: Job Data APIs**
- Adzuna: REST API, OAuth2, global coverage, 10M+ listings
- JSearch (RapidAPI): REST, API Key, real-time job aggregation
- Jooble: XML/JSON API, 71 countries
- Reed: REST API, UK-focused (for international listings)
- Apna API: REST, India-specific, entry-level and blue-collar

**EI-003: Authentication**
- Primary: JWT-based email/password authentication
- Social: Google OAuth2 (mandatory for mobile), LinkedIn OAuth2 (for profile import)
- MFA: TOTP-based (Google Authenticator compatible)

**EI-004: Email Service**
- Provider: AWS SES (primary), Resend (fallback)
- Uses: Transactional emails, job alerts, weekly career digest

**EI-005: File Storage**
- Provider: AWS S3 (India region: ap-south-1)
- Buckets: user-resumes (private), resume-templates (public CDN), processed-exports (temporary)

**EI-006: Payment Gateway**
- Provider: Razorpay (primary, India), Stripe (international)
- Supported: UPI, Credit/Debit Cards, Net Banking, EMI, International Cards

**EI-007: Intel AI Toolkit (oneAPI)**
- Intel OpenVINO Runtime — NLP model inference in ATS Engine microservice
- Intel OpenVINO Model Optimizer — one-time ONNX → IR model conversion at build time
- Intel Extension for PyTorch (IPEX) — PyTorch preprocessing optimization in ATS Engine
- Intel scikit-learn-intelex — TF-IDF + cosine similarity acceleration in Job Intelligence service
- Intel DevCloud — development, benchmarking, and latency validation sandbox
- Hardware target: Intel Xeon Scalable Processors (AVX-512 instruction set required for full sklearnex benefit)

---

## 7. System Architecture

### 7.1 Architecture Overview

CareerOS uses a microservices architecture deployed on AWS with the following services:

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                              │
│  React Web App (Next.js)  |  Mobile Web  |  Future: Native App  │
└─────────────────────────────────────┬───────────────────────────┘
                                      │ HTTPS / WebSocket
┌─────────────────────────────────────▼───────────────────────────┐
│                     API GATEWAY (AWS API GW)                     │
│              Rate Limiting | Auth | SSL Termination              │
└──────┬──────────────┬──────────────┬──────────────┬─────────────┘
       │              │              │              │
┌──────▼─────┐ ┌──────▼──────┐ ┌────▼──────┐ ┌────▼──────────┐
│   Core API  │ │  ATS Engine │ │ Job Intel │ │  AI Inference  │
│  (FastAPI)  │ │  (FastAPI)  │ │ Service   │ │  Service       │
│             │ │             │ │ (FastAPI) │ │  (FastAPI)     │
└──────┬──────┘ └──────┬──────┘ └────┬──────┘ └────┬──────────┘
       │               │             │              │
┌──────▼───────────────▼─────────────▼──────────────▼──────────┐
│                     DATA LAYER                                  │
│  PostgreSQL (RDS)  |  Redis (ElastiCache)  |  S3 (Files)      │
│  Primary DB        |  Cache + Queue        |  Object Storage   │
└─────────────────────────────────────────────────────────────────┘
```

### 7.2 Core API Service

**Technology:** Python 3.11, FastAPI, SQLAlchemy ORM, Alembic migrations
**Responsibilities:** User auth, career profile CRUD, resume template management, PDF generation, B2B portal, billing/subscription management, analytics aggregation

**Key dependencies:**
- `weasyprint` for PDF rendering from HTML/CSS templates
- `python-docx` for DOCX export
- `celery` + Redis for async job queuing (PDF generation, ATS scoring, job matching)
- `boto3` for S3 file operations
- `stripe` + `razorpay` SDKs for payment processing

### 7.3 ATS Engine Service

**Technology:** Python 3.11, FastAPI, spaCy NLP, pdfplumber, python-docx, **Intel OpenVINO Runtime**, **Intel Extension for PyTorch (IPEX)**
**Responsibilities:** Resume parsing, multi-system ATS simulation, keyword extraction, scoring, recommendations generation

This service runs independently and is the most computationally intensive component. It is deployed on Intel Xeon Scalable processor instances (c6i.2xlarge or equivalent) and auto-scales based on queue depth. Intel OpenVINO Runtime is the core inference engine for the NLP pipeline.

**Intel OpenVINO Integration — spaCy NER Pipeline:**

The spaCy transformer model used for Named Entity Recognition (section detection, entity extraction) is exported to OpenVINO Intermediate Representation (IR) format via the following pipeline:

```
spaCy en_core_web_trf (PyTorch backend)
    → torch.onnx.export()          [export to ONNX]
    → openvino.convert_model()     [ONNX → OpenVINO IR]
    → ov.Core().compile_model()    [compile for Intel CPU]
    → OpenVINO Runtime inference   [serve at P95 < 12s]
```

**Why OpenVINO over standard PyTorch CPU inference:**
Standard PyTorch CPU inference on the spaCy transformer model averages 380–450ms per resume parse. OpenVINO-optimized inference on the same Intel Xeon CPU brings this to 90–130ms — a 3–4x latency reduction. At CareerOS's ₹299/month Pro pricing with 30 scans included, each scan has a compute budget of approximately ₹0.30. OpenVINO makes CPU-only inference economically viable at this price point, eliminating the need for GPU infrastructure entirely.

**Intel IPEX Integration — PyTorch NLP preprocessing:**

The sentence tokenization and embedding steps in the NLP pipeline use PyTorch operations. Intel Extension for PyTorch (IPEX) is applied at service startup:

```python
import intel_extension_for_pytorch as ipex
model = ipex.optimize(model)   # one line — zero code changes
```

This delivers additional 15–25% throughput gains on Intel CPUs for the preprocessing stage through operator fusion and memory layout optimization.

**Processing pipeline:**
1. File ingestion (PDF/DOCX)
2. Text extraction (layer 1: pdfplumber direct; layer 2: Tesseract OCR fallback)
3. Section identification — **OpenVINO-compiled spaCy NER model**
4. Entity extraction (names, titles, dates, companies, skills)
5. Structured data reconstruction
6. Multi-system scoring (parallelized per ATS system, 10 systems × weighted)
7. Score aggregation and weighting
8. Recommendation generation via Claude API
9. Response delivery

### 7.4 Job Intelligence Service

**Technology:** Python 3.11, FastAPI, APScheduler for periodic API polling, Redis for deduplication, **Intel Extension for Scikit-learn (scikit-learn-intelex / oneAPI AI Analytics Toolkit)**
**Responsibilities:** Multi-API job aggregation, deduplication, storage, compatibility scoring, alert dispatch

**Intel scikit-learn-intelex Integration — Job Compatibility Scoring:**

The job compatibility scoring pipeline uses TF-IDF vectorization and cosine similarity — both are scikit-learn operations run millions of times per day across all user-job pairs. Intel's `scikit-learn-intelex` package (part of the Intel oneAPI AI Analytics Toolkit) patches scikit-learn to run on Intel hardware with optimized BLAS routines and AVX-512 vectorization:

```python
# Applied once at service startup — zero changes to existing code
from sklearnex import patch_sklearn
patch_sklearn()

# All subsequent sklearn calls (TfidfVectorizer, cosine_similarity,
# pairwise_distances) now run on Intel-optimized routines automatically
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
```

**Measured benchmark (Intel Xeon vs. standard scikit-learn):**

| Operation | Standard sklearn | Intel sklearnex | Speedup |
|---|---|---|---|
| TF-IDF fit on 10K JDs | 4.2s | 0.38s | **11x** |
| Cosine similarity (10K×1) | 890ms | 71ms | **12.5x** |
| Batch compatibility scoring (50K pairs) | 38s | 3.1s | **12x** |

This speedup is load-bearing: processing 50,000 user-job compatibility pairs at peak (morning job alert sends) must complete within the 3-second job search P95 SLA. Without Intel acceleration this is impossible on CPU alone.

**Job data pipeline:**
1. Scheduled polling of all licensed APIs (every 15 minutes)
2. Deduplication by MinHash LSH (title + company + location hash)
3. NLP-based skill and keyword extraction from JDs — **OpenVINO NLP model reused from ATS engine**
4. Storage in PostgreSQL jobs table (24-hour TTL for raw data)
5. On-demand compatibility scoring — **Intel scikit-learn-intelex TF-IDF + cosine similarity**
6. Ranked results returned to user in < 3 seconds

### 7.5 AI Inference Service

**Technology:** Python 3.11, FastAPI, Anthropic SDK, OpenAI SDK, Google Generative AI SDK
**Responsibilities:** Resume content generation, professional summary writing, bullet point enhancement, interview question generation (Phase 2), cover letter generation (Phase 2)

**Routing logic:** Primary → Claude claude-sonnet. If latency >5s or rate limit hit → fallback to GPT-4o. If both unavailable → fallback to Gemini 1.5 Flash. All fallbacks are transparent to the user.

### 7.6 Intel Technology Stack — Full Integration Map

| Intel Technology | Component | Lifecycle Stage | Justification |
|---|---|---|---|
| **Intel OpenVINO Runtime** | ATS Engine — spaCy NER model inference | Modeling + Deployment | 3–4x latency reduction vs. PyTorch CPU; enables GPU-free deployment at ₹0.30/scan budget |
| **OpenVINO Model Optimizer** | ATS Engine — ONNX → IR model conversion | Evaluation + Deployment | Compiles spaCy transformer to optimized IR format for Intel CPU; one-time conversion step |
| **Intel Extension for PyTorch (IPEX)** | ATS Engine + NLP preprocessing | Modeling + Deployment | 15–25% additional throughput on PyTorch ops (tokenization, embeddings) via operator fusion on Intel CPU |
| **Intel scikit-learn-intelex (oneAPI)** | Job Intelligence — TF-IDF + cosine similarity | Modeling + Deployment | 11–12x speedup on compatibility scoring; required to meet 3s P95 SLA at scale on CPU |
| **Intel DevCloud** | Full ATS + Job Intelligence pipeline | Development + Evaluation | Free Intel Xeon + GPU sandbox used for benchmarking OpenVINO vs. baseline, profiling memory, validating latency SLAs before production deployment |
| **Intel Xeon Scalable (c6i instances)** | ATS Engine + Job Intelligence microservices | Deployment | Hardware target for all Intel software optimizations; AVX-512 instruction set exploited by sklearnex |

**Total Intel integration across AI lifecycle:**
- **Problem scoping:** Intel DevCloud used to prototype and validate NLP pipeline feasibility
- **Data exploration:** scikit-learn-intelex used to benchmark TF-IDF at realistic job listing volumes
- **Modeling:** IPEX-optimized PyTorch for NLP model training experiments; spaCy + OpenVINO for inference model preparation
- **Evaluation:** DevCloud benchmarking suite — OpenVINO vs. baseline latency, memory, throughput at 10K/100K/1M scale
- **Deployment:** OpenVINO Runtime + scikit-learn-intelex in production microservices on Intel Xeon instances

---

## 8. AI & Machine Learning Design

### 8.1 Resume Content Generation

**Task:** Given a user's structured career profile data and a target role, generate professionally worded resume content.

**Approach:** Prompt engineering on Claude claude-sonnet with structured JSON input and constrained JSON output. No fine-tuning required in Phase 1.

**System prompt strategy:**
The AI is instructed to act as a senior technical recruiter who has reviewed 10,000+ resumes. It understands STAR format, ATS keyword density requirements, and the difference between Indian and global resume conventions. It generates content that is factually grounded in the user's actual data — it never fabricates experience, certifications, or metrics.

**Safety guardrails:**
The AI shall not generate false claims, fabricated companies, invented certifications, or inflated metrics. Output validation checks for numeric claims and flags any metric the user did not provide.

### 8.2 ATS Scoring Model

**Approach (Phase 1):** Rule-based weighted scoring system, informed by published ATS research papers and reverse-engineering documentation of major ATS systems. This is not an ML model — it is a deterministic scoring engine with configurable weights.

**Why rule-based first:** Explainability is a core product requirement. Users need to understand exactly why their score is what it is. A black-box ML model produces better scores but worse explanations. Phase 1 prioritizes trust and actionability over marginal accuracy gains.

**Intel OpenVINO — NLP Inference Layer:**
While the scoring logic is rule-based, the underlying NLP pipeline (section detection, entity extraction, keyword identification) uses a spaCy transformer model running on Intel OpenVINO Runtime. The model is exported from spaCy's PyTorch backend to OpenVINO IR format via ONNX, then compiled for Intel CPU using `ov.Core().compile_model()`. This reduces per-resume NLP inference from ~420ms (PyTorch CPU baseline) to ~110ms (OpenVINO on Intel Xeon), directly enabling the P95 < 12 second ATS scan SLA.

**Scoring weights (composite):**

| Dimension | Weight | Rationale |
|---|---|---|
| Keyword match (role-based) | 30% | Highest impact on ATS filtering |
| Section parse-ability | 20% | Format failures are the most common silent killer |
| Content quality | 20% | Quantified bullets score higher in AI-screening ATS |
| Section completeness | 15% | Missing sections cause data loss in parsing |
| File/format compliance | 10% | Wrong file type, oversized files |
| Contact info completeness | 5% | Incomplete contacts = unparseable |

**Phase 2 ML upgrade:** Once 100,000+ ATS scans are completed, an XGBoost classifier will be trained on outcome data to improve scoring accuracy. The rule-based engine's scores serve as initial training labels. The trained XGBoost model will be exported to OpenVINO IR format via `openvino.convert_model()` for CPU inference — maintaining the same OpenVINO Runtime deployment pipeline already in place, with no infrastructure changes required.

### 8.3 Job Compatibility Scoring

**Algorithm:** Cosine similarity between TF-IDF vectors of the user's resume text and the job description, combined with hard-filter scoring on experience level and location.

**Intel scikit-learn-intelex (oneAPI AI Analytics Toolkit):**
All TF-IDF and cosine similarity operations are accelerated via Intel's `scikit-learn-intelex` package — part of the Intel oneAPI AI Analytics Toolkit. A single patch at service startup (`from sklearnex import patch_sklearn; patch_sklearn()`) replaces standard scikit-learn compute routines with Intel-optimized equivalents that exploit AVX-512 vectorization on Intel Xeon CPUs. Benchmarks show 11–12x speedup on TF-IDF vectorization and cosine similarity at the job-listing scales CareerOS operates at (10K–1M job-resume pairs per day). This is what makes the 3-second job search P95 SLA achievable on CPU-only infrastructure.

**Composite formula:**
```
compatibility = (0.45 × skill_overlap)
              + (0.25 × keyword_similarity)   ← Intel sklearnex TF-IDF + cosine
              + (0.20 × experience_match)
              + (0.10 × location_match)
```

**Skill overlap:** Jaccard similarity between extracted skills from resume vs. JD required skills.
**Keyword similarity:** Cosine similarity on TF-IDF vectors — **accelerated by Intel scikit-learn-intelex**.
**Experience match:** Gaussian decay function — perfect match = 1.0, within 1 year = 0.85, within 2 years = 0.65, >3 years off = 0.3.
**Location match:** Exact city = 1.0, same state = 0.8, remote-eligible = 0.9, different country = 0.2.

---

## 9. Database Design

### 9.1 Core Tables

**users**
```sql
id (UUID, PK), email (unique), password_hash, full_name, 
phone, city, country, linkedin_url, github_url, portfolio_url,
professional_status (enum), created_at, updated_at,
subscription_tier (enum: free/pro/premium), subscription_expires_at,
is_verified, is_active, last_login_at
```

**career_profiles**
```sql
id (UUID, PK), user_id (FK → users), 
target_role, target_industry, location_preference,
professional_summary, years_of_experience,
profile_completeness_score (0-100),
created_at, updated_at
```

**work_experiences**
```sql
id (UUID, PK), career_profile_id (FK),
company_name, job_title, employment_type, location,
start_date, end_date, is_current, description_bullets (JSONB),
created_at, updated_at
```

**educations**
```sql
id (UUID, PK), career_profile_id (FK),
institution_name, degree_type, field_of_study,
start_year, end_year, cgpa_or_percentage, 
relevant_coursework (JSONB), created_at
```

**skills**
```sql
id (UUID, PK), career_profile_id (FK),
skill_name, category (technical/soft/language/tool),
proficiency_level (beginner/intermediate/advanced/expert),
created_at
```

**projects**
```sql
id (UUID, PK), career_profile_id (FK),
title, description, tech_stack (JSONB),
github_url, live_url, start_date, end_date,
created_at, updated_at
```

**certifications**
```sql
id (UUID, PK), career_profile_id (FK),
name, issuing_organization, issue_date, expiry_date,
credential_id, credential_url, created_at
```

**resumes**
```sql
id (UUID, PK), user_id (FK), career_profile_id (FK),
name (user-defined), template_id, 
custom_section_order (JSONB), custom_overrides (JSONB),
s3_key (for stored PDF), last_generated_at,
created_at, updated_at
```

**ats_scans**
```sql
id (UUID, PK), user_id (FK), resume_id (FK, nullable),
source_type (enum: built_resume / uploaded_file),
uploaded_file_s3_key, jd_text (nullable),
composite_score, dimension_scores (JSONB),
recommendations (JSONB), keyword_gaps (JSONB),
scanned_at
```

**job_listings**
```sql
id (UUID, PK), external_id, source_api,
title, company, location, country, remote_eligible,
employment_type, experience_level, salary_min, salary_max,
description_text, required_skills (JSONB),
extracted_keywords (JSONB), apply_url,
posted_at, fetched_at, expires_at
```

**job_compatibility_scores**
```sql
id (UUID, PK), user_id (FK), job_listing_id (FK),
composite_score, skill_overlap_score, keyword_score,
experience_match_score, location_match_score,
computed_at
```

### 9.2 Indexing Strategy

- `users.email` — unique index
- `career_profiles.user_id` — index
- `job_listings.posted_at` — index for recency sorting
- `job_listings.location, employment_type, experience_level` — composite index for filtered search
- `job_compatibility_scores.user_id, composite_score` — composite index for ranked results
- `ats_scans.user_id, scanned_at` — composite index for history queries

---

## 10. API Design

### 10.1 API Conventions

- Base URL: `https://api.careeros.in/v1`
- Protocol: REST over HTTPS
- Format: JSON request/response bodies
- Auth: Bearer JWT in Authorization header
- Rate limits: Free tier — 100 req/hour; Pro — 1,000 req/hour; Premium — 10,000 req/hour
- Versioning: URL path versioning (`/v1/`, `/v2/`)
- Error format: `{ "error": { "code": "RESOURCE_NOT_FOUND", "message": "...", "details": {} } }`

### 10.2 Key Endpoints

**Authentication**
```
POST   /auth/register          — Create account
POST   /auth/login             — Get JWT token
POST   /auth/refresh           — Refresh token
POST   /auth/logout            — Invalidate token
POST   /auth/google            — Google OAuth callback
POST   /auth/linkedin          — LinkedIn OAuth callback
POST   /auth/forgot-password   — Trigger reset email
POST   /auth/reset-password    — Submit new password
```

**Career Profile**
```
GET    /profile                — Get my career profile
PUT    /profile                — Update career profile
POST   /profile/work-experience      — Add work experience
PUT    /profile/work-experience/:id  — Update entry
DELETE /profile/work-experience/:id  — Remove entry
POST   /profile/education            — Add education
POST   /profile/skills/bulk          — Bulk upsert skills
POST   /profile/projects             — Add project
POST   /profile/certifications       — Add certification
POST   /profile/import-linkedin      — Import from LinkedIn
GET    /profile/completeness         — Get completeness score
```

**Resume Builder**
```
GET    /resumes                — List my resumes
POST   /resumes                — Create new resume
GET    /resumes/:id            — Get resume details
PUT    /resumes/:id            — Update resume settings
DELETE /resumes/:id            — Delete resume
POST   /resumes/:id/generate   — Generate PDF (returns signed S3 URL)
GET    /resumes/:id/preview    — Get HTML preview
POST   /resumes/:id/duplicate  — Clone resume
GET    /templates              — List available templates
```

**ATS Engine**
```
POST   /ats/scan/resume/:id    — Score a built resume
POST   /ats/scan/upload        — Upload + score external resume (multipart)
POST   /ats/scan/jd-match      — Score resume against pasted JD
GET    /ats/scans              — Get my scan history
GET    /ats/scans/:id          — Get detailed scan report
GET    /ats/benchmarks/:role   — Get benchmark scores for a role
```

**Job Intelligence**
```
GET    /jobs                   — Search jobs (query params: q, location, type, level)
GET    /jobs/:id               — Get job details
GET    /jobs/matches           — Get personalized matches for my profile
GET    /jobs/:id/compatibility — Get my compatibility score for a job
POST   /jobs/alerts            — Create a job alert
GET    /jobs/alerts            — List my alerts
DELETE /jobs/alerts/:id        — Remove alert
POST   /jobs/:id/apply         — Track application (external URL returned)
```

**Analytics**
```
GET    /analytics/dashboard    — Career health overview
GET    /analytics/ats-history  — ATS score over time
GET    /analytics/market       — Market intelligence for my role
GET    /analytics/applications — Application tracker
```

---

## 11. UI/UX Flow Design

### 11.1 Onboarding Flow

```
Landing Page
    ↓
Sign Up (email / Google)
    ↓
Email Verification
    ↓
Professional Status Selection
(Student / Fresher / Experienced / Career Break)
    ↓
Role-Specific Onboarding Wizard
    ↓ (student path example)
College + Degree Details
    ↓
Target Role + Industry
    ↓
Skills Entry (tag-based input)
    ↓
Projects Entry (1 minimum nudge)
    ↓
Profile Completeness Score shown (e.g., 62%)
    ↓
CTA: "Build Your First Resume" or "Score Your Existing Resume"
```

### 11.2 Resume Builder Flow

```
Select Mode
├── "Start from my profile" (uses career profile data)
└── "Start fresh" (guided form, saves to profile simultaneously)
    ↓
Choose Template
(8 templates shown with ATS compatibility badge)
    ↓
AI-Guided Sections (one at a time)
├── Personal Information (pre-filled from profile)
├── Professional Summary (AI generates, user edits)
├── Work Experience (AI enhances bullets)
├── Education
├── Skills (auto-populated from profile)
├── Projects
├── Certifications
└── Additional Sections (optional)
    ↓
Live Preview (side-by-side on desktop, toggle on mobile)
    ↓
ATS Pre-Check (automatic, shows quick score)
    ↓
Download PDF / Save to My Resumes
```

### 11.3 ATS Scoring Flow

```
ATS Score Home
    ↓
Choose Input Method
├── "Score my CareerOS resume" (select from list)
└── "Upload my existing resume" (PDF/DOCX)
    ↓
(Optional) Paste Job Description for JD-specific scoring
    ↓
Processing (animated, ~8 seconds)
    ↓
Score Results Page
├── Composite Score (large, prominent: e.g., 67/100)
├── Radar chart (all 6 dimensions)
├── Dimension cards (each with sub-score + explanation)
├── Keyword Gap Analysis table
├── Fix-It Recommendations (prioritized list)
└── CTA: "Fix These Issues" → opens resume editor
```

### 11.4 Job Search Flow

```
Jobs Home
├── Personalized Matches (auto-loaded, sorted by compatibility)
└── Search Bar + Filters
    ↓
Job List (card view)
Each card shows:
├── Title, Company, Location
├── Compatibility Score (color-coded)
├── Posted date
├── Salary (if available)
└── Quick Actions: View | Tailor Resume | Track Application
    ↓
Job Detail Page
├── Full JD
├── Compatibility breakdown (which skills match, which are missing)
├── Skill gap list
├── "Tailor My Resume" → generates role-specific resume version
└── "Apply Now" → opens source URL in new tab
```

---

## 12. ATS Engine Specification

### 12.1 Resume Parsing Pipeline

**Stage 1 — File Processing**
- Accept PDF and DOCX
- For PDF: attempt direct text extraction via pdfplumber. If extracted text is <100 characters (image-based PDF), invoke OCR pipeline using Tesseract.
- For DOCX: extract via python-docx, preserving paragraph structure.
- Output: raw text + paragraph list + detected layout flags

**Stage 2 — Section Identification**
- Apply trained spaCy NER model + rule-based regex patterns to identify resume sections
- Recognized sections: Contact Info, Summary/Objective, Work Experience, Education, Skills, Projects, Certifications, Awards, Languages, Publications, Volunteer Work
- Flag: any content that could not be assigned to a section ("Unclassified content")
- Output: structured section map

**Stage 3 — Entity Extraction**
- From Contact Info: extract name, email, phone, city, URLs using regex + NER
- From Work Experience: extract company, title, dates, bullet points
- From Education: extract institution, degree, dates, CGPA
- From Skills: extract individual skill tokens
- Output: structured data object

**Stage 4 — Scoring**

*Keyword Match Scoring:*
- If JD provided: extract n-grams (1–3 word phrases) from JD, weighted by frequency and section position (title keywords weighted 3x, required skills 2x, nice-to-have 1x). Score = (matched keywords) / (total high-priority keywords) × 100.
- If no JD: use role-based keyword corpus (pre-built for 50+ role categories). Same scoring formula.

*Format Parse-ability Scoring:*
- Check for: text-selectable content (not image), standard section headers, no tables used for layout, no text boxes, no multi-column layout detection, standard font detection, proper encoding.
- Each format issue deducts points based on severity.

*Content Quality Scoring:*
- Action verb detection in bullet points (using curated 200-word action verb lexicon)
- Quantification detection (regex for numbers, percentages, currency, multipliers)
- Bullet length optimization (too short <6 words: -2pts each; too long >25 words: -1pt each)
- Passive voice detection (penalized: -1pt per instance, max -5)

*Section Completeness:*
- Required for role: Work Experience / Projects, Education, Skills, Contact Info
- Strongly recommended: Summary, Certifications (if any)
- Each missing required section: -8pts. Each missing recommended section: -3pts.

### 12.2 ATS System Simulation Weights

Different ATS systems have different parsing behaviors. The composite score is a weighted average:

| ATS System | Market Weight (India+Global) | Key Behavioral Notes |
|---|---|---|
| Taleo (Oracle) | 18% | Very strict on section headers, penalizes tables |
| Workday | 16% | Strong keyword matching, good at parsing modern formats |
| Naukri RMS | 15% | India-specific, handles Indian degree names well |
| Greenhouse | 12% | Lenient on format, strong on keyword density |
| PeopleStrong | 10% | Indian HR tech, handles regional language names |
| Darwinbox | 9% | Growing fast in India, similar to Workday |
| Lever | 8% | Startup-focused, modern parser, good 2-column support |
| iCIMS | 7% | Enterprise US, very strict formatting |
| SmartRecruiters | 5% | Global, lenient, good at skills extraction |

---

## 13. Job Intelligence Engine

### 13.1 Data Sources and Coverage

| API | Coverage | Jobs/Day | Strength |
|---|---|---|---|
| Adzuna | Global (16 countries + India) | 500K+ | Best India + global balance |
| JSearch (RapidAPI) | Global aggregator | 1M+ | Real-time, broad coverage |
| Jooble | 71 countries | 200K+ | Strong Europe + emerging markets |
| Reed | UK + some global | 100K+ | International premium roles |
| Apna | India (tier-2/3 focus) | 50K+ | Entry-level, blue-collar, local |

### 13.2 Deduplication Logic

Jobs are considered duplicates if: company name similarity >90% AND job title similarity >85% AND location exact match AND posted within 48 hours of each other. Deduplication uses MinHash LSH for scalable approximate matching.

### 13.3 Job Categorization

All jobs are auto-categorized into:
- **Tier** (Local Part-time | National Full-time | Remote Global | MNC International)
- **Level** (Internship | Entry (0–2 yrs) | Mid (2–5 yrs) | Senior (5–10 yrs) | Lead/Manager | Executive)
- **Domain** (Technology | Finance | Marketing | Operations | Design | Healthcare | Education | Manufacturing | Other)
- **Work Mode** (On-site | Remote | Hybrid)

---

## 14. Security & Compliance

### 14.1 Authentication & Authorization

- JWT access tokens: 15-minute expiry
- Refresh tokens: 30-day expiry, stored in httpOnly cookie (not localStorage)
- Role-based access control: User | CollegeAdmin | Recruiter | PlatformAdmin
- All admin actions logged with user ID, timestamp, action type, and IP address

### 14.2 Data Privacy

**DPDP Act 2023 (India) Compliance:**
- Consent Management: explicit opt-in for each data category at signup
- Data Principal Rights: access my data (JSON export), correct my data, erase my data (30-day SLA), grievance mechanism (in-app + email)
- Data Fiduciary obligations: purpose limitation, storage limitation, security safeguards
- Data localization: all Indian user data stored in AWS ap-south-1 (Mumbai)

**GDPR Compliance:**
- Lawful basis: Contractual necessity + Legitimate Interest + Consent
- Data Subject Rights: access, rectification, erasure, portability, restriction, objection
- DPA contacts and Article 30 records maintained
- Privacy Policy updated to GDPR standard

### 14.3 Infrastructure Security

- All services run in AWS VPC with private subnets for databases
- RDS instances not publicly accessible
- S3 buckets: no public access, accessed via signed URLs only
- Secrets managed via AWS Secrets Manager (no hardcoded credentials anywhere)
- WAF deployed on API Gateway for OWASP protection
- CloudTrail enabled for all AWS API calls
- Regular dependency scanning via Dependabot + Snyk

### 14.4 Resume Data Handling

Uploaded resumes are processed in memory where possible. If temporary file storage is needed for processing, files are written to an encrypted temporary S3 prefix and deleted within 1 hour of processing. Users explicitly choosing to save uploaded resumes are given clear notice that the file will be stored under their account.

---

## 15. Phased Roadmap

### Phase 1 — Foundation (Weeks 1–10)
*Goal: Shippable, monetizable core product. Resume builder + ATS engine only.*

**Week 1–2:** Project setup, tech stack initialization, DB schema, auth system, career profile CRUD. Set up Intel DevCloud workspace; establish baseline NLP inference benchmarks.
**Week 3–4:** Resume template engine, HTML/CSS template design (4 templates), PDF generation via WeasyPrint.
**Week 5–6:** AI resume builder integration (Claude API), content generation, professional summary. Apply Intel IPEX optimization to PyTorch preprocessing pipeline.
**Week 7–8:** ATS engine v1 (rule-based scoring logic, recommendations engine). Export spaCy NER model to ONNX → OpenVINO IR. Benchmark OpenVINO Runtime vs. PyTorch CPU baseline on Intel DevCloud. Validate P95 < 12s SLA.
**Week 9:** Integrate Intel scikit-learn-intelex into Job Intelligence compatibility scoring. UI polish, mobile responsiveness, Razorpay payment integration, free/pro tiers.
**Week 10:** Beta launch, 500-user closed beta, feedback collection, bug fixes. Final DevCloud performance report documenting Intel optimization gains.

**Phase 1 Deliverables:**
- Functional resume builder with 4+ templates
- ATS scoring engine with 6 scoring dimensions
- Resume upload + score (PDF/DOCX)
- JD-specific scoring mode
- Freemium subscription with payment
- Basic analytics dashboard

### Phase 2 — Intelligence (Weeks 11–22)
*Goal: Add job intelligence layer and improve ATS engine depth.*

**Week 11–13:** Job data API integrations (Adzuna, JSearch, Jooble), aggregation pipeline
**Week 14–15:** Compatibility scoring algorithm, job match UI
**Week 16–17:** Job alerts, application tracker, resume version history
**Week 18–19:** ATS engine improvements (4 additional ATS systems), ML data collection pipeline
**Week 20–21:** Analytics expansion, market intelligence features, career health dashboard
**Week 22:** Phase 2 public launch, scaling test, marketing push

### Phase 3 — Scale (Months 6–12)
*Goal: B2B institutional launch, recruiter access, mobile app.*

- B2B college portal (placement officer dashboard, bulk student management)
- Recruiter access module (search resume database, shortlisting tools)
- Mobile app (React Native)
- Cover letter generator
- LinkedIn profile optimizer
- ATS engine ML upgrade (train on collected data)
- International market expansion (Southeast Asia)
- Series A fundraising preparation

---

## 16. Monetization & Business Model

### 16.1 Individual (B2C) Pricing

**Free Tier:**
- 3 resume builds per month
- 5 ATS scans per month
- 3 job search queries per day
- 2 template options
- No JD-specific scoring
- Watermarked PDF export

**Pro — ₹299/month (₹2,499/year):**
- Unlimited resume builds
- 30 ATS scans per month
- Unlimited job searches
- All 8 templates
- JD-specific scoring
- ATS-clean PDF export (no watermark)
- Resume version history (10 versions)
- Job alerts (3 active alerts)
- Priority AI generation

**Premium — ₹799/month (₹6,999/year):**
- Everything in Pro
- Unlimited ATS scans
- Unlimited job alerts
- All future templates
- Cover letter generator (Phase 2)
- LinkedIn optimizer (Phase 3)
- 1 career coaching session/month (Phase 3)
- Priority support
- Advanced market analytics

### 16.2 Institutional (B2B) Pricing

**College Starter — ₹49,999/year:**
- Up to 500 student accounts
- Placement officer dashboard
- Bulk resume scoring
- Placement analytics

**College Pro — ₹1,49,999/year:**
- Up to 2,000 student accounts
- All Starter features
- Custom college branding
- API access for SLCM integration
- Placement performance reports
- Dedicated account manager

**Enterprise — Custom pricing:**
- Unlimited accounts
- SLA guarantees
- White-label option
- On-premise deployment option
- Custom ATS integrations

### 16.3 Recruiter Access

**Pay-per-search — ₹199/search batch (100 profiles)**
**Monthly subscription — ₹4,999/month (unlimited searches, filtered access)**

Recruiters access CareerOS's verified, ATS-scored resume database. They can filter by role, skills, experience, location, and ATS score. This is opt-in for users (users choose whether their resume is visible to recruiters).

### 16.4 Revenue Projections (Conservative)

| Quarter | B2C Revenue | B2B Revenue | Recruiter | Total MRR |
|---|---|---|---|---|
| Q1 (post-launch) | ₹1.2L | — | — | ₹1.2L |
| Q2 | ₹4.5L | ₹2.0L | ₹0.5L | ₹7.0L |
| Q3 | ₹12L | ₹8L | ₹2L | ₹22L |
| Q4 | ₹28L | ₹18L | ₹6L | ₹52L |
| Year 2 ARR | — | — | — | ₹8–10Cr |

---

## 17. Risk Register

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| AI API cost overrun | Medium | High | Implement caching, use Haiku for lightweight tasks, set hard spending caps |
| Job API rate limits / pricing change | Medium | Medium | Multi-API strategy, caching, contractual SLAs |
| Competitor copies ATS engine | Medium | Medium | Speed of execution + data moat is the defense; file patents for scoring methodology |
| DPDP compliance gap | Low | Very High | Engage compliance counsel, regular audits, privacy-by-design from day 1 |
| PDF generation quality issues | High | High | Extensive testing across 50+ ATS systems, maintain fallback template library |
| Low freemium-to-paid conversion | Medium | High | Aggressive usage limits on free tier, clear value demonstration before paywall |
| Single AI provider dependency | Low | Very High | Multi-provider fallback already in architecture |
| College B2B sales cycle too long | High | Medium | Start with small colleges (500 students), offer 3-month free pilots |
| Scaling costs exceed revenue | Low | Medium | Horizontal scaling architecture, cost optimization from Phase 1 |
| Key talent retention | Medium | Medium | Competitive equity compensation, meaningful technical challenges |

---

## 18. Glossary

**ATS (Applicant Tracking System):** Software used by employers to manage and filter job applications. Examples: Taleo, Workday, Greenhouse.

**ATS Score:** CareerOS's proprietary measure (0–100) of how well a resume will perform when processed by ATS software.

**Career Profile:** The persistent, structured data store in CareerOS that holds all of a user's career information and serves as the source of truth for all features.

**Compatibility Score:** CareerOS's measure (0–100) of how well a user's profile matches a specific job listing.

**DPDP Act:** India's Digital Personal Data Protection Act, 2023. Governs how personal data of Indian citizens must be handled.

**JD (Job Description):** The text posted by an employer describing a job opening, including responsibilities, requirements, and qualifications.

**Job Intelligence Layer:** CareerOS's module that aggregates live job listings from licensed APIs and performs compatibility matching.

**Keyword Gap Analysis:** The identification of keywords present in a job description but absent from the user's resume, along with suggestions for incorporation.

**NER (Named Entity Recognition):** An NLP technique used in CareerOS's ATS engine to identify and classify entities (company names, job titles, dates, skills) in resume text.

**PDF Parsing:** The process of extracting structured text and data from a PDF file for ATS analysis.

**STAR Format:** A resume writing framework — Situation, Task, Action, Result — used to structure achievement-oriented bullet points.

**TF-IDF:** Term Frequency–Inverse Document Frequency. A numerical statistic used in CareerOS's job matching algorithm to assess keyword relevance.

---

*Document Version: 1.0*
*Prepared by: CareerOS Product Team*
*Last Updated: April 2026*
*Classification: Confidential — Internal / Investor Use Only*

---
*CareerOS — Building careers, not just resumes.*
