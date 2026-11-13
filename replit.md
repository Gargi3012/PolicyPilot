# India Policy Impact Simulator

## Overview

This is an AI-powered web application specifically designed for India that simulates and predicts the real-world impacts of Indian government policies on economic indicators like GDP, inflation, unemployment, and environmental factors across different Indian regions. The system uses machine learning models trained on Indian historical data to analyze policy inputs and generate comprehensive impact predictions with confidence scores and detailed reports.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Flask with Jinja2 templating
- **UI Framework**: Bootstrap 5.3 for responsive design
- **JavaScript Libraries**: Chart.js for data visualization, custom JavaScript for dashboard interactions
- **Styling**: Custom CSS with CSS variables for theming and responsive design
- **Components**: Multi-page web application with forms, dashboards, comparison views, and results pages

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Database ORM**: SQLAlchemy with Flask-SQLAlchemy extension
- **Machine Learning**: Scikit-learn with Random Forest and Linear Regression models
- **Report Generation**: ReportLab for PDF report creation
- **Data Processing**: Custom data processing pipeline with economic indicators

### Database Architecture
- **Primary Database**: SQLite (configurable to other databases via DATABASE_URL)
- **Models**: 
  - `Policy`: Stores policy configurations and metadata
  - `PolicyPrediction`: Stores ML prediction results linked to policies
  - `HistoricalPolicy`: Stores historical policy data for model training and comparison
- **Relationships**: One-to-many between Policy and PolicyPrediction with cascade deletion

## Key Components

### Machine Learning Engine (`ml_models.py`)
- **Purpose**: Core prediction engine using ensemble methods
- **Models**: Separate models for GDP, inflation, unemployment, and environmental impact
- **Features**: Sector multipliers, regional factors, and synthetic training data generation
- **Approach**: Random Forest for complex economic indicators, Linear Regression for environmental impact

### Data Processing (`data_processor.py`, `data/`)
- **Indian Historical Data Loader**: Loads sample Indian historical policies like GST, Digital India, Make in India for model validation
- **Indian Economic Baseline Data**: Indian regional economic indicators for all 6 major regions with state-wise data
- **Indian Sample Policies**: Pre-configured Indian policy examples including sector-specific initiatives
- **State-wise Economic Data**: Detailed economic data for major Indian states with GDP contribution, unemployment rates, and key industries

### Report Generation (`pdf_generator.py`)
- **Purpose**: Creates comprehensive PDF reports with charts and analysis
- **Features**: Policy details, prediction results, confidence scores, and visualizations
- **Technology**: ReportLab for professional PDF generation

### Web Interface
- **Dashboard**: Overview of all policies with statistics and filtering
- **Policy Input Form**: User-friendly form for policy configuration
- **Results View**: Detailed prediction results with interactive charts
- **Comparison Tools**: Side-by-side policy comparison functionality

## Data Flow

1. **Policy Input**: User submits policy details through web form
2. **Data Validation**: Backend validates and sanitizes input data
3. **ML Prediction**: Policy parameters fed to trained ML models
4. **Impact Calculation**: Models generate predictions for economic indicators
5. **Data Storage**: Policy and predictions stored in database
6. **Results Display**: Web interface shows predictions with confidence scores
7. **Report Generation**: Optional PDF report creation for detailed analysis
8. **Dashboard Update**: New policy appears in dashboard overview

## External Dependencies

### Python Packages
- **Flask**: Web framework and routing
- **SQLAlchemy**: Database ORM and migrations
- **Scikit-learn**: Machine learning models and preprocessing
- **ReportLab**: PDF generation and charts
- **NumPy/Pandas**: Data manipulation and analysis
- **Werkzeug**: WSGI utilities and security

### Frontend Libraries
- **Bootstrap 5.3**: CSS framework and components
- **Chart.js**: Interactive charts and data visualization
- **Font Awesome**: Icon library
- **Custom CSS**: Application-specific styling

### Database
- **SQLite**: Default database (production-ready for PostgreSQL via DATABASE_URL)
- **Database migrations**: Handled by SQLAlchemy with automatic table creation

## Deployment Strategy

### Environment Configuration
- **Environment Variables**: DATABASE_URL, SESSION_SECRET for production security
- **Development Mode**: Debug mode enabled for local development
- **Production Ready**: ProxyFix middleware for reverse proxy deployment

### Database Setup
- **Automatic Migration**: Tables created automatically on startup
- **Sample Data**: Historical data loaded on first run
- **Connection Pooling**: Configured for production database connections

### Scalability Considerations
- **Model Caching**: ML models initialized once at startup
- **Database Optimization**: Connection pooling and query optimization
- **Static Assets**: CDN-ready static file serving
- **Session Management**: Secure session handling with configurable secrets

### Monitoring and Logging
- **Application Logging**: Comprehensive logging throughout the application
- **Error Handling**: Graceful error handling with user feedback
- **Performance Tracking**: Database query monitoring and optimization