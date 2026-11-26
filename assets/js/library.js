(function () {
  const THEME_KEY = "ai_books_theme";
  const PROGRESS_KEY = "ai_books_progress";

  const booksGrid = document.getElementById("booksGrid");
  const searchInput = document.getElementById("globalSearchInput");
  const searchResults = document.getElementById("globalSearchResults");
  const themeBtn = document.getElementById("themeToggleBtn");
  const themeIcon = document.getElementById("themeIcon");
  const tocModal = document.getElementById("tocModal");
  const tocModalTitle = document.getElementById("tocModalTitle");
  const tocModalBody = document.getElementById("tocModalBody");
  const closeTocModal = document.getElementById("closeTocModal");

  let books = [];
  const searchCache = new Map();

  function normalizeVi(str) {
    return (str || "")
      .toLowerCase()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .replace(/đ/g, "d");
  }

  function escapeHtml(str) {
    return (str || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function applyTheme(theme) {
    const t = theme === "dark" ? "dark" : "light";
    document.documentElement.setAttribute("data-theme", t);
    localStorage.setItem(THEME_KEY, t);
    themeIcon.textContent = t === "dark" ? "☀️" : "🌙";
  }

  applyTheme(localStorage.getItem(THEME_KEY) || "light");
  themeBtn.addEventListener("click", () => {
    const cur = document.documentElement.getAttribute("data-theme");
    applyTheme(cur === "dark" ? "light" : "dark");
  });

  function getProgressMap() {
    try {
      return JSON.parse(localStorage.getItem(PROGRESS_KEY) || "{}");
    } catch {
      return {};
    }
  }

  function countLessons(book) {
    let count = 0;
    for (const grp of book.toc || []) {
      if (grp.group.startsWith("Chủ đề")) {
        count += (grp.items || []).length;
      }
    }
    return count;
  }

  function countTopics(book) {
    return (book.toc || []).filter((g) => g.group.startsWith("Chủ đề")).length;
  }

  function renderBooks() {
    const progress = getProgressMap();
    let totalLessons = 0;
    let totalPages = 0;

    booksGrid.innerHTML = books
      .map((book) => {
        const lessons = countLessons(book);
        const topics = countTopics(book);
        totalLessons += lessons;
        totalPages += book.pages || 90;

        const saved = progress[book.id];
        const readHref = saved && saved.lessonId 
          ? `reader.html?book=${encodeURIComponent(book.id)}&lesson=${encodeURIComponent(saved.lessonId)}`
          : `reader.html?book=${encodeURIComponent(book.id)}`;
        const readLabel = saved && saved.lessonTitle ? `Tiếp tục: ${escapeHtml(saved.lessonTitle)}` : "Đọc sách HTML";

        return `
          <article class="book-card">
            <div class="book-cover-stage" style="background: ${book.accentSoft};">
              <span class="grade-badge" style="background: ${book.accent};">Lớp ${book.grade}</span>
              <a class="book-cover-link" href="${readHref}" aria-label="Mở ${escapeHtml(book.title)}">
                <img src="${book.cover}" alt="Bìa ${escapeHtml(book.title)}" loading="eager" />
              </a>
            </div>
            <div class="book-info">
              <h2>${escapeHtml(book.title)}</h2>
              <p class="book-authors">${escapeHtml(book.authors)}<br/>${escapeHtml(book.publisher)} · ISBN ${escapeHtml(book.isbn)}</p>
              <div class="book-meta-pills">
                <span class="meta-pill">📖 Sách chữ HTML</span>
                <span class="meta-pill">${topics} chủ đề</span>
                <span class="meta-pill">${lessons} bài học</span>
              </div>
            </div>
            <div class="book-actions">
              <a class="btn-primary" style="background: ${book.accent};" href="${readHref}">
                ${readLabel}
              </a>
              <button class="btn-secondary" data-open-toc="${book.id}">Mục lục</button>
            </div>
          </article>
        `;
      })
      .join("");

    document.getElementById("statLessons").textContent = String(totalLessons);
    document.getElementById("statPages").textContent = String(totalPages);

    booksGrid.querySelectorAll("[data-open-toc]").forEach((btn) => {
      btn.addEventListener("click", () => openTocModal(btn.getAttribute("data-open-toc")));
    });
  }

  function openTocModal(bookId) {
    const book = books.find((b) => b.id === bookId);
    if (!book) return;
    tocModalTitle.textContent = `Mục lục — ${book.title}`;
    tocModalBody.innerHTML = (book.toc || [])
      .map((grp) => {
        const groupHeader = grp.page
          ? `<a class="toc-group-title" href="reader.html?book=${book.id}&page=${grp.page}">
               <span>${escapeHtml(grp.group)}</span>
               <span class="toc-p">Tr. ${grp.printPage ?? grp.page}</span>
             </a>`
          : `<div class="toc-group-title"><span>${escapeHtml(grp.group)}</span></div>`;

        const items = (grp.items || [])
          .map(
            (it) => `
              <a class="toc-item" href="reader.html?book=${book.id}&lesson=${it.id || ''}&page=${it.page}">
                <span>${escapeHtml(it.title)}</span>
                <span class="toc-p">${it.printPage ? `Tr. ${it.printPage}` : `Tr. ${it.page}`}</span>
              </a>
            `
          )
          .join("");

        return `<div class="toc-group">${groupHeader}${items}</div>`;
      })
      .join("");
    tocModal.classList.add("open");
  }

  closeTocModal.addEventListener("click", () => tocModal.classList.remove("open"));
  tocModal.addEventListener("click", (e) => {
    if (e.target === tocModal) tocModal.classList.remove("open");
  });

  async function ensureSearchData(bookId) {
    if (searchCache.has(bookId)) return searchCache.get(bookId);
    const res = await fetch(`data/search-${bookId}.json`);
    const docs = await res.json();
    const indexed = docs.map((d) => ({
      ...d,
      norm: normalizeVi(d.t),
    }));
    searchCache.set(bookId, indexed);
    return indexed;
  }

  function makeSnippet(rawText, query) {
    const normText = normalizeVi(rawText);
    const normQuery = normalizeVi(query);
    const idx = normText.indexOf(normQuery);
    if (idx === -1) return escapeHtml(rawText.slice(0, 120));
    const start = Math.max(0, idx - 42);
    const end = Math.min(rawText.length, idx + query.length + 78);
    const before = escapeHtml(rawText.slice(start, idx));
    const match = escapeHtml(rawText.slice(idx, idx + query.length));
    const after = escapeHtml(rawText.slice(idx + query.length, end));
    return `${start > 0 ? "..." : ""}${before}<mark>${match}</mark>${after}${end < rawText.length ? "..." : ""}`;
  }

  let searchTimer = null;
  searchInput.addEventListener("input", () => {
    clearTimeout(searchTimer);
    const q = searchInput.value.trim();
    if (q.length < 2) {
      searchResults.classList.remove("open");
      searchResults.innerHTML = "";
      return;
    }
    searchTimer = setTimeout(() => runGlobalSearch(q), 180);
  });

  async function runGlobalSearch(q) {
    const normQ = normalizeVi(q);
    searchResults.innerHTML = `<div class="search-result-item"><span class="search-result-snippet">Đang tìm "${escapeHtml(q)}"...</span></div>`;
    searchResults.classList.add("open");

    const allData = await Promise.all(books.map((b) => ensureSearchData(b.id).then((docs) => ({ book: b, docs }))));
    const hits = [];

    for (const { book, docs } of allData) {
      for (const doc of docs) {
        if (doc.norm.includes(normQ)) {
          hits.push({ book, doc });
          if (hits.length >= 24) break;
        }
      }
      if (hits.length >= 24) break;
    }

    if (!hits.length) {
      searchResults.innerHTML = `<div class="search-result-item"><span class="search-result-snippet">Không tìm thấy kết quả phù hợp cho "${escapeHtml(q)}".</span></div>`;
      return;
    }

    searchResults.innerHTML = hits
      .map(
        ({ book, doc }) => `
        <a class="search-result-item" href="reader.html?book=${book.id}&page=${doc.p}">
          <div class="search-result-meta">
            <span>${escapeHtml(book.title)}</span>
            <span>${escapeHtml(doc.label)}</span>
          </div>
          <div class="search-result-snippet">${makeSnippet(doc.t, q)}</div>
        </a>
      `
      )
      .join("");
  }

  document.addEventListener("click", (e) => {
    if (!e.target.closest(".global-search-wrap")) {
      searchResults.classList.remove("open");
    }
  });

  document.addEventListener("keydown", (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") {
      e.preventDefault();
      searchInput.focus();
      searchInput.select();
    } else if (e.key === "Escape") {
      searchResults.classList.remove("open");
      tocModal.classList.remove("open");
    }
  });

  fetch("data/books.json")
    .then((r) => r.json())
    .then((data) => {
      books = data.books || [];
      renderBooks();
    })
    .catch((err) => {
      booksGrid.innerHTML = `<p>Không tải được danh sách sách: ${escapeHtml(err.message)}</p>`;
    });
})();
