(function () {
    'use strict';

    const cfg = window.EDU_CONFIG;
    const SEARCH_DEBOUNCE_DELAY = 300; // ms

    const loadingState = document.getElementById('loading');
    const errorState = document.getElementById('error');
    const emptyState = document.getElementById('empty');
    const gridContainer = document.getElementById('grid');
    const searchForm = document.getElementById('education-search-form');
    const searchInput = document.getElementById('search-input');
    const educationForm = document.getElementById('education-form'); // null untuk non-superuser

    let educationAbortController;
    let searchDebounceTimer;

    
    function displayPageSection({ showLoading = false, showError = false, showEmpty = false, showGrid = false }) {
        loadingState.classList.toggle('hide', !showLoading);
        errorState.classList.toggle('hide', !showError);
        emptyState.classList.toggle('hide', !showEmpty);
        gridContainer.classList.toggle('hide', !showGrid);
    }

    function urlFor(template, id) {
        return template.replace(cfg.dummyId, id);
    }

    
    function isSafeHttpUrl(value) {
        try {
            const url = new URL(value, window.location.origin);
            return url.protocol === 'http:' || url.protocol === 'https:';
        } catch (e) {
            return false;
        }
    }

    function extractErrorMessage(result, response) {
        if (result.errors) {
            return Object.values(result.errors).flat().map(err => err.message).join(' ');
        }
        return result.message || `Terjadi kesalahan (status ${response.status}).`;
    }

    
    function starButtonHtml(fields) {
        const starredClass = fields.is_starred ? ' is-starred' : '';
        const starText = fields.is_starred ? 'Unstar' : 'Star';
        const starTitle = fields.star_count > 0
            ? `Dibintangi oleh ${fields.starred_by_names}`
            : 'Jadilah yang pertama memberi star';
        return `
            <button type="submit" class="button button-star${starredClass}" title="${escapeHtml(starTitle)}">
                <span aria-hidden="true">★</span>
                ${starText}
                <span class="star-count">${Number(fields.star_count) || 0}</span>
            </button>`;
    }

    function deleteModalHtml(pk, fields) {
        const modalId = `delete-education-modal-${escapeHtml(pk)}`;
        return `
            <button type="button" popovertarget="${modalId}" class="button button-danger">Hapus</button>
            <div id="${modalId}" popover class="project-delete-modal">
                <button type="button" popovertarget="${modalId}" popovertargetaction="hide"
                        class="project-delete-modal__backdrop" aria-label="Tutup"></button>
                <div class="project-delete-modal__content">
                    <button type="button" popovertarget="${modalId}" popovertargetaction="hide"
                            class="project-delete-modal__close" aria-label="Tutup">&times;</button>
                    <h2>Hapus Riwayat Pendidikan?</h2>
                    <p>Yakin ingin menghapus riwayat pendidikan di
                       "${escapeHtml(fields.institution)}"? Tindakan ini tidak dapat dibatalkan.</p>
                    <div class="project-delete-modal__actions">
                        <button type="button" popovertarget="${modalId}" popovertargetaction="hide"
                                class="button button-secondary">Batal</button>
                        <form method="post" action="${urlFor(cfg.deleteUrlTemplate, pk)}">
                            <input type="hidden" name="csrfmiddlewaretoken"
                                   value="${escapeHtml(getCookie('csrftoken'))}">
                            <button type="submit" class="button button-danger">Hapus</button>
                        </form>
                    </div>
                </div>
            </div>`;
    }

    function buildEducationCard(item) {
        const education = item.fields;
        const educationId = item.pk;

        const article = document.createElement('article');
        article.className = 'experience-card';

        const imageHtml = education.thumbnail && isSafeHttpUrl(education.thumbnail)
            ? `<img src="${escapeHtml(education.thumbnail)}" alt="Logo ${escapeHtml(education.institution)}" class="project-image">`
            : '';
        const programHtml = education.program
            ? `<p class="experience-description">${escapeHtml(education.program)}</p>` : '';
        const descriptionHtml = education.description
            ? `<p class="experience-description">${escapeHtml(education.description)}</p>` : '';
        const editHtml = (cfg.isSuperuser || cfg.isEditor)
            ? `<a href="${urlFor(cfg.editUrlTemplate, educationId)}" class="button">Edit</a>` : '';
        const deleteHtml = cfg.isSuperuser ? deleteModalHtml(educationId, education) : '';

        article.innerHTML = `
            ${imageHtml}
            <h2>${escapeHtml(education.institution)}</h2>
            <span class="experience-category">${escapeHtml(education.level_display)}</span>
            ${programHtml}
            ${descriptionHtml}
            <p class="gallery-date">${escapeHtml(education.period)}</p>
            <p class="gallery-status">${education.is_ongoing ? 'Sedang berlangsung' : 'Selesai'}</p>
            <div class="project-card-actions">
                <div class="project-actions">
                    ${editHtml}
                    <form method="post" action="${urlFor(cfg.starUrlTemplate, educationId)}" class="star-form">
                        ${starButtonHtml(education)}
                    </form>
                    ${deleteHtml}
                </div>
            </div>`;
        return article;
    }

    
    async function fetchEducation(searchQuery = '') {
        if (educationAbortController) educationAbortController.abort();
        educationAbortController = new AbortController();

        try {
            displayPageSection({ showLoading: true });

            const url = searchQuery
                ? `${cfg.listUrl}?q=${encodeURIComponent(searchQuery)}`
                : cfg.listUrl;
            const response = await fetch(url, {
                headers: { 'Accept': 'application/json' },
                signal: educationAbortController.signal,
            });
            if (!response.ok) throw new Error('Failed to fetch data');

            const educationData = await response.json();

            if (educationData.length === 0) {
                emptyState.querySelector('p').textContent = searchQuery
                    ? 'Tidak ada riwayat pendidikan yang cocok dengan pencarian.'
                    : 'Belum ada riwayat pendidikan yang ditambahkan.';
                displayPageSection({ showEmpty: true });
                return;
            }

            gridContainer.innerHTML = '';
            educationData.forEach(item => gridContainer.appendChild(buildEducationCard(item)));
            displayPageSection({ showGrid: true });
        } catch (error) {
            if (error.name === 'AbortError') return; // request lama dibatalkan, bukan error
            console.error('Error loading education:', error);
            displayPageSection({ showError: true });
        }
    }

    
    function searchEducation() {
        fetchEducation(searchInput.value.trim());
    }

    searchInput.addEventListener('input', function () {
        clearTimeout(searchDebounceTimer);
        searchDebounceTimer = setTimeout(searchEducation, SEARCH_DEBOUNCE_DELAY);
    });

    searchForm.addEventListener('submit', function (event) {
        event.preventDefault();
        clearTimeout(searchDebounceTimer);
        searchEducation();
    });

    
    async function addEducation(event) {
        event.preventDefault();

        const submitButton = educationForm.querySelector('button[type="submit"]');
        submitButton.disabled = true;

        try {
            const response = await fetch(cfg.createUrl, {
                method: 'POST',
                headers: { 'X-CSRFToken': getCookie('csrftoken') },
                body: new FormData(educationForm), // juga memuat csrfmiddlewaretoken
            });
            const result = await response.json().catch(() => ({}));

            if (response.ok) {
                educationForm.reset();
                document.getElementById('add-education-modal').hidePopover();
                showToast('Berhasil', 'Riwayat pendidikan berhasil ditambahkan!', 'success');
                fetchEducation(searchInput.value.trim());
            } else {
                showToast('Gagal menambahkan data', extractErrorMessage(result, response), 'error');
            }
        } catch (error) {
            console.error('Error adding education:', error);
            showToast('Gagal menambahkan data', 'Tidak dapat terhubung ke server. Silakan coba lagi.', 'error');
        } finally {
            submitButton.disabled = false;
        }
    }

    
    if (educationForm) {
        educationForm.addEventListener('submit', addEducation);
    }

    
    gridContainer.addEventListener('submit', async function (event) {
        const form = event.target.closest('.star-form');
        if (!form) return;
        event.preventDefault();

        const button = form.querySelector('button');
        if (button) button.disabled = true;

        try {
            const response = await fetch(form.action, {
                method: 'POST',
                headers: { 'X-CSRFToken': getCookie('csrftoken') },
            });
            const result = await response.json().catch(() => ({}));

            if (response.ok) {
                form.innerHTML = starButtonHtml(result.fields);
            } else {
                showToast('Gagal memberi star', extractErrorMessage(result, response), 'error');
                if (button) button.disabled = false;
            }
        } catch (error) {
            console.error('Error toggling star:', error);
            showToast('Gagal memberi star', 'Tidak dapat terhubung ke server.', 'error');
            if (button) button.disabled = false;
        }
    });

    fetchEducation(searchInput.value.trim());
})();