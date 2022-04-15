from flask import Flask,render_template,request,jsonify,redirect,url_for,Blueprint
from ml import predict_lang,trans_lang
from flask import session
import db
from datetime import timedelta
bp = Blueprint('public', __name__, url_prefix='/public')


# @bp.route('/tip')
# def tip():
#   return render_template('/public/tip.html', userName="사용자명")

@bp.route('/tip_ver2')
def tip2():
  return render_template('/public/tip-ver2.html', userName="사용자명")

@bp.route('/sang')
def sang():
  return render_template('/public/sang.html', userName="사용자명")

@bp.route('/chung')
def chung():
  return render_template('/public/chung.html', userName="사용자명")


@bp.route('/ggae')
def ggae():
  return render_template('/public/ggae.html', userName="사용자명")   


