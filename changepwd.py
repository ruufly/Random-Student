import pickle
if input('请输入原密码：') == pickle.load(open('password.pkl','rb')):
    with open('password.pkl','wb') as f:
        pickle.dump(input('请输入新密码：'),f)
