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
    const educationForm = document.getElementById('education-form');      // null kecuali superuser
    const editForm = document.getElementById('education-edit-form');      // null kecuali superuser/Editor
    const editModal = document.getElementById('edit-education-modal');

    const FIELD_LABELS = {
        institution: 'Institusi',
        program: 'Program Studi',
        level: 'Jenjang',
        description: 'Deskripsi',
        thumbnail: 'URL Gambar/Logo',
        started_at: 'Tanggal Mulai',
        ended_at: 'Tanggal Selesai',
    };
    const EDITABLE_TEXT_FIELDS = ['institution', 'program', 'level', 'description', 'thumbnail'];

    const educationById = new Map(); // id -> data terakhir dari API (untuk mengisi form ubah)
    let educationAbortController;
    let searchDebounceTimer;
    let editingId = null;


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

    
    async function apiRequest(url, { method = 'GET', body, signal } = {}) {
        const headers = { 'Accept': 'application/json' };
        if (method !== 'GET') headers['X-CSRFToken'] = getCookie('csrftoken');
        if (body !== undefined) headers['Content-Type'] = 'application/json';

        const response = await fetch(url, {
            method,
            headers,
            signal,
            credentials: 'same-origin',
            body: body === undefined ? undefined : JSON.stringify(body),
        });
        const data = response.status === 204 ? null : await response.json().catch(() => null);
        return { response, data };
    }

    
    function extractErrorMessage(data, response) {
        if (response.status === 403 && !cfg.isAuthenticated) {
            return 'Login terlebih dahulu untuk melakukan tindakan ini.';
        }
        if (data && typeof data === 'object') {
            if (data.detail) return String(data.detail);
            const messages = Object.entries(data).map(([field, errors]) => {
                const text = [].concat(errors).join(' ');
                return FIELD_LABELS[field] ? `${FIELD_LABELS[field]}: ${text}` : text;
            });
            if (messages.length) return messages.join(' ');
        }
        return `Terjadi kesalahan (status ${response.status}).`;
    }

    function formToPayload(form) {
        const payload = {};
        new FormData(form).forEach((value, key) => {
            if (key !== 'csrfmiddlewaretoken') payload[key] = value;
        });
        payload.ended_at = payload.ended_at || null; // kosong = masih berlangsung
        return payload;
    }


    function starButtonHtml(item) {
        const starredClass = item.is_starred ? ' is-starred' : '';
        const starText = item.is_starred ? 'Unstar' : 'Star';
        const starTitle = item.star_count > 0
            ? `Dibintangi oleh ${item.starred_by_names}`
            : 'Jadilah yang pertama memberi star';
        return `
            <button type="button" class="button button-star${starredClass}"
                    data-action="star" data-id="${escapeHtml(item.id)}"
                    title="${escapeHtml(starTitle)}">
                <span aria-hidden="true">★</span>
                ${starText}
                <span class="star-count">${Number(item.star_count) || 0}</span>
            </button>`;
    }

    function deleteModalHtml(item) {
        const modalId = `delete-education-modal-${escapeHtml(item.id)}`;
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
                       "${escapeHtml(item.institution)}"? Tindakan ini tidak dapat dibatalkan.</p>
                    <div class="project-delete-modal__actions">
                        <button type="button" popovertarget="${modalId}" popovertargetaction="hide"
                                class="button button-secondary">Batal</button>
                        <button type="button" class="button button-danger"
                                data-action="delete" data-id="${escapeHtml(item.id)}">Hapus</button>
                    </div>
                </div>
            </div>`;
    }


    function buildEducationCard(item) {
        
        const article = document.createElement('article');
        article.className = 'experience-card';

        const imageHtml = item.thumbnail && isSafeHttpUrl(item.thumbnail)
            ? `<img src="${escapeHtml(item.thumbnail)}" alt="Logo ${escapeHtml(item.institution)}" class="project-image">`
            : '';
        const programHtml = item.program
            ? `<p class="experience-description">${escapeHtml(item.program)}</p>` : '';
        const descriptionHtml = item.description
            ? `<p class="experience-description">${escapeHtml(item.description)}</p>` : '';
        const editHtml = (cfg.isSuperuser || cfg.isEditor)
            ? `<button type="button" class="button" data-action="edit" data-id="${escapeHtml(item.id)}">Edit</button>` : '';
        const deleteHtml = cfg.isSuperuser ? deleteModalHtml(item) : '';

        article.innerHTML = `
            ${imageHtml}
            <h2>${escapeHtml(item.institution)}</h2>
            <span class="experience-category">${escapeHtml(item.level_display)}</span>
            ${programHtml}
            ${descriptionHtml}
            <p class="gallery-date">${escapeHtml(item.period)}</p>
            <p class="gallery-status">${item.is_ongoing ? 'Sedang berlangsung' : 'Selesai'}</p>
            <div class="project-card-actions">
                <div class="project-actions">
                    ${editHtml}
                    <span class="star-form">${starButtonHtml(item)}</span>
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
            const { response, data } = await apiRequest(url, { signal: educationAbortController.signal });
            if (!response.ok) throw new Error('Failed to fetch data');

            educationById.clear();
            data.forEach(item => educationById.set(item.id, item));

            if (data.length === 0) {
                emptyState.querySelector('p').textContent = searchQuery
                    ? 'Tidak ada riwayat pendidikan yang cocok dengan pencarian.'
                    : 'Belum ada riwayat pendidikan yang ditambahkan.';
                displayPageSection({ showEmpty: true });
                return;
            }

            gridContainer.innerHTML = '';
            data.forEach(item => gridContainer.appendChild(buildEducationCard(item)));
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
            const { response, data } = await apiRequest(cfg.listUrl, {
                method: 'POST',
                body: formToPayload(educationForm),
            });


            if (response.status === 201) {
                educationForm.reset();
                document.getElementById('add-education-modal').hidePopover();
                showToast('Berhasil', 'Riwayat pendidikan berhasil ditambahkan!', 'success');
                fetchEducation(searchInput.value.trim());
            } else {
                showToast('Gagal menambahkan data', extractErrorMessage(data, response), 'error');
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


    function toDatetimeLocal(value) {
        return value ? value.slice(0, 16) : '';
    }

    function openEditModal(id) {
        const item = educationById.get(id);
        if (!item || !editForm) return;

        editingId = id;
        EDITABLE_TEXT_FIELDS.forEach(name => {
            editForm.elements[name].value = item[name] ?? '';
        });
        editForm.elements.started_at.value = toDatetimeLocal(item.started_at);
        editForm.elements.ended_at.value = toDatetimeLocal(item.ended_at);
        editModal.showPopover();
    }

    async function updateEducation(event) {
        event.preventDefault();
        if (!editingId) return;

        const submitButton = editForm.querySelector('button[type="submit"]');
        submitButton.disabled = true;

        try {
            const { response, data } = await apiRequest(urlFor(cfg.detailUrlTemplate, editingId), {
                method: 'PATCH',
                body: formToPayload(editForm),
            });

            if (response.ok) {
                editModal.hidePopover();
                editingId = null;
                showToast('Berhasil', 'Riwayat pendidikan berhasil diperbarui!', 'success');
                fetchEducation(searchInput.value.trim());
            } else {
                showToast('Gagal memperbarui data', extractErrorMessage(data, response), 'error');
            }
        } catch (error) {
            console.error('Error updating education:', error);
            showToast('Gagal memperbarui data', 'Tidak dapat terhubung ke server. Silakan coba lagi.', 'error');
        } finally {
            submitButton.disabled = false;
        }
    }

    if (editForm) {
        editForm.addEventListener('submit', updateEducation);
    }


    async function deleteEducation(id, button) {
        button.disabled = true;
        const modal = button.closest('[popover]');

        try {
            const { response, data } = await apiRequest(urlFor(cfg.detailUrlTemplate, id), { method: 'DELETE' });

            if (response.status === 204) {
                showToast('Berhasil', 'Riwayat pendidikan berhasil dihapus!', 'success');
                fetchEducation(searchInput.value.trim());
            } else {
                if (modal) modal.hidePopover();
                showToast('Gagal menghapus data', extractErrorMessage(data, response), 'error');
            }
        } catch (error) {
            console.error('Error deleting education:', error);
            showToast('Gagal menghapus data', 'Tidak dapat terhubung ke server.', 'error');
        } finally {
            button.disabled = false;
        }
    }


    async function toggleStar(id, button) {
        button.disabled = true;

        try {
            const { response, data } = await apiRequest(urlFor(cfg.starUrlTemplate, id), { method: 'POST' });

            if (response.ok) {
                educationById.set(id, { ...educationById.get(id), ...data });
                button.closest('.star-form').innerHTML = starButtonHtml(data);
            } else {
                showToast('Gagal memberi star', extractErrorMessage(data, response), 'error');
                button.disabled = false;
            }
        } catch (error) {
            console.error('Error toggling star:', error);
            showToast('Gagal memberi star', 'Tidak dapat terhubung ke server.', 'error');
            button.disabled = false;
        }
    }

    // Satu event listener untuk semua tombol di dalam kartu (event delegation).
    gridContainer.addEventListener('click', function (event) {
        const button = event.target.closest('[data-action]');
        if (!button) return;

        const { action, id } = button.dataset;
        if (action === 'star') toggleStar(id, button);
        else if (action === 'edit') openEditModal(id);
        else if (action === 'delete') deleteEducation(id, button);
    });

    fetchEducation(searchInput.value.trim());
})();