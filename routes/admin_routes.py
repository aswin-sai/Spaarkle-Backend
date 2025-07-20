from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import Service, Event, GalleryItem, BlogPost, FAQ, Testimonial, Inquiry
from extensions import db

admin_bp = Blueprint('admin', __name__)

# Example for services CRUD (repeat for other models)
@admin_bp.route('/services', methods=['POST'])
@jwt_required()
def create_service():
    data = request.json
    service = Service(
        name=data.get('name'),
        description=data.get('description'),
        icon=data.get('icon')
    )
    db.session.add(service)
    db.session.commit()
    return jsonify({'id': service.id}), 201

@admin_bp.route('/services/<int:id>', methods=['PUT'])
@jwt_required()
def update_service(id):
    service = Service.query.get_or_404(id)
    data = request.json
    service.name = data.get('name', service.name)
    service.description = data.get('description', service.description)
    service.icon = data.get('icon', service.icon)
    db.session.commit()
    return jsonify({'message': 'Updated'})

@admin_bp.route('/services/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_service(id):
    service = Service.query.get_or_404(id)
    db.session.delete(service)
    db.session.commit()
    return jsonify({'message': 'Deleted'})

@admin_bp.route('/services', methods=['GET'])
@jwt_required()
def list_services():
    try:
        services = Service.query.all()
        return jsonify([
            {
                'id': s.id,
                'name': s.name,
                'description': s.description,
                'icon': s.icon
            } for s in services
        ])
    except Exception as e:
        print('Error in list_services:', e)
        # Always return a list, even on error
        return jsonify([]), 200

@admin_bp.route('/services/<int:id>', methods=['GET'])
@jwt_required()
def get_service(id):
    s = Service.query.get_or_404(id)
    return jsonify({
        'id': s.id,
        'name': s.name,
        'description': s.description,
        'icon': s.icon
    })

# EVENTS CRUD
@admin_bp.route('/events', methods=['POST'])
@jwt_required()
def create_event():
    data = request.json
    event = Event(
        title=data.get('title'),
        description=data.get('description'),
        date=data.get('date'),
        category=data.get('category'),
        media=data.get('media')
    )
    db.session.add(event)
    db.session.commit()
    return jsonify({'id': event.id}), 201

@admin_bp.route('/events/<int:id>', methods=['PUT'])
@jwt_required()
def update_event(id):
    event = Event.query.get_or_404(id)
    data = request.json
    event.title = data.get('title', event.title)
    event.description = data.get('description', event.description)
    event.date = data.get('date', event.date)
    event.category = data.get('category', event.category)
    event.media = data.get('media', event.media)
    db.session.commit()
    return jsonify({'message': 'Updated'})

@admin_bp.route('/events/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_event(id):
    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    return jsonify({'message': 'Deleted'})

@admin_bp.route('/events', methods=['GET'])
@jwt_required()
def list_events():
    events = Event.query.all()
    return jsonify([{
        'id': e.id, 'title': e.title, 'description': e.description, 'date': e.date, 'category': e.category, 'media': e.media
    } for e in events])

@admin_bp.route('/events/<int:id>', methods=['GET'])
@jwt_required()
def get_event(id):
    e = Event.query.get_or_404(id)
    return jsonify({'id': e.id, 'title': e.title, 'description': e.description, 'date': e.date, 'category': e.category, 'media': e.media})

# GALLERY CRUD
@admin_bp.route('/gallery', methods=['POST'])
@jwt_required()
def create_gallery_item():
    if 'image' in request.files:
        image = request.files['image']
        # Save the file to a directory (e.g., static/uploads/)
        import os
        upload_dir = os.path.join('static', 'uploads')
        os.makedirs(upload_dir, exist_ok=True)
        image_path = os.path.join(upload_dir, image.filename)
        image.save(image_path)
        filename = f'/static/uploads/{image.filename}'
        category = request.form.get('category')
        description = request.form.get('description')
    else:
        data = request.get_json()
        filename = data.get('filename')
        category = data.get('category')
        description = data.get('description')
    item = GalleryItem(
        filename=filename,
        category=category,
        description=description
    )
    db.session.add(item)
    db.session.commit()
    return jsonify({'id': item.id}), 201

@admin_bp.route('/gallery/<int:id>', methods=['PUT'])
@jwt_required()
def update_gallery_item(id):
    item = GalleryItem.query.get_or_404(id)
    if 'image' in request.files:
        image = request.files['image']
        import os
        upload_dir = os.path.join('static', 'uploads')
        os.makedirs(upload_dir, exist_ok=True)
        image_path = os.path.join(upload_dir, image.filename)
        image.save(image_path)
        item.filename = f'/static/uploads/{image.filename}'
        item.category = request.form.get('category', item.category)
        item.description = request.form.get('description', item.description)
    else:
        data = request.get_json()
        item.filename = data.get('filename', item.filename)
        item.category = data.get('category', item.category)
        item.description = data.get('description', item.description)
    db.session.commit()
    return jsonify({'message': 'Updated'})

@admin_bp.route('/gallery/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_gallery_item(id):
    item = GalleryItem.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Deleted'})

@admin_bp.route('/gallery', methods=['GET'])
@jwt_required()
def list_gallery():
    items = GalleryItem.query.all()
    return jsonify([{
        'id': g.id, 'filename': g.filename, 'category': g.category, 'description': g.description
    } for g in items])

@admin_bp.route('/gallery/<int:id>', methods=['GET'])
@jwt_required()
def get_gallery_item(id):
    g = GalleryItem.query.get_or_404(id)
    return jsonify({'id': g.id, 'filename': g.filename, 'category': g.category, 'description': g.description})

# BLOG CRUD
@admin_bp.route('/blogs', methods=['POST'])
@jwt_required()
def create_blog():
    data = request.json
    blog = BlogPost(
        title=data.get('title'),
        content=data.get('content'),
        cover_image=data.get('cover_image'),
        tags=data.get('tags'),
        published_at=data.get('published_at')
    )
    db.session.add(blog)
    db.session.commit()
    return jsonify({'id': blog.id}), 201

@admin_bp.route('/blogs/<int:id>', methods=['PUT'])
@jwt_required()
def update_blog(id):
    blog = BlogPost.query.get_or_404(id)
    data = request.json
    blog.title = data.get('title', blog.title)
    blog.content = data.get('content', blog.content)
    blog.cover_image = data.get('cover_image', blog.cover_image)
    blog.tags = data.get('tags', blog.tags)
    blog.published_at = data.get('published_at', blog.published_at)
    db.session.commit()
    return jsonify({'message': 'Updated'})

@admin_bp.route('/blogs/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_blog(id):
    blog = BlogPost.query.get_or_404(id)
    db.session.delete(blog)
    db.session.commit()
    return jsonify({'message': 'Deleted'})

@admin_bp.route('/blogs', methods=['GET'])
@jwt_required()
def list_blogs():
    blogs = BlogPost.query.all()
    return jsonify([{
        'id': b.id, 'title': b.title, 'content': b.content, 'cover_image': b.cover_image, 'tags': b.tags, 'published_at': b.published_at
    } for b in blogs])

@admin_bp.route('/blogs/<int:id>', methods=['GET'])
@jwt_required()
def get_blog(id):
    b = BlogPost.query.get_or_404(id)
    return jsonify({'id': b.id, 'title': b.title, 'content': b.content, 'cover_image': b.cover_image, 'tags': b.tags, 'published_at': b.published_at})

# FAQ CRUD
@admin_bp.route('/faqs', methods=['POST'])
@jwt_required()
def create_faq():
    data = request.json
    faq = FAQ(
        question=data.get('question'),
        answer=data.get('answer')
    )
    db.session.add(faq)
    db.session.commit()
    return jsonify({'id': faq.id}), 201

@admin_bp.route('/faqs/<int:id>', methods=['PUT'])
@jwt_required()
def update_faq(id):
    faq = FAQ.query.get_or_404(id)
    data = request.json
    faq.question = data.get('question', faq.question)
    faq.answer = data.get('answer', faq.answer)
    db.session.commit()
    return jsonify({'message': 'Updated'})

@admin_bp.route('/faqs/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_faq(id):
    faq = FAQ.query.get_or_404(id)
    db.session.delete(faq)
    db.session.commit()
    return jsonify({'message': 'Deleted'})

@admin_bp.route('/faqs', methods=['GET'])
@jwt_required()
def list_faqs():
    faqs = FAQ.query.all()
    return jsonify([{'id': f.id, 'question': f.question, 'answer': f.answer} for f in faqs])

@admin_bp.route('/faqs/<int:id>', methods=['GET'])
@jwt_required()
def get_faq(id):
    f = FAQ.query.get_or_404(id)
    return jsonify({'id': f.id, 'question': f.question, 'answer': f.answer})

# TESTIMONIAL CRUD
@admin_bp.route('/testimonials', methods=['POST'])
@jwt_required()
def create_testimonial():
    data = request.json
    t = Testimonial(
        name=data.get('name'),
        message=data.get('message'),
        event_name=data.get('event_name'),
        date=data.get('date')
    )
    db.session.add(t)
    db.session.commit()
    return jsonify({'id': t.id}), 201

@admin_bp.route('/testimonials/<int:id>', methods=['PUT'])
@jwt_required()
def update_testimonial(id):
    t = Testimonial.query.get_or_404(id)
    data = request.json
    t.name = data.get('name', t.name)
    t.message = data.get('message', t.message)
    t.event_name = data.get('event_name', t.event_name)
    t.date = data.get('date', t.date)
    db.session.commit()
    return jsonify({'message': 'Updated'})

@admin_bp.route('/testimonials/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_testimonial(id):
    t = Testimonial.query.get_or_404(id)
    db.session.delete(t)
    db.session.commit()
    return jsonify({'message': 'Deleted'})

@admin_bp.route('/testimonials', methods=['GET'])
@jwt_required()
def list_testimonials():
    testimonials = Testimonial.query.all()
    return jsonify([{'id': t.id, 'name': t.name, 'message': t.message, 'event_name': t.event_name, 'date': t.date} for t in testimonials])

@admin_bp.route('/testimonials/<int:id>', methods=['GET'])
@jwt_required()
def get_testimonial(id):
    t = Testimonial.query.get_or_404(id)
    return jsonify({'id': t.id, 'name': t.name, 'message': t.message, 'event_name': t.event_name, 'date': t.date})

# INQUIRIES LIST & DELETE
@admin_bp.route('/inquiries', methods=['GET'])
@jwt_required()
def list_inquiries():
    print("HIT: /admin/inquiries GET")
    inquiries = Inquiry.query.all()
    return jsonify([
        {
            'id': i.id,
            'name': i.name,
            'email': i.email,
            'phone': i.phone,
            'event_type': i.event_type,
            'event_date': i.event_date,
            'budget': i.budget,
            'message': i.message,
            'status': i.status,
            'created_at': i.created_at
        } for i in inquiries
    ])

@admin_bp.route('/inquiries', methods=['POST'])
@jwt_required()
def create_admin_inquiry():
    print("HIT: /admin/inquiries POST")
    # Implement as needed or return a clear error if not supported
    return jsonify({'msg': 'POST not supported on /admin/inquiries'}), 405

@admin_bp.route('/inquiries/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_inquiry(id):
    inquiry = Inquiry.query.get_or_404(id)
    db.session.delete(inquiry)
    db.session.commit()
    return jsonify({'message': 'Deleted'})

@admin_bp.route('/manage-inquiries', methods=['GET'])
@jwt_required()
def manage_inquiries():
    inquiries = Inquiry.query.all()
    return jsonify([
        {
            'id': i.id,
            'name': i.name,
            'email': i.email,
            'phone': i.phone,
            'event_type': i.event_type,
            'event_date': i.event_date,
            'budget': i.budget,
            'message': i.message,
            'status': i.status,
            'created_at': i.created_at
        } for i in inquiries
    ])

@admin_bp.route('/manage-inquiries/<int:id>', methods=['GET'])
@jwt_required()
def view_inquiry(id):
    inquiry = Inquiry.query.get_or_404(id)
    return jsonify({
        'id': inquiry.id,
        'name': inquiry.name,
        'email': inquiry.email,
        'phone': inquiry.phone,
        'event_type': inquiry.event_type,
        'event_date': inquiry.event_date,
        'budget': inquiry.budget,
        'message': inquiry.message,
        'status': inquiry.status,
        'created_at': inquiry.created_at
    })
