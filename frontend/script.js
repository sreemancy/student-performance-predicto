const API_BASE_URL = 'http://localhost:5000';

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('predictionForm');
    const resultDiv = document.getElementById('result');
    const loadingDiv = document.getElementById('loading');
    const errorDiv = document.getElementById('error');
    const historyDiv = document.getElementById('history');
    const loadHistoryBtn = document.getElementById('loadHistory');

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        await makePrediction();
    });

    loadHistoryBtn.addEventListener('click', loadHistory);

    async function makePrediction() {
        // Show loading
        showLoading();
        hideResult();
        hideError();

        // Get form data
        const formData = {
            attendance: parseFloat(document.getElementById('attendance').value),
            study_hours: parseFloat(document.getElementById('study_hours').value),
            internal_marks: parseFloat(document.getElementById('internal_marks').value),
            assignments_submitted: parseInt(document.getElementById('assignments_submitted').value),
            activities: parseInt(document.getElementById('activities').value)
        };

        try {
            const response = await fetch(`${API_BASE_URL}/predict`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            displayResult(result);
        } catch (error) {
            console.error('Error:', error);
            showError('Failed to get prediction. Make sure the backend server is running.');
        } finally {
            hideLoading();
        }
    }

    function displayResult(result) {
        const predictionSpan = document.getElementById('prediction');
        const confidenceSpan = document.getElementById('confidence');

        predictionSpan.textContent = result.prediction;
        predictionSpan.className = `prediction-value ${result.prediction.toLowerCase()}`;
        confidenceSpan.textContent = `${result.confidence}%`;

        showResult();
    }

    async function loadHistory() {
        try {
            const response = await fetch(`${API_BASE_URL}/history`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const history = await response.json();
            displayHistory(history);
        } catch (error) {
            console.error('Error loading history:', error);
            showError('Failed to load history.');
        }
    }

    function displayHistory(history) {
        if (history.length === 0) {
            historyDiv.innerHTML = '<p>No predictions found.</p>';
            return;
        }

        const historyHTML = history.map(item => `
            <div class="history-item">
                <div><strong>Attendance:</strong> ${item.attendance}%</div>
                <div><strong>Study Hours:</strong> ${item.study_hours}</div>
                <div><strong>Internal Marks:</strong> ${item.internal_marks}%</div>
                <div><strong>Assignments:</strong> ${item.assignments_submitted}</div>
                <div><strong>Activities:</strong> ${item.activities}</div>
                <div><strong>Prediction:</strong> ${item.prediction}</div>
                <div><strong>Confidence:</strong> ${item.confidence}%</div>
                <div><strong>Date:</strong> ${new Date(item.timestamp).toLocaleString()}</div>
            </div>
        `).join('');

        historyDiv.innerHTML = historyHTML;
    }

    function showLoading() {
        loadingDiv.classList.remove('hidden');
    }

    function hideLoading() {
        loadingDiv.classList.add('hidden');
    }

    function showResult() {
        resultDiv.classList.remove('hidden');
    }

    function hideResult() {
        resultDiv.classList.add('hidden');
    }

    function showError(message) {
        errorDiv.textContent = message;
        errorDiv.classList.remove('hidden');
    }

    function hideError() {
        errorDiv.classList.add('hidden');
    }
});