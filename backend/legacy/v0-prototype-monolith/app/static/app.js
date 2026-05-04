const API = "";
let token = localStorage.getItem("cos_token") || null;

// ---- Utilities ----

function toast(msg, type) {
  const el = document.getElementById("toast");
  el.textContent = msg;
  el.className = "toast show " + (type || "info");
  clearTimeout(el._t);
  el._t = setTimeout(() => { el.className = "toast"; }, 3000);
}

async function api(path, method, body) {
  const opts = {
    method: method || "GET",
    headers: Object.assign(
      { "Content-Type": "application/json" },
      token ? { Authorization: "Bearer " + token } : {}
    ),
  };
  if (body) opts.body = JSON.stringify(body);
  const res = await fetch(API + path, opts);
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || "Request failed");
  return data;
}

function setAuthState(name) {
  const dot = document.querySelector(".auth-dot");
  const state = document.getElementById("authState");
  if (name) {
    dot.className = "auth-dot online";
    state.textContent = name.split(" ")[0];
  } else {
    dot.className = "auth-dot offline";
    state.textContent = "Not signed in";
  }
}

// ---- Nav ----

document.querySelectorAll(".nav-item").forEach(function(btn) {
  btn.addEventListener("click", function() {
    document.querySelectorAll(".nav-item").forEach(function(b) { b.classList.remove("active"); });
    document.querySelectorAll(".screen").forEach(function(s) { s.classList.remove("active"); });
    btn.classList.add("active");
    document.getElementById(btn.dataset.screen).classList.add("active");
  });
});

// ---- Auth ----

document.getElementById("registerBtn").addEventListener("click", async function() {
  try {
    const data = await api("/api/auth/register", "POST", {
      full_name: document.getElementById("nameInput").value,
      email: document.getElementById("emailInput").value,
      password: document.getElementById("passwordInput").value,
    });
    token = data.token;
    localStorage.setItem("cos_token", token);
    setAuthState(data.user.full_name);
    document.getElementById("statusText").textContent = "Signed in";
    toast("Account created! Welcome to CareerOS.", "success");
  } catch (e) {
    toast(e.message, "error");
  }
});

document.getElementById("loginBtn").addEventListener("click", async function() {
  try {
    const data = await api("/api/auth/login", "POST", {
      email: document.getElementById("emailInput").value,
      password: document.getElementById("passwordInput").value,
    });
    token = data.token;
    localStorage.setItem("cos_token", token);
    setAuthState(data.user.full_name);
    document.getElementById("statusText").textContent = "Signed in";
    toast("Welcome back!", "success");
    loadProfile();
  } catch (e) {
    toast(e.message, "error");
  }
});

// ---- Profile ----

async function loadProfile() {
  if (!token) return;
  try {
    const d = await api("/api/profile");
    document.getElementById("nameInput").value = d.full_name || "";
    document.getElementById("cityInput").value = d.city || "";
    document.getElementById("statusInput").value = d.professional_status || "Fresher";
    document.getElementById("roleInput").value = d.target_role || "";
    document.getElementById("skillsInput").value = d.skills_csv || "";
    document.getElementById("summaryInput").value = d.summary || "";
    document.getElementById("expInput").value = d.experience_bullet || "";
    updateResumePreview();
    setAuthState(d.full_name);
  } catch (_) {}
}

document.getElementById("saveProfileBtn").addEventListener("click", async function() {
  try {
    await api("/api/profile", "PUT", {
      full_name: document.getElementById("nameInput").value,
      city: document.getElementById("cityInput").value,
      professional_status: document.getElementById("statusInput").value,
      target_role: document.getElementById("roleInput").value,
      skills_csv: document.getElementById("skillsInput").value,
      summary: document.getElementById("summaryInput").value,
      experience_bullet: document.getElementById("expInput").value,
    });
    toast("Profile saved!", "success");
    updateResumePreview();
  } catch (e) {
    toast(e.message, "error");
  }
});

// ---- Resume Builder ----

function updateResumePreview() {
  document.getElementById("pvName").textContent = document.getElementById("nameInput").value || "Your Name";
  document.getElementById("pvRole").textContent = document.getElementById("roleInput").value || "Target Role";
  document.getElementById("pvSummary").textContent = document.getElementById("summaryInput").value || "Your professional summary will appear here.";
  document.getElementById("pvExp").textContent = document.getElementById("expInput").value || "Your experience bullet will appear here.";
  document.getElementById("pvSkills").textContent = document.getElementById("skillsInput").value || "Your skills will appear here.";
}

["summaryInput", "expInput", "skillsInput", "nameInput", "roleInput"].forEach(function(id) {
  document.getElementById(id).addEventListener("input", updateResumePreview);
});

document.getElementById("autofillBtn").addEventListener("click", function() {
  document.getElementById("summaryInput").value =
    "Results-driven software engineer with strong fundamentals in full-stack development. Passionate about building scalable, user-centric applications. Quick learner with hands-on experience in Python, React, and cloud infrastructure.";
  document.getElementById("expInput").value =
    "Built a REST API using FastAPI and PostgreSQL, serving 5,000+ daily users with 99.8% uptime. Reduced page load time by 40% through lazy loading and caching optimization. Led a team of 3 in delivering a college project within a 4-week sprint.";
  updateResumePreview();
  toast("Sample content loaded!", "success");
});

document.getElementById("saveProfileFromResumeBtn").addEventListener("click", async function() {
  try {
    await api("/api/profile", "PUT", {
      full_name: document.getElementById("nameInput").value,
      city: document.getElementById("cityInput").value,
      professional_status: document.getElementById("statusInput").value,
      target_role: document.getElementById("roleInput").value,
      skills_csv: document.getElementById("skillsInput").value,
      summary: document.getElementById("summaryInput").value,
      experience_bullet: document.getElementById("expInput").value,
    });
    toast("Saved to profile!", "success");
  } catch (e) {
    toast(e.message, "error");
  }
});

document.getElementById("generateResumeBtn").addEventListener("click", async function() {
  if (!token) { toast("Please sign in first.", "error"); return; }
  try {
    const d = await api("/api/resumes/generate", "POST", {
      template_name: document.getElementById("templateSelect").value,
    });
    document.getElementById("resumeText").style.display = "block";
    document.getElementById("resumeText").textContent = d.content;
    toast("Resume generated and saved!", "success");
  } catch (e) {
    toast(e.message, "error");
  }
});

// ---- ATS Scanner ----

function setBar(id, value) {
  document.getElementById(id).style.width = value + "%";
}

function scoreColor(v) {
  if (v >= 75) return "#06d6a0";
  if (v >= 55) return "#ffd166";
  return "#ff6b6b";
}

document.getElementById("scanBtn").addEventListener("click", async function() {
  if (!token) { toast("Please sign in first.", "error"); return; }
  const jd = document.getElementById("jdInput").value.trim();
  if (!jd) { toast("Please paste a job description.", "error"); return; }

  document.getElementById("scanBtn").textContent = "Scanning…";
  try {
    const d = await api("/api/ats/scan", "POST", { jd_text: jd });

    document.getElementById("scoresGrid").style.display = "grid";
    document.getElementById("composite").textContent = d.composite;

    const circumference = 251;
    const offset = circumference - (d.composite / 100) * circumference;
    const ring = document.getElementById("ringFill");
    ring.style.stroke = scoreColor(d.composite);
    setTimeout(function() { ring.style.strokeDashoffset = offset; }, 50);

    document.getElementById("keyword").textContent = d.keyword;
    document.getElementById("format").textContent = d.format;
    document.getElementById("quality").textContent = d.quality;
    document.getElementById("complete").textContent = d.complete;
    document.getElementById("contact").textContent = d.contact;

    setBar("barKeyword", d.keyword);
    setBar("barFormat", d.format);
    setBar("barQuality", d.quality);
    setBar("barComplete", d.complete);
    setBar("barContact", d.contact);

    document.getElementById("suggestionsCard").style.display = "block";
    const list = document.getElementById("suggestionsList");
    list.innerHTML = "";
    (d.suggestions || []).forEach(function(s) {
      const li = document.createElement("li");
      li.textContent = s;
      list.appendChild(li);
    });

    const missingWrap = document.getElementById("missingKeywordsWrap");
    if (d.missing_keywords && d.missing_keywords.length > 0) {
      missingWrap.style.display = "block";
      document.getElementById("missingKeywords").innerHTML =
        d.missing_keywords.map(function(k) { return '<span class="chip">' + k + '</span>'; }).join("");
    } else {
      missingWrap.style.display = "none";
    }

    toast("ATS scan complete!", "success");
  } catch (e) {
    toast(e.message, "error");
  } finally {
    document.getElementById("scanBtn").textContent = "🔍 Run ATS Scan";
  }
});

// ---- Job Matches ----

async function loadJobs() {
  if (!token) { toast("Please sign in first.", "error"); return; }
  try {
    const d = await api("/api/jobs/matches");
    const list = document.getElementById("jobList");
    list.innerHTML = "";
    d.jobs.forEach(function(j) {
      const matchClass = j.score >= 75 ? "match-high" : j.score >= 60 ? "match-mid" : "match-low";
      const card = document.createElement("div");
      card.className = "job-card";
      card.innerHTML =
        '<div class="job-left">' +
          '<div class="job-title">' + j.title + '</div>' +
          '<div class="job-meta">' +
            '<span>🏢 ' + j.company + '</span>' +
            '<span>📍 ' + j.location + '</span>' +
            '<span>🔧 ' + j.skills.slice(0, 3).join(", ") + '</span>' +
          '</div>' +
        '</div>' +
        '<div class="job-right">' +
          '<div class="match-badge ' + matchClass + '">' + j.score + '%</div>' +
          '<div class="job-type-badge">' + (j.type || "Full-time") + '</div>' +
        '</div>';
      list.appendChild(card);
    });
    toast("Jobs loaded!", "success");
  } catch (e) {
    toast(e.message, "error");
  }
}

document.getElementById("refreshJobsBtn").addEventListener("click", loadJobs);

// ---- Dashboard ----

async function loadDashboard() {
  if (!token) { toast("Please sign in first.", "error"); return; }
  try {
    const d = await api("/api/dashboard");
    document.getElementById("bestScore").textContent = d.best_ats_score;
    document.getElementById("totalResumes").textContent = d.total_resumes;
    document.getElementById("scansPerformed").textContent = d.scans_performed;
    document.getElementById("jobs70").textContent = d.jobs_matched_over_70;
    document.getElementById("appsTracked").textContent = d.applications_tracked;
    document.getElementById("profileComplete").textContent = d.profile_completeness + "%";
    document.getElementById("profileBar").style.width = d.profile_completeness + "%";
    document.getElementById("profileTip").textContent =
      d.profile_completeness === 100
        ? "🎉 Profile is 100% complete — all modules are fully powered."
        : "Fill in the remaining fields to reach 100% and boost your ATS scores.";
    toast("Dashboard updated!", "success");
  } catch (e) {
    toast(e.message, "error");
  }
}

document.getElementById("refreshDashBtn").addEventListener("click", loadDashboard);

// ---- Init ----

if (token) loadProfile();
