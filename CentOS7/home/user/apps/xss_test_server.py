# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @time		: 	2020/04/12
# @Author	:	Magic
# @File		:	xss_test_server.py


from flask import Flask,render_template,request,redirect,url_for

app = Flask(__name__)


comment = []


@app.route('/', methods=["GET","POST"])
def index():
	return render_template("XSS.html", comment=comment, query=None)



# Realize the Reflected XSS attack Vulnerable Search box
@app.route('/rxss', methods=["GET","POST"])
def rxss():
	global qdata
	if request.method == "GET":
		qdata = request.args.get('query')
		action = request.args.get('anti-XSS')
	if not action:
		action = 0
	print(request.args)
	if int(action):
		qdata = escape(qdata)
	print(qdata)
	return render_template("XSS.html", query=qdata)


# Realize the Persistent XSS attack Vulnerable Comment
@app.route('/pxss', methods=["GET","POST"])
def pxss():
	if request.method == "POST":
		qcomment = request.form.get('qcomment')
		action = request.form.get('anti-XSS')
	global comment
	if not action:
		action = 0
	print(request.form)
	if int(action):
		qcomment = escape(qcomment)
	comment.append(qcomment)
	print(comment)
	#return render_template("XSS.html", comment=comment)
	return redirect(url_for('index'))


# 检查字符串是否含有HTML标签并编码
def escape(s, quote=True):
    """
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true (the default), the quotation mark
    characters, both double quote (") and single quote (') characters are also
    translated.
    """
    s = s.replace("&", "&amp;") # Must be done first!
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    if quote:
        s = s.replace('"', "&quot;")
        s = s.replace('\'', "&#x27;")
    return s


if __name__ == '__main__':
	app.run(debug=True, port=12345)
