// Handle scan form submission
document.addEventListener('DOMContentLoaded', function() {
    const scanForm = document.getElementById('scanForm');

    if (scanForm) {
        scanForm.addEventListener('submit', handleScanSubmit);
    }
});

async function handleScanSubmit(e) {
    e.preventDefault();

    const form = e.target;
    const scanButton = document.getElementById('scanButton');
    const scanProgress = document.getElementById('scanProgress');
    const scanError = document.getElementById('scanError');
    const btnText = scanButton.querySelector('.btn-text');
    const btnLoader = scanButton.querySelector('.btn-loader');

    // Disable button and show loading state
    scanButton.disabled = true;
    btnText.style.display = 'none';
    btnLoader.style.display = 'inline';
    scanError.style.display = 'none';

    // Show progress
    scanProgress.style.display = 'block';

    // Collect form data
    const formData = {
        host: form.host.value,
        port: parseInt(form.port.value),
        database: form.database.value,
        user: form.user.value,
        password: form.password.value,
        compliance_framework: form.compliance_framework.value
    };

    // Animate progress steps
    animateProgressSteps();

    try {
        const response = await fetch('/scan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Scan failed');
        }

        // Redirect to results page
        window.location.href = `/results/${data.scan_id}`;

    } catch (error) {
        console.error('Scan error:', error);

        // Show error message
        scanError.textContent = `Error: ${error.message}`;
        scanError.style.display = 'block';

        // Reset button
        scanButton.disabled = false;
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
        scanProgress.style.display = 'none';
    }
}

function animateProgressSteps() {
    const steps = document.querySelectorAll('.step');
    let currentStep = 0;

    const interval = setInterval(() => {
        if (currentStep < steps.length) {
            steps[currentStep].classList.add('active');
            currentStep++;
        } else {
            clearInterval(interval);
        }
    }, 2000); // Activate each step every 2 seconds
}

// Auto-hide alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.error-message');

    alerts.forEach(alert => {
        if (alert.style.display !== 'none') {
            setTimeout(() => {
                alert.style.display = 'none';
            }, 5000);
        }
    });
});
