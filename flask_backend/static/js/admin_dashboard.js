document.addEventListener('DOMContentLoaded', function() {
    fetch('/admin/stats-data')
    .then(response => response.json())
    .then(data => {
        document.getElementById('totalUsers').textContent = data.total_users;
        document.getElementById('premiumUsers').textContent = data.premium_users;
        document.getElementById('trialUsers').textContent = data.trial_users;
        document.getElementById('totalSearches').textContent = data.total_searches;

        const ctx = document.getElementById('subscriptionChart').getContext('2d');
        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['Premium Users', 'Trial Users'],
                datasets: [{
                    data: [data.premium_users, data.trial_users],
                    backgroundColor: [
                        'rgba(40, 167, 69, 0.7)',   // green
                        'rgba(255, 193, 7, 0.7)'    // yellow
                    ],
                    borderColor: [
                        'rgba(40, 167, 69, 1)',
                        'rgba(255, 193, 7, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    })
    .catch(error => console.error('Error fetching stats:', error));
});
