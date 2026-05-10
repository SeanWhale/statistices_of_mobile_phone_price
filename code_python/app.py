# code_python/app.py
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from .network import NetRequester
from .spider import DataParser
from . import config

app = FastAPI(title="ZOL API")

# 解决跨域问题（让网页能调通接口）
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"])

@app.get("/api/crawl")
def crawl_data(url: str = Query(..., description="ZOL手机列表页网址")):
    req = NetRequester(config.HEADERS)
    p = DataParser(config.EXTRACTION_SCHEMA)
    
    html = req.fetch(url)
    if not html:
        return {"status": "error", "message": "获取网页失败"}
    
    items = p.parse(html)
    return {"status": "success", "total": len(items), "data": items}