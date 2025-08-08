from flask import Blueprint, request, jsonify
from src.models.mood import db, Mood, TestResult
from datetime import datetime

mood_bp = Blueprint('mood', __name__)

@mood_bp.route('/mood', methods=['POST'])
def save_mood():
    try:
        data = request.get_json()
        mood_level = data.get('mood_level')
        notes = data.get('notes', '')
        
        if not mood_level:
            return jsonify({'error': 'Mood level is required'}), 400
        
        mood = Mood(
            mood_level=mood_level,
            notes=notes
        )
        
        db.session.add(mood)
        db.session.commit()
        
        return jsonify({
            'message': 'Mood saved successfully',
            'mood': mood.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@mood_bp.route('/mood', methods=['GET'])
def get_moods():
    try:
        moods = Mood.query.order_by(Mood.date_created.desc()).limit(10).all()
        return jsonify([mood.to_dict() for mood in moods])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@mood_bp.route('/test-result', methods=['POST'])
def save_test_result():
    try:
        data = request.get_json()
        test_type = data.get('test_type')
        score = data.get('score')
        result_category = data.get('result_category')
        
        if not all([test_type, score is not None, result_category]):
            return jsonify({'error': 'All fields are required'}), 400
        
        test_result = TestResult(
            test_type=test_type,
            score=score,
            result_category=result_category
        )
        
        db.session.add(test_result)
        db.session.commit()
        
        return jsonify({
            'message': 'Test result saved successfully',
            'result': test_result.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@mood_bp.route('/test-results', methods=['GET'])
def get_test_results():
    try:
        results = TestResult.query.order_by(TestResult.date_created.desc()).limit(10).all()
        return jsonify([result.to_dict() for result in results])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

