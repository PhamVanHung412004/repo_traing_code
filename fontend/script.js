// DOM elements
const emailInput = document.getElementById('emailInput');
const analyzeBtn = document.getElementById('analyzeBtn');
const loadingSection = document.getElementById('loadingSection');
const resultSection = document.getElementById('resultSection');
const errorSection = document.getElementById('errorSection');
const predictionResult = document.getElementById('predictionResult');
const confidenceBar = document.getElementById('confidenceBar');
const confidenceText = document.getElementById('confidenceText');
const probabilitiesList = document.getElementById('probabilitiesList');
const errorMessage = document.getElementById('errorMessage');

// --- PHÂN TÍCH EMAIL (bọc trong điều kiện kiểm tra DOM) ---
if (document.getElementById('analyzeBtn') && document.getElementById('emailInput')) {
    // API configuration
    const API_URL = 'http://127.0.0.1:5000/email';

    // Event listeners
    document.addEventListener('DOMContentLoaded', function() {
        analyzeBtn.addEventListener('click', handleAnalyzeClick);
        emailInput.addEventListener('keydown', function(e) {
            if (e.ctrlKey && e.key === 'Enter') {
                handleAnalyzeClick();
            }
        });
    });

    // Main function to handle analyze button click
    async function handleAnalyzeClick() {
        const emailContent = emailInput.value.trim();
        
        // Validate input
        if (!emailContent) {
            showError('Vui lòng nhập nội dung email để phân tích.');
            return;
        }
        
        // Show loading state
        showLoading();
        
        try {
            // Call API
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: emailContent
                })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            const result = data.response;
            
            // Display results
            displayResults(result);
            
        } catch (error) {
            console.error('Error analyzing email:', error);
            showError('Có lỗi xảy ra khi phân tích email. Vui lòng thử lại.');
        }
    }

    // Function to display results
    function displayResults(result) {
        // Hide loading and error sections
        hideLoading();
        hideError();
        
        // Display prediction
        predictionResult.textContent = result.prediction;
        predictionResult.className = 'prediction-result';
        
        // Add color coding based on prediction
        if (result.prediction.toLowerCase().includes('spam')) {
            predictionResult.style.backgroundColor = '#ffebee';
            predictionResult.style.borderColor = '#f44336';
            predictionResult.style.color = '#c62828';
        } else if (result.prediction.toLowerCase().includes('ham')) {
            predictionResult.style.backgroundColor = '#e8f5e8';
            predictionResult.style.borderColor = '#4caf50';
            predictionResult.style.color = '#2e7d32';
        } else {
            predictionResult.style.backgroundColor = '#fff3e0';
            predictionResult.style.borderColor = '#ff9800';
            predictionResult.style.color = '#ef6c00';
        }
        
        // Display confidence
        const confidencePercent = Math.round(result.confidence * 100);
        confidenceBar.style.width = `${confidencePercent}%`;
        confidenceText.textContent = `${confidencePercent}%`;
        
        // Display probabilities
        displayProbabilities(result.probabilities);
        
        // Show result section
        resultSection.classList.remove('hidden');
        
        // Scroll to results
        resultSection.scrollIntoView({ behavior: 'smooth' });
    }

    // Function to display probabilities
    function displayProbabilities(probabilities) {
        probabilitiesList.innerHTML = '';
        
        // Sort probabilities by value (descending)
        const sortedProbabilities = Object.entries(probabilities)
            .sort(([,a], [,b]) => b - a);
        
        sortedProbabilities.forEach(([label, probability]) => {
            const probabilityPercent = Math.round(probability * 100);
            
            const probabilityItem = document.createElement('div');
            probabilityItem.className = 'probability-item';
            
            const labelSpan = document.createElement('span');
            labelSpan.className = 'probability-label';
            labelSpan.textContent = formatLabel(label);
            
            const valueSpan = document.createElement('span');
            valueSpan.className = 'probability-value';
            valueSpan.textContent = `${probabilityPercent}%`;
            
            probabilityItem.appendChild(labelSpan);
            probabilityItem.appendChild(valueSpan);
            probabilitiesList.appendChild(probabilityItem);
        });
    }

    // Function to format label for display
    function formatLabel(label) {
        // Convert label to proper case and Vietnamese
        const labelMap = {
            'spam': 'Spam',
            'ham': 'Email thường',
            'phishing': 'Lừa đảo',
            'legitimate': 'Hợp lệ',
            'suspicious': 'Đáng ngờ'
        };
        
        return labelMap[label.toLowerCase()] || label;
    }

    // Function to show loading state
    function showLoading() {
        hideError();
        hideResults();
        loadingSection.classList.remove('hidden');
        analyzeBtn.disabled = true;
        analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Đang phân tích...';
    }

    // Function to hide loading state
    function hideLoading() {
        loadingSection.classList.add('hidden');
        analyzeBtn.disabled = false;
        analyzeBtn.innerHTML = '<i class="fas fa-search"></i> Phân tích Email';
    }

    // Function to show error
    function showError(message) {
        hideLoading();
        hideResults();
        errorMessage.textContent = message;
        errorSection.classList.remove('hidden');
    }

    // Function to hide error
    function hideError() {
        errorSection.classList.add('hidden');
    }

    // Function to hide results
    function hideResults() {
        resultSection.classList.add('hidden');
    }

    // Add sample emails for testing
    function addSampleEmails() {
        const sampleEmails = [
            {
                name: "Email thường",
                content: "Chào bạn, tôi muốn trao đổi về dự án mới. Bạn có thể liên hệ lại với tôi qua email này không? Cảm ơn bạn."
            },
            {
                name: "Email spam",
                content: "🎉 CHÀO MỪNG! Bạn đã trúng thưởng $1000! Click ngay để nhận thưởng! 🎁 FREE GIFT! Không thể bỏ lỡ cơ hội này! $$$"
            },
            {
                name: "Email lừa đảo",
                content: "CẢNH BÁO: Tài khoản ngân hàng của bạn đã bị khóa! Vui lòng cập nhật thông tin ngay lập tức để tránh mất tiền! Click vào link để xác minh!"
            }
        ];
        
        // Create sample buttons
        const sampleSection = document.createElement('div');
        sampleSection.className = 'sample-section';
        sampleSection.innerHTML = `
            <h4><i class="fas fa-lightbulb"></i> Email mẫu để thử nghiệm:</h4>
            <div class="sample-buttons">
                ${sampleEmails.map((sample, index) => `
                    <button class="sample-btn" onclick="loadSampleEmail(${index})">
                        ${sample.name}
                    </button>
                `).join('')}
            </div>
        `;
        
        // Insert after input section
        const inputSection = document.querySelector('.input-section');
        inputSection.appendChild(sampleSection);
        
        // Store samples globally
        window.sampleEmails = sampleEmails;
    }

    // Function to load sample email
    function loadSampleEmail(index) {
        if (window.sampleEmails && window.sampleEmails[index]) {
            emailInput.value = window.sampleEmails[index].content;
            emailInput.focus();
        }
    }

    // Initialize sample emails when page loads
    document.addEventListener('DOMContentLoaded', function() {
        // Add sample emails after a short delay
        setTimeout(addSampleEmails, 1000);
    });

    // Add CSS for sample section
    const sampleStyles = `
    .sample-section {
        margin-top: 30px;
        padding-top: 20px;
        border-top: 1px solid #e1e5e9;
    }

    .sample-section h4 {
        display: flex;
        align-items: center;
        gap: 10px;
        color: #333;
        margin-bottom: 15px;
        font-size: 1rem;
    }

    .sample-section h4 i {
        color: #ffd700;
    }

    .sample-buttons {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
    }

    .sample-btn {
        background: #f8f9fa;
        border: 2px solid #e1e5e9;
        padding: 8px 15px;
        border-radius: 8px;
        font-size: 0.9rem;
        cursor: pointer;
        transition: all 0.3s ease;
        color: #333;
    }

    .sample-btn:hover {
        background: #667eea;
        border-color: #667eea;
        color: white;
        transform: translateY(-1px);
    }
    `;

    // Add styles to document
    const styleSheet = document.createElement('style');
    styleSheet.textContent = sampleStyles;
    document.head.appendChild(styleSheet); 
}
// --- KẾT THÚC PHÂN TÍCH EMAIL ---

let offset = 0;
const limit = 10;
let total = 0;

async function loadMoreRows() {
    const res = await fetch('http://localhost:5000/show_csv' + offset + '&limit=' + limit);
    const data = await res.json();
    total = data.total;
    const table = document.getElementById('csv-table');
    // Nếu là lần đầu, thêm header
    if (table.rows.length === 0 && data.rows.length > 0) {
        const header = document.createElement('tr');
        data.rows[0].forEach(cell => {
            const th = document.createElement('th');
            th.textContent = cell;
            header.appendChild(th);
        });
        table.appendChild(header);
        data.rows.shift();
    }
    // Thêm từng dòng một với hiệu ứng
    for (const row of data.rows) {
        const tr = document.createElement('tr');
        tr.classList.add('new-row');
        row.forEach(cell => {
            const td = document.createElement('td');
            td.textContent = cell;
            tr.appendChild(td);
        });
        table.appendChild(tr);
        // Hiệu ứng fade màu nền dòng mới
        setTimeout(() => tr.classList.remove('new-row'), 1000);
    }
    offset += data.rows.length;
    if (offset >= total) {
        document.getElementById('load-more-btn').style.display = 'none';
    }
}

window.onload = function() {
    loadMoreRows();
}; 