API Key Management Service

## Cài đặt

    ### 1. Clone dự án về:
    Đầu tiên, clone dự án từ GitHub về máy của bạn:
    ```bash
    git clone https://github.com/your-username/api-key-management.git
    cd api-key-management
    ```


    ### 2. Cài đặt các thư viện yêu cầu:
    Tạo môi trường ảo (virtual environment) và kích hoạt nó:
    ```bash
    python -m venv venv
    source venv/bin/activate   # Trên Linux/Mac
    .\venv\Scripts\activate    # Trên Windows
    ```

    Cài đặt các thư viện yêu cầu từ `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```


    ### 3. Cài đặt và chạy MongoDB (Nếu sử dụng Docker):
    Nếu bạn chưa có MongoDB, hãy sử dụng Docker để khởi động MongoDB container.

    - **Đảm bảo Docker đã được cài và chạy trên máy của bạn**.
    - Nếu chưa có MongoDB image, chạy lệnh sau để tải xuống:
      ```bash
      docker pull mongo
      ```

    - **Chạy MongoDB container**:
      Trong thư mục chứa file `docker-compose.yml`, chạy lệnh:
      ```bash
      docker-compose up
      ```
      Điều này sẽ khởi động MongoDB và kết nối với ứng dụng Flask.


    ### 4. Chạy ứng dụng Flask:
    Sau khi MongoDB đã chạy, bạn có thể khởi động ứng dụng Flask bằng lệnh:
    ```bash
    docker-compose up
    ```
    Hoặc nếu bạn không sử dụng Docker, chạy Flask trực tiếp:
    ```bash
    python app/main.py
    ```
    Flask sẽ chạy trên cổng `5000` (http://127.0.0.1:5000/).

## Các API cần test bằng Postman

    ### 1. Tạo API key cho Developer (Chỉ hoạt động với `/webhook/trigger`):
      - **URL**: `http://127.0.0.1:5000/apikeys/generate`
      - **Method**: `POST`
      - **Body (JSON)**:
        ```json
        {
          "role": "developer",
          "environment": "production"
        }
        ```
      - **Kiểm tra**: Sau khi tạo API key, thử gửi một yêu cầu **POST** đến `/webhook/trigger` với header `x-api-key` là API key vừa tạo.


    ### 2. Kiểm tra Compliance role không thể POST webhook:
      - **URL**: `http://127.0.0.1:5000/webhook/trigger`
      - **Method**: `POST`
      - **Body (JSON)**:
        ```json
        {
          "event": "plan_update",
          "payload": {
            "plan_id": "ABC123",
            "status": "active"
          }
        }
        ```
      - **Header**: `x-api-key` là API key của role `compliance`.
      - **Kiểm tra**: Bạn sẽ nhận được thông báo **403 Forbidden** nếu dùng API key của role `compliance` để POST webhook.


    ### 3. Kiểm tra Logs được lưu với metadata chính xác và có thể truy xuất:
      - **URL**: `http://127.0.0.1:5000/logs`
      - **Method**: `GET`
      - Kiểm tra xem các logs đã được lưu vào MongoDB với metadata chính xác (status, timestamp, api_key_used) và có thể truy xuất qua endpoint này.

## Cấu trúc thư mục

```
.
├── app/
│   ├── __init__.py
│   ├── apikeys.py
│   ├── auth.py
│   ├── config.py
│   ├── db.py
│   ├── logs.py
│   ├── main.py
│   └── webhook.py
├── requirements.txt
├── docker-compose.yml
└── README.md
```

## Các bước kiểm tra

    ### 1. Tạo API Key cho Developer:
      - Chạy `POST` request đến `/apikeys/generate` để tạo API key cho role `developer`.
      - Kiểm tra rằng API key được tạo thành công và chỉ hoạt động trên các endpoint `/webhook/trigger`.

    ### 2. Kiểm tra Compliance role không thể POST webhook:
      - Thử sử dụng API key của role `compliance` để gửi **POST** request đến `/webhook/trigger` và chắc chắn rằng sẽ nhận được lỗi **403 Forbidden**.

    ### 3. Kiểm tra Logs được lưu chính xác:
      - Gửi một số yêu cầu API (cả thành công và thất bại).
      - Truy vấn logs qua endpoint `/logs` và kiểm tra xem các thông tin như **status**, **timestamp**, **api_key_used** có được lưu đúng trong MongoDB.
