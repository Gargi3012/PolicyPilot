from flask import render_template, request, flash, redirect, url_for, jsonify, send_file
from app import app, db
from models import Policy, PolicyPrediction, HistoricalPolicy
from ml_models import PolicyImpactPredictor
from pdf_generator import generate_policy_report
from data_processor import load_historical_data
import logging
import io

# Initialize the ML predictor
predictor = PolicyImpactPredictor()

@app.route('/')
def index():
    """Home page with policy input form"""
    recent_policies = Policy.query.order_by(Policy.created_at.desc()).limit(5).all()
    return render_template('index.html', recent_policies=recent_policies)

@app.route('/dashboard')
def dashboard():
    """Dashboard showing overview of all policies and predictions"""
    policies = Policy.query.order_by(Policy.created_at.desc()).all()
    total_policies = len(policies)
    
    # Calculate average impacts
    predictions = PolicyPrediction.query.all()
    avg_gdp_impact = sum(p.gdp_impact or 0 for p in predictions) / len(predictions) if predictions else 0
    avg_inflation_impact = sum(p.inflation_impact or 0 for p in predictions) / len(predictions) if predictions else 0
    avg_unemployment_impact = sum(p.unemployment_impact or 0 for p in predictions) / len(predictions) if predictions else 0
    
    return render_template('dashboard.html', 
                         policies=policies,
                         total_policies=total_policies,
                         avg_gdp_impact=avg_gdp_impact,
                         avg_inflation_impact=avg_inflation_impact,
                         avg_unemployment_impact=avg_unemployment_impact)

@app.route('/simulate', methods=['POST'])
def simulate_policy():
    """Handle policy simulation request"""
    try:
        # Extract form data
        policy_name = request.form.get('policy_name')
        sector = request.form.get('sector')
        region = request.form.get('region')
        numeric_change = float(request.form.get('numeric_change', 0))
        time_period = int(request.form.get('time_period', 12))
        description = request.form.get('description', '')
        
        # Validate inputs
        if not all([policy_name, sector, region]):
            flash('Please fill in all required fields.', 'error')
            return redirect(url_for('index'))
        
        # Create new policy record
        policy = Policy(
            name=policy_name,
            sector=sector,
            region=region,
            numeric_change=numeric_change,
            time_period=time_period,
            description=description
        )
        
        db.session.add(policy)
        db.session.commit()
        
        # Generate predictions using ML model
        prediction_data = predictor.predict_impact(
            sector=sector,
            numeric_change=numeric_change,
            time_period=time_period,
            region=region
        )
        
        # Create prediction record
        prediction = PolicyPrediction(
            policy_id=policy.id,
            gdp_impact=prediction_data['gdp_impact'],
            inflation_impact=prediction_data['inflation_impact'],
            unemployment_impact=prediction_data['unemployment_impact'],
            environmental_impact=prediction_data['environmental_impact'],
            confidence_score=prediction_data['confidence_score'],
            sentiment_score=prediction_data.get('sentiment_score', 0),
            sentiment_confidence=prediction_data.get('sentiment_confidence', 0)
        )
        
        prediction.set_sector_breakdown(prediction_data['sector_breakdown'])
        
        db.session.add(prediction)
        db.session.commit()
        
        flash('Policy simulation completed successfully!', 'success')
        return redirect(url_for('view_results', policy_id=policy.id))
        
    except ValueError as e:
        flash(f'Invalid input: {str(e)}', 'error')
        return redirect(url_for('index'))
    except Exception as e:
        logging.error(f'Error in simulate_policy: {str(e)}')
        flash('An error occurred during simulation. Please try again.', 'error')
        return redirect(url_for('index'))

@app.route('/results/<int:policy_id>')
def view_results(policy_id):
    """View simulation results for a specific policy"""
    policy = Policy.query.get_or_404(policy_id)
    prediction = PolicyPrediction.query.filter_by(policy_id=policy_id).first()
    
    if not prediction:
        flash('No prediction found for this policy.', 'error')
        return redirect(url_for('dashboard'))
    
    # Find similar historical policies
    similar_policies = HistoricalPolicy.query.filter_by(sector=policy.sector).limit(3).all()
    
    return render_template('results.html', 
                         policy=policy, 
                         prediction=prediction,
                         similar_policies=similar_policies)

@app.route('/compare')
def compare_policies():
    """Compare multiple policies"""
    policy_ids = request.args.getlist('policies')
    
    if len(policy_ids) < 2:
        flash('Please select at least 2 policies to compare.', 'error')
        return redirect(url_for('dashboard'))
    
    policies_data = []
    for policy_id in policy_ids:
        policy = Policy.query.get(policy_id)
        if policy:
            prediction = PolicyPrediction.query.filter_by(policy_id=policy_id).first()
            policies_data.append({
                'policy': policy,
                'prediction': prediction
            })
    
    return render_template('comparison.html', policies_data=policies_data)

@app.route('/export_pdf/<int:policy_id>')
def export_pdf(policy_id):
    """Generate and download PDF report for a policy"""
    policy = Policy.query.get_or_404(policy_id)
    prediction = PolicyPrediction.query.filter_by(policy_id=policy_id).first()
    
    if not prediction:
        flash('No prediction found for this policy.', 'error')
        return redirect(url_for('dashboard'))
    
    try:
        # Generate PDF report
        pdf_buffer = generate_policy_report(policy, prediction)
        
        # Return PDF as download
        return send_file(
            io.BytesIO(pdf_buffer),
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'policy_report_{policy.name.replace(" ", "_")}.pdf'
        )
        
    except Exception as e:
        logging.error(f'Error generating PDF: {str(e)}')
        flash('Error generating PDF report. Please try again.', 'error')
        return redirect(url_for('view_results', policy_id=policy_id))

@app.route('/api/policy_data/<int:policy_id>')
def get_policy_data(policy_id):
    """API endpoint to get policy data for charts"""
    policy = Policy.query.get_or_404(policy_id)
    prediction = PolicyPrediction.query.filter_by(policy_id=policy_id).first()
    
    if not prediction:
        return jsonify({'error': 'No prediction found'}), 404
    
    return jsonify({
        'policy': policy.to_dict(),
        'prediction': prediction.to_dict()
    })

@app.route('/load_sample_data')
def load_sample_data():
    """Load sample historical policy data"""
    try:
        load_historical_data()
        flash('Sample historical data loaded successfully!', 'success')
    except Exception as e:
        logging.error(f'Error loading sample data: {str(e)}')
        flash('Error loading sample data.', 'error')
    
    return redirect(url_for('dashboard'))

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
