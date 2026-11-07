async function loadIPAnalysis() {
    try {
        const res = await fetch('/api/ip-analysis');
        const ips = await res.json();

        const tbody = document.getElementById('ip-analysis-body');
        tbody.innerHTML = '';

        if (ips.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; color: var(--text-muted);">No IP activity recorded.</td></tr>';
            return;
        }

        ips.forEach(ip => {
            let riskBadge = '<span class="badge badge-informational">Normal</span>';
            if (ip.risk_level === 'Suspicious') riskBadge = '<span class="badge badge-medium">Suspicious</span>';
            if (ip.risk_level === 'High Risk') riskBadge = '<span class="badge badge-critical">High Risk</span>';

            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><code>${ip.source_ip}</code></td>
                <td>${ip.total_events}</td>
                <td>${ip.failed_logins}</td>
                <td>${ip.distinct_users}</td>
                <td>${riskBadge}</td>
                <td>${ip.last_seen}</td>
            `;
            tbody.appendChild(tr);
        });
    } catch (e) {
        console.error("Error loading IP analysis:", e);
    }
}

loadIPAnalysis();