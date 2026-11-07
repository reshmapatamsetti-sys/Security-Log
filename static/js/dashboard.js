document.addEventListener("DOMContentLoaded", async () => {
    // Fetch stats
    const statsRes = await fetch('/api/dashboard/stats');
    const stats = await statsRes.json();
    
    document.getElementById('stat-total').textContent = stats.total_events;
    document.getElementById('stat-success').textContent = stats.successful_logins;
    document.getElementById('stat-failed').textContent = stats.failed_logins;
    document.getElementById('stat-alerts').textContent = stats.active_alerts;
    document.getElementById('stat-critical').textContent = stats.critical_alerts;
    document.getElementById('stat-ips').textContent = stats.unique_ips;

    // Fetch charts
    const chartsRes = await fetch('/api/dashboard/charts');
    const chartData = await chartsRes.json();

    // Event Distribution Doughnut Chart
    const eventCtx = document.getElementById('eventChart').getContext('2d');
    new Chart(eventCtx, {
        type: 'doughnut',
        data: {
            labels: chartData.event_distribution.map(item => item.event_type),
            datasets: [{
                data: chartData.event_distribution.map(item => item.count),
                backgroundColor: ['#06b6d4', '#10b981', '#f59e0b', '#f97316', '#ef4444', '#8b5cf6', '#ec4899', '#64748b']
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { position: 'bottom', labels: { color: '#f8fafc' } } }
        }
    });

    // Severity Bar Chart
    const severityCtx = document.getElementById('severityChart').getContext('2d');
    new Chart(severityCtx, {
        type: 'bar',
        data: {
            labels: chartData.severity_distribution.map(item => item.severity),
            datasets: [{
                label: 'Events by Severity',
                data: chartData.severity_distribution.map(item => item.count),
                backgroundColor: '#06b6d4'
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: {
                x: { ticks: { color: '#f8fafc' }, grid: { color: '#334155' } },
                y: { ticks: { color: '#f8fafc' }, grid: { color: '#334155' } }
            }
        }
    });
});