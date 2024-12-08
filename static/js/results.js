document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('gift-modal');
    const closeModal = document.querySelector('.close-modal');
    const viewDetailsBtns = document.querySelectorAll('.view-details-btn');
    
    // Open modal with gift details
    viewDetailsBtns.forEach(btn => {
        btn.addEventListener('click', async function() {
            const giftCard = this.closest('.gift-card');
            const giftId = giftCard.dataset.id;
            
            try {
                // Fetch detailed product information
                const response = await fetch(`/analyze_product`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        product_url: giftCard.querySelector('.buy-now-btn').href
                    })
                });
                
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                
                const data = await response.json();
                
                // Update modal content
                const modalContent = modal.querySelector('.modal-content');
                modalContent.querySelector('img').src = giftCard.querySelector('.gift-image img').src;
                modalContent.querySelector('h3').textContent = giftCard.querySelector('.gift-info h3').textContent;
                modalContent.querySelector('.price').textContent = giftCard.querySelector('.gift-price').textContent;
                
                // Update review summary
                const prosList = modalContent.querySelector('.pros ul');
                const consList = modalContent.querySelector('.cons ul');
                
                prosList.innerHTML = data.review_summary.pros
                    .map(pro => `<li>${pro}</li>`)
                    .join('');
                
                consList.innerHTML = data.review_summary.cons
                    .map(con => `<li>${con}</li>`)
                    .join('');
                
                // Update purchase section
                const purchaseSection = modalContent.querySelector('.purchase-section');
                purchaseSection.querySelector('.buy-now-btn').href = giftCard.querySelector('.buy-now-btn').href;
                
                if (data.discount_code) {
                    purchaseSection.querySelector('.discount-code').textContent = 
                        `Use code ${data.discount_code} for an extra discount!`;
                }
                
                // Show modal
                modal.style.display = 'block';
                document.body.style.overflow = 'hidden';
                
            } catch (error) {
                console.error('Error:', error);
                alert('Sorry, there was an error loading the product details. Please try again.');
            }
        });
    });
    
    // Close modal
    closeModal.addEventListener('click', function() {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    });
    
    // Close modal when clicking outside
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    });
    
    // Handle category filtering
    const categoryTags = document.querySelectorAll('.category-tag');
    categoryTags.forEach(tag => {
        tag.addEventListener('click', function() {
            const category = this.textContent.toLowerCase();
            const giftCards = document.querySelectorAll('.gift-card');
            
            categoryTags.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
            
            giftCards.forEach(card => {
                if (category === 'all' || card.dataset.category === category) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
});
