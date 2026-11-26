(function () {
  "use strict";

  const THEME_KEY = "ai_books_theme";
  const FONT_SIZE_KEY = "ai_books_font_size";
  const PROGRESS_KEY = "ai_books_progress";

  // Elements
  const bookSwitcher = document.getElementById("bookSwitcher");
  const lessonIndicator = document.getElementById("lessonIndicator");
  const toggleSidebarBtn = document.getElementById("toggleSidebarBtn");
  const readerSidebar = document.getElementById("readerSidebar");
  const tabToc = document.getElementById("tabToc");
  const tabSearch = document.getElementById("tabSearch");
  const sidebarSearchInput = document.getElementById("sidebarSearchInput");
  const sidebarSearchResults = document.getElementById("sidebarSearchResults");
  const lessonContent = document.getElementById("lessonContent");
  const outlineList = document.getElementById("outlineList");
  const textReaderStage = document.getElementById("textReaderStage");

  // Controls
  const btnFontDec = document.getElementById("btnFontDec");
  const btnFontInc = document.getElementById("btnFontInc");
  const themeCycleBtn = document.getElementById("themeCycleBtn");
  const btnViewScan = document.getElementById("btnViewScan");
  const fullscreenBtn = document.getElementById("fullscreenBtn");

  // Scan modal
  const scanModal = document.getElementById("scanModal");
  const scanModalTitle = document.getElementById("scanModalTitle");
  const scanImage = document.getElementById("scanImage");
  const scanPageIndicator = document.getElementById("scanPageIndicator");
  const scanPrevBtn = document.getElementById("scanPrevBtn");
  const scanNextBtn = document.getElementById("scanNextBtn");
  const closeScanModal = document.getElementById("closeScanModal");

  // State
  const ASSET_VER = "20261126-v5";
  let books = [];
  let currentBookId = "lop-10";
  let currentBookMeta = null;
  let currentLessons = [];
  let currentLessonIndex = 0;
  let currentFontSize = 16.5;

  // Scan modal state
  let scanStartPage = 1;
  let scanEndPage = 1;
  let scanCurrentPage = 1;

  // Cache lessons
  const lessonsCache = new Map();

  function escapeHtml(str) {
    return (str || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function normalizeVi(str) {
    return (str || "")
      .toLowerCase()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .replace(/đ/g, "d");
  }

  // --- THEME ---
  function applyTheme(t) {
    const valid = ["light", "sepia", "dark"];
    const theme = valid.includes(t) ? t : "light";
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem(THEME_KEY, theme);
    const icons = { light: "☀️", sepia: "📜", dark: "🌙" };
    themeCycleBtn.textContent = icons[theme] || "☀️";
  }

  function cycleTheme() {
    const cur = document.documentElement.getAttribute("data-theme") || "light";
    const next = cur === "light" ? "sepia" : cur === "sepia" ? "dark" : "light";
    applyTheme(next);
  }

  themeCycleBtn.addEventListener("click", cycleTheme);
  applyTheme(localStorage.getItem(THEME_KEY) || "light");

  // --- FONT SIZE ---
  function setFontSize(size) {
    currentFontSize = Math.min(Math.max(14, size), 22);
    document.documentElement.style.setProperty("--reader-font-size", `${currentFontSize}px`);
    localStorage.setItem(FONT_SIZE_KEY, String(currentFontSize));
  }

  btnFontDec.addEventListener("click", () => setFontSize(currentFontSize - 1));
  btnFontInc.addEventListener("click", () => setFontSize(currentFontSize + 1));
  setFontSize(parseFloat(localStorage.getItem(FONT_SIZE_KEY)) || 16.5);

  // --- FULLSCREEN ---
  fullscreenBtn.addEventListener("click", () => {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(() => {});
    } else {
      document.exitFullscreen().catch(() => {});
    }
  });

  // --- SIDEBAR TOGGLE ---
  toggleSidebarBtn.addEventListener("click", () => {
    readerSidebar.classList.toggle("collapsed");
    toggleSidebarBtn.classList.toggle("active", !readerSidebar.classList.contains("collapsed"));
  });

  // --- SIDEBAR TABS ---
  document.querySelectorAll(".sidebar-tab").forEach((tab) => {
    tab.addEventListener("click", () => {
      document.querySelectorAll(".sidebar-tab").forEach((t) => t.classList.remove("active"));
      tab.classList.add("active");
      const target = tab.getAttribute("data-tab");
      tabToc.classList.toggle("active", target === "toc");
      tabSearch.classList.toggle("active", target === "search");
      if (target === "search") {
        sidebarSearchInput.focus();
      }
    });
  });

  // --- INIT ---
  async function init() {
    try {
      const res = await fetch(`data/books.json?v=${ASSET_VER}`);
      const data = await res.json();
      books = data.books || data;

      const urlParams = new URLSearchParams(window.location.search);
      const bParam = urlParams.get("book");
      if (bParam && books.some((b) => b.id === bParam)) {
        currentBookId = bParam;
      }

      currentBookMeta = books.find((b) => b.id === currentBookId) || books[0];

      renderBookSwitcher();
      await loadBook(currentBookId);

      // Handle lesson param or page param
      const lesParam = urlParams.get("lesson");
      const pageParam = parseInt(urlParams.get("page"), 10);

      if (lesParam) {
        const foundIdx = currentLessons.findIndex((l) => l.id === lesParam);
        if (foundIdx >= 0) {
          selectLesson(foundIdx);
          return;
        }
      }

      if (!isNaN(pageParam)) {
        const foundIdx = currentLessons.findIndex(
          (l) => pageParam >= l.startPage && pageParam <= l.endPage
        );
        if (foundIdx >= 0) {
          selectLesson(foundIdx);
          return;
        }
      }

      // Default to first real lesson (or first item)
      const firstBaiIdx = currentLessons.findIndex((l) => l.id.startsWith("bai-"));
      selectLesson(firstBaiIdx >= 0 ? firstBaiIdx : 0);
    } catch (err) {
      console.error("Init reader error:", err);
      lessonContent.innerHTML = `
        <div style="padding: 40px; color: #ef4444; text-align: center;">
          <h3>Không thể tải sách</h3>
          <p>${escapeHtml(err.message)}</p>
        </div>
      `;
    }
  }

  function renderBookSwitcher() {
    bookSwitcher.innerHTML = books
      .map(
        (b) => `
        <button class="book-tab ${b.id === currentBookId ? "active" : ""}" data-book="${b.id}">
          Lớp ${b.grade}
        </button>
      `
      )
      .join("");

    bookSwitcher.querySelectorAll(".book-tab").forEach((btn) => {
      btn.addEventListener("click", () => {
        const bid = btn.getAttribute("data-book");
        if (bid !== currentBookId) {
          switchBook(bid);
        }
      });
    });
  }

  async function switchBook(bookId) {
    currentBookId = bookId;
    currentBookMeta = books.find((b) => b.id === currentBookId) || books[0];
    renderBookSwitcher();

    // Update URL
    const url = new URL(window.location);
    url.searchParams.set("book", bookId);
    url.searchParams.delete("lesson");
    url.searchParams.delete("page");
    window.history.pushState({}, "", url);

    await loadBook(bookId);
    const firstBaiIdx = currentLessons.findIndex((l) => l.id.startsWith("bai-"));
    selectLesson(firstBaiIdx >= 0 ? firstBaiIdx : 0);
  }

  async function loadBook(bookId) {
    if (lessonsCache.has(bookId)) {
      currentLessons = lessonsCache.get(bookId);
    } else {
      const res = await fetch(`data/lessons-${bookId}.json?v=${ASSET_VER}`);
      currentLessons = await res.json();
      lessonsCache.set(bookId, currentLessons);
    }

    renderToC();
    setupSearch();
  }

  function renderToC() {
    // Group lessons by `group`
    const groups = new Map();
    currentLessons.forEach((les, idx) => {
      const g = les.group || "Chung";
      if (!groups.has(g)) {
        groups.set(g, []);
      }
      groups.get(g).push({ ...les, index: idx });
    });

    let html = "";
    for (const [groupTitle, items] of groups.entries()) {
      html += `
        <div class="toc-group">
          <div class="toc-group-title">
            <span>${escapeHtml(groupTitle)}</span>
          </div>
          <div class="toc-group-items">
            ${items
              .map(
                (it) => `
                <a class="toc-item ${it.index === currentLessonIndex ? "active" : ""}" 
                   href="#" data-index="${it.index}" id="toc-item-${it.index}">
                  <span class="toc-item-title">${escapeHtml(it.title)}</span>
                  <span class="toc-p">Tr.${it.startPage}</span>
                </a>
              `
              )
              .join("")}
          </div>
        </div>
      `;
    }

    tabToc.innerHTML = html;

    tabToc.querySelectorAll(".toc-item").forEach((link) => {
      link.addEventListener("click", (e) => {
        e.preventDefault();
        const idx = parseInt(link.getAttribute("data-index"), 10);
        selectLesson(idx);
        // Mobile auto collapse sidebar
        if (window.innerWidth <= 960) {
          readerSidebar.classList.add("collapsed");
          toggleSidebarBtn.classList.remove("active");
        }
      });
    });
  }

  function selectLesson(index) {
    if (index < 0 || index >= currentLessons.length) return;
    currentLessonIndex = index;
    const lesson = currentLessons[index];

    // Update active in ToC
    tabToc.querySelectorAll(".toc-item").forEach((el, idx) => {
      el.classList.toggle("active", idx === index);
    });

    const activeEl = document.getElementById(`toc-item-${index}`);
    if (activeEl) {
      activeEl.scrollIntoView({ block: "nearest", behavior: "smooth" });
    }

    // Update toolbar indicator
    lessonIndicator.textContent = `${currentBookMeta.title} · ${lesson.title}`;
    document.title = `${lesson.title} — ${currentBookMeta.title}`;

    // Update URL without reload
    const url = new URL(window.location);
    url.searchParams.set("book", currentBookId);
    url.searchParams.set("lesson", lesson.id);
    url.searchParams.delete("page");
    window.history.pushState({}, "", url);

    // Save reading progress
    try {
      const prog = JSON.parse(localStorage.getItem(PROGRESS_KEY) || "{}");
      prog[currentBookId] = {
        lessonId: lesson.id,
        lessonTitle: lesson.title,
        page: lesson.startPage,
        updatedAt: Date.now(),
      };
      localStorage.setItem(PROGRESS_KEY, JSON.stringify(prog));
    } catch {}

    // Prepare Scan button pages
    scanStartPage = lesson.startPage;
    scanEndPage = lesson.endPage;
    scanCurrentPage = lesson.startPage;

    // Render HTML content
    renderLessonBody(lesson, index);

    // Scroll to top of stage
    textReaderStage.scrollTop = 0;
  }

  function renderLessonBody(lesson, index) {
    let html = lesson.html || `<div class="lesson-p">${escapeHtml(lesson.summary)}</div>`;

    // Append Bottom Navigation
    const prevLesson = index > 0 ? currentLessons[index - 1] : null;
    const nextLesson = index + 1 < currentLessons.length ? currentLessons[index + 1] : null;

    let navHtml = '<nav class="lesson-bottom-nav">';
    if (prevLesson) {
      navHtml += `
        <a href="#" class="btn-lesson-nav nav-prev" data-target-index="${index - 1}">
          <span class="nav-dir-label">‹ Bài trước</span>
          <span class="nav-lesson-name">${escapeHtml(prevLesson.title)}</span>
        </a>
      `;
    } else {
      navHtml += `<div></div>`;
    }

    if (nextLesson) {
      navHtml += `
        <a href="#" class="btn-lesson-nav nav-next" data-target-index="${index + 1}">
          <span class="nav-dir-label">Bài tiếp theo ›</span>
          <span class="nav-lesson-name">${escapeHtml(nextLesson.title)}</span>
        </a>
      `;
    }
    navHtml += "</nav>";

    lessonContent.innerHTML = html + navHtml;

    // Attach bottom nav clicks
    lessonContent.querySelectorAll(".btn-lesson-nav").forEach((btn) => {
      btn.addEventListener("click", (e) => {
        e.preventDefault();
        const target = parseInt(btn.getAttribute("data-target-index"), 10);
        selectLesson(target);
      });
    });

    // Attach copy code buttons
    lessonContent.querySelectorAll(".btn-copy-code").forEach((btn) => {
      btn.addEventListener("click", () => {
        const pre = btn.closest(".code-block-wrapper").querySelector("code");
        if (pre) {
          navigator.clipboard.writeText(pre.innerText).then(() => {
            const old = btn.textContent;
            btn.textContent = "✓ Đã chép";
            setTimeout(() => (btn.textContent = old), 1800);
          });
        }
      });
    });

    // Attach click to zoom on lesson images
    lessonContent.querySelectorAll(".lesson-img").forEach((img) => {
      img.style.cursor = "zoom-in";
      img.title = "Bấm để xem phóng to";
      img.addEventListener("click", () => {
        scanImage.src = img.src;
        scanModalTitle.textContent = img.alt || "Hình minh hoạ bài học";
        scanPageIndicator.textContent = "Ảnh minh họa";
        scanPrevBtn.disabled = true;
        scanNextBtn.disabled = true;
        scanModal.classList.add("open");
      });
    });

    // Build Right Outline
    buildOutline();
  }

  function buildOutline() {
    const headings = lessonContent.querySelectorAll(
      ".section-badge-header, .subheading-h3"
    );
    if (!headings.length) {
      outlineList.innerHTML = '<li style="color:var(--text-soft); font-size:12.5px;">Toàn văn bài học</li>';
      return;
    }

    let outlineHtml = "";
    headings.forEach((h, i) => {
      const card = h.closest(".lesson-card");
      let id = card ? card.id : null;
      if (!id) {
        id = `heading-ref-${i}`;
        h.id = id;
      }
      const title = h.querySelector(".section-title")?.textContent || h.textContent;
      outlineHtml += `
        <li>
          <a class="outline-link" href="#${id}">${escapeHtml(title.trim())}</a>
        </li>
      `;
    });

    outlineList.innerHTML = outlineHtml;

    outlineList.querySelectorAll(".outline-link").forEach((link) => {
      link.addEventListener("click", (e) => {
        e.preventDefault();
        const targetId = link.getAttribute("href").slice(1);
        const targetEl = document.getElementById(targetId);
        if (targetEl) {
          targetEl.scrollIntoView({ behavior: "smooth", block: "start" });
          outlineList.querySelectorAll(".outline-link").forEach((l) => l.classList.remove("active"));
          link.classList.add("active");
        }
      });
    });
  }

  // --- SEARCH ---
  function setupSearch() {
    sidebarSearchInput.addEventListener("input", () => {
      const q = sidebarSearchInput.value.trim();
      if (!q) {
        sidebarSearchResults.innerHTML = "";
        return;
      }

      const qNorm = normalizeVi(q);
      const matches = [];

      currentLessons.forEach((les, idx) => {
        const titleNorm = normalizeVi(les.title);
        const textNorm = normalizeVi(les.summary + " " + (les.html || ""));

        let score = 0;
        if (titleNorm.includes(qNorm)) score += 10;
        if (textNorm.includes(qNorm)) score += 2;

        if (score > 0) {
          // Find matching excerpt
          let snippet = les.summary;
          const pos = textNorm.indexOf(qNorm);
          if (pos >= 0) {
            const rawText = les.summary;
            const start = Math.max(0, pos - 40);
            snippet = (start > 0 ? "..." : "") + rawText.slice(start, start + 120) + "...";
          }
          matches.push({ lesson: les, index: idx, snippet, score });
        }
      });

      matches.sort((a, b) => b.score - a.score);

      if (!matches.length) {
        sidebarSearchResults.innerHTML = `
          <div style="padding: 16px; color: var(--text-soft); font-size: 13px; text-align: center;">
            Không tìm thấy kết quả phù hợp cho "<strong>${escapeHtml(q)}</strong>"
          </div>
        `;
        return;
      }

      sidebarSearchResults.innerHTML = matches
        .map(
          (m) => `
          <div class="sidebar-search-item" data-index="${m.index}">
            <div style="font-weight: 700; font-size: 13.5px; color: var(--accent); margin-bottom: 4px;">
              ${escapeHtml(m.lesson.title)}
            </div>
            <div style="font-size: 12px; color: var(--text-muted); line-height: 1.5;">
              ${escapeHtml(m.snippet)}
            </div>
            <div style="font-size: 11px; color: var(--text-soft); margin-top: 4px;">
              ${escapeHtml(m.lesson.group)} · Trang ${m.lesson.startPage}
            </div>
          </div>
        `
        )
        .join("");

      sidebarSearchResults.querySelectorAll(".sidebar-search-item").forEach((el) => {
        el.addEventListener("click", () => {
          const idx = parseInt(el.getAttribute("data-index"), 10);
          selectLesson(idx);
          if (window.innerWidth <= 960) {
            readerSidebar.classList.add("collapsed");
            toggleSidebarBtn.classList.remove("active");
          }
        });
      });
    });
  }

  // --- SCAN MODAL (BẢN IN GỐC) ---
  window.openOriginalPages = function (startP, endP) {
    scanStartPage = startP;
    scanEndPage = endP;
    scanCurrentPage = startP;
    renderScanViewer();
    scanModal.classList.add("open");
  };

  btnViewScan.addEventListener("click", () => {
    window.openOriginalPages(scanStartPage, scanEndPage);
  });

  function renderScanViewer() {
    const pad = String(scanCurrentPage).padStart(3, "0");
    scanImage.src = `books/${currentBookId}/page-${pad}.webp`;
    scanModalTitle.textContent = `Bản in gốc — Trang ${scanCurrentPage} (${currentBookMeta.title})`;
    scanPageIndicator.textContent = `Trang ${scanCurrentPage} / ${scanEndPage}`;
    scanPrevBtn.disabled = scanCurrentPage <= scanStartPage;
    scanNextBtn.disabled = scanCurrentPage >= scanEndPage;
  }

  scanPrevBtn.addEventListener("click", () => {
    if (scanCurrentPage > scanStartPage) {
      scanCurrentPage--;
      renderScanViewer();
    }
  });

  scanNextBtn.addEventListener("click", () => {
    if (scanCurrentPage < scanEndPage) {
      scanCurrentPage++;
      renderScanViewer();
    }
  });

  closeScanModal.addEventListener("click", () => {
    scanModal.classList.remove("open");
  });

  scanModal.addEventListener("click", (e) => {
    if (e.target === scanModal) {
      scanModal.classList.remove("open");
    }
  });

  // Global Keyboard shortcuts
  window.addEventListener("keydown", (e) => {
    if (e.target.tagName === "INPUT" || e.target.tagName === "TEXTAREA") return;

    if (scanModal.classList.contains("open")) {
      if (e.key === "Escape") scanModal.classList.remove("open");
      if (e.key === "ArrowLeft") scanPrevBtn.click();
      if (e.key === "ArrowRight") scanNextBtn.click();
      return;
    }

    if (e.key === "t" || e.key === "T") {
      toggleSidebarBtn.click();
    }
    if (e.key === "ArrowLeft") {
      const prev = currentLessonIndex > 0 ? currentLessonIndex - 1 : null;
      if (prev !== null) selectLesson(prev);
    }
    if (e.key === "ArrowRight") {
      const next = currentLessonIndex + 1 < currentLessons.length ? currentLessonIndex + 1 : null;
      if (next !== null) selectLesson(next);
    }
  });

  init();
})();
