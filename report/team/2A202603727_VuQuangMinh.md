# Báo cáo cá nhân — Vũ Quang Minh

## 1. Thông tin thành viên

- Họ tên: Vũ Quang Minh
- MSSV: 2A202603727
- Email: vuquangminh240804@gmail.com

## 2. Phần việc phụ trách

- Xây dựng giao diện chat cho Research Agent bằng Streamlit.
- Xây dựng và tích hợp tool mới `text_cleaner`, đồng thời bổ sung kiểm thử cho tool.
- Hỗ trợ cấu hình provider và chạy, lưu kết quả evaluation cho các phiên bản của agent.

## 3. Đóng góp cụ thể

- Xây dựng giao diện Streamlit cho phép người dùng chọn provider, model và phiên bản artifact; nhập yêu cầu qua giao diện chat nhiều lượt; theo dõi arguments và kết quả của từng tool call; bắt lỗi provider; quản lý trạng thái chờ người dùng; và tự động lưu transcript sau mỗi lượt.
- Bổ sung dependency `streamlit` và giữ API key ở biến môi trường, không hiển thị thông tin nhạy cảm trên giao diện.
- Thiết kế và hiện thực tool `text_cleaner` để chuyển nội dung HTML/Markdown do người dùng cung cấp thành văn bản thuần. Tool loại bỏ `script`/`style`, thẻ HTML và một số Markdown phổ biến, giải mã HTML entities, đồng thời chuẩn hóa khoảng trắng; tool không tải URL và không tạo side effect bên ngoài.
- Đăng ký `text_cleaner` trong danh sách tool và `tools.yaml`, viết tài liệu sử dụng, đồng thời bổ sung các case liên quan vào dữ liệu eval nhóm.
- Viết kiểm thử cho ba nhóm hành vi của `text_cleaner`: chuyển đổi HTML/Markdown đúng ở happy path; từ chối dữ liệu rỗng hoặc sai kiểu; và xử lý HTML chưa đóng mà không phát sinh exception.
- Ghi nhận transcript chạy thử trực tiếp với `text_cleaner`, qua đó kiểm tra tool được agent gọi và kết quả làm sạch được trả về cho người dùng.
- Hỗ trợ cấu hình OpenAI-compatible provider và lưu các run eval. Hai run v2–v3 hợp lệ đều đo đủ 20/20 case, không có provider error; v3 đạt 19/20 case, tương ứng case accuracy 0.95 và tool-routing accuracy 1.00.

## 4. Bằng chứng

- UI Streamlit — commit `63df906`: [app.py](../../starter_v0/app.py), [requirements.txt](../../starter_v0/requirements.txt).
- Tool mới và kiểm thử — commit `a2c5251`: [tool.py](../../starter_v0/tools/text_cleaner/tool.py), [TOOL.md](../../starter_v0/tools/text_cleaner/TOOL.md), [tools/__init__.py](../../starter_v0/tools/__init__.py), [tools.yaml](../../starter_v0/artifacts/tools.yaml), [test_tools_todo.py](../../starter_v0/tests/test_tools_todo.py).
- Transcript chạy thử tool: [v0_gemini_20261110T190911198094.transcript.json](../../starter_v0/transcripts/v0_gemini_20261110T190911198094.transcript.json).
- Cấu hình provider — commit `e29bf52`: [openai_provider.py](../../starter_v0/providers/openai_provider.py), [.env.example](../../starter_v0/.env.example).
- Kết quả eval: [run v2](../../starter_v0/runs/v2_B_base_openai_20261110T194931562980.json), [run v3](../../starter_v0/runs/v3_B_base_openai_20261110T200349662898.json).
- AI/công cụ và cách tự kiểm tra: dùng Git và lịch sử commit để đối chiếu phạm vi thay đổi; dùng transcript để xác nhận luồng chat/tool thực tế; dùng `pytest` cho các hành vi chính của `text_cleaner`; và dùng run JSON để kiểm tra số case đo được, provider errors cùng các metric thay vì chỉ đánh giá thủ công.

## 5. Tự đánh giá

Tôi đã hoàn thành các phần việc chính về giao diện, tool mới và hỗ trợ evaluation. Giao diện đáp ứng được luồng chat nhiều lượt, hiển thị hoạt động của tool và lưu bằng chứng dưới dạng transcript. Tool `text_cleaner` có phạm vi rõ ràng, không tạo side effect và đã có kiểm thử cho đầu vào hợp lệ, đầu vào không hợp lệ cũng như HTML không hoàn chỉnh. Kết quả v3 cho thấy agent đạt 19/20 case, nhưng vẫn còn một case `wrong_boundary`; ngoài ra bộ test chung vẫn còn các test TODO của những tool có sẵn. Nếu tiếp tục, tôi sẽ hoàn thiện toàn bộ test còn thiếu, bổ sung kiểm thử UI/provider và chạy thêm live transcript cho các phiên bản v1–v3 để bằng chứng đầy đủ hơn.
