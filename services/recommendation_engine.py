"""Gift recommendation engine."""
import random
from typing import List, Dict, Any

def get_recommendations(interests: List[str], age: int, budget: float) -> List[Dict[str, Any]]:
    """Generate personalized gift recommendations based on interests, age, and budget."""
    
    # Weight categories based on interests
    category_weights = {
        'tech': 1.0,
        'creative': 1.0,
        'gaming': 1.0,
        'outdoor': 1.0,
        'photography': 1.0,
        'fashion': 1.0,
        'beauty': 1.0,
        'home': 1.0
    }

    # Adjust weights based on interests
    for interest in interests:
        interest = interest.lower().strip()
        for category in category_weights:
            if interest in category or category in interest:
                category_weights[category] += 2.0
            elif any(word in interest for word in ['gadget', 'electronics']) and category == 'tech':
                category_weights['tech'] += 1.5
            elif any(word in interest for word in ['art', 'draw', 'paint']) and category == 'creative':
                category_weights['creative'] += 1.5
            elif any(word in interest for word in ['nature', 'adventure']) and category == 'outdoor':
                category_weights['outdoor'] += 1.5
            elif any(word in interest for word in ['photo', 'camera', 'instagram']) and category == 'photography':
                category_weights['photography'] += 1.5
            elif any(word in interest for word in ['style', 'clothes']) and category == 'fashion':
                category_weights['fashion'] += 1.5
            elif any(word in interest for word in ['makeup', 'skincare']) and category == 'beauty':
                category_weights['beauty'] += 1.5
            elif any(word in interest for word in ['decor', 'cozy']) and category == 'home':
                category_weights['home'] += 1.5

    # Age-based adjustments
    if age < 18:
        category_weights['gaming'] *= 1.5
        category_weights['tech'] *= 1.3
    elif 18 <= age <= 25:
        category_weights['fashion'] *= 1.4
        category_weights['beauty'] *= 1.3
        category_weights['tech'] *= 1.2
    elif 26 <= age <= 35:
        category_weights['home'] *= 1.4
        category_weights['photography'] *= 1.3
        category_weights['outdoor'] *= 1.2
    else:
        category_weights['home'] *= 1.5
        category_weights['creative'] *= 1.3

    # Current in-stock gift database
    gift_database = {
        'tech': [
            {
                'name': 'Govee Smart LED Strip Lights',
                'description': '65.6ft LED Strip Lights with App Control, Music Sync',
                'price': 49.99,
                'amazon_link': 'https://www.amazon.com/Govee-Changing-Bluetooth-Controlled-Decoration/dp/B08149RHYZ/',
                'match_reason': 'Perfect for room ambiance and tech lovers'
            },
            {
                'name': 'RENPHO Smart Scale',
                'description': 'Digital Bluetooth Scale for Body Weight, BMI',
                'price': 29.99,
                'amazon_link': 'https://www.amazon.com/RENPHO-Bluetooth-Body-Fat-Scale/dp/B01N1UX8RW/',
                'match_reason': 'Great for health and tech enthusiasts'
            }
        ],
        'creative': [
            {
                'name': 'Paint by Numbers Kit for Adults',
                'description': 'DIY Oil Painting with Frame, Brushes, and Acrylic Paint',
                'price': 19.99,
                'amazon_link': 'https://www.amazon.com/DECORARTIST-Paint-Numbers-Adults-Landscape/dp/B0BZ8B5QQK/',
                'etsy_link': 'https://www.etsy.com/listing/1619671517/paint-by-numbers-kit/',
                'match_reason': 'Perfect for creative expression'
            },
            {
                'name': 'Cricut Joy Machine',
                'description': 'Compact DIY Smart Cutting Machine',
                'price': 179.00,
                'amazon_link': 'https://www.amazon.com/Cricut-Joy-Machine-Compact-Cutting/dp/B0845CCDM5/',
                'match_reason': 'Ideal for DIY crafters'
            }
        ],
        'gaming': [
            {
                'name': 'Nintendo Switch OLED Model',
                'description': '7-inch OLED Screen, 64GB Storage',
                'price': 349.99,
                'amazon_link': 'https://www.amazon.com/Nintendo-Switch-OLED-Model-White-Joy/dp/B098RKWHHZ/',
                'match_reason': 'Perfect for gaming enthusiasts'
            },
            {
                'name': 'Logitech G502 HERO Gaming Mouse',
                'description': 'High Performance Gaming Mouse',
                'price': 39.99,
                'amazon_link': 'https://www.amazon.com/Logitech-G502-Performance-Gaming-Mouse/dp/B07GBZ4Q68/',
                'match_reason': 'Great for PC gamers'
            }
        ],
        'outdoor': [
            {
                'name': 'YETI Hopper Flip 12 Cooler',
                'description': 'Portable Soft Cooler',
                'price': 249.99,
                'amazon_link': 'https://www.amazon.com/YETI-Hopper-Portable-Cooler-Charcoal/dp/B07TQZMH2Z/',
                'match_reason': 'Perfect for outdoor adventures'
            },
            {
                'name': 'Hydro Flask Water Bottle',
                'description': '32 oz Wide Mouth with Flex Cap',
                'price': 44.95,
                'amazon_link': 'https://www.amazon.com/Hydro-Flask-Water-Bottle-Pacific/dp/B01ACAXURU/',
                'match_reason': 'Great for active lifestyles'
            }
        ],
        'photography': [
            {
                'name': 'Ring Light with Tripod Stand',
                'description': '12" LED Ring Light with Phone Holder',
                'price': 35.99,
                'amazon_link': 'https://www.amazon.com/UBeesize-Ringlight-YouTube-Photography-Compatible/dp/B08B3X7NXC/',
                'match_reason': 'Perfect for content creators'
            },
            {
                'name': 'Fujifilm Instax Mini 12 Camera',
                'description': 'Instant Camera with Auto Exposure',
                'price': 79.95,
                'amazon_link': 'https://www.amazon.com/Fujifilm-Instax-Mini-Camera-Pastel/dp/B0BVXF2GFH/',
                'match_reason': 'Great for instant photography'
            }
        ],
        'fashion': [
            {
                'name': 'PAVOI 14K Gold Plated Jewelry Set',
                'description': 'Dainty Necklace and Earring Set',
                'price': 14.95,
                'amazon_link': 'https://www.amazon.com/PAVOI-Plated-Sterling-Necklace-Earrings/dp/B07MQKFY5L/',
                'match_reason': 'Perfect for fashion lovers'
            },
            {
                'name': 'UGG Women\'s Scuffette II Slipper',
                'description': 'Suede Slipper with Wool Lining',
                'price': 94.95,
                'amazon_link': 'https://www.amazon.com/UGG-Womens-Scuffette-Slipper-Chestnut/dp/B0BN6QXWXJ/',
                'match_reason': 'Cozy and stylish'
            }
        ],
        'beauty': [
            {
                'name': 'LANEIGE Lip Sleeping Mask Set',
                'description': 'Holiday Collection Gift Set',
                'price': 45.00,
                'amazon_link': 'https://www.amazon.com/LANEIGE-Holiday-Collection-Sleeping-Original/dp/B0CKVWX2VG/',
                'match_reason': 'Perfect for skincare enthusiasts'
            },
            {
                'name': 'Revlon One-Step Hair Dryer',
                'description': 'Volumizing Hot Air Brush',
                'price': 39.99,
                'amazon_link': 'https://www.amazon.com/Revlon-One-Step-Volumizer-Original-Brush/dp/B01LSUQSB0/',
                'match_reason': 'Great for hair styling'
            }
        ],
        'home': [
            {
                'name': 'Yankee Candle Holiday Gift Set',
                'description': '3 Premium Holiday Scented Candles',
                'price': 29.99,
                'amazon_link': 'https://www.amazon.com/Yankee-Candle-Holiday-Season-Collection/dp/B0CGYD5S3L/',
                'match_reason': 'Perfect for holiday ambiance'
            },
            {
                'name': 'Barefoot Dreams CozyChic Throw',
                'description': 'Ultra Soft Premium Blanket',
                'price': 147.00,
                'amazon_link': 'https://www.amazon.com/Barefoot-Dreams-CozyChic-Throw-Blanket/dp/B002HWRSDG/',
                'match_reason': 'Luxuriously cozy'
            }
        ]
    }

    # Get weighted random categories
    categories = list(category_weights.keys())
    weights = [category_weights[cat] for cat in categories]
    
    # Normalize weights
    total_weight = sum(weights)
    normalized_weights = [w/total_weight for w in weights]
    
    # Select categories based on weights
    selected_categories = random.choices(
        categories,
        weights=normalized_weights,
        k=min(4, len(categories))
    )
    
    recommendations = []
    
    # Get recommendations from selected categories
    for category in selected_categories:
        available_gifts = [
            gift for gift in gift_database[category]
            if gift['price'] <= budget
        ]
        if available_gifts:
            recommendations.append(random.choice(available_gifts))
    
    # If we need more recommendations, add from other categories
    while len(recommendations) < 4 and len(recommendations) < len(gift_database):
        remaining_categories = [
            cat for cat in categories
            if cat not in [g.get('category', '') for g in recommendations]
        ]
        if not remaining_categories:
            break
            
        category = random.choice(remaining_categories)
        available_gifts = [
            gift for gift in gift_database[category]
            if gift['price'] <= budget and gift not in recommendations
        ]
        if available_gifts:
            recommendations.append(random.choice(available_gifts))
    
    # Shuffle final recommendations
    random.shuffle(recommendations)
    
    return recommendations[:4]
