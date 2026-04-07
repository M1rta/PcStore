from flask import Blueprint

from controllers.auth_controller import (
    get_current_session,
    login_user,
    logout_user,
    register_user,
)

auth_bp = Blueprint('auth_bp', __name__)

auth_bp.route('/auth/register', methods=['POST'])(register_user)
auth_bp.route('/auth/login', methods=['POST'])(login_user)
auth_bp.route('/auth/session', methods=['GET'])(get_current_session)
auth_bp.route('/auth/logout', methods=['POST'])(logout_user)
