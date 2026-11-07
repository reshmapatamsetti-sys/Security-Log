async function loadAlerts() {
    const status = document.getElementById('filter-status').value;
    const severity = document.getElementById('filter-severity').value;

    try {
        const res = ackUrl = `/api/alerts?status=${status}&severity=${severity}`;
        const response = await fetch(ackUrl);
        const alerts = await response.json();

        const tbody = document.getElementById('alerts-table-body');
        tbody.innerHTML = '';

        if (alerts.length === 0) {
            tbody.innerHTML = '<tr><td colspan="9" style="text-align: center; color: var(--text-muted);">No alerts found.</td></tr>';
            return;
        }

        alerts.forEach(alert => {
            const badgeClass = `badge badge-${alert.severity.toLowerCase()}`;
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>#${alert.id}</td>
                <td>${alert.timestamp}</td>
                <td><strong>${alert.alert_type}</strong></td>
                <td><code>${alert.source_ip}</code></td>
                <td>${alert.username}</td>
                <td><span class="${badgeClass}">${alert.severity}</span></td>
                <td>
                    <div>${alert.description}</div>
                    <small style="color: var(--text-muted);">${alert.detection_reason}</small>
                </td>
                <td>${alert.status}</td>
                <td>
                    <select class="form-control" style="padding: 4px; font-size: 0.8rem;" onchange="updateAlertStatus(${alert.id}, this.value)">
                        <option value="Open" ${alert.status === 'Open' ? 'selected' : ''}>Open</option>
                        <option value="Acknowledged" ${alert.status === 'Acknowledged' ? 'selected' : ''}>Ack</option>
                        <option value="Resolved" ${alert.status === 'Resolved' ? 'selected' : ''}>Resolved</option>
                    </select>
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (e) {
        console.error("Error loading alerts:", e);
    }
}

async function updateAlertStatus(alertId, newStatus) {
    try {
        const res = await fetch(`/api/alerts/${alertId}/status`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status: newStatus })
        });
        const data = await res.json();
        if (data.success) {
            loadAlerts();
        } else {
            alert(data.message);
        }
    } catch (e) {
        alert("Failed to update alert status.");
    }
}

loadAlerts();