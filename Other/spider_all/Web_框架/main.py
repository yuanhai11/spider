from sanic import Sanic
from sanic.response import json
from sanic.response import HTTPResponse
app = Sanic("My Hello, world app")

@app.post('/')
async def test(request):
    response = await request.respond()
    await response.send("foo", False)
    await response.send("bar", False)
    await response.send("", True)
    print(response)
    print(response.text)
    return response

import requests
def demo():
    purl = 'http://127.0.0.1:8000/'
    data = {
        "exceptionCause": "个税未知错误",
        "fileName": "个税(工资薪金所得)",
        "taxDeclarationId": 1,
        "taxName": "个税(工资薪金所得)"
    }
    data = json.dumps(data)
    aaa = requests.post(url=purl, data=data).text
    return aaa



if __name__ == '__main__':
    app.run()
    # pass