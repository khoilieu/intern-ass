# Sử dụng image chính thức của Python làm nền tảng
FROM python:3.9-slim

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Sao chép các file của dự án vào container
COPY . /app

# Cài đặt các thư viện cần thiết
RUN pip install --no-cache-dir -r requirements.txt

# Cài đặt gunicorn nếu bạn muốn sử dụng cho production
RUN pip install gunicorn

# Mở cổng 5000 cho Flask (cổng mặc định của Flask)
EXPOSE 5000

# Chạy ứng dụng Flask khi container khởi động
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app.main:app"]

# Thiết lập các biến môi trường Flask
ENV FLASK_APP=app
ENV FLASK_ENV=development
