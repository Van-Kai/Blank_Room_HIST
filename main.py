import json
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import room_data
with open('./data/lf_code.json', 'r', encoding="utf-8") as file:
    buildings = json.load(file) # 读取所有楼的资源 获取教学楼的code
with open('./data/codebylou.json', 'r', encoding="utf-8") as file:
    codebylou = json.load(file) #读取响应编号对应楼的json文件名 以便于获取教学楼的教室
app = FastAPI()
# 设置静态资源目录
app.mount("/data", StaticFiles(directory="data"), name="data")
# 设置Jinja2模板目录
templates = Jinja2Templates(directory="./")
@app.get("/")
async def read_root(request: Request,lf,zc,z):
    """
    :param request:
    :param lf: eg:弘毅楼
    :param zc: eg:5 代表第五周
    :param z: eg: 5 代表周五
    :return: 返回第五周周五的html
    """
    def find_code_by_name(buildings, name):
        for building in buildings:
            if building['name'] == name:
                return building['code']
        return None
    def find_lou_by_code(codebylou, code):
        for lou in codebylou:
            if lou['code'] == code:
                return lou['name']
        return None
    try:
        code = find_code_by_name(buildings,lf)
    except Exception as e:
        return str(e) + "find_code_by_name函数错误"
    try:
        name = find_lou_by_code(codebylou,code)
    except Exception as e:
        return str(e) + "find_lou_by_code函数错误"

    roomdatas = room_data.main(zc, z, code)
    if roomdatas:
        with open(f'./data/{name}', 'r', encoding="utf-8") as file:
            louname = json.load(file)
        # 定义教室和课程信息
        classrooms = louname
        class_schedule = roomdatas[0]
        return templates.TemplateResponse("空教室.html", {"request": request, "classrooms": classrooms, "class_schedule": class_schedule,"campus": roomdatas[1],"building": roomdatas[2],"week_and_day": roomdatas[3]})
    else:
        return 'COOKIES失效'
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)