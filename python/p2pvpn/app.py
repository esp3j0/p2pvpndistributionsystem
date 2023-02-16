from flask import Flask, request, jsonify
from nodebuilder import nodes_builder
from model import resp_file_download
from markupsafe import escape
from flask_cors import *
import os
app = Flask(__name__)
CORS(app,supports_credentials=True)
pwd = os.popen("pwd").readline()[:-1]


@app.route("/generate", methods = ["POST"])
def generat():
    data = request.json
    dic = {'1':'/24','2':'/16','3':'/8'}
    network = data['Internet']+dic[data['region']]
    count = data['count']
    nBuilder = nodes_builder(int(count),network)
    out = nBuilder.BuildAll()
    return out


@app.route('/downloadw/<path:uuid>/<int:node>')
def file_downloadw(uuid,node):
    '''返回文件下载结果信息'''
    requ_data = f'./configs/config-{escape(uuid)}/{escape(node)}'
    print((requ_data))
    return resp_file_download(requ_data,'w',pwd)
@app.route('/downloadl/<path:uuid>/<int:node>')
def file_downloadl(uuid,node):
    '''返回文件下载结果信息'''
    requ_data = f'./configs/config-{escape(uuid)}/{escape(node)}'
    return resp_file_download(requ_data,'l',pwd)
@app.route('/downloadm/<path:uuid>/<int:node>')
def file_downloadm(uuid,node):
    '''返回文件下载结果信息'''
    requ_data = f'./configs/config-{escape(uuid)}/{escape(node)}'
    return resp_file_download(requ_data,'m',pwd)


