document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('gift-finder-form');
    const imageInput = document.getElementById('profileImage');
    const imagePreview = document.getElementById('imagePreview');
    const resultsSection = document.getElementById('results');
    const loadingSpinner = document.getElementById('loading-spinner');
    
    // Handle image preview
    imageInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                imagePreview.innerHTML = `<img src="${e.target.result}" alt="Preview">`;
                imagePreview.classList.remove('hidden');
            };
            reader.readAsDataURL(file);
        }
    });
    
    // Handle form submission
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Show loading spinner
        loadingSpinner.classList.remove('hidden');
        resultsSection.classList.add('hidden');
        
        // Create FormData object
        const formData = new FormData(form);
        
        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (response.ok) {
                displayResults(data);
            } else {
                throw new Error(data.error || 'An error occurred');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error: ' + error.message);
        } finally {
            loadingSpinner.classList.add('hidden');
        }
    });
    
    function displayResults(data) {
        // Display profile insights
        const interestsList = document.getElementById('interests-list');
        interestsList.innerHTML = data.profile.interests
            .map(interest => `<li>${interest}</li>`)
            .join('');
        
        // Display personality traits
        const traitsList = document.getElementById('traits-list');
        traitsList.innerHTML = data.profile.traits
            .map(trait => `<li>${trait}</li>`)
            .join('');
        
        // Display gift recommendations
        const recommendationsGrid = document.getElementById('recommendations-grid');
        recommendationsGrid.innerHTML = data.recommendations
            .map(recommendation => `
                <div class="gift-card">
                    <h4>${recommendation.name}</h4>
                    <p>${recommendation.description}</p>
                    <p class="price">$${recommendation.price}</p>
                </div>
            `)
            .join('');
        
        // Show results section
        resultsSection.classList.remove('hidden');
    }
});
