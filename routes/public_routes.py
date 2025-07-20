from flask import Blueprint, jsonify, request
from models import Service, Event, GalleryItem, BlogPost, FAQ, Testimonial, Inquiry
from extensions import db
from utils.email import send_inquiry_email

public_bp = Blueprint('public', __name__)

@public_bp.route('/services', methods=['GET'])
def get_services():
    services = Service.query.all()
    return jsonify([{
        'id': s.id, 'name': s.name, 'description': s.description, 'icon': s.icon, 'created_at': s.created_at.isoformat() if s.created_at else None
    } for s in services])

@public_bp.route('/events', methods=['GET'])
def get_events():
    events = Event.query.all()
    return jsonify([{
        'id': e.id, 'title': e.title, 'description': e.description, 'date': e.date, 'category': e.category, 'media': e.media, 'created_at': e.created_at.isoformat() if e.created_at else None
    } for e in events])

@public_bp.route('/gallery', methods=['GET'])
def get_gallery():
    items = GalleryItem.query.all()
    return jsonify([{
        'id': g.id, 'filename': g.filename, 'category': g.category, 'description': g.description, 'created_at': g.created_at.isoformat() if g.created_at else None
    } for g in items])

@public_bp.route('/blogs', methods=['GET'])
def get_blogs():
    posts = BlogPost.query.all()
    return jsonify([{
        'id': b.id, 'title': b.title, 'content': b.content, 'cover_image': b.cover_image, 'tags': b.tags, 'published_at': b.published_at.isoformat() if b.published_at else None, 'created_at': b.created_at.isoformat() if b.created_at else None
    } for b in posts])

@public_bp.route('/faqs', methods=['GET'])
def get_faqs():
    faqs = FAQ.query.all()
    return jsonify([{
        'id': f.id, 'question': f.question, 'answer': f.answer, 'created_at': f.created_at.isoformat() if f.created_at else None
    } for f in faqs])

@public_bp.route('/testimonials', methods=['GET'])
def get_testimonials():
    testimonials = Testimonial.query.all()
    return jsonify([{
        'id': t.id, 'name': t.name, 'message': t.message, 'event_name': t.event_name, 'date': t.date, 'created_at': t.created_at.isoformat() if t.created_at else None
    } for t in testimonials])

@public_bp.route('/inquiries', methods=['GET'])
def get_inquiries():
    inquiries = Inquiry.query.all()
    return jsonify([{
        'id': i.id, 'name': i.name, 'email': i.email, 'phone': i.phone, 'event_type': i.event_type, 'event_date': i.event_date, 'budget': i.budget, 'message': i.message, 'status': i.status, 'created_at': i.created_at.isoformat() if i.created_at else None
    } for i in inquiries])

@public_bp.route('/inquiries', methods=['POST'])
def create_inquiry():
    data = request.json
    inquiry = Inquiry(
        name=data.get('name'),
        email=data.get('email'),
        phone=data.get('phone'),
        event_type=data.get('event_type'),
        event_date=data.get('event_date'),
        budget=data.get('budget'),
        message=data.get('message')
    )
    db.session.add(inquiry)
    db.session.commit()
    send_inquiry_email(inquiry)
    return jsonify({'message': 'Inquiry submitted successfully.'}), 201
