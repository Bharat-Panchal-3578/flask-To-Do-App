from flask import render_template
import logging

def success_response(data=None,message="ok",status=200):
    """Standard JSON successful responses"""
    return {
        'status':'success',
        'message':message,
        'data':data
    }, status

def error_response(message='Something went wrong',status=404):
    """Standar JSON for errors."""
    return {
        'status':'error',
        'message':message
    }, status

def handle_404(error):
    """404 Error handler"""
    logging.warning(f"404 Error: {error}")
    return render_template('404.html'), 404

def handle_500(error):
    """500 Error handler"""
    logging.error(f"500 Error: {error}", exc_info=error)
    return render_template('500.html'), 500