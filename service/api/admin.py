from flask import Blueprint
from flask import request

admin_module = Blueprint("admin_module", __name__)

@admin_module.route('/admin/parameters', methods=['GET', 'POST'])
def get_parameters():
    
