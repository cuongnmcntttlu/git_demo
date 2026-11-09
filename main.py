from datetime import datetime
from typing import List

from fastapi import FastAPI, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

app = FastAPI(
    title="FastAPI Demo (GET & POST)",
    description="Ứng dụng web FastAPI hỗ trợ phương thức GET & POST với giao diện HTML/CSS"
)

# Phục vụ thư mục static (CSS, JS, hình ảnh)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Cấu hình template engine Jinja2
templates = Jinja2Templates(directory="templates")

# Bộ nhớ tạm lưu trữ danh sách tin nhắn
messages_db = [
    {
        "id": 1,
        "sender": "Admin",
        "content": "Chào mừng bạn đến với ứng dụng FastAPI! Hãy thử gửi lời nhắn qua form bên trên nhé.",
        "created_at": datetime.now().strftime("%H:%M:%S %d/%m/%Y")
    }
]


# Pydantic Model cho API POST
class MessageCreate(BaseModel):
    sender: str = Field(..., min_length=1, max_length=50, description="Tên người gửi")
    content: str = Field(..., min_length=1, max_length=500, description="Nội dung lời nhắn")


# ==========================================
# 1. GIAO DIỆN WEB (HTML / Form)
# ==========================================

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Endpoint GET: Render trang chủ HTML với danh sách tin nhắn."""
    context = {
        "request": request,
        "title": "Trang Web FastAPI (GET & POST)",
        "subtitle": "Giao diện HTML & CSS kết hợp phương thức GET và POST",
        "description": "Ứng dụng minh họa cách xử lý request GET (lấy dữ liệu & render giao diện) và POST (nhận dữ liệu từ form HTML hoặc JSON API).",
        "messages": list(reversed(messages_db)),
        "features": [
            {
                "name": "Phương thức GET",
                "description": "Truy xuất danh sách tin nhắn và tải trang giao diện người dùng."
            },
            {
                "name": "Phương thức POST (HTML Form)",
                "description": "Nhận dữ liệu từ form người dùng gửi lên và tự động chuyển hướng làm mới trang."
            },
            {
                "name": "Phương thức POST (JSON API)",
                "description": "Cung cấp endpoint POST /api/messages cho client hoặc ứng dụng bên ngoài."
            },
            {
                "name": "Tài liệu tự động",
                "description": "Kiểm thử trực tiếp các API GET/POST tại đường dẫn /docs."
            }
        ]
    }
    return templates.TemplateResponse(request=request, name="index.html", context=context)


@app.post("/messages")
async def create_message_from_form(
    sender: str = Form(...),
    content: str = Form(...)
):
    """Endpoint POST: Nhận dữ liệu từ form HTML và thêm tin nhắn mới."""
    new_message = {
        "id": len(messages_db) + 1,
        "sender": sender.strip(),
        "content": content.strip(),
        "created_at": datetime.now().strftime("%H:%M:%S %d/%m/%Y")
    }
    messages_db.append(new_message)
    # Chuyển hướng về trang chủ sau khi POST thành công (HTTP 303 See Other)
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


# ==========================================
# 2. JSON API ENDPOINTS
# ==========================================

@app.get("/api/info")
async def get_info():
    """Endpoint GET: Trả về thông tin hệ thống dạng JSON."""
    return {
        "status": "success",
        "message": "FastAPI đang chạy với đầy đủ phương thức GET và POST.",
        "total_messages": len(messages_db),
        "version": "1.1.0"
    }


@app.get("/api/messages")
async def list_messages():
    """Endpoint GET: Lấy danh sách toàn bộ tin nhắn dưới dạng JSON."""
    return {
        "status": "success",
        "data": messages_db
    }


@app.post("/api/messages", status_code=status.HTTP_201_CREATED)
async def create_message_api(message: MessageCreate):
    """Endpoint POST: Nhận payload JSON để tạo tin nhắn mới."""
    new_message = {
        "id": len(messages_db) + 1,
        "sender": message.sender.strip(),
        "content": message.content.strip(),
        "created_at": datetime.now().strftime("%H:%M:%S %d/%m/%Y")
    }
    messages_db.append(new_message)
    return {
        "status": "success",
        "message": "Đã thêm lời nhắn thành công!",
        "data": new_message
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
