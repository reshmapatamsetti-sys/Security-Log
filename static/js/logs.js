let currentPage = 1;
let searchTimeout = null;

async function loadLogs(page = 1) {
    currentPage = page;
    const search = document.getElementById('search-input').value;
    const eventType = document.getElementById('filter-type').value;
    const severity = document.getElementById('filter-severity').value;

    const url = `/api/logs?page=${page}&per_page=15&search=${encodeURIComponent(search)}&event_type=${encodeURIComponent(eventType)}&severity=${encodeURIComponent(severity)}`;

    try {
        const res = await fetch(url);
        const data = await res.json();
        
        const tbody = document.getElementById('logs-table-body');
        tbody.innerHTML = '';

        if (data.logs.length === 0) {
            tbody.innerHTML = '<tr><td colspan="8" style="text-align: center; color: var(--text-muted);">No security logs found matching criteria.</td></tr>';
            document.getElementById('pagination-info').innerText = 'No pages';
            return;
        }

        data.logs.forEach(log => {
            const badgeClass = `badge badge-${log.severity.toLowerCase()}`;
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>#${log.id}</td>
                <td>${log.timestamp}</td>
                <td><code>${log.source_ip}</code></td>
                <td>${log.username}</td>
                <td>${log.event_type}</td>
                <td><span class="${badgeClass}">${log.severity}</span></td>
                <td>${log.description}</td>
                <td>${log.status}</td>
            `;
            tbody.appendChild(tr);
        });

        document.getElementById('pagination-info').innerText = `Showing page ${data.page} of ${data.total_pages} (Total logs: ${data.total})`;
        document.getElementById('prev-btn').disabled = data.page <= 1;
        document.getElementById('next-btn').disabled = data.page >= data.total_pages;

    } catch (e) {
        console.error("Error loading logs:", e);
    }
}

function debounceSearch() {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => loadLogs(1), 300);
}

function changePage(direction) {
    loadLogs(currentPage + direction);
}

async function uploadCSV(input) {
    if (!input.files || input.files.length === 0) return;
    const formData = new FormData();
    formData.append('file', input.files[0]);

    try {
        const res = await fetch('/api/logs/import', { method: 'POST', body: formData });
        const data = await res.json();
        alert(data.message);
        loadLogs(1);
    } catch (e) {
        alert("Failed to import CSV file.");
    }
    input.value = '';
}

loadLogs(1);

async function clearLogs() {
    if (!confirm("Are you sure you want to clear all security logs and alerts? This cannot be undone.")) return;
    
    try {
        const res = await fetch('/api/logs/clear', { method: 'POST' });
        const data = await res.json();
        alert(data.message);
        loadLogs(1);
    } catch (e) {
        alert("Failed to clear logs.");
    }
}