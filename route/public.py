from flask import Flask,render_template,request,jsonify,redirect,url_for,Blueprint
from ml import predict_lang,trans_lang
from flask import session
import db
from datetime import timedelta
bp = Blueprint('public', __name__, url_prefix='/public')


@bp.route('/tip')
def tip():
  return render_template('/public/tip.html', userName="사용자명")




