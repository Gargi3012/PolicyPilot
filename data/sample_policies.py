"""
Sample policy configurations for testing and demonstration
"""

SAMPLE_POLICIES = [
    {
        'name': 'Green Energy Transition Tax Credit',
        'sector': 'Energy',
        'region': 'North America',
        'numeric_change': 15.0,
        'time_period': 24,
        'description': 'Tax credits for businesses transitioning to renewable energy sources'
    },
    {
        'name': 'Universal Basic Healthcare',
        'sector': 'Healthcare',
        'region': 'Europe',
        'numeric_change': 25.0,
        'time_period': 36,
        'description': 'Implementation of universal healthcare coverage for all citizens'
    },
    {
        'name': 'Digital Skills Training Initiative',
        'sector': 'Education',
        'region': 'Asia',
        'numeric_change': 20.0,
        'time_period': 18,
        'description': 'Nationwide program to train workers in digital and technology skills'
    },
    {
        'name': 'Carbon Emission Reduction Mandate',
        'sector': 'Manufacturing',
        'region': 'Europe',
        'numeric_change': -30.0,
        'time_period': 48,
        'description': 'Mandatory reduction in carbon emissions for manufacturing companies'
    },
    {
        'name': 'Small Business Support Package',
        'sector': 'Finance',
        'region': 'North America',
        'numeric_change': 10.0,
        'time_period': 12,
        'description': 'Financial support and tax breaks for small and medium enterprises'
    }
]

SECTOR_DESCRIPTIONS = {
    'Energy': 'Policies affecting energy production, distribution, and consumption',
    'Healthcare': 'Healthcare system reforms, coverage, and medical services',
    'Education': 'Educational system changes, funding, and skill development programs',
    'Transportation': 'Infrastructure, public transit, and transportation policies',
    'Agriculture': 'Agricultural subsidies, farming practices, and food security',
    'Finance': 'Economic policies, taxation, and financial system regulation',
    'Technology': 'Digital transformation, innovation incentives, and tech regulation',
    'Manufacturing': 'Industrial policies, trade regulations, and production standards'
}

REGION_INFO = {
    'North America': {
        'description': 'United States, Canada, and Mexico',
        'economic_characteristics': 'Developed economies with service-oriented focus'
    },
    'Europe': {
        'description': 'European Union and associated countries',
        'economic_characteristics': 'Mature economies with strong social systems'
    },
    'Asia': {
        'description': 'Asian countries including China, India, Japan, and Southeast Asia',
        'economic_characteristics': 'Diverse economies with high growth potential'
    },
    'Africa': {
        'description': 'African continent countries',
        'economic_characteristics': 'Developing economies with resource-based focus'
    },
    'South America': {
        'description': 'South American countries',
        'economic_characteristics': 'Emerging economies with commodity dependence'
    },
    'Oceania': {
        'description': 'Australia, New Zealand, and Pacific islands',
        'economic_characteristics': 'Developed economies with resource exports'
    }
}
