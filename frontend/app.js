const API_BASE = "http://127.0.0.1:8000";
const REFRESH_INTERVAL = 60; // seconds

// ── DOM Elements ──
const navBtns = document.querySelectorAll(".nav-btn");
const views = document.querySelectorAll(".view");
const sourcePills = document.querySelectorAll(".source-pill");
const sentenceSlider = document.getElementById("sentenceSlider");
const sentenceValue = document.getElementById("sentenceValue");
const customSlider = document.getElementById("customSlider");
const customSliderValue = document.getElementById("customSliderValue");
const articlesGrid = document.getElementById("articlesGrid");
const loadingState = document.getElementById("loadingState");
const emptyState = document.getElementById("emptyState");
const autoRefreshToggle = document.getElementById("autoRefresh");
const refreshTimerEl = document.getElementById("refreshTimer");
const countdownEl = document.getElementById("countdown");
const summarizeBtn = document.getElementById("summarizeBtn");
const customText = document.getElementById("customText");
const customResult = document.getElementById("customResult");
const customSummaryText = document.getElementById("customSummaryText");
const customLoading = document.getElementById("customLoading");

let currentSource = "all";
let countdownInterval = null;
let countdown = REFRESH_INTERVAL;

// ── Navigation ──
navBtns.forEach((btn) => {
  btn.addEventListener("click", () => {
    navBtns.forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");
    const target = btn.dataset.view;
    views.forEach((v) => v.classList.remove("active"));
    document.getElementById(target + "View").classList.add("active");
  });
});

// ── Source Selection ──
sourcePills.forEach((pill) => {
  pill.addEventListener("click", () => {
    sourcePills.forEach((p) => p.classList.remove("active"));
    pill.classList.add("active");
    currentSource = pill.dataset.source;
    fetchNews();
  });
});

// ── Sliders ──
sentenceSlider.addEventListener("input", () => {
  sentenceValue.textContent = sentenceSlider.value + " sentences";
});

customSlider.addEventListener("input", () => {
  customSliderValue.textContent = customSlider.value + " sentences";
});

// ── Fetch News ──
async function fetchNews() {
  articlesGrid.innerHTML = "";
  emptyState.classList.add("hidden");
  loadingState.classList.remove("hidden");

  const count = sentenceSlider.value;
  let url;
  if (currentSource === "all") {
    url = `${API_BASE}/news?sentence_count=${count}`;
  } else {
    url = `${API_BASE}/news/${currentSource}?sentence_count=${count}`;
  }

  try {
    const res = await fetch(url);
    if (!res.ok) throw new Error("Failed to fetch");
    const data = await res.json();

    loadingState.classList.add("hidden");

    if (!data.articles || data.articles.length === 0) {
      emptyState.classList.remove("hidden");
      return;
    }

    renderArticles(data.articles);
  } catch (err) {
    loadingState.classList.add("hidden");
    emptyState.classList.remove("hidden");
    console.error(err);
  }
}

// ── Render Articles ──
function renderArticles(articles) {
  articlesGrid.innerHTML = articles
    .map(
      (a) => `
    <article class="article-card">
      <div class="article-card-body">
        <div class="article-source">${escapeHtml(a.source)}</div>
        <h3 class="article-title">
          <a href="${escapeHtml(a.link)}" target="_blank" rel="noopener">${escapeHtml(a.title)}</a>
        </h3>
        <p class="article-summary">${escapeHtml(a.summary)}</p>
      </div>
      <div class="article-footer">
        <a href="${escapeHtml(a.link)}" target="_blank" rel="noopener" class="article-link">
          Read full article
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M7 17L17 7M17 7H7M17 7v10"/>
          </svg>
        </a>
      </div>
    </article>
  `
    )
    .join("");
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str || "";
  return div.innerHTML;
}

// ── Custom Summarize ──
summarizeBtn.addEventListener("click", async () => {
  const text = customText.value.trim();
  if (!text) return;

  summarizeBtn.disabled = true;
  customResult.classList.add("hidden");
  customLoading.classList.remove("hidden");

  try {
    const res = await fetch(`${API_BASE}/summarize`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        text: text,
        sentence_count: parseInt(customSlider.value),
      }),
    });

    if (!res.ok) throw new Error("Summarization failed");
    const data = await res.json();

    customLoading.classList.add("hidden");
    customSummaryText.textContent = data.summary;
    customResult.classList.remove("hidden");
  } catch (err) {
    customLoading.classList.add("hidden");
    customSummaryText.textContent = "Something went wrong. Please try again.";
    customResult.classList.remove("hidden");
    console.error(err);
  } finally {
    summarizeBtn.disabled = false;
  }
});

// ── Auto Refresh ──
autoRefreshToggle.addEventListener("change", () => {
  if (autoRefreshToggle.checked) {
    startAutoRefresh();
  } else {
    stopAutoRefresh();
  }
});

function startAutoRefresh() {
  countdown = REFRESH_INTERVAL;
  refreshTimerEl.classList.remove("hidden");
  updateCountdown();

  countdownInterval = setInterval(() => {
    countdown--;
    updateCountdown();
    if (countdown <= 0) {
      countdown = REFRESH_INTERVAL;
      fetchNews();
    }
  }, 1000);
}

function stopAutoRefresh() {
  clearInterval(countdownInterval);
  refreshTimerEl.classList.add("hidden");
}

function updateCountdown() {
  countdownEl.textContent = countdown;
}

// ── Initial Load ──
fetchNews();
