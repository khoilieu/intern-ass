API Key Management Service

1. Cài đặt
  1.1 Clone dự án về:
      git clone https://github.com/khoilieu/intern-ass.git
      cd intern-ass 


  1.2 Cài đặt các thư viện yêu cầu:
      source venv/bin/activate   # Trên Linux/Mac
      .\venv\Scripts\activate    # Trên Windows


  1.3 Cài đặt và chạy MongoDB (Nếu sử dụng Docker):
    Nếu bạn chưa có MongoDB, hãy sử dụng Docker để khởi động MongoDB container.
    - Đảm bảo Docker đã được cài và chạy trên máy của bạn.
    - Chạy MongoDB container:
      Trong thư mục chứa file `docker-compose.yml`, chạy lệnh:
        docker-compose up
      Điều này sẽ khởi động MongoDB và kết nối với ứng dụng Flask.


  1.4. Chạy ứng dụng Flask:
    Sau khi MongoDB đã chạy, bạn có thể khởi động ứng dụng Flask bằng lệnh:
      docker-compose up
    Hoặc nếu bạn không sử dụng Docker, chạy Flask trực tiếp:
      python app/main.py
    Flask sẽ chạy trên cổng `5000` (http://127.0.0.1:5000/).

2 Các API cần test bằng Postman
  2.1. Tạo API key
      - URL: `http://127.0.0.1:5000/apikeys/generate`
      - Method: `POST`
      - Body (JSON):
          {
            "role": "developer",
            "environment": "production"
          }
      - Kiểm tra: Sau khi tạo API key, thử gửi một yêu cầu POST đến `/webhook/trigger` với header `x-api-key` là API key vừa tạo.


  2.2 Kiểm tra Compliance role không thể POST webhook:
      - URL: `http://127.0.0.1:5000/webhook/trigger`
      - Method: `POST`
      - Body (JSON):
          {
            "event": "plan_update",
            "payload": {
              "plan_id": "ABC123",
              "status": "active"
            }
          }
      - Header: `x-api-key` là API key của role `compliance`.
      - Kiểm tra: Bạn sẽ nhận được thông báo 403 Forbidden nếu dùng API key của role `compliance` để POST webhook.


  2.3. Kiểm tra Logs được lưu với metadata chính xác và có thể truy xuất:
      - URL: `http://127.0.0.1:5000/logs`
      - Method: `GET`
      - Kiểm tra xem các logs đã được lưu vào MongoDB với metadata chính xác (status, timestamp, api_key_used) và có thể truy xuất qua endpoint này.
