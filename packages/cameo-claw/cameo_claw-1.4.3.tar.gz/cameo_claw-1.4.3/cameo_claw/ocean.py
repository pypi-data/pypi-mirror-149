from time import strftime
import msgpack
from starlette.requests import Request
from cameo_claw import mkdir
from cameo_claw.cameo_claw_reuse import fastapi_app
from fastapi.staticfiles import StaticFiles
import json

app = fastapi_app()

# .msgpack path and filename like:
# http://localhost:8000/data/log_msg/2022-04-30/2022-04-30_11_09.msgpack
mkdir('data')
app.mount("/data", StaticFiles(directory="data"))


# 2022-05-01 bowen, one json iot request size 757 bytes
# rust actix 37.3k r/s, 34.77 MB/s
# python fastapi 12.4k r/s, 11.71 MB/s
# actix 3x faster than fastapi
@app.post("/api/log_msgpack/")
async def log_msgpack(request: Request):
    directory = f'data/log_msgpack/{strftime("%Y-%m-%d")}/'
    mkdir(directory)
    with open(f'{directory}{strftime("%Y-%m-%d_%H_%M")}.msgpack', 'ab') as f:
        f.write(msgpack.packb(
            {'headers': request.headers.items(),
             'body': json.loads(await request.body())}))
