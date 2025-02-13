import os
import shutil
import zipfile
import datetime
from io import BytesIO
import os
import numpy as np
import torch
import torchvision
from PIL import Image
import torchvision.transforms as transforms
from albumentations.core.composition import Compose
from albumentations import Resize
from torch import nn
from albumentations.augmentations import transforms
from src.network.conv_based.U_Net import U_Net  # 导入您所用的U-Net模型
from src.network.conv_based.CMUNeXt import CMUNeXt, cmunext  # 导入您所用的U-Net模型
from src.network.conv_based.CMUNet import CMUNet
from src.network.conv_based.AttU_Net import AttU_Net
from src.network.conv_based.UNetplus import ResNet34UnetPlus
import cv2
from zipfile import ZipFile
import pandas as pd
import imageio as imageio
import openpyxl as openpyxl
import pydicom as pydicom
from flask_cors import CORS
from flask import Flask, jsonify, request, send_file, url_for
from DbConfig import conn

app = Flask(__name__, static_url_path='/static')
cur = conn.cursor()

# 解决跨域问题
CORS(app, origins='*')  # 允许所有来源的请求访问


# CORS(app, resources={r"/upload/*": {"origins": "http://localhost:8080"}})
# CORS(app)


# 遍历图片文件夹，获取所有图片文件的路径
def get_file_list(folder_path):
    file_list = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.jpg') or file.endswith('.png') or file.endswith('.jpeg'):
                file_list.append(os.path.join(root, file))
    return file_list


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/login', methods=['GET', 'POST'])
def login():  # put application's code here
    if request.method == 'POST':
        post_data = request.get_json()
        username = post_data.get('name')
        password = post_data.get('password')
        roleId = int(post_data.get('roleId'))
        print(username)
        sql = "SELECT * FROM user WHERE username ='%s' and password ='%s' and role ='%s' " % (
        username, password, roleId)
        cur.execute(sql)
        user = cur.fetchone()
        print(user)

        # 获取表的元数据信息（列名、顺序等）
        cur.execute("SHOW COLUMNS FROM user")
        columns = [col[0] for col in cur.fetchall()]

        # 将数据转换为字典列表，并以 JSON 格式返回
        userData = dict(zip(columns, user))
        print(userData)

        sql = "SELECT menu_id FROM role_menu WHERE role_id ='%d' " % roleId
        cur.execute(sql)
        menu_ids = [row[0] for row in cur.fetchall()]  # 获取查询结果并转换为列表

        cursor = conn.cursor()
        # 将 menu_ids 转换为字符串格式，例如 '1, 2, 3'，用于 SQL 的 IN 语句
        menu_ids_str = ', '.join(str(menu_id) for menu_id in menu_ids)

        # 使用 IN 语句查询数据库中对应菜单 ID 的记录
        query = f"SELECT * FROM menu WHERE id IN ({menu_ids_str})"
        cursor.execute(query)
        data = cursor.fetchall()
        # 将菜单数据组织成带有父子关系的格式
        menu_dict = {}
        for row in data:
            menu_id, name, path, icon, description, pid, sort_num = row
            if pid not in menu_dict:
                menu_dict[pid] = []
            menu_dict[pid].append({
                'id': menu_id,
                'label': name,
                'path': path,
                'icon': icon,
                'description': description,
                'sortNum': sort_num,
                'children': []
            })

        # 根据父子关系构建菜单树形结构
        menu_tree = menu_dict[None]  # 假设根菜单的 pid 为 None
        build_menu_tree(menu_tree, menu_dict)

        cursor.close()
        print(menu_tree)

        if user is None:
            return jsonify({'status': 'failed', 'menus': menu_tree})
        return jsonify({'status': 'success', 'userData': userData, 'menus': menu_tree})
        # if response_object['status'] == 'success':
        #     if user[2] == 'admin':
        #         print(user[2])
        #         response_object = {'status': 'admin'}
    return jsonify({'status': 'success', })


@app.route('/get_User', methods=['GET'])
def get_User():
    username = request.args.get('name')
    print(username)
    sql = "SELECT * FROM user WHERE username ='%s' " % username
    cur.execute(sql)
    user = cur.fetchone()
    print(user)

    # 获取表的元数据信息（列名、顺序等）
    cur.execute("SHOW COLUMNS FROM user")
    columns = [col[0] for col in cur.fetchall()]

    # 将数据转换为字典列表，并以 JSON 格式返回
    userData = dict(zip(columns, user))
    print(userData)
    return jsonify({'userData': userData})


@app.route('/user_register', methods=['GET', 'POST'])
def register():  # put application's code here
    if request.method == 'POST':
        post_data = request.get_json()
        username = post_data.get('name')
        password = post_data.get('password')
        roleId = post_data.get('roleId')
        print(type(username))
        response_object = {'status': 'success'}
        print(username)
        try:
            sql = "INSERT INTO user(username, password,role) VALUES('%s','%s','%s')" % (username, password, roleId)
            print(sql)
            cur.execute(sql)
            conn.commit()
        except conn.IntegrityError:
            response_object = {'status': 'already'}

        print(response_object['status'])
        return jsonify(response_object)
    return jsonify({'status': 'success'})


@app.route('/get_image_data', methods=['GET'])
def get_image_data():
    # 获取前端发送的页码和每页数量参数
    page = int(request.args.get('page'))
    pageSize = int(request.args.get('pageSize'))
    patientId = request.args.get('patientId')
    selectedColumn = request.args.get('selectedColumn')
    print(patientId)
    print(selectedColumn)
    cursor = conn.cursor()
    if patientId != '' and selectedColumn != '':
        cursor.execute("SELECT * FROM image where patient_id = %s and {} = '1'".format((patientId,), selectedColumn))
    elif patientId == '' and selectedColumn != '':
        print("SELECT * FROM image WHERE {} = '1'".format(selectedColumn))
        cursor.execute("SELECT * FROM image WHERE {} = '1'".format(selectedColumn))
    elif patientId != '' and selectedColumn == '':
        print('SELECT * FROM image where patient_id = %s', (patientId,))
        cursor.execute('SELECT * FROM image where patient_id = %s', (patientId,))
    else:
        cursor.execute("SELECT * FROM image")
    data = cursor.fetchall()
    print(data)
    # 计算分页的起始索引和结束索引
    start = (page - 1) * pageSize
    end = start + pageSize

    # 获取特定页的图片数据
    # 获取特定页的图片数据
    paginated_data = data[start:end]

    # 获取表的元数据信息（列名、顺序等）
    cursor.execute("SHOW COLUMNS FROM image")
    columns = [col[0] for col in cursor.fetchall()]

    # 将数据转换为字典列表，并以 JSON 格式返回
    result = []
    for row in paginated_data:
        row_dict = dict(zip(columns, row))
        result.append(row_dict)

    cursor.close()

    return jsonify({'columns': columns, 'result': result, 'total': len(data)})


@app.route('/get_image/<path:image_name>', methods=['GET'])
def get_image(image_name):
    try:
        # 通过 Flask 的 url_for 函数获取图片的 URL
        image_url = url_for('static', filename='images/' + image_name)  # 'images/' 是存储图片的文件夹路径
        return image_url
    except Exception as e:
        return str(e), 404


@app.route('/get_dataByColumn', methods=['GET', 'POST'])
def get_dataByColumn():
    data = request.get_json()

    selected_column = data.get('selectedColumn')
    table_data = data.get('tableData')

    # 在此处根据 selected_column 对 table_data 进行筛选操作
    # 这里仅做示例，实际应用中需根据实际需求进行逻辑处理
    filtered_table_data = []

    for row in table_data:
        if row[selected_column] == '1':
            filtered_table_data.append(row)

    # 返回筛选后的数据给前端
    return jsonify({'filteredTableData': filtered_table_data})


@app.route('/upload', methods=['POST'])
def upload_file():
    global List
    uploaded_files = request.files.getlist('file')  # 获取上传的文件列表
    print(uploaded_files)
    file_list = []
    patientIds = []
    base_dirname = ''
    excel_name = ''
    for file in uploaded_files:
        if file.filename.endswith('.xlsx') or file.filename.endswith('.xls'):
            # 处理上传的 Excel 文件逻辑
            # 保存文件到服务器或进行其他操作
            file.save(os.path.join('data', file.filename))
            excel_name = file.filename
            file_list.append(file.filename)
        elif file.filename.endswith('.zip'):
            # 处理上传的 Zip 文件逻辑
            # 保存文件到服务器或进行其他操作

            file_list.append(file.filename)

            # 要处理的压缩包
            filename = file.filename
            zip_file = ZipFile(file)

            # 提取压缩包的最后一部分用于创建目录存储处理过后的dicom文件
            dir_name = os.path.basename(filename)

            # 将压缩包的最后一部分后缀名.zip去掉
            (base_dirname, suffix) = os.path.splitext(dir_name)
            print(dir_name)
            extract_dirname = os.path.join('data/extract/', base_dirname)
            # extract_dirname = 'extract_dir'

            # 将之前的文件夹清除
            if os.path.exists(extract_dirname):
                shutil.rmtree(extract_dirname)

            # 解压
            zip_file.extractall(extract_dirname)

            jpg_dirname = os.path.join('data/deal/', base_dirname)

            if os.path.exists(jpg_dirname):
                shutil.rmtree(jpg_dirname)

            # 创建文件夹存储得到的jpg文件
            os.makedirs(jpg_dirname)

            # 遍历文件夹及其子文件夹中的文件，并存储在一个列表中
            # 输入文件夹路径、空文件列表[]
            # 返回 文件列表Filelist,包含文件名（完整路径）
            def get_filelist(dir, Filelist):
                newDir = dir
                if os.path.isfile(dir):
                    if not (dir.endswith('.jpg') or dir.endswith('.JPG') or dir.endswith('DICOMDIR')):
                        ds = pydicom.read_file(dir)
                        Filelist.append((dir, ds.StudyDate + ds.StudyTime, ds.InstanceNumber))
                    # # 若只是要返回文件夹，使用这个
                    # Filelist.append(os.path.basename(dir))
                elif os.path.isdir(dir):
                    for s in os.listdir(dir):
                        # 如果需要忽略某些文件夹，使用以下代码
                        # if s == "xxx":
                        # continue
                        newDir = os.path.join(dir, s)
                        get_filelist(newDir, Filelist)
                # 按照 StudyDate、StudyTime 以及 InstanceNumber 对文件进行排序
                sorted_files = sorted(Filelist, key=lambda x: (x[1], x[2]))
                return sorted_files

            List = get_filelist('./' + extract_dirname, [])
            print(len(List))

            # 存储每个病人的目前文件序号
            count = {}

            # 遍历所有dicom文件
            for e in List:
                # print(e)
                ds = pydicom.read_file(e[0])
                patient_name = str(ds.PatientName)
                patient_name = patient_name.replace('^', ' ')
                path = jpg_dirname + '/Patient-' + patient_name  # 一个病人对应一个文件夹
                if not os.path.exists(path):  # 判断是否存在文件夹如果不存在则创建为文件夹
                    os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
                    count[patient_name] = 1

                output_jpg_path = path + '/' + '{:05d}'.format(count[patient_name]) + '.jpg'
                # Az 像素值矩阵
                pix = ds.pixel_array
                shape = pix.shape
                if shape[0] == 768:  # 如果是视频就不做处理
                    imageio.imwrite(output_jpg_path, pix)  # imageio保存图片
                    count[patient_name] = count[patient_name] + 1

    # 递归删除文件夹
    def del_file(path_data):
        for i in os.listdir(path_data):  # os.listdir(path_data)#返回一个列表，里面是当前目录下面的所有东西的相对路径
            file_data = path_data + "\\" + i  # 当前文件夹的下面的所有东西的绝对路径
            if os.path.isfile(file_data):  # os.path.isfile判断是否为文件,如果是文件,就删除.如果是文件夹.递归给del_file.
                os.remove(file_data)
            else:
                del_file(file_data)

    xls_path = os.path.join('data/', excel_name)  # AI表格路径
    # patient_path = "D:/Users/Desktop/dicom/"
    patient_path = os.path.join('data/deal/', base_dirname + '/')  # 提取图片路径
    save_path = os.path.join('static/images/', base_dirname + '/')  # 保存路径

    if not os.path.exists(save_path):
        os.mkdir(save_path)
    del_file(save_path)

    wb = openpyxl.load_workbook(xls_path)
    sheets = wb.sheetnames
    for i in range(len(sheets)):
        frame = pd.read_excel(xls_path)
        columns = frame.columns.values.tolist()
        patient = None
        Patient_file = None
        imgid = 0
        for idx, row in frame.iterrows():  # 迭代数据 以键值对的形式 获取 每行的数据
            if idx == 0 or row[columns[2]] == "备注":
                continue
            # 找到患者id对应的文件夹
            if str(row[columns[0]]) != "nan":
                if "OB" in str(row[columns[0]]):
                    patient_num = str(int(row[columns[0]][3:]))
                    patient = str("OB-" + patient_num)
                elif "GOUT" in str(row[columns[0]]):
                    print(row[columns[0]])
                    patient_num = str(int(row[columns[0]][5:]))
                    patient = str("GOUT-" + patient_num)
                else:
                    patient_num = str(int(row[columns[0]]))
                    patient = str("GOUT-" + patient_num)
                # print(patient_num)
                patientIds.append(patient_num)
                # patient=str(row[columns[0]]).split(".")[0]
                # print(row[columns[0]])
                # if patient[-1]==" " :
                #     patient=patient[0:-1]
                # if patient[0]=="0" and patient[1]=="B" :
                #     patient ="O"+patient[1:]

                imgid = 0
                scan_sum = 0
                w = 0
                for patient_file in os.listdir(patient_path):
                    if str(patient_num) in patient_file:  # 判断patient_num是否在文件夹名字中出现
                        Patient_file = patient_file
                        w = 1
                if w == 0:
                    print("无法找到患者对应图片文件夹", patient)
                    exit()
                if Patient_file is None:
                    print("无法找到患者对应图片文件夹", patient)
                    exit()
            # print("患者文件", Patient_file)

            # 根据表中一行的内容生成文件名
            if row[columns[2]] == "其他关节" or row[columns[2]] == "肾脏图片" or ("删除" in str(row[columns[2]])):
                continue
            imgid = int(row[columns[1]])
            if row[columns[2]] == "血流图":
                print("血流图")
            elif row[columns[2]] == None and row[columns[3]] == None and row[columns[4]] == None and row[
                columns[5]] == None:
                print("出现特殊行")
                exit()
            elif row[columns[2]] == "动态扫描图":
                scan_sum = scan_sum + 1
                continue
            else:
                print(int(imgid - 1 - scan_sum))
                # print(
                #     patient_path + Patient_file + "/" + os.listdir(patient_path + Patient_file)[
                #         int(imgid - 1 - scan_sum)])
                img = cv2.imread(
                    patient_path + Patient_file + "/" + os.listdir(patient_path + Patient_file)[imgid - 1 - scan_sum])
                location = 0
                # print(row[columns[3]], row[columns[4]], row[columns[5]])
                if str(row[columns[3]]) != "nan":
                    location = 0
                elif str(row[columns[4]]) != "nan":
                    location = 1
                elif str(row[columns[5]]) != "nan":
                    location = 2
                else:
                    continue
                feature = "_"
                dzghs = "0"
                hmzh = "0"
                tfsxc = "0"
                gzph = "0"
                gjjy = "0"
                sgz = "0"
                if str(row[columns[6]]) != "nan":
                    feature = feature + "1"
                    dzghs = "1"
                if str(row[columns[7]]) != "nan":
                    feature = feature + "2"
                    hmzh = "1"
                if str(row[columns[8]]) != "nan":
                    feature = feature + "3"
                    tfsxc = "1"
                if str(row[columns[9]]) != "nan":
                    feature = feature + "4"
                    gzph = "1"
                if str(row[columns[10]]) != "nan":
                    feature = feature + "5"
                    gjjy = "1"
                if str(row[columns[11]]) != "nan":
                    feature = feature + "6"
                    sgz = "1"
                if feature == "_":
                    feature = feature + "0"
                if "OB" in patient:
                    # print(save_path+str(patient_num)+"_OB"+"_"+str(imgid)+"_"+str(location)+feature+".png")
                    cv2.imwrite(
                        save_path + str(patient_num) + "_OB" + "_" + str(imgid) + "_" + str(
                            location) + feature + ".png",
                        img)
                    sql = "INSERT INTO image(upload_time, imagePath,patient_id,location,dzghs,hmzh,tfsxc,gzph,gjjy,sgz) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                        datetime.datetime.now().strftime('%Y-%m-%d'),
                        'http://localhost:5000/' + save_path + str(patient_num) + "_OB" + "_" + str(imgid) + "_" + str(
                            location) + feature + ".png", patient_num, location, dzghs, hmzh, tfsxc, gzph, gjjy, sgz)
                    cur.execute(sql)
                    conn.commit()
                    print("保存OB")
                if "GOUT" in patient:
                    cv2.imwrite(
                        save_path + str(patient_num) + "_GOUT" + "_" + str(imgid) + "_" + str(
                            location) + feature + ".png",
                        img)
                    sql = "INSERT INTO image(upload_time, imagePath,patient_id,location,dzghs,hmzh,tfsxc,gzph,gjjy,sgz) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                        datetime.datetime.now().strftime('%Y-%m-%d'),
                        'http://localhost:5000/' + save_path + str(patient_num) + "_GOUT" + "_" + str(
                            imgid) + "_" + str(
                            location) + feature + ".png", patient_num, location, dzghs, hmzh, tfsxc, gzph, gjjy, sgz)
                    # print(sql)
                    cur.execute(sql)
                    conn.commit()
                    print("保存Gout")
        break
    patient_Ids = list(set(patientIds))
    print(patient_Ids)
    for id in patient_Ids:
        cur.execute("insert into patient(patient_id) values ('%s') " % id)
        conn.commit()
    # cur.close()
    return jsonify({'files': file_list, 'patientIds': patient_Ids})


# 获取partient表格中的所有数据并传到前端

@app.route('/get_patient_ids', methods=['GET'])
def get_patient_ids():
    # 获取前端发送的页码和每页数量参数
    page = int(request.args.get('page'))
    pageSize = int(request.args.get('pageSize'))
    patientId = request.args.get('patientId')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM patient where patient_id  like %s', ('%' + patientId + '%'))
    data = cursor.fetchall()
    print(data)
    # 计算分页的起始索引和结束索引
    start = (page - 1) * pageSize
    end = start + pageSize

    # 获取特定页的图片数据
    paginated_data = data[start:end]

    # 获取表的元数据信息（列名、顺序等）
    cursor.execute("SHOW COLUMNS FROM patient")
    columns = [col[0] for col in cursor.fetchall()]
    # 将数据转换为字典列表，并以 JSON 格式返回
    result = []
    for row in paginated_data:
        row_dict = dict(zip(columns, row))
        result.append(row_dict)
    cursor.close()
    return jsonify({'columns': columns, 'result': result, 'total': len(data)})


# 删除patient表格中对应的病人数据，并同时删除病人对应的图片

@app.route('/del_patient_data', methods=['DELETE'])
def del_patient_data():
    id = request.args.get('id')
    cursor = conn.cursor()
    print("DELETE FROM patient WHERE patient_id = %s", id)
    cursor.execute("DELETE FROM patient WHERE patient_id = %s", id)
    cursor.execute("DELETE FROM image WHERE patient_id = %s", id)

    cursor.close()

    return jsonify({'code': '200'})


# 病人界面批量删除数据

@app.route('/del_patient_batchdata', methods=['DELETE'])
def del_patient_batchdata():
    ids = request.args.get('ids')
    id_list = ids.split(',')  # 使用逗号分隔字符串，生成 ID 列表
    cursor = conn.cursor()
    for id in id_list:
        print("DELETE FROM patient WHERE patient_id = %s", id)
        cursor.execute("DELETE FROM patient WHERE patient_id = %s", id)
        cursor.execute("DELETE FROM image WHERE patient_id = %s", id)
    cursor.close()
    return jsonify({'code': '200'})


# 根据多选框中选择的patient_id进行多个病人图片数据的下载

@app.route('/download_batchPatient', methods=['GET'])
def download_batchPatient():
    ids = request.args.get('ids')
    print(ids)
    id_list = ids.split(',')  # 使用逗号分隔字符串，生成 ID 列表
    cursor = conn.cursor()
    file_paths = []
    for id in id_list:
        cursor.execute("SELECT imagePath FROM image where patient_id = %s", id)
        data = cursor.fetchall()
        file_paths.extend(row[0].replace('http://localhost:5000/', '') for row in data)  # 获取所有满足条件的文件路径列表
    folder_path = 'static/images/'
    cursor.close()
    file_paths = list(set(file_paths))
    if file_paths:
        # 创建一个内存中的 ZIP 文件
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
            for file_path in file_paths:
                # 将查询到的文件添加到 ZIP 文件中
                relative_path = os.path.relpath(file_path, folder_path)
                zip_file.write(file_path, arcname=relative_path)
        # 回到 ZIP 文件的开头
        zip_buffer.seek(0)
        # 发送 ZIP 文件给前端
        return send_file(zip_buffer, as_attachment=True
                         , download_name='download.zip')
    else:
        return "No files found for the specified patientId", 404


@app.route('/download/<patientId>', methods=['GET'])
def download(patientId):
    folder_path = 'static/images/'
    # 在数据库中查询满足 patientId 的文件路径列表，假设这里使用一个名为 get_file_paths_by_patient_id 的函数来查询
    cursor = conn.cursor()
    print('SELECT imagePath FROM image where patient_id = %s', (patientId,))
    cursor.execute('SELECT imagePath FROM image where patient_id = %s', (patientId,))

    file_paths = [row[0].replace('http://localhost:5000/', '') for row in cursor.fetchall()]  # 获取所有满足条件的文件路径列表
    cursor.close()
    file_paths = list(set(file_paths))
    if file_paths:

        # 创建一个内存中的 ZIP 文件
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
            for file_path in file_paths:
                # 将查询到的文件添加到 ZIP 文件中
                relative_path = os.path.relpath(file_path, folder_path)
                zip_file.write(file_path, arcname=relative_path)

        # 回到 ZIP 文件的开头
        zip_buffer.seek(0)

        # 发送 ZIP 文件给前端
        return send_file(zip_buffer, as_attachment=True, download_name=os.path.join(patientId, '.zip'))
    else:
        return "No files found for the specified patientId", 404


@app.route('/downloadAllFile', methods=['GET'])
def downloadAllFile():
    folder_path = 'static/images/'
    # 在数据库中查询满足 patientId 的文件路径列表，假设这里使用一个名为 get_file_paths_by_patient_id 的函数来查询
    cursor = conn.cursor()
    print('SELECT imagePath FROM image ')
    cursor.execute('SELECT imagePath FROM image ')
    data = cursor.fetchall()
    print(data)
    row_first = data[0]
    zip_name = row_first[0].split('/')[-2]
    print(zip_name)
    file_paths = [row[0].replace('http://localhost:5000/', '') for row in data]  # 获取所有满足条件的文件路径列表
    cursor.close()
    print(file_paths)
    if file_paths:

        # 创建一个内存中的 ZIP 文件
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
            for file_path in file_paths:
                # 将查询到的文件添加到 ZIP 文件中
                relative_path = os.path.relpath(file_path, folder_path)
                zip_file.write(file_path, arcname=relative_path)

        # 回到 ZIP 文件的开头
        zip_buffer.seek(0)

        # 发送 ZIP 文件给前端
        return send_file(zip_buffer, as_attachment=True, download_name=os.path.join(zip_name, '.zip'))
    else:
        return "No files found for the specified patientId", 404


@app.route('/download_batch', methods=['GET'])
def download_batch():
    ids = request.args.get('ids')
    print(ids)
    id_list = ids.split(',')  # 使用逗号分隔字符串，生成 ID 列表
    cursor = conn.cursor()
    file_paths = []
    for id in id_list:
        id = int(id)
        print("SELECT imagePath FROM image where id = %d" % id)
        cursor.execute("SELECT imagePath FROM image where id = %d" % id)
        file_paths.append(''.join([row[0].replace('http://localhost:5000/', '') for row in cursor.fetchall()]))
    folder_path = 'static/images/'
    cursor.close()
    print(file_paths)

    if file_paths:

        # 创建一个内存中的 ZIP 文件
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
            for file_path in file_paths:
                # 将查询到的文件添加到 ZIP 文件中
                relative_path = os.path.relpath(file_path, folder_path)
                zip_file.write(file_path, arcname=relative_path)

        # 回到 ZIP 文件的开头
        zip_buffer.seek(0)

        # 发送 ZIP 文件给前端
        return send_file(zip_buffer, as_attachment=True
                         , download_name='download.zip')
    else:
        return "No files found for the specified patientId", 404


@app.route('/dicom_upload', methods=['GET', 'POST'])
def dicom_upload():
    if 'file' not in request.files:
        return 'No file part'
    dicom_file = request.files['file']
    if dicom_file.filename == '':
        return 'No selected file'
    dicom_file.save(os.path.join('data/', dicom_file.filename))
    ds = pydicom.read_file(os.path.join('data/', dicom_file.filename))

    # 查看有哪些属性
    print(ds.dir())  # 查看全部的属性
    print(ds.dir("pat"))  # 查看带关键字pat的属性

    # 查看属性对应的具体值
    print(ds.PatientName)  # 查看PatientName属性对应的具体值，想查看哪个可以直接?出来
    print(ds.StudyTime)
    # 打印完整的数据元素，包括(Group,Element)，VR，Value，两种方式都可以
    data_element = ds.data_element("PatientID")
    print(data_element.tag, data_element.VR, data_element.value)
    print(ds.data_element('PatientID'))
    print(ds.data_element('InstanceNumber'))
    # 原始二进制文件
    pixel_bytes = ds.PixelData

    # 像素值矩阵
    pix = ds.pixel_array

    # 打印矩阵维度
    print(pix.shape)
    file_list = []
    imageio.imwrite('static/images/' + os.path.splitext(dicom_file.filename)[0] + '.jpg', pix)  # imageio保存图片
    file_list.append(os.path.splitext(dicom_file.filename)[0])
    path = 'http://localhost:5000/static/images/' + os.path.splitext(dicom_file.filename)[0] + '.jpg'
    return jsonify({'files': file_list, 'path': path, 'patientID': str(ds.PatientName), 'studyDate': str(ds.StudyDate)})


@app.route('/image_upload', methods=['GET', 'POST'])
def image_upload():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    file.save(os.path.join('static/images/', file.filename))
    file_list = [file.filename]
    path = 'http://localhost:5000/static/images/' + file.filename
    return jsonify({'files': file_list, 'path': path})


@app.route('/seg_image', methods=['GET', 'POST'])
def seg_image():
    image_path = request.args.get('imagePath')
    print(image_path)
    image_path = image_path.replace('http://localhost:5000/', '')
    print(image_path)
    # 指定模型权重文件路径、单张图片路径和保存结果的路径
    pth_dir = "checkpoint/UNetplus_model.pth"
    save_path = "static/"
    save_name = 'segged_' + image_path.split('/')[-1]
    img_size = 256
    threshold = 0.5

    def load_model(pth_dir):
        model = ResNet34UnetPlus(num_class=1)  # 这里假设使用的是 U-Net 模型，根据您的实际模型进行修改
        model.load_state_dict(torch.load(pth_dir, map_location=torch.device('cpu')))
        return model

    def infer(output, threshold):
        edge = output > threshold
        return edge

    def save_png(edge):
        image = cv2.imread(image_path)
        w0, h0, _ = image.shape
        image = cv2.resize(image, dsize=(256, 256))
        image = np.transpose(image, (2, 0, 1))
        w, h = edge.shape[1], edge.shape[2]
        mask = np.zeros_like(image)
        for i in range(w):
            for j in range(h):
                if edge[0][i][j]:
                    mask[:, i, j] = [255, 255, 255]
        mask = np.transpose(mask, (1, 2, 0))
        mask = cv2.resize(mask, (h0, w0))
        image = cv2.imread(image_path)

        # Convert mask to grayscale
        mask_gray = cv2.cvtColor(mask.astype(np.uint8), cv2.COLOR_BGR2GRAY)
        # Find contours in the resized mask
        contours, _ = cv2.findContours(mask_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        # Draw contours on the original image
        cv2.drawContours(image, contours, -1, (0, 0, 255), 2)  # You can change the color and thickness
        cv2.imwrite(save_path + save_name, image)

    device = torch.device('cpu')
    image = cv2.imread(image_path)
    test_transform = Compose([
        Resize(img_size, img_size),
        transforms.Normalize(),
    ])
    image = test_transform(image=image)["image"]

    # 转换图像为模型可接受的格式，并进行预测
    image = torch.tensor(image, dtype=torch.float).permute(2, 0, 1).unsqueeze(0) / 255.0
    model = load_model(pth_dir).to(device)
    output = torch.sigmoid(model(image))
    edge = infer(output[0], threshold)
    save_png(edge)
    path = 'http://localhost:5000/' + save_path + save_name
    print(path)
    return jsonify({'path': path})

@app.route('/detect_image', methods=['GET', 'POST'])
def detect_image():
    save_path = r"\static\75606_GOUT_6_1_13_mask.png"
    path = 'http://localhost:5000/' + save_path
    return jsonify({'path': path})
@app.route('/save_seg_image', methods=['GET', 'POST'])
def save_seg_image():
    image_path = request.args.get('segmentedImagePath')
    print(image_path)
    file_name = image_path.split('/')[-1]
    shutil.copy('./static/' + file_name, './segged_image/' + file_name)
    return jsonify({'status': 'success'})


@app.route('/check_image', methods=['GET', 'POST'])
def check_image():
    from net.resnet import resnet50
    image_path = request.args.get('imagePath')
    res = []
    print(image_path)
    image_path = image_path.replace('http://localhost:5000/', '')
    print(image_path)

    model = resnet50()

    # 处理单张图片并输出结果
    def process_single_image(image_path):
        target = []
        target.append(1) if '1' in image_path.split('_')[-1] else target.append(0)
        target.append(1) if '3' in image_path.split('_')[-1] else target.append(0)
        target.append(1) if '4' in image_path.split('_')[-1] else target.append(0)
        target.append(1) if '6' in image_path.split('_')[-1] else target.append(0)
        print(target)
        # image = Image.open(image_path).convert('RGB')
        # image = transform(image).unsqueeze(0)
        # image = cv2.imread(image_path)
        # cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # image = image.astype('float32') / 255
        # image = transform(image)  # 转换为 PyTorch 张量
        # image = image.transpose(2, 0, 1)
        image = cv2.imread(image_path)
        cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = image.astype('float32') / 255
        image = image.transpose(2, 0, 1)
        image = torch.Tensor(image).unsqueeze(0)

        with torch.no_grad():
            output = model(image)
            print(output)
            pred = torch.where(output < 0.5, 0, 1)

        return pred

    model_path = "checkpoint/64.03654485049834MLCepoch-180.pth"
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    model.eval()
    prediction = process_single_image(image_path)
    res = prediction.numpy()[0].tolist()

    print(res)

    return jsonify({'res': res})


@app.route('/multi_view_check_image', methods=['GET', 'POST'])
def multi_view_check_image():
    from net.resnet import resnet50
    # get image path array
    data = request.json

    image_paths = data['imagePaths']
    print("Received image paths:", image_paths)


    return jsonify({'res': [1, 1, 0, 0, 1]})


@app.route('/change_image_contrast', methods=['GET', 'POST'])
def change_image_contrast():
    image_path = request.args.get('imagePath')
    print(image_path)
    image_path = image_path.replace('http://localhost:5000/', '')
    print(image_path)
    image = cv2.imread(image_path)
    alpha = 2  # 可以根据需要调整对比度的值，1表示不改变对比度
    beta = 0  # 可以根据需要调整亮度的值
    # 增加或降低对比度
    adjusted_image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)  # 假设你已经处理了图像，现在要保存它
    save_path = 'static/adjusted_image.png'
    cv2.imwrite(save_path, adjusted_image)

    path = 'http://localhost:5000/' + save_path
    print(path)
    return jsonify({'path': path})


@app.route('/del_data', methods=['DELETE'])
def del_data():
    id = int(request.args.get('id'))
    cursor = conn.cursor()
    print("DELETE FROM image WHERE id = %d" % id)
    cursor.execute("DELETE FROM image WHERE id = %d" % id)

    cursor.close()

    return jsonify({'code': '200'})


@app.route('/del_batchdata', methods=['DELETE'])
def del_batchdata():
    ids = request.args.get('ids')
    id_list = ids.split(',')  # 使用逗号分隔字符串，生成 ID 列表
    cursor = conn.cursor()
    for id in id_list:
        id = int(id)
        print("DELETE FROM image WHERE id = %d" % id)
        cursor.execute("DELETE FROM image WHERE id = %d" % id)
    cursor.close()
    return jsonify({'code': '200'})


@app.route('/get_user_data', methods=['GET'])
def get_user_data():
    # 获取前端发送的页码和每页数量参数
    page = int(request.args.get('page'))
    pageSize = int(request.args.get('pageSize'))
    name = request.args.get('name')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user where username  like %s', ('%' + name + '%'))
    data = cursor.fetchall()
    print(data)
    # 计算分页的起始索引和结束索引
    start = (page - 1) * pageSize
    end = start + pageSize

    # 获取特定页的图片数据
    paginated_data = data[start:end]

    # 获取表的元数据信息（列名、顺序等）
    cursor.execute("SHOW COLUMNS FROM user")
    columns = [col[0] for col in cursor.fetchall()]

    # 将数据转换为字典列表，并以 JSON 格式返回
    result = []
    for row in paginated_data:
        row_dict = dict(zip(columns, row))
        result.append(row_dict)

    cursor.close()

    return jsonify({'columns': columns, 'result': result, 'total': len(data)})


# 插入user数据

@app.route('/insert_data', methods=['GET', 'POST'])
def insert_data():
    form_data = request.get_json()
    print(form_data)
    username = form_data.get('username')
    role = form_data.get('role')
    # Using parameterized query to prevent SQL injection
    cursor = conn.cursor()
    print("INSERT INTO user (username,role) VALUES (%s,%s,)", (username, role))
    cursor.execute("INSERT INTO user (username,role) VALUES (%s,%s)", (username, role))
    conn.commit()
    cursor.close()

    return jsonify({'code': '200'})


@app.route('/update_data', methods=['GET', 'POST'])
def update_user():
    try:
        form_data = request.get_json()
        print(form_data)
        id = form_data.get('id')
        username = form_data.get('username')
        role = form_data.get('role')
        cursor = conn.cursor()
        # 构建 SQL 更新语句，直接格式化字符串
        sql_query = f"UPDATE user SET username = '{username}' , role = '{role}' WHERE id = {id}"

        print(sql_query)
        cursor.execute(sql_query)
        conn.commit()

        return jsonify({'code': '200', 'message': '用户信息更新成功'})
    except Exception as e:
        conn.rollback()
        return jsonify({'code': '500', 'message': '服务器错误'})


@app.route('/del_userdata', methods=['DELETE'])
def del_userdata():
    id = int(request.args.get('id'))
    cursor = conn.cursor()
    print("DELETE FROM user WHERE id = %d" % id)
    cursor.execute("DELETE FROM user WHERE id = %d" % id)

    cursor.close()

    return jsonify({'code': '200'})


@app.route('/del_userbatchdata', methods=['DELETE'])
def del_userbatchdata():
    ids = request.args.get('ids')
    id_list = ids.split(',')  # 使用逗号分隔字符串，生成 ID 列表
    cursor = conn.cursor()
    for id in id_list:
        id = int(id)
        print("DELETE FROM user WHERE id = %d" % id)
        cursor.execute("DELETE FROM user WHERE id = %d" % id)
    cursor.close()
    return jsonify({'code': '200'})


@app.route('/get_role_data', methods=['GET'])
def get_role_data():
    # 获取前端发送的页码和每页数量参数
    page = int(request.args.get('page'))
    pageSize = int(request.args.get('pageSize'))
    name = request.args.get('name')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM role where name  like %s', ('%' + name + '%'))
    data = cursor.fetchall()
    print(data)
    # 计算分页的起始索引和结束索引
    start = (page - 1) * pageSize
    end = start + pageSize

    # 获取特定页的图片数据
    paginated_data = data[start:end]

    # 获取表的元数据信息（列名、顺序等）
    cursor.execute("SHOW COLUMNS FROM role")
    columns = [col[0] for col in cursor.fetchall()]

    # 将数据转换为字典列表，并以 JSON 格式返回
    result = []
    for row in paginated_data:
        row_dict = dict(zip(columns, row))
        result.append(row_dict)

    cursor.close()
    return jsonify({'columns': columns, 'result': result, 'total': len(data)})


@app.route('/insert_roledata', methods=['GET', 'POST'])
def insert_roledata():
    form_data = request.get_json()
    print(form_data)
    name = form_data.get('name')
    # Using parameterized query to prevent SQL injection
    cursor = conn.cursor()
    print("INSERT INTO role (name) VALUES (%s)", (name))
    cursor.execute("INSERT INTO role (name) VALUES (%s)", (name))
    conn.commit()
    cursor.close()

    return jsonify({'code': '200'})


@app.route('/del_roledata', methods=['DELETE'])
def del_roledata():
    id = int(request.args.get('id'))
    cursor = conn.cursor()
    print("DELETE FROM role WHERE id = %d" % id)
    cursor.execute("DELETE FROM role WHERE id = %d" % id)

    cursor.close()

    return jsonify({'code': '200'})


@app.route('/del_rolebatchdata', methods=['DELETE'])
def del_rolebatchdata():
    ids = request.args.get('ids')
    id_list = ids.split(',')  # 使用逗号分隔字符串，生成 ID 列表
    cursor = conn.cursor()
    for id in id_list:
        id = int(id)
        print("DELETE FROM role WHERE id = %d" % id)
        cursor.execute("DELETE FROM role WHERE id = %d" % id)
    cursor.close()
    return jsonify({'code': '200'})


@app.route('/get_menu_data', methods=['GET'])
def get_menu_data():
    # 获取前端发送的页码和每页数量参数
    page = int(request.args.get('page'))
    pageSize = int(request.args.get('pageSize'))
    name = request.args.get('name')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM menu where name  like %s', ('%' + name + '%',))
    data = cursor.fetchall()
    print(data)
    # 计算分页的起始索引和结束索引
    start = (page - 1) * pageSize
    end = start + pageSize

    # 获取特定页的图片数据
    paginated_data = data[start:end]

    # 获取表的元数据信息（列名、顺序等）
    cursor.execute("SHOW COLUMNS FROM menu")
    columns = [col[0] for col in cursor.fetchall()]

    # 将数据转换为字典列表，并以 JSON 格式返回
    result = []
    for row in paginated_data:
        row_dict = dict(zip(columns, row))
        result.append(row_dict)

    cursor.close()

    return jsonify({'columns': columns, 'result': result, 'total': len(data)})


# 示例：获取菜单数据并按照父子关系格式化
@app.route('/get_expend_menu', methods=['GET'])
def get_expend_menu():
    try:
        # 假设您已经建立了数据库连接 conn，请替换为您自己的连接
        cursor = conn.cursor()

        # 查询所有菜单数据
        cursor.execute('SELECT * FROM menu')
        rows = cursor.fetchall()

        # 将菜单数据组织成带有父子关系的格式
        menu_dict = {}
        for row in rows:
            menu_id, name, path, icon, description, pid, sort_num = row
            if pid not in menu_dict:
                menu_dict[pid] = []
            menu_dict[pid].append({
                'id': menu_id,
                'label': name,
                'path': path,
                'icon': icon,
                'description': description,
                'sortNum': sort_num,
                'children': []
            })

        # 根据父子关系构建菜单树形结构
        menu_tree = menu_dict[None]  # 假设根菜单的 pid 为 None
        build_menu_tree(menu_tree, menu_dict)

        cursor.close()
        print(menu_tree)
        return jsonify({'data': menu_tree})  # 返回带有父子关系的菜单数据
    except Exception as e:
        return jsonify({'error': str(e)})  # 返回错误信息给前端


# 辅助函数：递归构建菜单树形结构
def build_menu_tree(menu_tree, menu_dict):
    for menu_item in menu_tree:
        menu_id = menu_item['id']
        if menu_id in menu_dict:
            menu_item['children'] = menu_dict[menu_id]
            build_menu_tree(menu_item['children'], menu_dict)


@app.route('/get_check_menu', methods=['GET'])
def get_check_menu():
    id = int(request.args.get('id'))
    cursor = conn.cursor()
    cursor.execute('SELECT menu_id FROM role_menu where  role_id  = %d ' % id)
    menu_ids = [row[0] for row in cursor.fetchall()]  # 获取查询结果并转换为列表
    return jsonify({'result': menu_ids})


@app.route('/get_menu_ids', methods=['GET'])
def get_menu_ids():
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM menu')
    ids = [row[0] for row in cursor.fetchall()]  # 获取查询结果并转换为列表
    return jsonify({'result': ids})


@app.route('/change_menu_data', methods=['GET', 'POST'])
def change_menu_data():
    form_data = request.get_json()
    print(form_data)
    id = form_data.get('id')
    name = form_data.get('name')
    path = form_data.get('path')
    # pagePath = form_data.get('pagePath')
    icon = form_data.get('icon')
    description = form_data.get('description')

    # Using parameterized query to prevent SQL injection
    cursor = conn.cursor()

    # 构建 SQL 更新语句，直接格式化字符串
    sql_query = f"UPDATE menu SET name= '{name}',path= '{path}',icon= '{icon}',description= '{description}' WHERE id = {id} "

    print(sql_query)
    cursor.execute(sql_query)

    # print("INSERT INTO menu(name,path,pagePath,description) VALUES (%s,%s,%s,%s,)", (name,path,pagePath,description))
    # cursor.execute("INSERT INTO menu(name,path,pagePath,description) VALUES (%s,%s,%s,%s,)", (name,path,pagePath,description))
    conn.commit()
    cursor.close()

    return jsonify({'code': '200'})


@app.route('/save_rolemenu', methods=['GET', 'POST'])
def save_rolemenu():
    try:
        role_id = int(request.args.get('id'))  # 获取角色ID
        menu_keys = request.json  # 获取前端发送的菜单键列表

        # 假设您已经建立了数据库连接 conn，请替换为您自己的连接
        cursor = conn.cursor()

        # 清除之前该角色的菜单分配关系
        cursor.execute('DELETE FROM role_menu WHERE role_id = %d' % role_id)
        cursor.execute("SELECT id FROM menu where pid is  null")
        data = cursor.fetchall()
        menu_keys.extend(row[0] for row in data)
        menu_keys = list(set(menu_keys))
        print(menu_keys)
        # 逐个插入新的菜单分配关系
        for menu_key in menu_keys:
            cursor.execute('INSERT INTO role_menu (role_id, menu_id) VALUES (%d, %d)' % (role_id, int(menu_key)))

        conn.commit()  # 提交事务
        cursor.close()

        return jsonify({'code': '200', 'msg': '菜单分配成功'})
    except Exception as e:
        return jsonify({'code': '500', 'msg': str(e)})  # 返回错误信息给前端


@app.route('/update_logged_userdata', methods=['GET', 'POST'])
def update_logged_userdata():
    form_data = request.get_json()
    print(form_data)
    id = form_data.get('id')
    username = form_data.get('username')
    role = form_data.get('role')
    phone = form_data.get('phone')
    avatar = form_data.get('avatarUrl')
    cursor = conn.cursor()
    # 构建 SQL 更新语句，直接格式化字符串
    sql_query = f"UPDATE user SET username = '{username}' , role = '{role}', phone = '{phone}', avatarUrl = '{avatar}' WHERE id = {id}"

    print(sql_query)
    cursor.execute(sql_query)
    conn.commit()

    return jsonify({'code': '200', 'message': '用户信息更新成功'})


# 上传头像接口
@app.route('/upload_avartar', methods=['POST'])
def upload_avartar():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        file.save(os.path.join('static/', file.filename))
        # 在这里你可以对文件进行进一步处理，比如保存文件路径到数据库等
        return os.path.join('http://localhost:5000/static/', file.filename)
    else:
        return jsonify({'error': 'Invalid file format'})


@app.route('/get_notice_data', methods=['GET'])
def get_notice_data():
    # 获取前端发送的页码和每页数量参数
    page = int(request.args.get('page'))
    pageSize = int(request.args.get('pageSize'))
    name = request.args.get('name')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM notice where content  like %s', ('%' + name + '%'))
    data = cursor.fetchall()
    print(data)
    # 计算分页的起始索引和结束索引
    start = (page - 1) * pageSize
    end = start + pageSize

    # 获取特定页的图片数据
    paginated_data = data[start:end]

    # 获取表的元数据信息（列名、顺序等）
    cursor.execute("SHOW COLUMNS FROM notice")
    columns = [col[0] for col in cursor.fetchall()]

    # 将数据转换为字典列表，并以 JSON 格式返回
    result = []
    for row in paginated_data:
        row_dict = dict(zip(columns, row))
        result.append(row_dict)

    cursor.close()

    return jsonify({'columns': columns, 'result': result, 'total': len(data)})


@app.route('/insert_notice_data', methods=['GET', 'POST'])
def insert_notice_data():
    form_data = request.get_json()
    print(form_data)
    content = form_data.get('content')
    author = form_data.get('author')
    created_at = form_data.get('created_at')
    # Using parameterized query to prevent SQL injection
    cursor = conn.cursor()
    print("INSERT INTO notice (content,author,created_at) VALUES (%s,%s,%s)", (content, author, created_at))
    cursor.execute("INSERT INTO notice (content,author,created_at) VALUES (%s,%s,%s)", (content, author, created_at))
    conn.commit()
    cursor.close()

    return jsonify({'code': '200'})


@app.route('/model_show', methods=['GET', 'POST'])
def model_show():
    image_path = request.args.get('imagePath')
    print(image_path)
    image_path = image_path.replace('http://localhost:5000/', '')
    print(image_path)
    # 指定模型权重文件路径、单张图片路径和保存结果的路径
    save_path = "infer_img/"
    img_size = 256
    threshold = 0.5
    pth = ["checkpoint/U_Net_model.pth", "checkpoint/CMUNet_model.pth", "checkpoint/CMUNeXt_model.pth",
           "checkpoint/AttU_Net_model.pth"]

    def load_model(model_path):
        if model_path == "checkpoint/CMUNet_model.pth":
            model = CMUNet(output_ch=1).cpu()
        elif model_path == "checkpoint/CMUNeXt_model.pth":
            model = cmunext(num_classes=1).cpu()
        elif model_path == "checkpoint/AttU_Net_model.pth":
            model = AttU_Net(output_ch=1).cpu()
        # elif model_path == "./checkpoint/U_Net_model.pth":
        #     model = U_Net(output_ch=1).cpu()
        else:
            model = U_Net(output_ch=1).cpu()
        model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
        return model

    def infer(output, threshold):
        edge = output > threshold
        return edge

    def save_png(edge, model_path):
        image = cv2.imread(image_path)
        image = cv2.resize(image, dsize=(256, 256))
        image = np.transpose(image, (2, 0, 1))
        w, h = edge.shape[1], edge.shape[2]
        for i in range(w):
            for j in range(h):
                if edge[0][i][j]:
                    image[:, i, j] = [0, 0, 255]
        image = np.transpose(image, (1, 2, 0))
        save_name = model_path.split('/')[-1].split('.')[0] + '_result.png'
        print(save_name)
        cv2.imwrite(save_path + save_name, image)

    device = torch.device('cpu')
    image = cv2.imread(image_path)
    test_transform = Compose([
        Resize(img_size, img_size),
        transforms.Normalize(),
    ])
    image = test_transform(image=image)["image"]

    # 转换图像为模型可接受的格式，并进行预测
    image = torch.tensor(image, dtype=torch.float).permute(2, 0, 1).unsqueeze(0) / 255.0
    path = []
    for model_path in pth:
        path.append(model_path.split('/')[-1].split('.')[0] + '_result.png')
        model = load_model(model_path).to(device)
        output = torch.sigmoid(model(image))
        edge = infer(output[0], threshold)
        save_png(edge, model_path)
    print(path)
    return jsonify({'path': path})


# 保存标注后的图片

@app.route('/save_imageLabel', methods=['POST'])
def save_imageLabel():
    image_data = request.json['imageData']  # 获取从前端发送的图像数据（base64编码）
    file_name = request.json['file_name']
    print(file_name)
    save_name = file_name.split('/')[-1]
    # 处理图像保存逻辑，这里仅为示例，你需要将base64转换为图像并保存到指定路径
    # 下面的代码是一个简单示例，使用Python处理base64编码的图像数据保存到本地
    import base64
    from PIL import Image
    import io

    # 从base64解码图像数据
    image = Image.open(io.BytesIO(base64.b64decode(image_data.split(',')[1])))
    image.save(os.path.join('labelled_image', 'labelled_' + save_name))  # 保存图像到指定路径

    return jsonify({'status': 'success', })


# 获取model表格中数据

@app.route('/get_model_data', methods=['GET'])
def get_model_data():
    # 获取前端发送的页码和每页数量参数
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM model')
    data = cursor.fetchall()

    # 获取表的元数据信息（列名、顺序等）
    cursor.execute("SHOW COLUMNS FROM model")
    columns = [col[0] for col in cursor.fetchall()]

    # 将数据转换为字典列表，并以 JSON 格式返回
    result = []
    for row in data:
        row_dict = dict(zip(columns, row))
        result.append(row_dict)

    cursor.close()
    return jsonify({'columns': columns, 'result': result, 'total': len(data)})


# 上传模型文件接口
@app.route('/upload_model', methods=['POST'])
def upload_model():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        file.save(os.path.join('static/', file.filename))
        # 在这里你可以对文件进行进一步处理，比如保存文件路径到数据库等
        return jsonify({'path': os.path.join('http://localhost:5000/static/', file.filename)})
    else:
        return jsonify({'error': 'Invalid file format'})


# 插入model数据

@app.route('/insert_model_data', methods=['GET', 'POST'])
def insert_model_data():
    form_data = request.get_json()
    print(form_data)
    name = form_data.get('name')
    path = form_data.get('path')
    upload_user = form_data.get('upload_user')
    description = form_data.get('description')
    params = form_data.get('params')
    FPS = form_data.get('FPS')
    IOU = form_data.get('IOU')
    F1_value = form_data.get('F1_value')
    # Using parameterized query to prevent SQL injection
    cursor = conn.cursor()
    print(
        "INSERT INTO model (name,path,upload_time,upload_user,description,params,FPS,IOU,F1_value) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        (
        name, path, datetime.datetime.now().strftime('%Y-%m-%d'), upload_user, description, params, FPS, IOU, F1_value))
    cursor.execute(
        "INSERT INTO model (name,path,upload_time,upload_user,description,params,FPS,IOU,F1_value) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        (
        name, path, datetime.datetime.now().strftime('%Y-%m-%d'), upload_user, description, params, FPS, IOU, F1_value))
    conn.commit()
    cursor.close()

    return jsonify({'code': '200'})


@app.route('/get_imagePath_byId', methods=['GET'])
def get_imagePath_byId():
    id = request.args.get('patientId')
    cursor = conn.cursor()
    file_paths = []
    cursor.execute("SELECT imagePath FROM image where patient_id = %s", id)
    data = cursor.fetchall()
    file_paths.extend(row[0] for row in data)  # 获取所有满足条件的文件路径列表
    cursor.close()
    file_paths = list(set(file_paths))
    return jsonify({'imagePaths': file_paths, 'totalnum': len(file_paths)})


if __name__ == '__main__':
    app.run()
