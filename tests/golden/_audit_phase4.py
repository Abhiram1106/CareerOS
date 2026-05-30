"""Phase 4 sub-score correctness audit — run inside core-api container."""
from careeros_scoring.resume_components import (
    evidence_quality_score,
    interview_readiness_score,
    placement_hygiene_score,
    profile_completeness_score,
)

def sec(name, raw):
    return {"section_name": name, "content_json": {"raw": raw}}

def check(label, got, lo, hi, all_ok_ref):
    ok = lo <= got <= hi
    if not ok:
        all_ok_ref.append(label)
    print(f'  [{"OK" if ok else "FAIL"}] {label:38} [{lo},{hi}]  got={got}')
    return ok

results = []

print("=== evidence_quality ===")
ev = [
    ("Empty sections",            evidence_quality_score([]),                   0,  5),
    ("No exp/proj text",          evidence_quality_score([sec("education","B.Tech CS 2025")]),  0, 30),
    ("Verbs only no metrics",     evidence_quality_score([sec("experience","Built developed designed implemented optimized deployed created engineered")]),  20, 55),
    ("Strong STAR bullets",       evidence_quality_score([sec("experience","- Built payment service in Python reducing latency by 40%.\n- Optimized SQL queries cutting p95 by 30%.\n- Deployed on Kubernetes serving 2M requests/day.\n- Led team of 5 engineers.\n- Reduced infra cost by 25%.")]),  45, 100),
    ("Repeated same verb",        evidence_quality_score([sec("experience","Built X. Built Y. Built Z. Built A. Built B. Built C.")]),  0, 38),  # 1 distinct verb
    ("Gameable repetition",       evidence_quality_score([sec("experience","built built built built built 50% 100k 30x")]),  0, 45),
]
for label, got, lo, hi in ev:
    check(label, got, lo, hi, results)

print()
print("=== interview_readiness ===")
ir = [
    ("Empty",                     interview_readiness_score([]),   0,  5),
    ("Thin experience only",      interview_readiness_score([sec("experience","did some work in python")]),  10, 42),
    ("Strong exp + projects",     interview_readiness_score([
        sec("experience","Software Intern, Razorpay, Jun 2024 - Aug 2024. Built payment service in Python FastAPI, reduced latency 40%. Deployed on Docker Kubernetes."),
        sec("projects","Implemented LRU cache in Go, handled 10k req/s. Built ML pipeline in PyTorch, 87% accuracy.")
    ]), 50, 100),
    ("Leadership POR",            interview_readiness_score([
        sec("positions_of_responsibility","President Tech Club. Led 50 members. Coordinated 5 events. Mentored 20 juniors. Founded coding community."),
        sec("experience","Intern built dashboard in React and Node serving 200 users.")
    ]), 40, 100),
    ("Only projects no exp",      interview_readiness_score([sec("projects","Built chatbot in Python. Created web scraper. Implemented sorting algorithms.")]),  10, 55),
]
for label, got, lo, hi in ir:
    check(label, got, lo, hi, results)

print()
print("=== placement_hygiene ===")
hy = [
    ("Full contact + clean",      placement_hygiene_score(
        [sec("header","john@mail.com | +91 9876543210 | linkedin.com/in/john | github.com/john"),
         sec("experience","Built payment service in Python, reducing latency 40%. Deployed on Docker."),
         sec("skills","Python, Docker, SQL")], []),  90, 100),
    ("No email flag",             placement_hygiene_score(
        [sec("header","+91 9876543210"), sec("experience","Built things.")], ["no_email_found"]),  45, 70),
    ("Filler phrases",            placement_hygiene_score(
        [sec("summary","I have good communication skills and am a team player. I am a quick learner and self-motivated.")], []),  0, 72),
    ("Wall of text no bullets",   placement_hygiene_score(
        [sec("experience","I did many things in college and worked hard and attended lectures and participated in events " * 4)], []),  0, 68),
    ("Tech skills present",       placement_hygiene_score(
        [sec("header","a@b.com | +91 9123456789 | linkedin.com/in/x"),
         sec("skills","Python docker kubernetes")], []),  78, 100),
    ("Soft skills only",          placement_hygiene_score(
        [sec("header","a@b.com | +91 9123456789 | linkedin.com/in/x"),
         sec("skills","communication leadership teamwork problem solving")], []),  70, 92),
]
for label, got, lo, hi in hy:
    check(label, got, lo, hi, results)

print()
print("=== profile_completeness ===")
pc = [
    ("All empty",                 profile_completeness_score([]),  0,  5),
    ("All whitespace",            profile_completeness_score([sec(n,"   ") for n in ["summary","education","experience","projects","skills"]]),  0, 10),
    ("All rich content",          profile_completeness_score([
        sec("summary","Motivated backend engineer with 2 internships and strong Python skills."),
        sec("education","B.Tech CS NIT Trichy 2025 CGPA 8.4"),
        sec("experience","Intern Razorpay Jun 2024 built payment service Python FastAPI reducing latency 40%"),
        sec("projects","Distributed cache in Go with Redis handling 10k req/s. ML pipeline PyTorch 87% accuracy."),
        sec("skills","Python FastAPI Docker Kubernetes SQL Go PyTorch"),
    ]), 95, 100),
    ("Only education present",    profile_completeness_score([sec("education","B.Tech CS 2025")]),  10, 22),
    ("3 of 5 sections",           profile_completeness_score([sec(n,"Some reasonable content here with enough words for this section") for n in ["education","experience","skills"]]),  50, 75),
]
for label, got, lo, hi in pc:
    check(label, got, lo, hi, results)

print()
if results:
    print(f"PHASE 4 AUDIT FAILED — {len(results)} failure(s):")
    for r in results:
        print(f"  - {r}")
    raise SystemExit(1)
else:
    print("PHASE 4 AUDIT PASSED — all sub-score ranges correct")
