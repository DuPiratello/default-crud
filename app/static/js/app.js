// CRUD API Frontend
const API = '/api/v1/items';
const PAGE_SIZE = 10;

let currentPage = 0;
let totalItems = 0;
let deleteTargetId = null;
let searchTimeout = null;
let allItems = [];

// DOM references
const $ = (sel) => document.querySelector(sel);
const tableBody = $('#table-body');
const emptyState = $('#empty-state');
const modalOverlay = $('#modal-overlay');
const deleteOverlay = $('#delete-overlay');
const form = $('#item-form');
const toastContainer = $('#toast-container');

// ========================================
// API CALLS
// ========================================

async function api(method, path = '', body = null) {
  const opts = {
    method,
    headers: { 'Content-Type': 'application/json' },
  };
  if (body) opts.body = JSON.stringify(body);
  const res = await fetch(`${API}${path}`, opts);
  if (res.status === 204) return null;
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Request failed' }));
    throw new Error(err.detail || 'Request failed');
  }
  return res.json();
}

// ========================================
// RENDER
// ========================================

async function loadItems() {
  try {
    const data = await api('GET', `/?skip=${currentPage * PAGE_SIZE}&limit=${PAGE_SIZE}`);
    allItems = data.items;
    totalItems = data.total;
    renderTable(allItems);
    renderStats(allItems, totalItems);
    renderPagination();
  } catch (e) {
    toast('Failed to load items', 'error');
  }
}

function renderTable(items) {
  const search = $('#search').value.toLowerCase();
  const filtered = search
    ? items.filter(i => i.name.toLowerCase().includes(search) || (i.description || '').toLowerCase().includes(search))
    : items;

  if (filtered.length === 0) {
    tableBody.innerHTML = '';
    emptyState.style.display = 'flex';
    $('table thead').style.display = 'none';
    return;
  }

  emptyState.style.display = 'none';
  $('table thead').style.display = '';

  tableBody.innerHTML = filtered.map((item, i) => `
    <tr style="animation-delay: ${i * 0.04}s">
      <td><span class="cell-id">#${item.id}</span></td>
      <td><span class="cell-name">${esc(item.name)}</span></td>
      <td><span class="cell-desc">${esc(item.description || '—')}</span></td>
      <td><span class="cell-price">$${Number(item.price).toFixed(2)}</span></td>
      <td>
        <span class="badge ${item.is_active ? 'badge-active' : 'badge-inactive'}">
          ${item.is_active ? 'Active' : 'Inactive'}
        </span>
      </td>
      <td><span class="cell-desc">${formatDate(item.created_at)}</span></td>
      <td>
        <div class="cell-actions">
          <button class="btn-icon" onclick="openEdit(${item.id})" title="Edit">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="15" height="15">
              <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/>
              <path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/>
            </svg>
          </button>
          <button class="btn-icon danger" onclick="openDelete(${item.id}, '${esc(item.name)}')" title="Delete">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="15" height="15">
              <polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2"/>
            </svg>
          </button>
        </div>
      </td>
    </tr>
  `).join('');
}

function renderStats(items, total) {
  const active = items.filter(i => i.is_active).length;
  // Use page-level counts but show total from API
  $('#stat-total').textContent = total;
  $('#stat-active').textContent = active;
  $('#stat-inactive').textContent = items.length - active;
}

function renderPagination() {
  const totalPages = Math.ceil(totalItems / PAGE_SIZE);
  const start = currentPage * PAGE_SIZE + 1;
  const end = Math.min((currentPage + 1) * PAGE_SIZE, totalItems);

  $('#pagination-info').textContent = totalItems > 0
    ? `${start}–${end} of ${totalItems}`
    : 'No items';

  $('#btn-prev').disabled = currentPage === 0;
  $('#btn-next').disabled = currentPage >= totalPages - 1;
}

// ========================================
// MODAL (CREATE / EDIT)
// ========================================

function openModal(title = 'New Item', item = null) {
  $('#modal-title').textContent = title;
  $('#btn-submit').textContent = item ? 'Save' : 'Create';
  $('#form-id').value = item ? item.id : '';
  $('#form-name').value = item ? item.name : '';
  $('#form-description').value = item ? (item.description || '') : '';
  $('#form-price').value = item ? item.price : '';
  $('#form-active').checked = item ? item.is_active : true;
  updateToggleLabel();
  modalOverlay.classList.add('active');
  setTimeout(() => $('#form-name').focus(), 100);
}

function closeModal() {
  modalOverlay.classList.remove('active');
  form.reset();
}

async function openEdit(id) {
  try {
    const item = await api('GET', `/${id}`);
    openModal('Edit Item', item);
  } catch (e) {
    toast('Failed to load item', 'error');
  }
}

// ========================================
// DELETE
// ========================================

function openDelete(id, name) {
  deleteTargetId = id;
  $('#delete-name').textContent = name;
  deleteOverlay.classList.add('active');
}

function closeDelete() {
  deleteOverlay.classList.remove('active');
  deleteTargetId = null;
}

async function confirmDelete() {
  if (!deleteTargetId) return;
  try {
    await api('DELETE', `/${deleteTargetId}`);
    toast('Item deleted', 'success');
    closeDelete();
    loadItems();
  } catch (e) {
    toast(e.message, 'error');
  }
}

// ========================================
// FORM SUBMIT
// ========================================

async function handleSubmit(e) {
  e.preventDefault();
  const id = $('#form-id').value;
  const body = {
    name: $('#form-name').value.trim(),
    description: $('#form-description').value.trim() || null,
    price: parseFloat($('#form-price').value),
    is_active: $('#form-active').checked,
  };

  try {
    if (id) {
      await api('PUT', `/${id}`, body);
      toast('Item updated', 'success');
    } else {
      await api('POST', '/', body);
      toast('Item created', 'success');
    }
    closeModal();
    loadItems();
  } catch (e) {
    toast(e.message, 'error');
  }
}

// ========================================
// TOAST
// ========================================

function toast(message, type = 'success') {
  const el = document.createElement('div');
  el.className = `toast ${type}`;
  el.textContent = message;
  toastContainer.appendChild(el);
  setTimeout(() => {
    el.classList.add('out');
    setTimeout(() => el.remove(), 300);
  }, 3000);
}

// ========================================
// HELPERS
// ========================================

function esc(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

function formatDate(iso) {
  const d = new Date(iso);
  return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}

function updateToggleLabel() {
  $('#toggle-label').textContent = $('#form-active').checked ? 'Active' : 'Inactive';
}

// ========================================
// EVENT LISTENERS
// ========================================

$('#btn-new').addEventListener('click', () => openModal());
$('#btn-close-modal').addEventListener('click', closeModal);
$('#btn-cancel').addEventListener('click', closeModal);
form.addEventListener('submit', handleSubmit);

$('#btn-close-delete').addEventListener('click', closeDelete);
$('#btn-cancel-delete').addEventListener('click', closeDelete);
$('#btn-confirm-delete').addEventListener('click', confirmDelete);

$('#form-active').addEventListener('change', updateToggleLabel);

$('#btn-prev').addEventListener('click', () => { currentPage--; loadItems(); });
$('#btn-next').addEventListener('click', () => { currentPage++; loadItems(); });

$('#search').addEventListener('input', () => {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => renderTable(allItems), 200);
});

// Close modals on overlay click
modalOverlay.addEventListener('click', (e) => { if (e.target === modalOverlay) closeModal(); });
deleteOverlay.addEventListener('click', (e) => { if (e.target === deleteOverlay) closeDelete(); });

// Close modals on Escape
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') { closeModal(); closeDelete(); }
});

// ========================================
// INIT
// ========================================

loadItems();
