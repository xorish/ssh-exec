
def init_status_set(self):
    init_status = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
    <html><head><meta name="qrichtext" content="1" /><style type="text/css">
    p, li { white-space: pre-wrap; }
    </style></head><body style=" font-family:'Ubuntu Mono'; font-size:13pt; font-weight:400; font-style:normal;">
    <p align="center" style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p>
    <p align="center" style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p>
    <p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">WELCOME</p>
    <p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">TO</p>
    <p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">SSH-EXEC</p>
    <p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">&lt; Developed By Sourish Datta &gt;</p>
    <p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">License: (https://www.gnu.org/licenses/gpl-3.0.en.html)</p>
    <p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">Git: (https://github.com/xorish)</p></body></html>'''
    self.status.setText(init_status)

def jump_server_info_init(self):
    import sys
    import os
    path = os.path.dirname(os.path.abspath(sys.argv[0]))
    try:
        file = open(f"{path}/latest_jump_server_info", "r")
        data=eval(file.read())
        file.close()
        self.jump_host.setText(data[0])
        self.jump_user.setText(data[1])
        self.jump_password.setText(data[2])
    except:
        pass
def status_clear(self):
    text = self.status.toPlainText()

    if "WELCOME" in text:
        self.status.clear()


def current_time():
    from datetime import datetime

    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    return str(current_time)


def add_server(self, cursor):
    import sys
    import os
    import json
    path = os.path.dirname(os.path.abspath(sys.argv[0]))
    hostx = self.host.text()
    userx = self.user.text()
    passwordx = self.password.text()
    aliasx = self.alias.text()
    groupx = self.group.text()

    if hostx and userx and passwordx and aliasx and groupx:
        file = open(f"{path}/server_db.json", "r")
        data = json.load(file)
        file.close()
        if groupx in data.keys():
            data[groupx][hostx] = [aliasx, userx, passwordx]
        else:
            data[groupx] = {hostx: [aliasx, userx, passwordx]}
        file = open(f"{path}/server_db.json", "w")
        json.dump(data, file, indent=6)
        file.close()
        status_clear(self)
        cursor.insertText(
            f"\n {current_time()}: Server '{hostx}' has added to the group '{groupx}'.")
        load_group(self)
    else:
        cursor.insertText(
            f"\n {current_time()}: Incorrect info please check! \n If you want a password less connection just add a "
            f"dummy password in the password field. ")


def load_group(self):
    import sys
    import os
    import json
    path = os.path.dirname(os.path.abspath(sys.argv[0]))
    file = open(f"{path}/server_db.json", "r")
    data = json.load(file)
    file.close()
    self.group_combo.clear()
    for i in data.keys():
        self.group_combo.addItem(i)


def load_server(self):
    try:
        groupx = self.group_combo.currentText()
        import sys
        import os
        import json
        path = os.path.dirname(os.path.abspath(sys.argv[0]))
        file = open(f"{path}/server_db.json", "r")
        data = json.load(file)
        file.close()
        self.server_combo.clear()
        for i in data[groupx].keys():
            self.server_combo.addItem( i +f" ({data[groupx][i][0]})")
    except:
        pass

def connect_server(self, cursor):
    try:
        groupx = self.group_combo.currentText()
        hostx = self.server_combo.currentText().split(" ")[0]
        import sys
        import os
        import json
        path = os.path.dirname(os.path.abspath(sys.argv[0]))
        file = open(f"{path}/server_db.json", "r")
        data = json.load(file)
        file.close()
        user = data[groupx][hostx][1]
        password = data[groupx][hostx][2]
        status_clear(self)
        if self.Jump.isChecked():
            jump_host = self.jump_host.text()
            jump_user = self.jump_user.text()
            jump_password = self.jump_password.text()
            if jump_host and jump_user:
                if jump_password:
                    cursor.insertText(
                        f"\n {current_time()}: Checking connection to jump-server {jump_host}... ")
                    check_cmd = f"sshpass -p {jump_password} ssh -o StrictHostKeyChecking=no {jump_user}@{jump_host} 'echo ola'"
                    check_status = os.popen(check_cmd).read()
                    if check_status == "ola\n":
                        cursor.insertText(
                            f"\n {current_time()}: connection to jump-server {jump_host} in root-mode is ok. ")

                        ssh_cmd = f'''gnome-terminal -e "sshpass -p {jump_password} ssh -o StrictHostKeyChecking=no -J {jump_user}@{jump_host} {user}@{hostx}"'''
                        os.system(ssh_cmd)
                else:
                        cursor.insertText(
                            f"\n {current_time()}: Checking connection to jump-server {jump_host}... ")
                        check_cmd = f"ssh -o StrictHostKeyChecking=no {jump_user}@{jump_host} 'echo ola'"
                        check_status = os.popen(check_cmd).read()
                        if check_status == "ola\n":
                            cursor.insertText(
                                f"\n {current_time()}: connection to jump-server {jump_host} is ok. ")

                            ssh_cmd = f'''gnome-terminal -e "ssh -X -o StrictHostKeyChecking=no -J {jump_user}@{jump_host} {user}@{hostx}"'''
                            os.system(ssh_cmd)
                file=open(f"{path}/latest_jump_server_info","w")
                file.write(str([jump_host,jump_user,jump_password]))
                file.close()


        else:
            if self.root.isChecked():



                cursor.insertText(
                    f"\n {current_time()}: Checking connection to server {hostx}... ")
                check_cmd = f"ssh -o StrictHostKeyChecking=no root@{hostx} 'echo ola'"
                check_status = os.popen(check_cmd).read()
                if check_status == "ola\n":
                    cursor.insertText(
                        f"\n {current_time()}: connection to server {hostx} in root-mode is ok. ")
                    ssh_cmd = f'''gnome-terminal -e "ssh -X -o StrictHostKeyChecking=no root@{hostx}"'''
                    os.system(ssh_cmd)
                else:

                    cursor.insertText(f"\n {current_time()}: connection to server as 'root'-user has failed check whether "
                                      f"public is added to that server and root login is enabled.")

            elif self.non_root.isChecked():
                cursor.insertText(
                    f"\n {current_time()}: Checking connection to server {hostx}... ")
                check_cmd = f"sshpass -p {password} ssh -o StrictHostKeyChecking=no {user}@{hostx} 'echo ola'"
                check_status = os.popen(check_cmd).read()
                if check_status == "ola\n":
                    cursor.insertText(
                        f"\n {current_time()}: connection to server {hostx} in user mode is ok. ")
                    ssh_cmd = f'''gnome-terminal -e "sshpass -p {password} ssh -X -o StrictHostKeyChecking=no {user}@{hostx}"'''
                    os.system(ssh_cmd)
                else:
                    cursor.insertText(
                        f"\n {current_time()}: connection to server as user-'{user}' has failed check server is up or not.")

    except Exception as e:
        cursor.insertText(
            f"\n {current_time()}: {e}")


def connect_group(self, cursor):
    try:
        groupx = self.group_combo.currentText()
        import sys
        import os
        import json
        path = os.path.dirname(os.path.abspath(sys.argv[0]))
        file = open(f"{path}/server_db.json", "r")
        data = json.load(file)
        file.close()

        status_clear(self)
        for i in data[groupx].keys():
            hostx = i
            user = data[groupx][hostx][1]
            password = data[groupx][hostx][2]
            if self.root.isChecked():

                cursor.insertText(
                    f"\n {current_time()}: Checking connection to server {hostx}... ")
                check_cmd = f"ssh -o StrictHostKeyChecking=no root@{hostx} 'echo ola'"
                check_status = os.popen(check_cmd).read()
                if check_status == "ola\n":
                    cursor.insertText(
                        f"\n {current_time()}: connection to server {hostx} in root-mode is ok. ")
                    ssh_cmd = f'''gnome-terminal -e "ssh -o StrictHostKeyChecking=no root@{hostx}"'''
                    os.system(ssh_cmd)
                else:

                    cursor.insertText(f"\n {current_time()}: connection to server as 'root'-user has failed check whether "
                                      f"public is added to that server and root login is enabled.")

            elif self.non_root.isChecked():
                cursor.insertText(
                    f"\n {current_time()}: Checking connection to server {hostx}... ")
                check_cmd = f"sshpass -p {password} ssh -o StrictHostKeyChecking=no {user}@{hostx} 'echo ola'"
                check_status = os.popen(check_cmd).read()
                if check_status == "ola\n":
                    cursor.insertText(
                        f"\n {current_time()}: connection to server {hostx} in user mode is ok. ")
                    ssh_cmd = f'''gnome-terminal -e "sshpass -p {password} ssh -o StrictHostKeyChecking=no {user}@{hostx}"'''
                    os.system(ssh_cmd)
                else:
                    cursor.insertText(
                        f"\n {current_time()}: connection to server as user-'{user}' has failed check server is up or not.")
    except Exception as e:
        cursor.insertText(
            f"\n {current_time()}: {e}")

def add_public_key_to_server(self, cursor):
    try:
        groupx = self.group_combo.currentText()
        hostx = self.server_combo.currentText().split(" ")[0]
        import sys
        import os
        import json
        path = os.path.dirname(os.path.abspath(sys.argv[0]))
        file = open(f"{path}/server_db.json", "r")
        data = json.load(file)
        file.close()
        user = data[groupx][hostx][1]
        password = data[groupx][hostx][2]
        status_clear(self)
        key = self.public_key.text()
        file = open(f"{path}/ssh_key_add_script_templete", "r")
        script = file.read().replace("KEY", key)
        file.close()
        file = open(f"{path}/temp_script.py", "w")
        file.write(script)
        file.close()
        cursor.insertText(
            f"\n {current_time()}: Checking connection to server {hostx}... ")
        check_cmd = f"sshpass -p {password} ssh -o StrictHostKeyChecking=no {user}@{hostx} 'echo ola'"
        check_status = os.popen(check_cmd).read()
        if check_status == "ola\n":
            scp_cmd = f"sshpass -p {password} scp -o StrictHostKeyChecking=no {path}/temp_script.py {user}@{hostx}:~/"
            os.system(scp_cmd)
            cmdx = f"echo {password} | sudo -S python3 ~/temp_script.py"
            ssh_cmd = f"sshpass -p {password} ssh -o StrictHostKeyChecking=no {user}@{hostx} '{cmdx}'"
            res = os.popen(ssh_cmd).read()
            if res != "done\n":
                cursor.insertText(f"\n {current_time()}: {res}")
            elif res == "done\n":
                cursor.insertText(
                    f"\n {current_time()}: Public key has added to the host '{hostx}'")
                ssh_cmd = f"sshpass -p {password} ssh -o StrictHostKeyChecking=no {user}@{hostx} 'rm ~/temp_script.py'"
                os.system(ssh_cmd)
            os.system(f"rm {path}/temp_script.py")

        else:
            cursor.insertText(
                f"\n {current_time()}: connection to server as user-'{user}' has failed check server is up or not.")
    except Exception as e:
        cursor.insertText(
            f"\n {current_time()}: {e}")

def add_public_key_to_group(self, cursor):
    try:
        groupx = self.group_combo.currentText()

        import sys
        import os
        import json
        path = os.path.dirname(os.path.abspath(sys.argv[0]))
        file = open(f"{path}/server_db.json", "r")
        data = json.load(file)
        file.close()

        status_clear(self)
        key = self.public_key.text()
        self.public_key.clear()
        file = open(f"{path}/ssh_key_add_script_templete", "r")
        script = file.read().replace("KEY", key)
        file.close()
        file = open(f"{path}/temp_script.py", "w")
        file.write(script)
        file.close()
        for i in data[groupx].keys():
            try:
                hostx = i
                user = data[groupx][hostx][1]
                password = data[groupx][hostx][2]
                cursor.insertText(
                    f"\n {current_time()}: Checking connection to server {hostx}... ")
                check_cmd = f"sshpass -p {password} ssh -o StrictHostKeyChecking=no {user}@{hostx} 'echo ola'"
                check_status = os.popen(check_cmd).read()
                if check_status == "ola\n":
                    scp_cmd = f"sshpass -p {password} scp -o StrictHostKeyChecking=no {path}/temp_script.py {user}@{hostx}:~/"
                    os.system(scp_cmd)
                    cmdx = f"echo {password} | sudo -S python3 ~/temp_script.py"
                    ssh_cmd = f"sshpass -p {password} ssh -o StrictHostKeyChecking=no {user}@{hostx} '{cmdx}'"
                    res = os.popen(ssh_cmd).read()
                    if res != "done\n":
                        cursor.insertText(f"\n {current_time()}: {res}")
                    elif res == "done\n":
                        cursor.insertText(
                            f"\n {current_time()}: Public key has added to the host '{hostx}'")
                        ssh_cmd = f"sshpass -p {password} ssh -o StrictHostKeyChecking=no {user}@{hostx} 'rm ~/temp_script.py'"
                        os.system(ssh_cmd)

                else:
                    cursor.insertText(
                        f"\n {current_time()}: connection to server as user-'{user}' has failed check server is up or not.")

            except:
                pass
        os.system(f"rm {path}/temp_script.py")
    except Exception as e:
        cursor.insertText(
            f"\n {current_time()}: {e}")

def file_upload_to_server(self,cursor):
    try:
        source_file_path=self.source_location.text()
        destination_file_path=self.destination_location.text()
        groupx = self.group_combo.currentText()
        hostx = self.server_combo.currentText().split(" ")[0]
        import sys
        import os
        import json
        from subprocess import Popen, PIPE
        path = os.path.dirname(os.path.abspath(sys.argv[0]))
        file = open(f"{path}/server_db.json", "r")
        data = json.load(file)
        file.close()
        user = data[groupx][hostx][1]
        password = data[groupx][hostx][2]
        status_clear(self)
        if self.root.isChecked():
            cursor.insertText(
                f"\n {current_time()}: Checking connection to server {hostx}... ")
            check_cmd = f"ssh -o StrictHostKeyChecking=no root@{hostx} 'echo ola'"
            check_status = os.popen(check_cmd).read()
            if check_status == "ola\n":
                cursor.insertText(
                    f"\n {current_time()}: connection to server {hostx} in root-mode is ok. ")
                if self.file.isChecked():
                    scp_cmd= f"scp -o StrictHostKeyChecking=no {source_file_path} root@{hostx}:{destination_file_path}"
                elif self.directory.isChecked():
                    scp_cmd= f"scp -o StrictHostKeyChecking=no -r {source_file_path} root@{hostx}:{destination_file_path}"

                cursor.insertText(f"\n {current_time()}: Started uploading...")

                pro = Popen("exec " + scp_cmd, stdout=PIPE, stderr=PIPE, shell=True)
                err_message = pro.stderr.read().decode()
                cursor.insertText(f"\n {current_time()}:{err_message}")
                output= pro.stdout.read().decode()
                cursor.insertText(f"\n {current_time()}:{output}")
                if err_message:
                    cursor.insertText(f"\n {current_time()}:{err_message}")
                elif output:

                    cursor.insertText(f"\n {current_time()}:{output}")
                else:
                    cursor.insertText(f"\n {current_time()}: Upload done.")


            else:
                cursor.insertText(f"\n {current_time()}: connection to server as 'root'-user has failed check whether "
                                  f"public is added to that server and root login is enabled.")

        elif self.non_root.isChecked():
            cursor.insertText(
                f"\n {current_time()}: Checking connection to server {hostx}... ")
            check_cmd = f"sshpass -p {password} ssh -o StrictHostKeyChecking=no {user}@{hostx} 'echo ola'"
            check_status = os.popen(check_cmd).read()
            if check_status == "ola\n":
                cursor.insertText(
                    f"\n {current_time()}: connection to server {hostx} in user mode is ok. ")
                if self.file.isChecked():
                    scp_cmd = f"sshpass -p {password} scp -o StrictHostKeyChecking=no {source_file_path} {user}@{hostx}:{destination_file_path}"
                elif self.directory.isChecked():
                    scp_cmd = f"sshpass -p {password} scp -o StrictHostKeyChecking=no -r {source_file_path} {user}@{hostx}:{destination_file_path}"
                cursor.insertText(f"\n {current_time()}: Started uploading...")
                pro = Popen("exec " + scp_cmd, stdout=PIPE, stderr=PIPE, shell=True)
                err_message = pro.stderr.read().decode()
                output = pro.stdout.read().decode()
                if err_message:
                    cursor.insertText(f"\n {current_time()}:{err_message}")
                elif output:

                    cursor.insertText(f"\n {current_time()}:{output}")
                else:
                    cursor.insertText(f"\n {current_time()}: Upload done.")

            else:
                cursor.insertText(
                    f"\n {current_time()}: connection to server as user-'{user}' has failed check server is up or not.")
    except Exception as e:
        cursor.insertText(
            f"\n {current_time()}: {e}")
def file_upload_to_group(self,cursor):
    try:
        source_file_path=self.source_location.text()
        destination_file_path=self.destination_location.text()
        groupx = self.group_combo.currentText()
        import sys
        import os
        import json
        from subprocess import Popen, PIPE
        path = os.path.dirname(os.path.abspath(sys.argv[0]))
        file = open(f"{path}/server_db.json", "r")
        data = json.load(file)
        file.close()

        status_clear(self)
        for i in data[groupx].keys():
            hostx=i
            user = data[groupx][hostx][1]
            password = data[groupx][hostx][2]
            if self.root.isChecked():
                cursor.insertText(
                    f"\n {current_time()}: Checking connection to server {hostx}... ")
                check_cmd = f"ssh -o StrictHostKeyChecking=no root@{hostx} 'echo ola'"
                check_status = os.popen(check_cmd).read()
                if check_status == "ola\n":
                    cursor.insertText(
                        f"\n {current_time()}: connection to server {hostx} in root-mode is ok. ")
                    if self.file.isChecked():
                        scp_cmd = f"scp -o StrictHostKeyChecking=no {source_file_path} root@{hostx}:{destination_file_path}"
                    elif self.directory.isChecked():
                        scp_cmd = f"scp -o StrictHostKeyChecking=no -r {source_file_path} root@{hostx}:{destination_file_path}"
                    cursor.insertText(f"\n {current_time()}: Started uploading...")

                    pro = Popen("exec " + scp_cmd, stdout=PIPE, stderr=PIPE, shell=True)
                    err_message = pro.stderr.read().decode()
                    cursor.insertText(f"\n {current_time()}:{err_message}")
                    output = pro.stdout.read().decode()
                    cursor.insertText(f"\n {current_time()}:{output}")
                    if err_message:
                        cursor.insertText(f"\n {current_time()}:{err_message}")
                    elif output:

                        cursor.insertText(f"\n {current_time()}:{output}")
                    else:
                        cursor.insertText(f"\n {current_time()}: Upload done.")


                else:
                    cursor.insertText(f"\n {current_time()}: connection to server as 'root'-user has failed check whether "
                                      f"public is added to that server and root login is enabled.")

            elif self.non_root.isChecked():
                cursor.insertText(
                    f"\n {current_time()}: Checking connection to server {hostx}... ")
                check_cmd = f"sshpass -p {password} ssh -o StrictHostKeyChecking=no {user}@{hostx} 'echo ola'"
                check_status = os.popen(check_cmd).read()
                if check_status == "ola\n":
                    cursor.insertText(
                        f"\n {current_time()}: connection to server {hostx} in user mode is ok. ")
                    if self.file.isChecked():
                        scp_cmd = f"sshpass -p {password} scp -o StrictHostKeyChecking=no {source_file_path} {user}@{hostx}:{destination_file_path}"
                    elif self.directory.isChecked():
                        scp_cmd = f"sshpass -p {password} scp -o StrictHostKeyChecking=no -r {source_file_path} {user}@{hostx}:{destination_file_path}"
                    cursor.insertText(f"\n {current_time()}: Started uploading...")
                    pro = Popen("exec " + scp_cmd, stdout=PIPE, stderr=PIPE, shell=True)
                    err_message = pro.stderr.read().decode()
                    output = pro.stdout.read().decode()
                    if err_message:
                        cursor.insertText(f"\n {current_time()}:{err_message}")
                    elif output:

                        cursor.insertText(f"\n {current_time()}:{output}")
                    else:
                        cursor.insertText(f"\n {current_time()}: Upload done.")

                else:
                    cursor.insertText(
                        f"\n {current_time()}: connection to server as user-'{user}' has failed check server is up or not.")
    except Exception as e:
        cursor.insertText(
            f"\n {current_time()}: {e}")

def download_from_server(self, cursor):
    try:
        source_file_path=self.source_location.text()
        destination_file_path=self.destination_location.text()
        groupx = self.group_combo.currentText()
        hostx = self.server_combo.currentText().split(" ")[0]
        import sys
        import os
        import json
        from subprocess import Popen, PIPE
        path = os.path.dirname(os.path.abspath(sys.argv[0]))
        file = open(f"{path}/server_db.json", "r")
        data = json.load(file)
        file.close()
        user = data[groupx][hostx][1]
        password = data[groupx][hostx][2]
        status_clear(self)
        if self.root.isChecked():
            cursor.insertText(
                f"\n {current_time()}: Checking connection to server {hostx}... ")
            check_cmd = f"ssh -o StrictHostKeyChecking=no root@{hostx} 'echo ola'"
            check_status = os.popen(check_cmd).read()
            if check_status == "ola\n":
                cursor.insertText(
                    f"\n {current_time()}: connection to server {hostx} in root-mode is ok. ")
                if self.file.isChecked():
                    scp_cmd= f"scp -o StrictHostKeyChecking=no root@{hostx}:{source_file_path} {destination_file_path}"
                elif self.directory.isChecked():
                    scp_cmd= f"scp -o StrictHostKeyChecking=no -r root@{hostx}:{source_file_path} {destination_file_path}"
                cursor.insertText(f"\n {current_time()}: Started downloading...")
                pro = Popen("exec " + scp_cmd, stdout=PIPE, stderr=PIPE, shell=True)
                err_message = pro.stderr.read().decode()
                cursor.insertText(f"\n {current_time()}:{err_message}")
                output= pro.stdout.read().decode()
                cursor.insertText(f"\n {current_time()}:{output}")
                if err_message:
                    cursor.insertText(f"\n {current_time()}:{err_message}")
                elif output:

                    cursor.insertText(f"\n {current_time()}:{output}")
                else:
                    cursor.insertText(f"\n {current_time()}: Download done.")


            else:
                cursor.insertText(f"\n {current_time()}: connection to server as 'root'-user has failed check whether "
                                  f"public is added to that server and root login is enabled.")

        elif self.non_root.isChecked():
            cursor.insertText(
                f"\n {current_time()}: Checking connection to server {hostx}... ")
            check_cmd = f"sshpass -p {password} ssh -o StrictHostKeyChecking=no {user}@{hostx} 'echo ola'"
            check_status = os.popen(check_cmd).read()
            if check_status == "ola\n":
                cursor.insertText(
                    f"\n {current_time()}: connection to server {hostx} in user mode is ok. ")
                if self.file.isChecked():
                    scp_cmd = f"sshpass -p {password} scp -o StrictHostKeyChecking=no {user}@{hostx}:{source_file_path} {destination_file_path}"
                elif self.directory.isChecked():
                    scp_cmd = f"sshpass -p {password} scp -o StrictHostKeyChecking=no -r {user}@{hostx}:{source_file_path} {destination_file_path}"
                cursor.insertText(f"\n {current_time()}: Started downloading...")
                pro = Popen("exec " + scp_cmd, stdout=PIPE, stderr=PIPE, shell=True)
                err_message = pro.stderr.read().decode()
                output = pro.stdout.read().decode()
                if err_message:
                    cursor.insertText(f"\n {current_time()}:{err_message}")
                elif output:

                    cursor.insertText(f"\n {current_time()}:{output}")
                else:
                    cursor.insertText(f"\n {current_time()}: Download done.")

            else:
                cursor.insertText(
                    f"\n {current_time()}: connection to server as user-'{user}' has failed check server is up or not.")
    except Exception as e:
        cursor.insertText(
            f"\n {current_time()}: {e}")

def command_runner_for_server(self, cursor):
    try:
        commandx=self.command.text()
        groupx = self.group_combo.currentText()
        hostx = self.server_combo.currentText().split(" ")[0]
        import sys
        import os
        import json
        path = os.path.dirname(os.path.abspath(sys.argv[0]))
        file = open(f"{path}/server_db.json", "r")
        data = json.load(file)
        file.close()
        user = data[groupx][hostx][1]
        password = data[groupx][hostx][2]
        status_clear(self)
        file=open(f"{path}/history_list", "a")
        file.write(f"\t{commandx}\n")
        file.close()
        if self.root.isChecked():

            cursor.insertText(
                f"\n {current_time()}: Checking connection to server {hostx}... ")
            check_cmd = f"ssh -o StrictHostKeyChecking=no root@{hostx} 'echo ola'"
            check_status = os.popen(check_cmd).read()
            if check_status == "ola\n":
                cursor.insertText(
                    f"\n {current_time()}: connection to server {hostx} in root-mode is ok. ")
                ssh_cmd = f'''gnome-terminal -e "ssh -o StrictHostKeyChecking=no root@{hostx} '{commandx}'"'''
                cursor.insertText(
                    f"\n {current_time()}: Running command on {hostx} in root mode. ")
                os.system(ssh_cmd)
            else:

                cursor.insertText(f"\n {current_time()}: connection to server as 'root'-user has failed check whether "
                                  f"public is added to that server and root login is enabled.")

        elif self.non_root.isChecked():
            cursor.insertText(
                f"\n {current_time()}: Checking connection to server {hostx}... ")
            check_cmd = f"sshpass -p {password} ssh -o StrictHostKeyChecking=no {user}@{hostx} 'echo ola'"
            check_status = os.popen(check_cmd).read()
            if check_status == "ola\n":
                cursor.insertText(
                    f"\n {current_time()}: connection to server {hostx} in user mode is ok. ")
                ssh_cmd = f'''gnome-terminal -e "sshpass -p {password} ssh -o StrictHostKeyChecking=no {user}@{hostx} '{commandx}'"'''
                cursor.insertText(
                    f"\n {current_time()}: Running command on {hostx} in user mode. ")
                os.system(ssh_cmd)
            else:
                cursor.insertText(
                    f"\n {current_time()}: connection to server as user-'{user}' has failed check server is up or not.")
    except Exception as e:
        cursor.insertText(
            f"\n {current_time()}: {e}")
def command_runner_for_group(self, cursor):
    try:
        commandx=self.command.text()
        groupx = self.group_combo.currentText()
        import sys
        import os
        import json
        path = os.path.dirname(os.path.abspath(sys.argv[0]))
        file = open(f"{path}/server_db.json", "r")
        data = json.load(file)
        file.close()
        file=open(f"{path}/history_list", "a")
        file.write(f"\t{commandx}\n")
        file.close()
        status_clear(self)
        for i in data[groupx].keys():
            hostx = i
            user = data[groupx][hostx][1]
            password = data[groupx][hostx][2]
            if self.root.isChecked():

                cursor.insertText(
                    f"\n {current_time()}: Checking connection to server {hostx}... ")
                check_cmd = f"ssh -o StrictHostKeyChecking=no root@{hostx} 'echo ola'"
                check_status = os.popen(check_cmd).read()
                if check_status == "ola\n":
                    cursor.insertText(
                        f"\n {current_time()}: connection to server {hostx} in root-mode is ok. ")
                    ssh_cmd = f'''gnome-terminal -e "ssh -o StrictHostKeyChecking=no root@{hostx} '{commandx}'"'''
                    cursor.insertText(
                        f"\n {current_time()}: Running command on {hostx} in root mode. ")
                    os.system(ssh_cmd)
                else:

                    cursor.insertText(f"\n {current_time()}: connection to server as 'root'-user has failed check whether "
                                      f"public is added to that server and root login is enabled.")

            elif self.non_root.isChecked():
                cursor.insertText(
                    f"\n {current_time()}: Checking connection to server {hostx}... ")
                check_cmd = f"sshpass -p {password} ssh -o StrictHostKeyChecking=no {user}@{hostx} 'echo ola'"
                check_status = os.popen(check_cmd).read()
                if check_status == "ola\n":
                    cursor.insertText(
                        f"\n {current_time()}: connection to server {hostx} in user mode is ok. ")
                    ssh_cmd = f'''gnome-terminal -e "sshpass -p {password} ssh -o StrictHostKeyChecking=no {user}@{hostx} '{commandx}'"'''
                    cursor.insertText(
                        f"\n {current_time()}: Running command on {hostx} in user mode. ")
                    os.system(ssh_cmd)
                else:
                    cursor.insertText(
                        f"\n {current_time()}: connection to server as user-'{user}' has failed check server is up or not.")

    except Exception as e:
        cursor.insertText(
            f"\n {current_time()}: {e}")

def clear_history(self, cursor):
    import sys
    import os
    path = os.path.dirname(os.path.abspath(sys.argv[0]))

    self.process_history.start('python3', ['-u', f'{path}/delete_history_consent.py'])


def history(self):
    import sys
    import os
    from PyQt5 import QtCore
    path = os.path.dirname(os.path.abspath(sys.argv[0]))
    self.process_history = QtCore.QProcess()
    self.process_history.start('python3', ['-u', f'{path}/history.py'])

def remove_server(self, cursor):
    import sys
    import os
    path = os.path.dirname(os.path.abspath(sys.argv[0]))
    groupx = self.group_combo.currentText()
    hostx = self.server_combo.currentText().split(" ")[0]
    file = open(f"{path}/temp_buff", "w")
    file.write(groupx+" "+hostx)
    file.close()
    self.process_delete_server_consent.start('python3', ['-u', f'{path}/delete_server_consent.py'])



def remove_group(self, cursor):
        import sys
        import os
        path = os.path.dirname(os.path.abspath(sys.argv[0]))
        groupx = self.group_combo.currentText()
        file=open(f"{path}/temp_buff","w")
        file.write(groupx)
        file.close()
        self.process_delete_group_consent.start('python3', ['-u', f'{path}/delete_group_consent.py'])
