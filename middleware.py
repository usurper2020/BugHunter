from functools import wraps
from datetime import datetime, timedelta
from typing import Callable, Dict, Any
import jwt
from flask import request, g, jsonify

from config import config
from logger_config import logger_config
from database import DatabaseManager, CacheManager
from models import User, RateLimit, AuditLog

logger = logger_config.get_logger(__name__)

def require_auth(f: Callable) -> Callable:
    """Decorator to require authentication for routes"""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            logger_config.log_security_event(
                'auth_failure',
                {'reason': 'missing_token', 'ip': request.remote_addr}
            )
            return jsonify({'error': 'No authorization token provided'}), 401
        
        try:
            # Extract token from "Bearer <token>"
            token = auth_header.split(' ')[1]
            payload = jwt.decode(
                token,
                config.get('JWT_SECRET_KEY'),
                algorithms=['HS256']
            )
            
            # Store user info in Flask's g object
            g.user_id = payload['user_id']
            g.username = payload['username']
            g.role = payload['role']
            
        except jwt.ExpiredSignatureError:
            logger_config.log_security_event(
                'auth_failure',
                {'reason': 'expired_token', 'ip': request.remote_addr}
            )
            return jsonify({'error': 'Token has expired'}), 401
            
        except jwt.InvalidTokenError:
            logger_config.log_security_event(
                'auth_failure',
                {'reason': 'invalid_token', 'ip': request.remote_addr}
            )
            return jsonify({'error': 'Invalid token'}), 401
            
        return f(*args, **kwargs)
    return decorated

def require_role(required_role: str) -> Callable:
    """Decorator to require specific role for routes"""
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated(*args, **kwargs):
            if not hasattr(g, 'role'):
                return jsonify({'error': 'Authentication required'}), 401
                
            if g.role != required_role:
                logger_config.log_security_event(
                    'unauthorized_access',
                    {
                        'user': g.username,
                        'required_role': required_role,
                        'actual_role': g.role,
                        'ip': request.remote_addr
                    }
                )
                return jsonify({'error': 'Insufficient permissions'}), 403
                
            return f(*args, **kwargs)
        return decorated
    return decorator

def rate_limit(requests_per_window: int = None, window_minutes: int = None) -> Callable:
    """Decorator to apply rate limiting to routes"""
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated(*args, **kwargs):
            if not hasattr(g, 'user_id'):
                return jsonify({'error': 'Authentication required'}), 401
                
            # Use config values if not specified
            max_requests = requests_per_window or config.get('RATE_LIMIT_REQUESTS')
            window = window_minutes or config.get('RATE_LIMIT_WINDOW_MINUTES')
            
            # Check cache first
            cache_key = f"rate_limit:{g.user_id}:{request.endpoint}"
            cached_count = CacheManager.get(cache_key)
            
            if cached_count:
                if int(cached_count) >= max_requests:
                    logger_config.log_security_event(
                        'rate_limit_exceeded',
                        {
                            'user': g.username,
                            'endpoint': request.endpoint,
                            'ip': request.remote_addr
                        }
                    )
                    return jsonify({'error': 'Rate limit exceeded'}), 429
                CacheManager.set(
                    cache_key,
                    int(cached_count) + 1,
                    expire=window * 60
                )
            else:
                CacheManager.set(cache_key, 1, expire=window * 60)
            
            return f(*args, **kwargs)
        return decorated
    return decorator

def audit_log(action: str) -> Callable:
    """Decorator to log audit events"""
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated(*args, **kwargs):
            start_time = datetime.now()
            
            try:
                result = f(*args, **kwargs)
                status = 'success'
            except Exception as e:
                status = 'error'
                logger.error(f"Error in {f.__name__}: {str(e)}", exc_info=True)
                raise
            finally:
                if hasattr(g, 'user_id'):
                    duration = (datetime.now() - start_time).total_seconds()
                    
                    audit_data = {
                        'endpoint': request.endpoint,
                        'method': request.method,
                        'ip': request.remote_addr,
                        'status': status,
                        'duration': duration,
                        'params': {
                            'args': request.args.to_dict(),
                            'form': request.form.to_dict(),
                            'json': request.get_json(silent=True)
                        }
                    }
                    
                    logger_config.log_audit_event(
                        g.username,
                        action,
                        audit_data
                    )
                    
                    # Store in database
                    with DatabaseManager.get_session() as session:
                        log = AuditLog(
                            user_id=g.user_id,
                            action=action,
                            entity_type=request.endpoint,
                            entity_id=kwargs.get('id', 0),
                            ip_address=request.remote_addr,
                            details=audit_data
                        )
                        session.add(log)
            
            return result
        return decorated
    return decorator

def error_handler(f: Callable) -> Callable:
    """Decorator to handle and log errors"""
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logger_config.log_error(
                __name__,
                e,
                {
                    'endpoint': request.endpoint,
                    'method': request.method,
                    'user': getattr(g, 'username', 'anonymous'),
                    'ip': request.remote_addr
                }
            )
            
            # Return appropriate error response
            if isinstance(e, jwt.InvalidTokenError):
                return jsonify({'error': 'Invalid authentication token'}), 401
            elif isinstance(e, PermissionError):
                return jsonify({'error': 'Insufficient permissions'}), 403
            else:
                return jsonify({
                    'error': 'Internal server error',
                    'message': str(e) if config.get('DEBUG') else 'An error occurred'
                }), 500
    
    return decorated

# Example usage:
# @app.route('/api/admin/users', methods=['GET'])
# @require_auth
# @require_role('admin')
# @rate_limit(100, 60)  # 100 requests per 60 minutes
# @audit_log('list_users')
# @error_handler
# def list_users():
#     # Route implementation
#     pass
