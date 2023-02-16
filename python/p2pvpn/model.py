import os
from flask import send_file, jsonify
import time

def resp_file_download(file_path,system,pwd):
    if system == 'w':  
        print(pwd)  
        os.chdir(pwd)
        if os.path.exists(file_path):
            file_path =  os.getcwd()+file_path[1:]
            file_dir = file_path+'-wclient'
            print(file_path)
            if not os.path.exists(file_dir):
                os.mkdir(file_dir)
                os.system('cp -r ./win-client/* '+ file_dir)
                os.system('cp -r '+ file_path + '/* ' + file_dir)
                time.sleep(3)
                os.chdir(file_dir)
                print(os.getcwd())
                os.system('zip -r -m -q ./win.zip'+' *')
            
            return send_file(file_dir+'/win.zip', as_attachment=True)
        else:
            return jsonify({
                'msg': '文件不存在',
            })
        
    if system == 'l':
        pass
    if system == 'm':
        pass
