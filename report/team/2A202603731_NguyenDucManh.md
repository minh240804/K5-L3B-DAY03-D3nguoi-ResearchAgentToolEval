# Báo cáo cá nhân — Thành viên 3

## 1. Thông tin thành viên

- Họ tên: Nguyễn Đức Mạnh
- MSSV: 2A202603731
- Email: manhgu3110@gmail.com

## 2. Phần việc phụ trách

- Chạy và phân tích các phiên bản đầu v0–v1 để xác định và phân tích lỗi trong các trường hợp sai tool, arguments. 
- Cải tiến system prompt ở giai đoạn đầu dựa trên các lỗi quan sát được từ baseline.
- Xây dựng bộ eval riêng của nhóm gồm 10 case và chuẩn hóa dữ liệu theo schema của eval runner.

## 3. Đóng góp cụ thể

- Tham gia chạy baseline v0 bằng Gemini và đọc kết quả từng case để nhận diện các lỗi như tự đoán thông tin còn thiếu, tự tạo URL, chọn thiếu tool, truyền query chưa đúng và thực hiện hành động có side effect khi chưa xác nhận.
- Cập nhật `system_prompt.md` ở commit `c63c739`, thay hành vi “luôn đoán và gọi tool ngay” bằng các nguyên tắc an toàn hơn: xác định ý định trước khi chọn tool, chỉ giả định khi thông tin thiếu không quan trọng, không bịa URL/nguồn/tác giả/kết quả, hỏi lại khi thiếu dữ liệu thiết yếu và phân biệt dữ kiện đã xác minh với giả định.
- Bổ sung hướng dẫn routing ban đầu: dùng `social_search` cho nội dung mạng xã hội, `lookup` để khám phá thông tin, `fetch` cho URL cụ thể; cho phép dùng nhiều tool khi yêu cầu có nhiều bước và bắt buộc arguments tuân thủ schema.
- Xây dựng `eval_group.json` gồm 10 case: 5 single-turn và 5 multi-turn. Các case kiểm tra hành vi hỏi lại khi thiếu tài khoản hoặc URL, xác nhận trước khi gửi, truyền arguments cho lookup, xử lý yêu cầu ngoài phạm vi, sửa tài khoản/số lượng qua nhiều lượt, giữ timeframe, gọi nhiều tool và chỉ format dữ liệu có sẵn mà không tự tìm kiếm thêm.
- Chuẩn hóa cấu trúc case theo eval runner: mỗi case có ID, phase/suite, metadata mô tả mục tiêu và failure type; expected tool calls dùng `name`/`args`; hội thoại nhiều lượt dùng `role`/`content`.
- Đối chiếu v0 và v1 để đánh giá hướng cải tiến. V0 chỉ đo được 15/20 case do 5 provider errors; v1 đo được 16/20 case do 4 provider errors. Các metric của hai run chỉ có giá trị chẩn đoán và không được dùng làm bằng chứng so sánh chính thức.

## 4. Bằng chứng

- Cải tiến system prompt giai đoạn đầu — commit `c63c739`: [system_prompt.md](../../starter_v0/artifacts/system_prompt.md).
- Xây dựng và chuẩn hóa eval nhóm — các commit `6afde18`, `001d3ef`, `add1147`: [eval_group.json](../../starter_v0/data/eval_group.json).
- Baseline v0: [v0_B_base_gemini_20261110T172652632360.json](../../starter_v0/runs/v0_B_base_gemini_20261110T172652632360.json).
- Run v1: [v1_B_base_gemini_20261110T190509281921.json](../../starter_v0/runs/v1_B_base_gemini_20261110T190509281921.json).
- Lịch sử phiên bản và đánh giá tính hợp lệ của run: [version_log.csv](../../starter_v0/artifacts/version_log.csv).
- AI/công cụ và cách tự kiểm tra: dùng kết quả trong run JSON để đối chiếu tool call, arguments, failure type và provider error; dùng schema của `eval_base.json` và eval runner để kiểm tra cấu trúc case; dùng Git history để xác định chính xác phạm vi thay đổi. Không dùng metric của run thiếu case làm kết luận chính thức.

## 5. Tự đánh giá

Tôi đã đóng góp vào giai đoạn nền tảng của quá trình cải tiến agent: chuyển system prompt từ cách xử lý thiên về phỏng đoán sang cách chọn tool có kiểm soát hơn, đồng thời xây dựng bộ eval nhóm để kiểm tra cả single-turn và multi-turn. Kết quả chẩn đoán v0–v1 cho thấy số case đạt và routing có xu hướng cải thiện, nhưng cả hai run đều gặp provider errors nên chưa đủ điều kiện so sánh chính thức. Ngoài ra, `eval_group.json` hiện còn các conflict marker từ quá trình merge và cần được xử lý, sau đó validate JSON và chạy lại toàn bộ 10 case trước khi coi bộ eval là bằng chứng hoàn chỉnh. Nếu tiếp tục, tôi sẽ ưu tiên giải quyết xung đột này, chạy validation theo schema và tạo một run không có provider error trên cùng provider/model để đánh giá tác động đáng tin cậy hơn.
