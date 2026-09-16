"""
Sample Indian policy examples for testing the simulator
"""

SAMPLE_INDIAN_POLICIES = [
    {
        'name': 'National Education Policy 2020 Implementation',
        'sector': 'Education',
        'region': 'Northern India',
        'numeric_change': 25.0,
        'time_period': 60,
        'description': 'Comprehensive education reform focusing on foundational literacy and numeracy, multilingual education, and vocational training integration.'
    },
    {
        'name': 'Solar Rooftop Subsidy Scheme',
        'sector': 'Energy',
        'region': 'Western India',
        'numeric_change': 40.0,
        'time_period': 36,
        'description': 'Subsidy for residential and commercial solar rooftop installations to achieve renewable energy targets.'
    },
    {
        'name': 'IT Hub Development in Tier-2 Cities',
        'sector': 'Technology',
        'region': 'Southern India',
        'numeric_change': 30.0,
        'time_period': 48,
        'description': 'Infrastructure development and incentives for IT companies to establish operations in tier-2 cities.'
    },
    {
        'name': 'Rural Healthcare Infrastructure Enhancement',
        'sector': 'Healthcare',
        'region': 'Eastern India',
        'numeric_change': 35.0,
        'time_period': 42,
        'description': 'Upgrading rural health centers, telemedicine facilities, and medical equipment in rural areas.'
    },
    {
        'name': 'Organic Farming Incentive Program',
        'sector': 'Agriculture',
        'region': 'Central India',
        'numeric_change': 20.0,
        'time_period': 36,
        'description': 'Financial incentives and technical support for farmers transitioning to organic farming methods.'
    },
    {
        'name': 'Digital Payment Infrastructure Expansion',
        'sector': 'Finance',
        'region': 'North-Eastern India',
        'numeric_change': 50.0,
        'time_period': 24,
        'description': 'Expanding digital payment infrastructure and financial inclusion in remote areas.'
    },
    {
        'name': 'Electric Vehicle Manufacturing Incentives',
        'sector': 'Manufacturing',
        'region': 'Western India',
        'numeric_change': 45.0,
        'time_period': 60,
        'description': 'Production-linked incentives for electric vehicle and battery manufacturing.'
    },
    {
        'name': 'High-Speed Rail Connectivity Project',
        'sector': 'Transportation',
        'region': 'Western India',
        'numeric_change': 60.0,
        'time_period': 120,
        'description': 'High-speed rail network development between major economic centers.'
    }
]

# Regional policy success factors based on Indian economic patterns
REGIONAL_POLICY_FACTORS = {
    'Northern India': {
        'agriculture_weight': 0.3,
        'manufacturing_weight': 0.25,
        'services_weight': 0.25,
        'technology_weight': 0.2,
        'policy_implementation_ease': 0.75
    },
    'Western India': {
        'agriculture_weight': 0.15,
        'manufacturing_weight': 0.35,
        'services_weight': 0.3,
        'technology_weight': 0.2,
        'policy_implementation_ease': 0.85
    },
    'Southern India': {
        'agriculture_weight': 0.2,
        'manufacturing_weight': 0.25,
        'services_weight': 0.25,
        'technology_weight': 0.3,
        'policy_implementation_ease': 0.9
    },
    'Eastern India': {
        'agriculture_weight': 0.35,
        'manufacturing_weight': 0.3,
        'services_weight': 0.2,
        'technology_weight': 0.15,
        'policy_implementation_ease': 0.7
    },
    'North-Eastern India': {
        'agriculture_weight': 0.4,
        'manufacturing_weight': 0.15,
        'services_weight': 0.2,
        'technology_weight': 0.25,
        'policy_implementation_ease': 0.65
    },
    'Central India': {
        'agriculture_weight': 0.4,
        'manufacturing_weight': 0.25,
        'services_weight': 0.2,
        'technology_weight': 0.15,
        'policy_implementation_ease': 0.7
    }
}