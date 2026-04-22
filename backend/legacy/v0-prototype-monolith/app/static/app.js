const state = {
  token: localStorage.getItem('careeros_token') || '',
  profile: null,
};

const navButtons = document.querySelectorAll('.nav-btn');
const screens = document.querySelectorAll('.screen');
navButtons.forEach((btn) => {
  btn.addEventListener('click', () => {
    navButtons.forEach((b) => b.classList.remove('active'));
    screens.forEach((s) => s.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById(btn.dataset.screen).classList.add('active');
  });
});

function setStatus(msg) {
  document.getElementById('statusText').textContent = msg;
}

function setAuthState() {
  document.getElementById('authState').textContent = state.token ? 'Signed in' : 'Not signed in';
}

async function api(path, method = 'GET', body = null) {
  const headers = { 'Content-Type': 'application/json' };
  if (state.token) headers.Authorization = `Bearer ${state.token}`;
  const res = await fetch(path, {
    method,
    headers,
    body: body ? JSON.stringify(body) : null,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Request failed');
  }
  return res.json();
}

function readProfileInputs() {
  return {
    full_name: document.getElementById('nameInput').value,
    city: document.getElementById('cityInput').value,
    professional_status: document.getElementById('statusInput').value,
    target_role: document.getElementById('roleInput').value,
    skills_csv: document.getElementById('skillsInput').value,
    summary: document.getElementById('summaryInput').value,
    experience_bullet: document.getElementById('expInput').value,
  };
}

function fillInputs(profile) {
  if (!profile) return;
  document.getElementById('nameInput').value = profile.full_name || '';
  document.getElementById('emailInput').value = profile.email || '';
  document.getElementById('cityInput').value = profile.city || '';
  document.getElementById('statusInput').value = profile.professional_status || 'Fresher';
  document.getElementById('roleInput').value = profile.target_role || '';
  document.getElementById('skillsInput').value = profile.skills_csv || '';
  document.getElementById('summaryInput').value = profile.summary || '';
  document.getElementById('expInput').value = profile.experience_bullet || '';
  syncPreview();
}

function syncPreview() {
  document.getElementById('pvName').textContent = document.getElementById('nameInput').value || 'Your Name';
  document.getElementById('pvRole').textContent = document.getElementById('roleInput').value || 'Target Role';
  document.getElementById('pvSummary').textContent = document.getElementById('summaryInput').value || 'Professional summary appears here.';
  document.getElementById('pvExp').textContent = document.getElementById('expInput').value || 'Experience bullet appears here.';
  document.getElementById('pvSkills').textContent = document.getElementById('skillsInput').value || 'Skills appear here.';
}

async function loadProfile() {
  if (!state.token) return;
  const profile = await api('/api/profile');
  state.profile = profile;
  fillInputs(profile);
}

async function saveProfile() {
  await api('/api/profile', 'PUT', readProfileInputs());
  setStatus('Profile saved');
}

async function register() {
  const payload = {
    email: document.getElementById('emailInput').value,
    password: document.getElementById('passwordInput').value,
    full_name: document.getElementById('nameInput').value || 'User',
  };
  const data = await api('/api/auth/register', 'POST', payload);
  state.token = data.token;
  localStorage.setItem('careeros_token', state.token);
  setAuthState();
  await loadProfile();
  setStatus('Registered and signed in');
}

async function login() {
  const payload = {
    email: document.getElementById('emailInput').value,
    password: document.getElementById('passwordInput').value,
  };
  const data = await api('/api/auth/login', 'POST', payload);
  state.token = data.token;
  localStorage.setItem('careeros_token', state.token);
  setAuthState();
  await loadProfile();
  setStatus('Logged in');
}

async function generateResume() {
  await saveProfile();
  const template_name = document.getElementById('templateSelect').value;
  const data = await api('/api/resumes/generate', 'POST', { template_name });
  document.getElementById('resumeText').textContent = data.content;
  setStatus(`Resume #${data.resume_id} generated`);
}

async function runScan() {
  await saveProfile();
  const jd_text = document.getElementById('jdInput').value;
  const data = await api('/api/ats/scan', 'POST', { jd_text });
  document.getElementById('composite').textContent = data.composite;
  document.getElementById('keyword').textContent = data.keyword;
  document.getElementById('format').textContent = data.format;
  document.getElementById('quality').textContent = data.quality;
  document.getElementById('complete').textContent = data.complete;
  document.getElementById('contact').textContent = data.contact;
  setStatus('ATS scan complete');
}

async function refreshJobs() {
  const data = await api('/api/jobs/matches');
  const list = document.getElementById('jobList');
  list.innerHTML = data.jobs.map((job) => `
    <article class="job-card">
      <div class="job-top">
        <div><h3>${job.title}</h3><p>${job.company} | ${job.location}</p></div>
        <span class="pill">${job.score}% Match</span>
      </div>
    </article>
  `).join('');
}

async function refreshDashboard() {
  const data = await api('/api/dashboard');
  document.getElementById('bestScore').textContent = data.best_ats_score;
  document.getElementById('totalResumes').textContent = data.total_resumes;
  document.getElementById('scansPerformed').textContent = data.scans_performed;
  document.getElementById('jobs70').textContent = data.jobs_matched_over_70;
  document.getElementById('appsTracked').textContent = data.applications_tracked;
  document.getElementById('profileComplete').textContent = `${data.profile_completeness}%`;
}

['nameInput','roleInput','summaryInput','expInput','skillsInput'].forEach((id) => {
  document.getElementById(id).addEventListener('input', syncPreview);
});

document.getElementById('autofillBtn').addEventListener('click', () => {
  document.getElementById('summaryInput').value = 'Results-oriented candidate with strengths in backend APIs, data modeling, and deployment.';
  document.getElementById('expInput').value = 'Developed a FastAPI + React platform used by 800+ students, improving completion by 38% in 6 weeks.';
  syncPreview();
});

document.getElementById('registerBtn').addEventListener('click', async () => { try { await register(); } catch (e) { setStatus(e.message); } });
document.getElementById('loginBtn').addEventListener('click', async () => { try { await login(); } catch (e) { setStatus(e.message); } });
document.getElementById('saveProfileBtn').addEventListener('click', async () => { try { await saveProfile(); } catch (e) { setStatus(e.message); } });
document.getElementById('saveProfileFromResumeBtn').addEventListener('click', async () => { try { await saveProfile(); } catch (e) { setStatus(e.message); } });
document.getElementById('generateResumeBtn').addEventListener('click', async () => { try { await generateResume(); } catch (e) { setStatus(e.message); } });
document.getElementById('scanBtn').addEventListener('click', async () => { try { await runScan(); } catch (e) { setStatus(e.message); } });
document.getElementById('refreshJobsBtn').addEventListener('click', async () => { try { await refreshJobs(); } catch (e) { setStatus(e.message); } });
document.getElementById('refreshDashBtn').addEventListener('click', async () => { try { await refreshDashboard(); } catch (e) { setStatus(e.message); } });

setAuthState();
syncPreview();
loadProfile().then(() => Promise.all([refreshJobs(), refreshDashboard()])).catch(() => {});
