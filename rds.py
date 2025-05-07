<<<<<<< HEAD
from tkinter import *
from tkinter import messagebox, filedialog, simpledialog, colorchooser, ttk
import matplotlib.pyplot as plt
import numpy as np
import pickle
from sys import argv
import os
import random
from urllib import request
import json
import yaml
import json
import time
import winsound
import shutil
import configparser
import ctypes
import threading


version = "v2.0"


def getPath(path):
    return os.path.join(os.path.dirname(__file__), path)


def raiseError(title, information):
    messagebox.showerror(title, information)
    mode = "a"
    if not os.path.exists(getPath("error.log")):
        mode = "w"
    with open(getPath("error.log"), mode) as f:
        f.write(information + "\n")


try:
    shutil.rmtree(getPath("temp"))
except FileNotFoundError:
    pass


rewrite = False
global setting
setting = {}
if os.path.exists(getPath("setting.json")):
    with open(getPath("setting.json"), "r") as f:
        try:
            setting = json.load(f)
        except Exception:
            rewrite = True
    if type(setting) == dict:
        for i in [
            "CDrawNumber",
            "Algorithm",
            "Background",
            "Foreground",
            "NameForeground",
            "DownloadFrom",
            "Language",
        ]:
            if not i in setting:
                rewrite = True
    else:
        rewrite = True
else:
    rewrite = True
if rewrite:
    if type(setting) != dict:
        setting = {}
    setting.update(
        {
            "CDrawNumber": 10,
            "Algorithm": "old",
            "Background": "#F8FAED",
            "Foreground": "#525059",
            "NameForeground": {"N": "#525059", "C": "#FBA346", "U": "#92B42A"},
            "DownloadFrom": "github",
            "Language": "zh-CN",
        }
    )
    with open(getPath("setting.json"), "w") as f:
        json.dump(setting, f)


if not os.path.exists(getPath(os.path.join("language", setting["Language"] + ".yml"))):
    raiseError("Error", "Cannot load the language file!")
    exit(1)

with open(
    getPath(os.path.join("language", setting["Language"] + ".yml")),
    "r",
    encoding="utf-8",
) as f:
    global lang
    lang = yaml.safe_load(f)

with open(
    getPath(os.path.join("language", "zh-CN.yml")),
    "r",
    encoding="utf-8",
) as f:
    global m_lang
    m_lang = yaml.safe_load(f)


def getLang(text):
    if text in lang:
        return lang[text]
    elif text in m_lang:
        return m_lang[text]
    else:
        raiseError("Error", "Cannot get the language information: %s" % (text))


global langDict
global langSList
with open(
    getPath(os.path.join("language", "languages.json")), "r", encoding="utf-8"
) as f:
    langDict = json.load(f)
langSList = []
for i in langDict:
    langSList.append(langDict[i]["show"])


if not os.path.exists(getPath("api.yml")):
    raiseError("Error", "Cannot load the API file!")
    exit(1)

with open(getPath("api.yml"), "r", encoding="utf-8") as f:
    global api
    api = yaml.safe_load(f)

try:
    global logics
    logics = api["logics"]
    global logicDList
    logicDList = []
    for i in logics:
        if logics[i]["show"]:
            logicDList.append(logics[i]["description"][setting["Language"]])
except KeyError:
    raiseError("Error", "Invalid API!")
    exit(1)

root = Tk(className="random student")
root.geometry(
    "%dx%d" % ((200, 200) if setting["Language"] in ["zh-CN"] else (230, 230))
)
root.title("Random Student")
root.attributes("-topmost", 1)
root.resizable(0, 0)


rewrite = False
studentList = {"version": version, "students": {}}
if os.path.exists(getPath("student.pkl")):
    with open(getPath("student.pkl"), "rb") as f:
        try:
            studentList = pickle.load(f)
            if not "version" in studentList:
                messagebox.showinfo(getLang("rdsMessage"), getLang("oldVersionList"))
                _studentList = {"version": version, "students": {}}
                for i in studentList:
                    name = i[:-1]
                    tag = "N"
                    if name[-1] == "]":
                        tag = name[-2]
                        name = name[:-3]
                    _studentList["students"][name] = tag
                studentList = _studentList
                rewrite = True
        except Exception:
            rewrite = True
else:
    rewrite = True
if rewrite:
    with open(getPath("student.pkl"), "wb") as f:
        pickle.dump(studentList, f)

historyList = []

os.makedirs(getPath("temp"))
with open(getPath("temp\\history.tmp"), "wb") as f:
    pickle.dump(historyList, f)


class GetNames(object):
    def __init__(self, name="rds"):
        self.name = name


global getNames
getNames = GetNames()


def trueRandom(
    student: dict,
    history: dict,
    isCdraw: bool = False,
    isTest: bool = False,
    CdrawTime: int = 0,
) -> list:
    times = 1
    if isCdraw:
        times = CdrawTime
    data = student["students"]
    names = tuple(data.keys())
    returnBack = []
    for i in range(times):
        returnBack.append(names[random.randint(0, len(data) - 1)])
    return returnBack


setattr(getNames, "logic::test::etr", trueRandom)


setattr(
    getNames,
    "lol",
    lambda: (
        messagebox.showerror(
            "ERROR?",
            "ERROR 0x00114514: AN ERROR HAS OCCURRED THAT COULD PERMANENTLY RENDER YOUR DEVICE UNUSABLE...?",
        ),
        time.sleep(1),
        messagebox.showinfo("LOL", "Happy April Fools' Day!"),
    ),
)

Frame(root, height=5).pack()
studentNow = Label(
    root, text=getLang("rdsMessage"), font=("Microsoft YaHei UI", 20), fg="gray"
)
studentNow.pack()


def about(*args):
    messagebox.showinfo(
        getLang("about"),
        """Random Student v2.0

Copyright 2023-2025 distjr_, ruufly!, hz, dyt_dirt, et al.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
""",
    )


def randomName(*args):
    winsound.Beep(2000,50)
    if api["logics"][setting["Algorithm"]]["type"] == "file":
        shouldAt = os.getcwd()
        os.chdir(getPath(""))
        os.system(getPath(api["logics"][setting["Algorithm"]]["file"]))
        os.chdir(shouldAt)
        with open(getPath("temp\\now.tmp"), "rb") as f:
            now = pickle.load(f)[0]
    elif api["logics"][setting["Algorithm"]]["type"] == "function":
        now = getattr(getNames, api["logics"][setting["Algorithm"]]["index"])(
            studentList, historyList, False, False
        )[0]
    elif api["logics"][setting["Algorithm"]]["type"] == "foolsday":
        getattr(getNames, api["logics"][setting["Algorithm"]]["index"])()
    historyList.append(
        {"name": now, "type": studentList["students"][now], "cdraw": False}
    )
    with open(getPath("temp\\history.tmp"), "wb") as f:
        pickle.dump(historyList, f)
    studentNow.config(
        text=now, fg=setting["NameForeground"][studentList["students"][now]]
    )
    # print(now)


def repeatedRandom(*args): ...


def update(show=False):
    try:
        data = json.loads(
            request.urlopen(
                "https://gitee.com/api/v5/repos/distjr/random-student/releases/latest"
            ).read()
        )
    except Exception:
        raiseError("Error", "Network Error")
        return
    if data["tag_name"] == "v2.0":
        if show:
            messagebox.showinfo(getLang("rdsMessage"), getLang("noNewVersion"))
    else:
        if messagebox.askyesno(
            getLang("rdsMessage"), getLang("newVersion") % data["name"]
        ):
            updateRoot = Toplevel(root)
            updateRoot.title(getLang("downloadProgress"))
            updateRoot.geometry("300x70")
            updateRoot.attributes("-topmost", 1)
            updateRoot.resizable(0, 0)
            global ttc
            ttc = ttk.Progressbar(
                updateRoot, orient="horizontal", length=250, mode="determinate"
            )
            ttc.place(x=5, y=5)
            global utc
            utc = Label(updateRoot)
            utc.place(x=85, y=40)

            def Schedule(a, b, c):
                global ttc
                global utc
                per = 100.0 * a * b / c
                if per > 100:
                    per == 100
                ttc["value"] = per
                utc.config(
                    text=getLang("progress")
                    % ((a * b) / (1024 * 1024), c / (1024 * 1024), per)
                )
                updateRoot.update()

            def del_update(*args):
                global downloading
                if downloading:
                    pass
                else:
                    updateRoot.destroy()

            updateRoot.protocol("WM_DELETE_WINDOW", del_update)
            global downloading
            downloading = True
            request.urlretrieve(
                data["assets"][0]["browser_download_url"], "update.exe", Schedule
            )
            downloading = False
            updateRoot.destroy()
            messagebox.showinfo(getLang("rdsMessage"), getLang("startInstall"))
            threading.Thread(target=os.system, args=("update.exe",)).start()


def showData(all_data):
    all_data[0] = np.array(all_data[0])
    all_data[1] = np.array(all_data[1])
    all_data[2] = np.array(all_data[2])
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(4, 4))
    bplot1 = axes.boxplot(
        all_data,
        tick_labels=["Censored", "Normal", "Uped"],
        vert=True,
        patch_artist=True,
    )
    colors = ["pink", "lightblue", "lightgreen"]
    for patch, color in zip(bplot1["boxes"], colors):
        patch.set_facecolor(color)
    plt.show()


def C_timeC(*args): ...
def C_checkU(*args): ...
def C_checkA(*args):
    shouldAt = os.getcwd()
    config = configparser.ConfigParser()
    config.read("C_checkA.ini")
    student = {"version": version, "students": {}}
    now_type = api["logics"][setting["Algorithm"]]["type"]
    try_time = int(config["checkA_%s" % (now_type)]["try_time"])
    C_size = int(config["checkA_%s" % (now_type)]["C_size"])
    N_size = int(config["checkA_%s" % (now_type)]["N_size"])
    U_size = int(config["checkA_%s" % (now_type)]["U_size"])
    for i in range(C_size):
        student["students"][
            "".join(random.sample("abcdefghijklmnopqrstuvwxyz", 10))
        ] = "C"
    for i in range(N_size):
        student["students"][
            "".join(random.sample("abcdefghijklmnopqrstuvwxyz", 10))
        ] = "N"
    for i in range(U_size):
        student["students"][
            "".join(random.sample("abcdefghijklmnopqrstuvwxyz", 10))
        ] = "U"

    updateRoot_ = Toplevel(root)
    updateRoot_.title(getLang("checkingS"))
    updateRoot_.geometry("300x70")
    updateRoot_.attributes("-topmost", 1)
    updateRoot_.resizable(0, 0)
    global ttc_
    ttc_ = ttk.Progressbar(
        updateRoot_,
        orient="horizontal",
        length=250,
        mode="determinate",
        maximum=try_time,
        value=0,
    )
    ttc_.place(x=5, y=5)

    history_check = []
    countingS = {}

    if api["logics"][setting["Algorithm"]]["type"] == "file":
        if os.path.exists(getPath("test")):
            shutil.rmtree(getPath("test"))
        os.mkdir(getPath("test"))
        shouldAt = os.getcwd()
        os.chdir(getPath("test"))
        os.mkdir("temp")
        with open("temp\\test.tmp", "wb"):
            pass
        with open("temp\\student.tmp", "wb") as f:
            pickle.dump(student, f)
        with open("temp\\history.tmp", "wb") as f:
            pickle.dump(tuple(), f)
        for i in range(try_time):
            os.system("..\\%s" % api["logics"][setting["Algorithm"]]["file"])
            with open("temp\\now.tmp", "rb") as f:
                now = pickle.load(f)[0]
            if now in countingS:
                countingS[now] += 1
            else:
                countingS[now] = 1
            history_check.append(
                {"name": now, "type": student["students"][now], "cdraw": False}
            )
            with open("temp\\history.tmp", "wb") as f:
                pickle.dump(tuple(history_check), f)
            ttc_["value"] = i + 1
            updateRoot_.update()
        os.remove("temp\\test.tmp")
    elif api["logics"][setting["Algorithm"]]["type"] == "function":
        api_function = getattr(getNames, api["logics"][setting["Algorithm"]]["index"])
        for i in range(try_time):
            now = api_function(student, history_check, False, True)[0]
            if now in countingS:
                countingS[now] += 1
            else:
                countingS[now] = 1
            history_check.append(
                {"name": now, "type": student["students"][now], "cdraw": False}
            )
            ttc_["value"] = i + 1
            updateRoot_.update()
    elif api["logics"][setting["Algorithm"]]["type"] == "foolsday":
        getattr(getNames, api["logics"][setting["Algorithm"]]["index"])()

    updateRoot_.destroy()
    all_data = [[], [], []]
    for i in countingS:
        if student["students"][i] == "C":
            all_data[0].append(countingS[i])
        if student["students"][i] == "N":
            all_data[1].append(countingS[i])
        if student["students"][i] == "U":
            all_data[2].append(countingS[i])
    # print(all_data)
    showData(all_data)
    # print(countingS)
    os.chdir(shouldAt)


def C_errorC(*args):
    errorRoot = Toplevel(root)
    errorRoot.title(getLang("errorC"))
    errorRoot.attributes("-topmost", 1)
    errorRoot.resizable(0, 0)
    errorRoot.geometry("520x380")

    global sb1
    sb1 = Scrollbar(errorRoot)
    sb1.pack(side=RIGHT, fill=Y)
    global Left_ListBox_01
    Left_ListBox_01 = Listbox(errorRoot, width=80, height=15, yscrollcommand=sb1.set)
    Left_ListBox_01.pack(side=LEFT, fill=BOTH, expand=True)
    sb1.config(command=Left_ListBox_01.yview)

    with open(getPath("error.log"), "r") as f:
        errors = f.readlines()
        if len(errors):
            for item in errors:
                Left_ListBox_01.insert("end", item[:-1])
        else:
            Left_ListBox_01.insert("end", "(empty)")


def counting(*args):
    countingWin = Toplevel(root)
    countingWin.title(getLang("counting"))
    countingWin.attributes("-topmost", 1)
    countingWin.resizable(0, 0)
    countingWin.geometry("420x220")
    ttk.Button(countingWin, text=getLang("timeC"), command=C_timeC).place(x=5, y=15)
    ttk.Button(countingWin, text=getLang("checkU"), command=C_checkU).place(x=5, y=55)
    ttk.Button(countingWin, text=getLang("checkA"), command=C_checkA).place(x=5, y=95)
    ttk.Button(countingWin, text=getLang("errorC"), command=C_errorC).place(x=5, y=135)
    ttk.Label(countingWin, text=getLang("timeCD")).place(x=100, y=20)
    ttk.Label(countingWin, text=getLang("checkUD")).place(x=100, y=60)
    ttk.Label(countingWin, text=getLang("checkAD")).place(x=100, y=100)
    ttk.Label(countingWin, text=getLang("errorCD")).place(x=100, y=140)


def individuation(*args): ...


def Setting(*args):
    global setting
    setup = Toplevel(root)
    setup.title(getLang("setting"))
    setup.attributes("-topmost", 1)
    setup.resizable(0, 0)
    setup.geometry("420x450")
    Label(setup, text=getLang("manageStudents")).place(x=5, y=20)
    ttk.Button(setup, text=getLang("manageStudentsButton")).place(x=100, y=15)
    Label(setup, text=getLang("count")).place(x=5, y=60)
    ttk.Button(setup, text=getLang("countButton"), command=counting).place(x=100, y=55)
    Label(setup, text=getLang("CDraw")).place(x=5, y=100)
    sp = ttk.Spinbox(setup, from_=1, to=15)
    sp.delete(0, "end")
    sp.insert("end", str(setting["CDrawNumber"]))
    sp.config(state="readonly")
    sp.place(x=100, y=95)
    Label(setup, text=getLang("logic")).place(x=5, y=140)
    global logicValue
    logicValue = StringVar()
    logicBox = ttk.Combobox(setup, textvariable=logicValue, state="readonly", width=30)
    logicBox.place(x=100, y=135)
    logicBox["value"] = tuple(logicDList)
    logicBox.set(logics[setting["Algorithm"]]["description"][setting["Language"]])
    Label(setup, text=getLang("update")).place(x=5, y=180)
    ttk.Button(setup, text=getLang("updateCheck"), command=lambda: update(True)).place(
        x=100, y=175
    )
    Label(setup, text=getLang("license")).place(x=5, y=220)
    ttk.Button(setup, text=getLang("licenseButton"), command=about).place(x=100, y=215)
    Label(setup, text=getLang("openSource")).place(x=5, y=260)

    def github(*args):
        os.system("start https://github.com/zhuoyue2023/random-student")

    def gitee(*args):
        os.system("start https://gitee.com/distjr/random-student")

    global tp_github
    tp_github = PhotoImage(file=getPath("github.gif"))
    l_github = Label(setup, image=tp_github, width=30, height=30)
    l_github.place(x=100, y=255)
    l_github.bind("<Button-1>", github)
    global tp_gitee
    tp_gitee = PhotoImage(file=getPath("gitee.gif"))
    l_gitee = Label(setup, image=tp_gitee, width=30, height=30)
    l_gitee.place(x=150, y=255)
    l_gitee.bind("<Button-1>", gitee)
    Label(setup, text=getLang("about")).place(x=5, y=300)

    def blog(*args):
        os.system("start https://ruufly.github.io/")

    global tp_blog
    tp_blog = PhotoImage(file=getPath("favicon.gif"))
    l_blog = Label(setup, image=tp_blog, width=30, height=30)
    l_blog.place(x=150, y=295)
    l_blog.bind("<Button-1>", blog)

    def bilibili(*args):
        os.system("start https://space.bilibili.com/1159124697")

    global tp_bilibili
    tp_bilibili = PhotoImage(file=getPath("bilibili.gif"))
    l_bilibili = Label(setup, image=tp_bilibili, width=30, height=30)
    l_bilibili.place(x=100, y=295)
    l_bilibili.bind("<Button-1>", bilibili)
    Label(setup, text=getLang("individuation")).place(x=5, y=340)
    ttk.Button(setup, text=getLang("individuationButton"), command=individuation).place(
        x=100, y=335
    )
    Label(setup, text=getLang("languageSet")).place(x=5, y=380)
    global langValue
    langValue = StringVar()
    langBox = ttk.Combobox(setup, textvariable=langValue, state="readonly", width=30)
    langBox.place(x=100, y=375)
    langBox["value"] = tuple(langSList)
    langBox.set(langDict[setting["Language"]]["show"])
    ttk.Button(setup, text=getLang("okay")).place(x=310, y=410)


Frame(root, height=10).pack()
butRds = ttk.Button(root, text=getLang("rds"), command=randomName)
butRds.pack()
butRep = ttk.Button(root, text=getLang("repeated"), command=repeatedRandom)
butRep.pack()
butSetting = ttk.Button(root, text=getLang("setting"), command=Setting)
butSetting.pack()

# update(False)

root.mainloop()
=======
from tkinter import *
# from tkinter.ttk import *
from tkinter import messagebox, filedialog, simpledialog, ttk
import pickle
from sys import argv
import os
import random
from urllib import request
import json
import time
import winsound
# from tkinter.ttk import Button
import threading
# import ctypes



styles = {
    "normal": ["#FAFAF0","#50505A"],
    "night": ["#50505A","#FAFAF0"],
    "miku": ["#39C5BB","#50505A"]
}

up = []

if len(argv) != 1:
    f = open(argv[1],'rb')
    ec = pickle.load(f)
    os.chdir(ec[0])
    up = ec[1]
    f.close()
    # c = {}
    # while True:
    #     p = f.readline()
    #     if not p: break
    #     if p == '': continue
    #     c[p] = 0
    # f.close()
    # with open('student.pkl','wb') as ff:
    #     pickle.dump(c,ff)
rm = {}
qer = 0
name = []
namelist = {}
ktime = [0.001,0.005,0.01,0.015,0.02,0.05]
tentime = 10
ccert = 86062



global useold
useold = 0
canrepeat = False

with open("setting.pkl","rb") as f:
    etddd = pickle.load(f)
    tentime = etddd[0]
    useold = etddd[1]
    isfirst = etddd[2]
    allbg = etddd[3]
    allfg = etddd[4]
    styletype = etddd[5]
# try:
#     isfirst = etddd[2]
# except Exception:
#     isfirst = False
#     with open("setting.pkl","wb") as f:
#         pickle.dump([tentime,useold,isfirst],f)

try:
    with open('student.pkl','rb') as f:
        rm = pickle.load(f)
except Exception:
    with open('student.pkl','wb') as f:
        pickle.dump({},f)

if isfirst:
    try:
        with open("_student.pkl","rb") as f:
            kf = pickle.load(f)
        with open("student.pkl","wb") as f:
            pickle.dump(kf,f)
        with open("_setting.pkl","rb") as f:
            kf = pickle.load(f)
        with open("setting.pkl","wb") as f:
            pickle.dump(kf,f)
    except Exception:
        with open("setting.pkl","wb") as f:
            pickle.dump([tentime,useold,0,allbg,allfg,styletype],f)
with open("student.pkl","rb") as f:
    kf = pickle.load(f)
with open("_student.pkl","wb") as f:
    pickle.dump(kf,f)
with open("setting.pkl","rb") as f:
    kf = pickle.load(f)
with open("_setting.pkl","wb") as f:
    pickle.dump(kf,f)

name = [i for i in rm]
namelist = rm
for i in name:
    try:
        namelist[i] = 1000 if ord(i[0]) + ord(i[1]) + ord(i[2]) != ccert else -1
    except IndexError:
        namelist[i] = 1000

class randomInGroup:
    def __init__(self, List, v):
        self.list1 = List
        self.list2 = []
        self.v = v
        self.ll1 = len(List)
        for i in List:
            self.list2.append(self.ll1)
        self.ll2 = self.ll1 * self.ll1
    def myrandom(self, a, b):
        e = random.randint(a, b)
        for i in range(0, random.randint(a, b)):
            e = random.randint(a, b)
        return e
    def getMember(self, i):
        for id1 in range(0, self.ll1):
            if i <= 0:
                return id1 - 1
            else:
                i -= self.list2[id1]
        return id1
    def addMember(self, i):
        # print("L1:%d"%self.ll2)
        self.ll2 += self.v[i]
        self.list2[i] += self.v[i]
    #  print("L2:%d"%self.ll2)
    def zero(self, i):
        #   print("L3:%d"%self.ll2)
        self.ll2 -= self.list2[i]
        self.list2[i] = 0
    #   print("L4:%d"%self.ll2)
    def randomMember(self, times, canRepeat=1):
        r = []
        for cnt in range(0, times):
            if not self.ll2:
                # 报错，取不到了
                return -1
            # print(self.ll2)
            i = self.myrandom(0, self.ll2 - 1)
            x = self.getMember(i)
            #  print("x:%d"%x)
            # print("x:%d"%x)
            r.append(self.list1[x])
            self.zero(x)
            for j in range(0, self.ll1):
                #   print("L5:%dj:%d"%(self.list2[j],j))
                if self.list2[j] or canRepeat:
                    #     print("ok")
                    self.addMember(j)
        if not canRepeat:
            for j in range(0, self.ll1):
                if not self.list2[j]:
                    self.list2[j] = self.v[j]
        return r

keup = []
for i in name:
    try:
        keup.append(10 if ord(i[0]) + ord(i[1]) + ord(i[2]) != ccert else 1)
    except IndexError:
        keup.append(10)
keuup = []
for i in name:
    if (len(i) >= 3):
        if (ord(i[0]) + ord(i[1]) + ord(i[2]) == ccert):
            keuup.append(1)
        elif i in up:
            keuup.append(100)
        else:
            keuup.append(10)
    else:
        keuup.append(100 if i in up else 10)
group = randomInGroup(name, keup)
groupup = randomInGroup(name, keuup)


def getname(ket = True):
    global rm
    global name
    global namelist
    global qer
    qer +=1
    for i in range(random.randint(10,100)):
        q = random.randint(0,len(name)-1)
    if not ket:
        if (len(name[q]) >= 3):
            if ord(name[q][0]) + ord(name[q][1]) + ord(name[q][2]) == ccert:
                if random.randint(0,10) == random.randint(0,10) or qer >= 100:
                    qer = 0
                    return name[q]
                else:
                    return getname(ket)
    if namelist[name[q]] == 1:
        if random.randint(0,10) == random.randint(0,10) or qer >= 100:
            qer = 0
            return name[q]
        else:
            return getname(ket)
    else:
        qer = 0
        namelist[name[q]] = ket
        return name[q]

# def getname(ket = True):
#     global rm
#     global name
#     global namelist
#     # global qer
#     # qer +=1
#     q = random.randint(0,len(name)-1)
#     qer = 0
#     while namelist[name[q]] < 10 and qer < 500:
#         q = random.randint(0,len(name)-1)
#         qer += 1
#     if (namelist[name[q]] == -1):
#         if random.randint(0,10) == random.randint(0,10):
#             return name[q];
#         else:
#             return getname(ket)
#     namelist[name[q]] = 0
#     for i in namelist:
#         if i != q and namelist[i] != -1:
#             namelist[i] += 1
#     return name[q]
#     # for i in range(random.randint(10,100)):
#     #     q = random.randint(0,len(name)-1)
#     # if not ket:
#     #     if (len(name[q]) >= 3):
#     #         if ord(name[q][0]) + ord(name[q][1]) + ord(name[q][2]) == ccert:
#     #             if random.randint(0,10) == random.randint(0,10) or qer >= 100:
#     #                 qer = 0
#     #                 return name[q]
#     #             else:
#     #                 return getname(ket)
#     # if namelist[name[q]] == 1:
#     #     if random.randint(0,10) == random.randint(0,10) or qer >= 100:
#     #         qer = 0
#     #         return name[q]
#     #     else:
#     #         return getname(ket)
#     # else:
#     #     qer = 0
#     #     namelist[name[q]] = ket
#     #     return name[q]

root = Tk(className="random name")
root.geometry('200x200')
root.attributes("-topmost",1)
root.resizable(0,0)

# ctypes.windll.shcore.SetProcessDpiAwareness(1)
# ScaleFactor=ctypes.windll.shcore.GetScaleFactorForDevice(0)
# root.tk.call('tk', 'scaling', ScaleFactor/75)

def ipsl(*args):
    # rroot = Tk(className='import')
    if simpledialog.askstring('输入密码','请输入密码',parent=root) == pickle.load(open('password.pkl','rb')):
        k=filedialog.askopenfilename(filetypes=[('Textfile', '*.txt'), ('All Files', '*')],parent=root)
        if k != '':
            f = open(k,'r',encoding='utf-8')
            c = {}
            while True:
                p = f.readline()
                if not p: break
                if p == '': continue
                c[p] = 0
            f.close()
            with open('student.pkl','wb') as ff:
                pickle.dump(c,ff)
            messagebox.showinfo('随机学生',"导入成功，重启软件以应用新的学生名单")
    # rroot.destroy()

def ipup(*args):
    k=filedialog.askopenfilename(filetypes=[('Textfile', '*.txt'), ('All Files', '*')],parent=root)
    if k != '':
        f = open(k,'r',encoding='utf-8')
        c = []
        while True:
            p = f.readline()
            if not p: break
            if p == '': continue
            c.append(p)
        f.close()
        ke=filedialog.asksaveasfilename(filetypes=[('手动UP配置文件', '*.rdsup'), ('All Files', '*')],parent=root)
        if ke != '':
            with open(ke+'.rdsup','wb') as ff:
                pickle.dump((os.getcwd(),c),ff)
            messagebox.showinfo('随机学生',"配置成功！\n如需应用手动UP，请直接打开手动UP配置文件\n该配置文件只能用于本机！")

def about(*args):
    cpy = '''Random Student v1.5

Copyright 2023-2024 distjr_

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''
    messagebox.showinfo('about',cpy)



label1 = Label(root,text='随机学生',font=('Microsoft YaHei UI',20),fg='gray')
label1.pack()

def gorandom(*args):
    global label1
    # for i in range(6):
    #     label1.config(text='%s' % (name[random.randint(0,len(name)-1)][:-1]),fg='black')
    #     root.update()
    #     time.sleep(ktime[i])
    cn = ""
    if useold == 1:
        cn = getname()
    elif useold == 2:
        cn = groupup.randomMember(1,1)[0]
    else:
        pass
    label1.config(text='%s' % (cn[:-1]),fg='black')
    root.update()
    winsound.Beep(2000,80)

def changepwd(*args):
    os.system('changepwd.exe')


def goup(ket = False):
    global rm
    global name
    global namelist
    global qer
    qer +=1
    for i in range(random.randint(10,100)):
        q = random.randint(0,len(name)-1)
    if (len(name[q]) >= 3):
        if ord(name[q][0]) + ord(name[q][1]) + ord(name[q][2]) == ccert:
            if random.randint(0,10) == random.randint(0,10) or qer >= 100:
                qer = 0
                return name[q]
            else:
                return goup()
    if not (name[q] in up):
        if random.randint(0,10) == random.randint(0,10) or qer >= 100:
            qer = 0
            return name[q]
        else:
            return goup()
    else:
        qer = 0
        return name[q]


# def goup(ket = False):
#     global rm
#     global name
#     global namelist
#     # global qer
#     # qer +=1
#     q = random.randint(0,len(name)-1)
#     qer = 0
#     for i in up:
#         try:
#             if (namelist[i] != 0):
#                 namelist[i] = 1000
#         except Exception:
#             continue
#     for i in namelist:
#         if (not i in up):
#             if (namelist[i] != 0):
#                 namelist[i] = 1
#     while namelist[name[q]] < 10 and qer < 20:
#         q = random.randint(0,len(name)-1)
#         qer += 1
#     if (namelist[name[q]] == -1):
#         if random.randint(0,10) == random.randint(0,10):
#             return name[q];
#         else:
#             return getname(ket)
#     namelist[name[q]] = 0
#     for i in namelist:
#         if i != q and namelist[i] != -1:
#             namelist[i] += 1
#     return name[q]
    # global rm
    # global name
    # global namelist
    # global qer
    # qer +=1
    # for i in range(random.randint(10,100)):
    #     q = random.randint(0,len(name)-1)
    # if (len(name[q]) >= 3):
    #     if ord(name[q][0]) + ord(name[q][1]) + ord(name[q][2]) == ccert:
    #         if random.randint(0,10) == random.randint(0,10) or qer >= 100:
    #             qer = 0
    #             return name[q]
    #         else:
    #             return goup()
    # if not (name[q] in up):
    #     if random.randint(0,10) == random.randint(0,10) or qer >= 100:
    #         qer = 0
    #         return name[q]
    #     else:
    #         return goup()
    # else:
    #     qer = 0
    #     return name[q]

def gorandomup(*args):
    global label1
    print("gorandomup")
    # for i in range(6):
    #     label1.config(text='%s' % (name[random.randint(0,len(name)-1)][:-1]),fg='black')
    #     root.update()
    #     time.sleep(ktime[i])
    cn = ""
    if useold == 1:
        cn = goup()
    elif useold == 2:
        cn = groupup.randomMember(1,1)[0]
    else:
        pass
    label1.config(text='%s' % (cn[:-1]),fg='black')
    root.update()
    winsound.Beep(2000,80)


def tenrandom(*args):
    global tenrandom
    tenrandom = Toplevel(root)
    tenrandom.title("连抽")
    tenrandom.attributes("-topmost",1)
    tenrandom.resizable(0,0)
    tenrandom.geometry("200x%d" % (tentime*40+40))
    if useold == 1:
        nowlst = []
        for i in range(tentime):
            labell = Label(tenrandom,font=('Microsoft YaHei UI',15),fg='black')
            labell.pack()
            kstr = (getname if len(argv) != 1 else goup)(False)
            ei = 0
            while kstr in nowlst and ei < 200:
                kstr = (getname if len(argv) != 1 else goup)(False)
                ei += 1
            root.update()
            for i in range(6):
                labell.config(text='%s' % (name[random.randint(0,len(name)-1)][:-1]))
                root.update()
                time.sleep(ktime[i])
            labell.config(text='%s' % (kstr[:-1]))
            nowlst.append(kstr)
            root.update()
    elif useold == 2:
        llist = (group if len(argv) != 1 else groupup).randomMember(tentime,canrepeat)
        print(llist)
        for sti in llist:
            labell = Label(tenrandom,font=('Microsoft YaHei UI',15),fg='black')
            labell.pack()
            root.update()
            for i in range(6):
                labell.config(text='%s' % (name[random.randint(0,len(name)-1)][:-1]))
                root.update()
                time.sleep(ktime[i])
            labell.config(text='%s' % (sti[:-1]))
            root.update()
    else:
        pass
    winsound.Beep(2000,80)
    but1 = ttk.Button(tenrandom,text="确定",command=lambda: tenrandom.destroy())
    but1.pack()



def getnew(*args):
    try:
        data = json.loads(request.urlopen("https://gitee.com/api/v5/repos/distjr/random-student/releases/latest").read())
    except Exception:
        messagebox.showerror("随机学生","网络错误！")
        return
    if data["name"] == "v1.5":
        messagebox.showinfo("随机学生","没有发现新版本！")
    else:
        if messagebox.askyesno("随机学生","发现新版本：%s\n是否需要安装？" % data["name"]):
            goingon = Toplevel(root)
            goingon.title("下载进度")
            goingon.geometry("300x70")
            goingon.attributes("-topmost",1)
            goingon.resizable(0,0)
            global ttc
            ttc = ttk.Progressbar(goingon, orient='horizontal', length=250, mode='determinate')
            ttc.place(x=5,y=5)
            global utc
            utc = Label(goingon)
            utc.place(x=85,y=40)
            # Button(goingon,text="取消",command=canceldown)
            def Schedule(a,b,c):
                global ttc
                global utc
                per = 100.0 * a * b / c
                if per > 100:
                    per == 100
                ttc['value'] = per
                utc.config(text="%.3f/%.3f(MB)，进度：%.2f%%" % ((a*b)/(1024*1024),c/(1024*1024),per))
                goingon.update()
                # print("%.2f%%" % per)
            request.urlretrieve(data["assets"][0]["browser_download_url"], "update.exe", Schedule)
            goingon.destroy()
            threading.Thread(target=os.system,args=("update.exe",)).start()
            # messagebox.showinfo("随机学生","更新完成！")


def setting(*args):
    global setup
    global allbg
    global allfg
    global styletype
    global tentime
    global useold
    global isfirst
    setup = Toplevel(root)
    setup.title("设置")
    setup.attributes("-topmost",1)
    setup.resizable(0,0)
    # setup.configure(bg="white")
    setup.geometry("420x450")
    logic = [("旧版逻辑 by ruufly! & distjr_",1),("新版逻辑A by hz （尚未debug好，暂时不推荐使用）",2)]#,("新版逻辑B by dyt_dirt",3)]
    global vnlog
    vnlog = IntVar()
    vnlog.set(useold)
    global gogogo
    def gogogo(*args):
        global tentime
        global useold
        tentime = int(sp.get())
        with open("setting.pkl","wb") as f:
            pickle.dump([tentime,vnlog.get(),isfirst,allbg,allfg,styletype],f)
        # print(type(tentime))
        useold = vnlog.get()
        setup.destroy()
    Label(setup,text="导入学生名单").place(x=5,y=20)
    ttk.Button(setup,text="点击此处导入",command=ipsl).place(x=100,y=15)
    Label(setup,text="新建手动UP").place(x=5,y=60)
    ttk.Button(setup,text="点击此处新建手动UP",command=ipup).place(x=100,y=55)
    ttk.Button(setup,text="点击此处检测新版本",command=getnew).place(x=100,y=195)
    Label(setup,text="版本更新").place(x=5,y=200)
    Label(setup,text="软件许可证").place(x=5,y=240)
    ttk.Button(setup,text="点击此处查看许可证",command=about).place(x=100,y=235)
    Label(setup,text="开放源代码").place(x=5,y=280)
    def github(*args):
        os.system("start https://github.com/zhuoyue2023/random-student")
    def gitee(*args):
        os.system("start https://gitee.com/distjr/random-student")
    global tpgithub
    tpgithub = PhotoImage(file="github.gif")
    lgithub = Label(setup,image=tpgithub,width=30,height=30)
    lgithub.place(x=100,y=275)
    lgithub.bind("<Button-1>",github)
    global tpgitee
    tpgitee = PhotoImage(file="gitee.gif")
    lgitee = Label(setup,image=tpgitee,width=30,height=30)
    lgitee.place(x=150,y=275)
    lgitee.bind("<Button-1>",gitee)
    Label(setup,text="关于作者").place(x=5,y=320)
    def blog(*args):
        os.system("start https://distjr.gitee.io/")
    def develop(*args):
        os.system("developer")
    global tpblog
    tpblog = PhotoImage(file="favicon.gif")
    lblog = Label(setup,image=tpblog,width=30,height=30)
    ### lblog.place(x=100,y=315)
    lblog.bind("<Button-1>",blog)
    def bblog(*args):
        os.system("start https://space.bilibili.com/1159124697")
    global tpbblog
    tpbblog = PhotoImage(file="bilibili.gif")
    lbvlog = Label(setup,image=tpbblog,width=30,height=30)
    lbvlog.place(x=100,y=315)
    lbvlog.bind("<Button-1>",bblog)
    # Button(setup,text="distjr_\'s blog",command=lambda:os.system("start https://distjr.gitee.io/")).place(x=100,y=215)
    # Button(setup,text="distjr_\'s bilibili",command=lambda:os.system("start https://space.bilibili.com/1159124697")).place(x=200,y=215)
    Label(setup,text="设置连抽次数").place(x=5,y=100)
    sp = Spinbox(setup,from_=1,to=15)
    sp.delete(0,"end")
    sp.insert("end",str(tentime))
    sp.config(state="readonly")
    sp.place(x=100,y=95)
    Label(setup,text="随机逻辑").place(x=5,y=140)
    dezy = 135
    for i in logic:
        Radiobutton(setup,text=i[0],variable=vnlog,value=i[1]).place(x=100,y=dezy)
        dezy += 25
    def dostyle(*args):
        global allbg
        global allfg
        global styletype
        global tentime
        global useold
        global isfirst
        egoingon = Toplevel(root)
        egoingon.title("个性化设置")
        egoingon.geometry("300x120")
        egoingon.attributes("-topmost",1)
        egoingon.resizable(0,0)
        def doneall(types):
            global allbg
            global allfg
            global styletype
            global tentime
            global useold
            global isfirst
            styletype = types
            allbg = styles[types][0]
            allfg = styles[types][1]
            with open("setting.pkl","wb") as f:
                pickle.dump([tentime,useold,isfirst,allbg,allfg,styletype],f)
            messagebox.showinfo("随机学生","设置成功！重启软件以完成设置！")
            egoingon.destroy()
        global sty1p
        sty1p = PhotoImage(file="style\\normal.gif")
        Label(egoingon,image=sty1p,width=80,height=50).place(x=15,y=10)
        global sty2p
        sty2p = PhotoImage(file="style\\night.gif")
        Label(egoingon,image=sty2p,width=80,height=50).place(x=105,y=10)
        global sty3p
        sty3p = PhotoImage(file="style\\miku.gif")
        Label(egoingon,image=sty3p,width=80,height=50).place(x=195,y=10)
        ttk.Button(egoingon,text="Normal",command=lambda: doneall("normal")).place(x=15,y=70)
        ttk.Button(egoingon,text="Night",command=lambda: doneall("night")).place(x=105,y=70)
        ttk.Button(egoingon,text="Miku",command=lambda: doneall("miku")).place(x=195,y=70)
    Label(setup,text="个性化").place(x=5,y=360)
    global ovtpbblog
    # ovtpbblog = PhotoImage(file="style\\%s.gif" % (styletype))
    tlbvlog = Label(setup,text="当前主题：%s" % (styletype))# image=ovtpbblog,width=80,height=50,text="Now: %s" % (styletype))
    tlbvlog.place(x=100,y=360)
    # tlbvlog.bind("<Button-1>",bblog)
    zqb = ttk.Button(setup,text="个性化设置",command=dostyle)
    zqb.place(x=250,y=355)
    # Label(setup,text="开发人员工具").place(x=5,y=340)
    # Button(setup,text="点击此处打开开发人员工具",command=develop).place(x=100,y=335)
    ttk.Button(setup,text="确定",command=gogogo).place(x=310,y=410)

button1 = Button(root,text="随机学生",command=gorandomup if len(argv) != 1 else gorandom)
button1.pack()
button3 = Button(root,text="连抽",command=tenrandom)
button3.pack()
button3 = Button(root,text="设置",command=setting)
button3.pack()
Label(root,text="\n\n          Copyright 2024 distjr_.\n                All rights reserved.").pack()
# button4 = Button(root,text="修改密码",command=changepwd)
# button4.pack()


# style = ttk.Style()
# style.configure("randomstudent.style",background=allbg)

root.configure(background=allbg)

for i in root.winfo_children():
    if type(i) == Button:
        i.configure(relief="groove")
    try:
        i.configure(bg=allbg,fg=allfg)
    except Exception:
        pass

root.mainloop()
>>>>>>> 5202344e0742f845b1b8a235f6a0654b3b382689
