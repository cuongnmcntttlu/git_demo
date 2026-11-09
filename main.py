from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(
    title="FastAPI Basic Demo",
    description="Ứng dụng web FastAPI cơ bản chỉ sử dụng phương thức GET với giao diện HTML/CSS"
)

# Phục vụ thư mục static (CSS, JS, hình ảnh)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Cấu hình template engine Jinja2
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Endpoint GET trả về giao diện HTML."""
    context = {
        "request": request,
        "title": "Trang Web FastAPI Cơ Bản",
        "subtitle": "Giao diện HTML & CSS kết hợp phương thức GET",
        "description": "Đây là ứng dụng web mẫu xây dựng bằng FastAPI, chỉ sử dụng các endpoint GET để hiển thị giao diện và trả dữ liệu.",
        "features": [
            {
                "name": "FastAPI Backend",
                "description": "Xử lý request nhanh chóng, hỗ trợ asynchronous và chuẩn OpenAPI."
            },
            {
                "name": "Jinja2 Templates",
                "description": "Render giao diện HTML linh hoạt trực tiếp từ server."
            },
            {
                "name": "Custom CSS",
                "description": "Giao diện được tùy biến với file tĩnh CSS riêng biệt."
            },
            {
                "name": "Tài liệu API tự động",
                "description": "Tự động sinh tài liệu tương tác tại đường dẫn /docs."
            }
        ]
    }
    return templates.TemplateResponse(request=request, name="index.html", context=context)


@app.get("/api/info")
async def get_info():
    """Endpoint GET trả về dữ liệu định dạng JSON."""
    return {
        "status": "success",
        "message": "Xin chào! Đây là dữ liệu trả về từ endpoint GET của FastAPI.",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
