from flask import Blueprint, request, jsonify, current_app
from .models import PromptCustomTemplate, db
from .template_types import VARIABLE_TYPES
import requests
from jinja2 import Environment, meta, Template

bp = Blueprint('api', __name__, url_prefix='/api/v1')

@bp.route('/template/types', methods=['GET'])
def get_template_types():
    return jsonify(VARIABLE_TYPES)

@bp.route('/template/analyze', methods=['POST'])
def analyze_template():
    data = request.json
    content = data.get('content', '')

    env = Environment()
    try:
        ast = env.parse(content)
        variables = meta.find_undeclared_variables(ast)
        return jsonify(list(variables))
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/template', methods=['POST'])
def create_template():
    data = request.json
    template = PromptCustomTemplate(
        name=data['name'],
        temp_description=data.get('temp_description', ''),
        content=data['content'],
        parameters_config=data['parameters_config']
    )
    db.session.add(template)
    db.session.commit()
    return jsonify(template.to_dict()), 201

@bp.route('/template/<int:id>', methods=['PUT'])
def update_template(id):
    template = PromptCustomTemplate.query.get_or_404(id)
    data = request.json
    template.name = data.get('name', template.name)
    template.temp_description = data.get('temp_description', template.temp_description)
    template.content = data.get('content', template.content)
    template.parameters_config = data.get('parameters_config', template.parameters_config)
    db.session.commit()
    return jsonify(template.to_dict())

@bp.route('/template/<int:id>', methods=['GET'])
def get_template(id):
    template = PromptCustomTemplate.query.get_or_404(id)
    return jsonify(template.to_dict())

@bp.route('/template/<int:id>', methods=['DELETE'])
def delete_template(id):
    template = PromptCustomTemplate.query.get_or_404(id)
    db.session.delete(template)
    db.session.commit()
    return jsonify({'message': 'Deleted'})

@bp.route('/template/list', methods=['GET'])
def list_templates():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    pagination = PromptCustomTemplate.query.paginate(page=page, per_page=page_size)
    return jsonify({
        'items': [item.to_dict() for item in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })

@bp.route('/render/proxy', methods=['POST'])
def render_proxy():
    data = request.json
    target_url = data.get('target_url')
    if not target_url:
        return jsonify({'error': 'target_url is required'}), 400

    try:
        # We forward the params provided in the request body to the external API
        resp = requests.get(target_url, params=data.get('params', {}), timeout=10)
        resp.raise_for_status()
        return jsonify(resp.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/render/execute', methods=['POST'])
def render_execute():
    data = request.json
    template_id = data.get('template_id')
    params = data.get('params', {})

    template = PromptCustomTemplate.query.get_or_404(template_id)

    try:
        rendered = Template(template.content).render(**params)
        return jsonify({'prompt': rendered})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
