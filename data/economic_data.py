"""
Economic indicators and baseline data for policy impact calculations
"""

# Indian economic baseline indicators (2024 estimates)
INDIAN_BASELINES = {
    'gdp_growth_rate': 6.7,  # Annual GDP growth percentage for India
    'inflation_rate': 5.1,   # Annual inflation percentage for India
    'unemployment_rate': 5.3, # Unemployment percentage for India
    'co2_emissions': 2.88,   # India's CO2 emissions in gigatons
    'population': 1428.6,    # Population in millions
    'per_capita_income': 2380, # USD per capita
}

# Indian Regional Economic Characteristics (State-wise)
REGIONAL_INDICATORS = {
    'Northern India': {
        'gdp_growth_rate': 6.8,
        'inflation_rate': 5.2,
        'unemployment_rate': 4.8,
        'economic_stability': 0.75,
        'policy_responsiveness': 0.80,
        'major_states': ['Delhi', 'Punjab', 'Haryana', 'Uttar Pradesh', 'Rajasthan'],
        'primary_sectors': ['Agriculture', 'Manufacturing', 'Technology']
    },
    'Western India': {
        'gdp_growth_rate': 8.2,
        'inflation_rate': 4.8,
        'unemployment_rate': 3.5,
        'economic_stability': 0.85,
        'policy_responsiveness': 0.85,
        'major_states': ['Maharashtra', 'Gujarat', 'Rajasthan', 'Goa'],
        'primary_sectors': ['Finance', 'Manufacturing', 'Technology']
    },
    'Southern India': {
        'gdp_growth_rate': 7.5,
        'inflation_rate': 4.5,
        'unemployment_rate': 4.2,
        'economic_stability': 0.80,
        'policy_responsiveness': 0.88,
        'major_states': ['Karnataka', 'Tamil Nadu', 'Andhra Pradesh', 'Kerala', 'Telangana'],
        'primary_sectors': ['Technology', 'Manufacturing', 'Healthcare']
    },
    'Eastern India': {
        'gdp_growth_rate': 5.8,
        'inflation_rate': 5.8,
        'unemployment_rate': 6.2,
        'economic_stability': 0.65,
        'policy_responsiveness': 0.75,
        'major_states': ['West Bengal', 'Odisha', 'Jharkhand', 'Bihar'],
        'primary_sectors': ['Manufacturing', 'Agriculture', 'Energy']
    },
    'North-Eastern India': {
        'gdp_growth_rate': 6.2,
        'inflation_rate': 6.1,
        'unemployment_rate': 5.8,
        'economic_stability': 0.60,
        'policy_responsiveness': 0.82,
        'major_states': ['Assam', 'Meghalaya', 'Tripura', 'Manipur', 'Mizoram'],
        'primary_sectors': ['Agriculture', 'Energy', 'Transportation']
    },
    'Central India': {
        'gdp_growth_rate': 6.0,
        'inflation_rate': 5.5,
        'unemployment_rate': 5.2,
        'economic_stability': 0.70,
        'policy_responsiveness': 0.78,
        'major_states': ['Madhya Pradesh', 'Chhattisgarh'],
        'primary_sectors': ['Agriculture', 'Manufacturing', 'Energy']
    }
}

# Detailed Indian State Economic Data
INDIAN_STATE_DATA = {
    'Maharashtra': {
        'gdp_contribution': 14.8,  # % of India's GDP
        'population': 112.4,       # millions
        'gdp_growth_rate': 8.1,
        'unemployment_rate': 3.2,
        'inflation_rate': 4.5,
        'major_cities': ['Mumbai', 'Pune', 'Nagpur'],
        'key_industries': ['Finance', 'Manufacturing', 'IT', 'Entertainment']
    },
    'Tamil Nadu': {
        'gdp_contribution': 8.5,
        'population': 72.1,
        'gdp_growth_rate': 7.8,
        'unemployment_rate': 4.1,
        'inflation_rate': 4.3,
        'major_cities': ['Chennai', 'Coimbatore', 'Madurai'],
        'key_industries': ['Manufacturing', 'IT', 'Healthcare', 'Textiles']
    },
    'Gujarat': {
        'gdp_contribution': 7.6,
        'population': 60.4,
        'gdp_growth_rate': 8.5,
        'unemployment_rate': 2.8,
        'inflation_rate': 4.2,
        'major_cities': ['Ahmedabad', 'Surat', 'Vadodara'],
        'key_industries': ['Chemicals', 'Textiles', 'Energy', 'Manufacturing']
    },
    'Karnataka': {
        'gdp_contribution': 7.3,
        'population': 61.1,
        'gdp_growth_rate': 7.9,
        'unemployment_rate': 3.8,
        'inflation_rate': 4.1,
        'major_cities': ['Bangalore', 'Mysore', 'Hubli'],
        'key_industries': ['IT', 'Biotechnology', 'Aerospace', 'Manufacturing']
    },
    'Uttar Pradesh': {
        'gdp_contribution': 9.2,
        'population': 199.8,
        'gdp_growth_rate': 6.2,
        'unemployment_rate': 5.8,
        'inflation_rate': 5.5,
        'major_cities': ['Lucknow', 'Kanpur', 'Agra'],
        'key_industries': ['Agriculture', 'Manufacturing', 'Textiles', 'Tourism']
    },
    'West Bengal': {
        'gdp_contribution': 6.1,
        'population': 91.3,
        'gdp_growth_rate': 5.5,
        'unemployment_rate': 6.5,
        'inflation_rate': 5.8,
        'major_cities': ['Kolkata', 'Howrah', 'Durgapur'],
        'key_industries': ['Manufacturing', 'IT', 'Healthcare', 'Jute']
    },
    'Andhra Pradesh': {
        'gdp_contribution': 4.9,
        'population': 49.4,
        'gdp_growth_rate': 7.2,
        'unemployment_rate': 4.5,
        'inflation_rate': 4.8,
        'major_cities': ['Visakhapatnam', 'Vijayawada', 'Guntur'],
        'key_industries': ['IT', 'Pharmaceuticals', 'Agriculture', 'Manufacturing']
    },
    'Telangana': {
        'gdp_contribution': 4.7,
        'population': 35.0,
        'gdp_growth_rate': 8.7,
        'unemployment_rate': 3.9,
        'inflation_rate': 4.4,
        'major_cities': ['Hyderabad', 'Warangal', 'Nizamabad'],
        'key_industries': ['IT', 'Pharmaceuticals', 'Biotechnology', 'Aerospace']
    },
    'Kerala': {
        'gdp_contribution': 3.8,
        'population': 33.4,
        'gdp_growth_rate': 6.8,
        'unemployment_rate': 5.1,
        'inflation_rate': 4.6,
        'major_cities': ['Thiruvananthapuram', 'Kochi', 'Kozhikode'],
        'key_industries': ['IT', 'Tourism', 'Spices', 'Marine Products']
    },
    'Rajasthan': {
        'gdp_contribution': 5.2,
        'population': 68.5,
        'gdp_growth_rate': 6.5,
        'unemployment_rate': 5.3,
        'inflation_rate': 5.2,
        'major_cities': ['Jaipur', 'Jodhpur', 'Udaipur'],
        'key_industries': ['Tourism', 'Mining', 'Textiles', 'Agriculture']
    }
}

# Sector-specific economic impact coefficients
SECTOR_COEFFICIENTS = {
    'Energy': {
        'gdp_elasticity': 0.15,      # How much GDP responds to energy policy changes
        'inflation_impact': 0.25,     # Energy's impact on inflation
        'employment_multiplier': 0.8, # Job creation/loss multiplier
        'environmental_factor': 2.5   # Environmental impact multiplier
    },
    'Healthcare': {
        'gdp_elasticity': 0.08,
        'inflation_impact': 0.12,
        'employment_multiplier': 1.2,
        'environmental_factor': 0.1
    },
    'Education': {
        'gdp_elasticity': 0.12,
        'inflation_impact': 0.05,
        'employment_multiplier': 1.1,
        'environmental_factor': 0.05
    },
    'Transportation': {
        'gdp_elasticity': 0.18,
        'inflation_impact': 0.20,
        'employment_multiplier': 0.9,
        'environmental_factor': 1.8
    },
    'Agriculture': {
        'gdp_elasticity': 0.10,
        'inflation_impact': 0.30,
        'employment_multiplier': 1.0,
        'environmental_factor': 1.2
    },
    'Finance': {
        'gdp_elasticity': 0.22,
        'inflation_impact': 0.15,
        'employment_multiplier': 0.7,
        'environmental_factor': 0.02
    },
    'Technology': {
        'gdp_elasticity': 0.25,
        'inflation_impact': 0.08,
        'employment_multiplier': 0.6,
        'environmental_factor': 0.3
    },
    'Manufacturing': {
        'gdp_elasticity': 0.20,
        'inflation_impact': 0.18,
        'employment_multiplier': 1.0,
        'environmental_factor': 1.5
    }
}

# Time-dependent decay factors (how policy effects diminish over time)
TIME_DECAY_FACTORS = {
    'immediate': 1.0,    # 0-6 months
    'short_term': 0.8,   # 6-18 months
    'medium_term': 0.6,  # 18-36 months
    'long_term': 0.4     # 36+ months
}

# Inter-sector dependency matrix (how policies in one sector affect others)
SECTOR_DEPENDENCIES = {
    'Energy': {
        'Transportation': 0.7,
        'Manufacturing': 0.6,
        'Technology': 0.3,
        'Agriculture': 0.4,
        'Healthcare': 0.2,
        'Education': 0.1,
        'Finance': 0.3
    },
    'Transportation': {
        'Energy': 0.8,
        'Manufacturing': 0.5,
        'Agriculture': 0.4,
        'Technology': 0.3,
        'Healthcare': 0.2,
        'Education': 0.2,
        'Finance': 0.3
    },
    'Manufacturing': {
        'Energy': 0.7,
        'Transportation': 0.6,
        'Technology': 0.5,
        'Agriculture': 0.3,
        'Healthcare': 0.2,
        'Education': 0.3,
        'Finance': 0.4
    },
    'Technology': {
        'Finance': 0.6,
        'Manufacturing': 0.5,
        'Education': 0.7,
        'Healthcare': 0.4,
        'Energy': 0.3,
        'Transportation': 0.3,
        'Agriculture': 0.2
    },
    'Healthcare': {
        'Education': 0.4,
        'Technology': 0.3,
        'Finance': 0.3,
        'Energy': 0.2,
        'Transportation': 0.2,
        'Manufacturing': 0.2,
        'Agriculture': 0.1
    },
    'Education': {
        'Technology': 0.6,
        'Healthcare': 0.3,
        'Manufacturing': 0.4,
        'Finance': 0.3,
        'Energy': 0.2,
        'Transportation': 0.2,
        'Agriculture': 0.2
    },
    'Finance': {
        'Technology': 0.5,
        'Manufacturing': 0.6,
        'Energy': 0.4,
        'Transportation': 0.3,
        'Healthcare': 0.3,
        'Education': 0.3,
        'Agriculture': 0.3
    },
    'Agriculture': {
        'Energy': 0.5,
        'Transportation': 0.4,
        'Manufacturing': 0.3,
        'Technology': 0.2,
        'Finance': 0.3,
        'Healthcare': 0.1,
        'Education': 0.2
    }
}

# Economic shock sensitivity by Indian region
SHOCK_SENSITIVITY = {
    'Northern India': 1.1,    # Moderate sensitivity due to mixed economy
    'Western India': 0.8,     # Lower sensitivity due to strong industrial base
    'Southern India': 0.9,    # Moderate-low sensitivity due to tech sector
    'Eastern India': 1.3,     # Higher sensitivity due to industrial challenges
    'North-Eastern India': 1.4, # High sensitivity due to remote location
    'Central India': 1.2      # Moderate-high sensitivity due to agrarian economy
}

# Policy implementation difficulty factors
IMPLEMENTATION_DIFFICULTY = {
    'Energy': 0.8,        # High infrastructure requirements
    'Healthcare': 0.9,    # Complex regulatory environment
    'Education': 0.6,     # Moderate implementation complexity
    'Transportation': 0.8, # Infrastructure dependent
    'Agriculture': 0.5,   # Relatively straightforward
    'Finance': 0.7,       # Regulatory complexity
    'Technology': 0.4,    # Fast implementation possible
    'Manufacturing': 0.6  # Moderate complexity
}

def get_time_decay_factor(time_period):
    """Get the appropriate time decay factor based on policy duration"""
    if time_period <= 6:
        return TIME_DECAY_FACTORS['immediate']
    elif time_period <= 18:
        return TIME_DECAY_FACTORS['short_term']
    elif time_period <= 36:
        return TIME_DECAY_FACTORS['medium_term']
    else:
        return TIME_DECAY_FACTORS['long_term']

def calculate_cross_sector_effects(primary_sector, impact_magnitude):
    """Calculate how a policy in one sector affects other sectors"""
    if primary_sector not in SECTOR_DEPENDENCIES:
        return {}
    
    cross_effects = {}
    dependencies = SECTOR_DEPENDENCIES[primary_sector]
    
    for sector, dependency_factor in dependencies.items():
        cross_effects[sector] = impact_magnitude * dependency_factor * 0.3  # 30% spillover
    
    return cross_effects

def get_regional_adjustment(region, base_impact):
    """Adjust policy impact based on regional economic characteristics"""
    if region not in REGIONAL_INDICATORS:
        return base_impact
    
    regional_data = REGIONAL_INDICATORS[region]
    stability_factor = regional_data['economic_stability']
    responsiveness = regional_data['policy_responsiveness']
    
    # More stable regions have dampened policy effects
    # More responsive regions have amplified policy effects
    adjusted_impact = base_impact * responsiveness * (2 - stability_factor)
    
    return adjusted_impact
