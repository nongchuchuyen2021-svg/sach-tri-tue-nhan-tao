(function () {
  const THEME_KEY = "ai_books_theme";
  const PROGRESS_KEY = "ai_books_progress";
  const BOOKMARKS_KEY = "ai_books_bookmarks";
  const THEMES = ["light", "sepia", "dark"];
  const THEME_ICONS = { light: "☀️", sepia: "📜", dark: "🌙" };

  const el = {
    bookSwitcher: document.getElementById("bookSwitcher"),
    toggleSidebarBtn: document.getElementById("toggleSidebarBtn"),
    sidebar: document.getElementById("readerSidebar"),
    lessonIndicator: document.getElementById("lessonIndicator"),
    pageJumpInput: document.getElementById("pageJumpInput"),
    pageTotalLabel: document.getElementById("pageTotalLabel"),
    modeTwoBtn: document.getElementById("modeTwoBtn"),
    modeOneBtn: document.getElementById("modeOneBtn"),
    modeScrollBtn: document.getElementById("modeScrollBtn"),
    zoomOutBtn: document.getElementById("zoomOutBtn"),
    zoomResetBtn: document.getElementById("zoomResetBtn"),
    zoomInBtn: document.getElementById("zoomInBtn"),
    zoomLabel: document.getElementById("zoomLabel"),
    bookmarkBtn: document.getElementById("bookmarkBtn"),
    gridBtn: document.getElementById("gridBtn"),
    themeCycleBtn: document.getElementById("themeCycleBtn"),
    fullscreenBtn: document.getElementById("fullscreenBtn"),
    tabToc: document.getElementById("tabToc"),
    tabSearch: document.getElementById("tabSearch"),
    tabBookmarks: document.getElementById("tabBookmarks"),
    sidebarSearchInput: document.getElementById("sidebarSearchInput"),
    sidebarSearchResults: document.getElementById("sidebarSearchResults"),
    stage: document.getElementById("readerStage"),
    spreadContainer: document.getElementById("spreadContainer"),
    prevBtn: document.getElementById("prevBtn"),
    nextBtn: document.getElementById("nextBtn"),
    bottomPrevBtn: document.getElementById("bottomPrevBtn"),
    bottomNextBtn: document.getElementById("bottomNextBtn"),
    scrubber: document.getElementById("pageScrubber"),
    bottomInfo: document.getElementById("bottomInfo"),
    gridModal: document.getElementById("gridModal"),
    gridModalTitle: document.getElementById("gridModalTitle"),
    closeGridModal: document.getElementById("closeGridModal"),
    thumbsGrid: document.getElementById("thumbsGrid"),
  };

  let books = [];
  let currentBook = null;
  let currentPage = 1;
  let viewMode = window.innerWidth >= 960 ? "two" : "one";
  let zoom = 100;
  let spreads = [];
  const searchCache = new Map();
  let scrollObserver = null;
  let isSyncingScroll = false;

  function pad3(n) {
    return String(n).padStart(3, "0");
  }

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
    const t = THEMES.includes(theme) ? theme : "light";
    document.documentElement.setAttribute("data-theme", t);
    localStorage.setItem(THEME_KEY, t);
    el.themeCycleBtn.textContent = THEME_ICONS[t];
  }

  applyTheme(localStorage.getItem(THEME_KEY) || "light");
  el.themeCycleBtn.addEventListener("click", () => {
    const cur = document.documentElement.getAttribute("data-theme") || "light";
    const next = THEMES[(THEMES.indexOf(cur) + 1) % THEMES.length];
    applyTheme(next);
  });

  function buildSpreads(book) {
    const list = [];
    const start = book.firstSpreadStart || 2;
    for (let p = 1; p < start; p++) {
      list.push([p]);
    }
    for (let p = start; p <= book.pages; p += 2) {
      if (p + 1 <= book.pages) {
        list.push([p, p + 1]);
      } else {
        list.push([p]);
      }
    }
    return list;
  }

  function findSpreadIndex(page) {
    for (let i = 0; i < spreads.length; i++) {
      if (spreads[i].includes(page)) return i;
    }
    return 0;
  }

  function getFlatTocEntries(book) {
    const entries = [];
    for (const grp of book.toc || []) {
      if (grp.page) {
        entries.push({ title: grp.group, page: grp.page, printPage: grp.printPage });
      }
      for (const it of grp.items || []) {
        entries.push({ title: it.title, page: it.page, printPage: it.printPage });
      }
    }
    entries.sort((a, b) => a.page - b.page);
    return entries;
  }

  function findCurrentSection(page) {
    const entries = getFlatTocEntries(currentBook);
    let active = entries[0] || { title: currentBook.title, page: 1 };
    for (const item of entries) {
      if (item.page <= page) active = item;
      else break;
    }
    return active;
  }

  function formatPageLabel(page) {
    if (!currentBook) return `Trang ${page}`;
    if (page === 1) return "Bìa trước";
    if (page === currentBook.pages) return "Bìa sau";
    if (currentBook.pageOffset === 2 && page === 2) return "Công văn thẩm định";
    if (currentBook.pageOffset === 2 && page === 3) return "Bìa lót";
    if (currentBook.pageOffset === 1 && page === 2) return "Bìa lót";
    return `Trang in ${page - currentBook.pageOffset}`;
  }

  function saveProgress() {
    if (!currentBook) return;
    try {
      const map = JSON.parse(localStorage.getItem(PROGRESS_KEY) || "{}");
      map[currentBook.id] = { page: currentPage, updatedAt: Date.now() };
      localStorage.setItem(PROGRESS_KEY, JSON.stringify(map));
    } catch {
      /* ignore */
    }
  }

  function getBookmarks() {
    try {
      const all = JSON.parse(localStorage.getItem(BOOKMARKS_KEY) || "{}");
      return all[currentBook.id] || [];
    } catch {
      return [];
    }
  }

  function setBookmarks(list) {
    try {
      const all = JSON.parse(localStorage.getItem(BOOKMARKS_KEY) || "{}");
      all[currentBook.id] = list;
      localStorage.setItem(BOOKMARKS_KEY, JSON.stringify(all));
    } catch {
      /* ignore */
    }
  }

  function updateBookmarkUI() {
    const bms = getBookmarks();
    const active = bms.some((b) => b.page === currentPage);
    el.bookmarkBtn.textContent = active ? "★" : "☆";
    el.bookmarkBtn.classList.toggle("active", active);
    renderBookmarksTab();
  }

  function renderBookmarksTab() {
    if (!currentBook) return;
    const bms = getBookmarks().sort((a, b) => a.page - b.page);
    if (!bms.length) {
      el.tabBookmarks.innerHTML = `<p style="font-size:13px;color:var(--text-soft);">Chưa có trang nào được đánh dấu. Nhấn nút ☆ hoặc phím <kbd>B</kbd> để lưu nhanh trang đang đọc.</p>`;
      return;
    }
    el.tabBookmarks.innerHTML = bms
      .map(
        (b) => `
        <div class="sidebar-search-item" style="display:flex;align-items:center;justify-content:space-between;gap:8px;">
          <button style="text-align:left;flex:1;" data-jump-page="${b.page}">
            <div style="font-size:12px;font-weight:700;color:var(--accent);">${escapeHtml(formatPageLabel(b.page))} (Ảnh ${b.page})</div>
            <div style="font-size:13px;color:var(--text-muted);margin-top:2px;">${escapeHtml(b.title)}</div>
          </button>
          <button class="icon-btn" style="height:28px;min-width:28px;padding:0;" data-del-bm="${b.page}" title="Xoá đánh dấu">✕</button>
        </div>
      `
      )
      .join("");

    el.tabBookmarks.querySelectorAll("[data-jump-page]").forEach((btn) => {
      btn.addEventListener("click", () => goToPage(Number(btn.dataset.jumpPage)));
    });
    el.tabBookmarks.querySelectorAll("[data-del-bm]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const p = Number(btn.dataset.delBm);
        setBookmarks(getBookmarks().filter((x) => x.page !== p));
        updateBookmarkUI();
      });
    });
  }

  function renderBookSwitcher() {
    el.bookSwitcher.innerHTML = books
      .map(
        (b) => `
        <button class="book-tab ${b.id === currentBook.id ? "active" : ""}" data-book-id="${b.id}">
          Lớp ${b.grade}
        </button>
      `
      )
      .join("");
    el.bookSwitcher.querySelectorAll("[data-book-id]").forEach((btn) => {
      btn.addEventListener("click", () => switchBook(btn.dataset.bookId, 1));
    });
  }

  function renderToc() {
    const activeSec = findCurrentSection(currentPage);
    el.tabToc.innerHTML = (currentBook.toc || [])
      .map((grp) => {
        const grpActive = grp.page && activeSec.page === grp.page ? "active" : "";
        const grpHtml = grp.page
          ? `<button class="toc-group-title ${grpActive}" style="width:100%;" data-toc-page="${grp.page}">
               <span>${escapeHtml(grp.group)}</span>
               <span class="toc-p">Tr.${grp.printPage ?? grp.page}</span>
             </button>`
          : `<div class="toc-group-title"><span>${escapeHtml(grp.group)}</span></div>`;

        const itemsHtml = (grp.items || [])
          .map((it) => {
            const isAct = activeSec.page === it.page ? "active" : "";
            return `
              <button class="toc-item ${isAct}" style="width:100%;text-align:left;" data-toc-page="${it.page}">
                <span>${escapeHtml(it.title)}</span>
                <span class="toc-p">${it.printPage ? `Tr.${it.printPage}` : `Ảnh ${it.page}`}</span>
              </button>
            `;
          })
          .join("");

        return `<div class="toc-group">${grpHtml}${itemsHtml}</div>`;
      })
      .join("");

    el.tabToc.querySelectorAll("[data-toc-page]").forEach((btn) => {
      btn.addEventListener("click", () => {
        goToPage(Number(btn.dataset.tocPage));
        if (window.innerWidth < 960) el.sidebar.classList.add("collapsed");
      });
    });
  }

  function highlightActiveToc() {
    const activeSec = findCurrentSection(currentPage);
    el.tabToc.querySelectorAll("[data-toc-page]").forEach((btn) => {
      const p = Number(btn.dataset.tocPage);
      const isAct = p === activeSec.page;
      btn.classList.toggle("active", isAct);
      if (isAct) {
        btn.scrollIntoView({ block: "nearest" });
      }
    });
    el.lessonIndicator.textContent = activeSec.title;
  }

  function preloadAround(page) {
    const candidates = [page - 2, page - 1, page + 1, page + 2, page + 3];
    for (const p of candidates) {
      if (p >= 1 && p <= currentBook.pages) {
        const img = new Image();
        img.src = `books/${currentBook.id}/page-${pad3(p)}.webp`;
      }
    }
  }

  function applyZoom() {
    el.zoomLabel.textContent = `${zoom}%`;
    const isZoomed = zoom > 100 && viewMode !== "scroll";
    el.stage.classList.toggle("zoomed", isZoomed);

    if (viewMode === "scroll") {
      el.spreadContainer.style.transform = "";
      return;
    }

    const imgs = el.spreadContainer.querySelectorAll(".page-img");
    imgs.forEach((img) => {
      if (zoom === 100) {
        img.style.height = "";
      } else {
        img.style.height = `calc((100dvh - 134px) * ${zoom / 100})`;
      }
    });
  }

  function renderStage(animate = false) {
    el.modeTwoBtn.classList.toggle("active", viewMode === "two");
    el.modeOneBtn.classList.toggle("active", viewMode === "one");
    el.modeScrollBtn.classList.toggle("active", viewMode === "scroll");

    el.stage.classList.toggle("scroll-mode", viewMode === "scroll");
    el.prevBtn.style.display = viewMode === "scroll" ? "none" : "flex";
    el.nextBtn.style.display = viewMode === "scroll" ? "none" : "flex";

    if (scrollObserver) {
      scrollObserver.disconnect();
      scrollObserver = null;
    }

    if (viewMode === "scroll") {
      renderScrollMode();
      return;
    }

    let pair = [currentPage];
    if (viewMode === "two") {
      const sIdx = findSpreadIndex(currentPage);
      pair = spreads[sIdx] || [currentPage];
      currentPage = pair[0];
    }

    const cls = pair.length === 2 ? "spread-container spread-pair" : "spread-container spread-single";
    el.spreadContainer.className = cls + (animate ? " flipping" : "");

    el.spreadContainer.innerHTML = pair
      .map(
        (p) => `
        <div class="book-page-frame">
          <img class="page-img" src="books/${currentBook.id}/page-${pad3(p)}.webp" alt="${escapeHtml(currentBook.title)} - ${escapeHtml(formatPageLabel(p))}" draggable="false" />
        </div>
      `
      )
      .join("");

    if (animate) {
      requestAnimationFrame(() => {
        setTimeout(() => el.spreadContainer.classList.remove("flipping"), 40);
      });
    }

    applyZoom();
    updateNavButtons(pair);
    preloadAround(currentPage);
  }

  function renderScrollMode() {
    el.spreadContainer.className = "scroll-stack";
    const cards = [];
    for (let p = 1; p <= currentBook.pages; p++) {
      cards.push(`
        <div class="scroll-page-card" data-scroll-page="${p}">
          <span class="scroll-page-tag">${escapeHtml(formatPageLabel(p))}</span>
          <img src="books/${currentBook.id}/thumbs/page-${pad3(p)}.webp" data-full="books/${currentBook.id}/page-${pad3(p)}.webp" alt="Trang ${p}" loading="lazy" />
        </div>
      `);
    }
    el.spreadContainer.innerHTML = cards.join("");

    const cardEls = el.spreadContainer.querySelectorAll(".scroll-page-card");
    scrollObserver = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          const p = Number(entry.target.dataset.scrollPage);
          if (entry.isIntersecting) {
            const img = entry.target.querySelector("img");
            if (img && img.dataset.full && img.getAttribute("src") !== img.dataset.full) {
              img.setAttribute("src", img.dataset.full);
            }
            if (!isSyncingScroll && entry.intersectionRatio >= 0.35) {
              currentPage = p;
              updatePageIndicators(false);
            }
          }
        }
      },
      { root: el.stage, threshold: [0.05, 0.35] }
    );
    cardEls.forEach((c) => scrollObserver.observe(c));

    // Jump to currentPage
    const target = el.spreadContainer.querySelector(`[data-scroll-page="${currentPage}"]`);
    if (target) {
      isSyncingScroll = true;
      target.scrollIntoView({ behavior: "auto", block: "start" });
      setTimeout(() => {
        isSyncingScroll = false;
      }, 250);
    }
    updatePageIndicators(false);
  }

  function updateNavButtons(pair) {
    if (viewMode === "two") {
      const idx = findSpreadIndex(currentPage);
      el.prevBtn.disabled = idx <= 0;
      el.nextBtn.disabled = idx >= spreads.length - 1;
    } else {
      el.prevBtn.disabled = currentPage <= 1;
      el.nextBtn.disabled = currentPage >= currentBook.pages;
    }
    el.bottomPrevBtn.disabled = el.prevBtn.disabled;
    el.bottomNextBtn.disabled = el.nextBtn.disabled;
    updatePageIndicators(true, pair);
  }

  function updatePageIndicators(syncUrl = true, pair = null) {
    el.pageJumpInput.value = String(currentPage);
    el.pageJumpInput.max = String(currentBook.pages);
    el.pageTotalLabel.textContent = `/ ${currentBook.pages}`;
    el.scrubber.max = String(currentBook.pages);
    el.scrubber.value = String(currentPage);

    if (pair && pair.length === 2) {
      el.bottomInfo.textContent = `${formatPageLabel(pair[0])} – ${formatPageLabel(pair[1])} (Ảnh ${pair[0]}–${pair[1]}/${currentBook.pages})`;
    } else {
      el.bottomInfo.textContent = `${formatPageLabel(currentPage)} (Ảnh ${currentPage}/${currentBook.pages})`;
    }

    document.title = `${currentBook.title} · ${formatPageLabel(currentPage)}`;
    highlightActiveToc();
    updateBookmarkUI();
    saveProgress();

    if (syncUrl) {
      const url = new URL(window.location.href);
      url.searchParams.set("book", currentBook.id);
      url.searchParams.set("page", String(currentPage));
      history.replaceState(null, "", url.toString());
    }
  }

  function goToPage(page, animate = true) {
    if (!currentBook) return;
    const p = Math.min(Math.max(1, page), currentBook.pages);
    currentPage = p;

    if (viewMode === "scroll") {
      const target = el.spreadContainer.querySelector(`[data-scroll-page="${p}"]`);
      if (target) {
        isSyncingScroll = true;
        target.scrollIntoView({ behavior: "smooth", block: "start" });
        setTimeout(() => {
          isSyncingScroll = false;
        }, 400);
      }
      updatePageIndicators(true);
      return;
    }

    el.stage.scrollTop = 0;
    el.stage.scrollLeft = 0;
    renderStage(animate);
  }

  function stepPage(delta) {
    if (!currentBook) return;
    if (viewMode === "two") {
      const idx = findSpreadIndex(currentPage);
      const nextIdx = Math.min(Math.max(0, idx + delta), spreads.length - 1);
      if (nextIdx !== idx) {
        goToPage(spreads[nextIdx][0], true);
      }
    } else {
      goToPage(currentPage + delta, true);
    }
  }

  function switchBook(bookId, startPage = null) {
    const found = books.find((b) => b.id === bookId) || books[0];
    if (!found) return;
    currentBook = found;
    document.documentElement.style.setProperty("--accent", currentBook.accent);
    document.documentElement.style.setProperty("--accent-soft", currentBook.accentSoft);
    spreads = buildSpreads(currentBook);

    if (startPage !== null) {
      currentPage = Math.min(Math.max(1, startPage), currentBook.pages);
    } else {
      try {
        const map = JSON.parse(localStorage.getItem(PROGRESS_KEY) || "{}");
        currentPage = map[currentBook.id]?.page || 1;
      } catch {
        currentPage = 1;
      }
    }

    renderBookSwitcher();
    renderToc();
    el.sidebarSearchResults.innerHTML = "";
    el.sidebarSearchInput.value = "";
    renderStage(false);
  }

  // Controls
  el.prevBtn.addEventListener("click", () => stepPage(-1));
  el.nextBtn.addEventListener("click", () => stepPage(1));
  el.bottomPrevBtn.addEventListener("click", () => stepPage(-1));
  el.bottomNextBtn.addEventListener("click", () => stepPage(1));

  el.scrubber.addEventListener("input", () => {
    goToPage(Number(el.scrubber.value), false);
  });

  el.pageJumpInput.addEventListener("change", () => {
    goToPage(Number(el.pageJumpInput.value) || 1, true);
  });

  el.modeTwoBtn.addEventListener("click", () => {
    viewMode = "two";
    renderStage(false);
  });
  el.modeOneBtn.addEventListener("click", () => {
    viewMode = "one";
    renderStage(false);
  });
  el.modeScrollBtn.addEventListener("click", () => {
    viewMode = "scroll";
    renderStage(false);
  });

  el.zoomOutBtn.addEventListener("click", () => {
    zoom = Math.max(50, zoom - 15);
    applyZoom();
  });
  el.zoomInBtn.addEventListener("click", () => {
    zoom = Math.min(250, zoom + 15);
    applyZoom();
  });
  el.zoomResetBtn.addEventListener("click", () => {
    zoom = 100;
    applyZoom();
  });

  el.toggleSidebarBtn.addEventListener("click", () => {
    const collapsed = el.sidebar.classList.toggle("collapsed");
    el.toggleSidebarBtn.classList.toggle("active", !collapsed);
  });

  document.querySelectorAll(".sidebar-tab").forEach((tabBtn) => {
    tabBtn.addEventListener("click", () => {
      const target = tabBtn.dataset.tab;
      document.querySelectorAll(".sidebar-tab").forEach((b) => b.classList.toggle("active", b === tabBtn));
      el.tabToc.classList.toggle("active", target === "toc");
      el.tabSearch.classList.toggle("active", target === "search");
      el.tabBookmarks.classList.toggle("active", target === "bookmarks");
      if (target === "search") {
        setTimeout(() => el.sidebarSearchInput.focus(), 50);
      }
    });
  });

  el.bookmarkBtn.addEventListener("click", () => {
    const bms = getBookmarks();
    const exists = bms.some((b) => b.page === currentPage);
    if (exists) {
      setBookmarks(bms.filter((b) => b.page !== currentPage));
    } else {
      const sec = findCurrentSection(currentPage);
      bms.push({ page: currentPage, title: sec.title });
      setBookmarks(bms);
    }
    updateBookmarkUI();
  });

  // Thumbnail grid
  el.gridBtn.addEventListener("click", () => {
    el.gridModalTitle.textContent = `Tất cả ${currentBook.pages} trang — ${currentBook.title}`;
    const tiles = [];
    for (let p = 1; p <= currentBook.pages; p++) {
      tiles.push(`
        <button class="thumb-tile ${p === currentPage ? "active" : ""}" data-grid-page="${p}">
          <img src="books/${currentBook.id}/thumbs/page-${pad3(p)}.webp" alt="Trang ${p}" loading="lazy" />
          <span>${escapeHtml(formatPageLabel(p))}</span>
        </button>
      `);
    }
    el.thumbsGrid.innerHTML = tiles.join("");
    el.thumbsGrid.querySelectorAll("[data-grid-page]").forEach((btn) => {
      btn.addEventListener("click", () => {
        el.gridModal.classList.remove("open");
        goToPage(Number(btn.dataset.gridPage), false);
      });
    });
    el.gridModal.classList.add("open");
  });

  el.closeGridModal.addEventListener("click", () => el.gridModal.classList.remove("open"));
  el.gridModal.addEventListener("click", (e) => {
    if (e.target === el.gridModal) el.gridModal.classList.remove("open");
  });

  el.fullscreenBtn.addEventListener("click", () => {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen?.();
    } else {
      document.exitFullscreen?.();
    }
  });

  // Search inside current book
  async function ensureBookSearch(bookId) {
    if (searchCache.has(bookId)) return searchCache.get(bookId);
    const res = await fetch(`data/search-${bookId}.json`);
    const docs = await res.json();
    const indexed = docs.map((d) => ({ ...d, norm: normalizeVi(d.t) }));
    searchCache.set(bookId, indexed);
    return indexed;
  }

  function makeSnippet(rawText, query) {
    const normText = normalizeVi(rawText);
    const normQuery = normalizeVi(query);
    const idx = normText.indexOf(normQuery);
    if (idx === -1) return escapeHtml(rawText.slice(0, 110));
    const start = Math.max(0, idx - 36);
    const end = Math.min(rawText.length, idx + query.length + 74);
    const before = escapeHtml(rawText.slice(start, idx));
    const match = escapeHtml(rawText.slice(idx, idx + query.length));
    const after = escapeHtml(rawText.slice(idx + query.length, end));
    return `${start > 0 ? "..." : ""}${before}<mark>${match}</mark>${after}${end < rawText.length ? "..." : ""}`;
  }

  let searchDebounce = null;
  el.sidebarSearchInput.addEventListener("input", () => {
    clearTimeout(searchDebounce);
    const q = el.sidebarSearchInput.value.trim();
    if (q.length < 2) {
      el.sidebarSearchResults.innerHTML = "";
      return;
    }
    searchDebounce = setTimeout(async () => {
      const docs = await ensureBookSearch(currentBook.id);
      const normQ = normalizeVi(q);
      const hits = docs.filter((d) => d.norm.includes(normQ)).slice(0, 40);
      if (!hits.length) {
        el.sidebarSearchResults.innerHTML = `<p style="font-size:13px;color:var(--text-soft);">Không tìm thấy "${escapeHtml(q)}".</p>`;
        return;
      }
      el.sidebarSearchResults.innerHTML =
        `<div style="font-size:12px;color:var(--text-soft);margin-bottom:8px;">Tìm thấy ${hits.length}${hits.length === 40 ? "+" : ""} trang khớp:</div>` +
        hits
          .map(
            (d) => `
          <button class="sidebar-search-item" data-sr-page="${d.p}">
            <div style="font-size:12px;font-weight:700;color:var(--accent);margin-bottom:4px;">${escapeHtml(d.label)} (Ảnh ${d.p})</div>
            <div style="font-size:12.5px;color:var(--text-muted);line-height:1.45;">${makeSnippet(d.t, q)}</div>
          </button>
        `
          )
          .join("");
      el.sidebarSearchResults.querySelectorAll("[data-sr-page]").forEach((btn) => {
        btn.addEventListener("click", () => goToPage(Number(btn.dataset.srPage), true));
      });
    }, 160);
  });

  // Panning when zoomed + double click zoom + wheel zoom
  let dragging = false;
  let dragStart = { x: 0, y: 0, sl: 0, st: 0 };

  el.stage.addEventListener("mousedown", (e) => {
    if (zoom <= 100 || viewMode === "scroll") return;
    dragging = true;
    el.stage.classList.add("dragging");
    dragStart = { x: e.clientX, y: e.clientY, sl: el.stage.scrollLeft, st: el.stage.scrollTop };
  });

  window.addEventListener("mousemove", (e) => {
    if (!dragging) return;
    el.stage.scrollLeft = dragStart.sl - (e.clientX - dragStart.x);
    el.stage.scrollTop = dragStart.st - (e.clientY - dragStart.y);
  });

  window.addEventListener("mouseup", () => {
    dragging = false;
    el.stage.classList.remove("dragging");
  });

  el.stage.addEventListener("dblclick", () => {
    if (viewMode === "scroll") return;
    zoom = zoom === 100 ? 160 : 100;
    applyZoom();
  });

  el.stage.addEventListener(
    "wheel",
    (e) => {
      if (e.ctrlKey && viewMode !== "scroll") {
        e.preventDefault();
        zoom = Math.min(250, Math.max(50, zoom + (e.deltaY < 0 ? 10 : -10)));
        applyZoom();
      }
    },
    { passive: false }
  );

  // Touch swipe on mobile/tablet
  let touchStartX = null;
  let touchStartY = null;
  el.stage.addEventListener(
    "touchstart",
    (e) => {
      if (e.touches.length === 1) {
        touchStartX = e.touches[0].clientX;
        touchStartY = e.touches[0].clientY;
      }
    },
    { passive: true }
  );
  el.stage.addEventListener(
    "touchend",
    (e) => {
      if (touchStartX === null || zoom > 105 || viewMode === "scroll") return;
      const dx = e.changedTouches[0].clientX - touchStartX;
      const dy = e.changedTouches[0].clientY - touchStartY;
      touchStartX = null;
      touchStartY = null;
      if (Math.abs(dx) > 55 && Math.abs(dx) > Math.abs(dy) * 1.4) {
        stepPage(dx < 0 ? 1 : -1);
      }
    },
    { passive: true }
  );

  // Keyboard shortcuts
  document.addEventListener("keydown", (e) => {
    const tag = document.activeElement?.tagName;
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") {
      e.preventDefault();
      el.sidebar.classList.remove("collapsed");
      document.querySelector('[data-tab="search"]').click();
      return;
    }
    if (tag === "INPUT" || tag === "TEXTAREA") {
      if (e.key === "Escape") document.activeElement.blur();
      return;
    }
    if (e.key === "ArrowLeft") stepPage(-1);
    else if (e.key === "ArrowRight") stepPage(1);
    else if (e.key === "Home") goToPage(1);
    else if (e.key === "End") goToPage(currentBook.pages);
    else if (e.key === "+" || e.key === "=") {
      zoom = Math.min(250, zoom + 15);
      applyZoom();
    } else if (e.key === "-") {
      zoom = Math.max(50, zoom - 15);
      applyZoom();
    } else if (e.key === "0") {
      zoom = 100;
      applyZoom();
    } else if (e.key.toLowerCase() === "t") {
      el.toggleSidebarBtn.click();
    } else if (e.key.toLowerCase() === "b") {
      el.bookmarkBtn.click();
    } else if (e.key.toLowerCase() === "f") {
      el.fullscreenBtn.click();
    } else if (e.key === "/") {
      e.preventDefault();
      el.sidebar.classList.remove("collapsed");
      document.querySelector('[data-tab="search"]').click();
    } else if (e.key === "Escape") {
      el.gridModal.classList.remove("open");
    }
  });

  if (window.innerWidth < 960) {
    el.sidebar.classList.add("collapsed");
    el.toggleSidebarBtn.classList.remove("active");
  }

  // Init from URL query params
  const params = new URLSearchParams(window.location.search);
  const reqBook = params.get("book") || "lop-10";
  const reqPage = params.has("page") ? Number(params.get("page")) : null;

  fetch("data/books.json")
    .then((r) => r.json())
    .then((data) => {
      books = data.books || [];
      switchBook(reqBook, Number.isFinite(reqPage) ? reqPage : null);
    })
    .catch((err) => {
      el.spreadContainer.innerHTML = `<p style="padding:20px;">Lỗi tải dữ liệu sách: ${escapeHtml(err.message)}</p>`;
    });
})();
