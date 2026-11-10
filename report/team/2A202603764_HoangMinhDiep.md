# Báo cáo cá nhân — Hoàng Minh Diệp

## 1. Thông tin thành viên

- Họ tên: Hoàng Minh Diệp
- MSSV: 2A202603764
- Email: hoangminhdiepnd2004@gmail.com

## 2. Phần việc phụ trách

- Phối hợp cải tiến system prompt và khai báo tool ở các phiên bản v2–v3 dựa trên lỗi quan sát được trong kết quả evaluation.
- Rà soát kết quả các run v2–v3, đối chiếu metric, provider errors và các case thất bại để ghi nhận hiệu quả cũng như giới hạn của thay đổi.
- Tổng hợp bằng chứng và tham gia hoàn thiện báo cáo nhóm, đặc biệt các phần kết quả, phân tích lỗi và khó khăn.

## 3. Đóng góp cụ thể

- Cùng nhóm rà soát hướng dẫn chọn tool và truyền arguments trong `system_prompt.md` và `tools.yaml`, bao gồm việc dùng query ngắn gọn, chọn đúng công cụ theo nguồn người dùng yêu cầu, và gọi các nguồn riêng biệt khi cần cả web lẫn X.
- Tham gia cải tiến quy tắc cho hành động có side effect: agent cần hỏi xác nhận yes/no riêng trước khi gọi `send`, và chỉ gửi sau khi người dùng đồng ý.
- Đối chiếu run v2 và v3 để xác định thay đổi có liên quan đến lỗi gọi lặp công cụ tìm kiếm. Run v3 có 20/20 case được đo, không có provider error, 19/20 case đạt; case accuracy là 0.95 và tool-routing accuracy là 1.00.
- Tổng hợp dữ liệu từ run JSON và version log để ghi lại metric, failure cases và giới hạn so sánh giữa các phiên bản. V0–v1 có provider errors nên không được dùng làm run hợp lệ để so sánh trực tiếp với v2–v3.
- Tham gia hoàn thiện nội dung báo cáo nhóm về giải pháp, kết quả evaluation, phân tích lỗi và khó khăn kỹ thuật.

## 4. Bằng chứng

- System prompt và khai báo tool: [system_prompt.md](../../starter_v0/artifacts/system_prompt.md), [tools.yaml](../../starter_v0/artifacts/tools.yaml).
- Run v2: [v2_B_base_openai_20261110T194931562980.json](../../starter_v0/runs/v2_B_base_openai_20261110T194931562980.json).
- Run v3: [v3_B_base_openai_20261110T200349662898.json](../../starter_v0/runs/v3_B_base_openai_20261110T200349662898.json).
- Lịch sử phiên bản và metric: [version_log.csv](../../starter_v0/artifacts/version_log.csv).
- Báo cáo nhóm: [group_report.md](./group_report.md).
- AI/công cụ và cách kiểm tra: các thay đổi được đối chiếu với system prompt, tool schema, version log và run JSON; kết quả run được dùng làm bằng chứng thay vì chỉ dựa vào nhận định. Chưa ghi nhận riêng trong tài liệu hiện có công cụ AI cá nhân hoặc quy trình kiểm tra độc lập ngoài các bằng chứng dự án nêu trên.

## 5. Tự đánh giá

Tôi đã tham gia vào quá trình cải tiến prompt/tool theo hướng dựa trên các lỗi quan sát được, đồng thời hỗ trợ kiểm tra số liệu và đưa bằng chứng vào báo cáo. Kết quả v3 cho thấy các metric được ghi nhận tốt hơn v2, nhưng vẫn còn một case thất bại; vì vậy kết quả chưa thể xem là hoàn hảo. V0–v1 có lỗi từ provider nên không đủ điều kiện làm mốc so sánh hợp lệ. Nếu tiếp tục, cần ưu tiên chạy lại các phiên bản trên cùng provider/model và cùng bộ case, sau đó rà soát các failure case còn lại để đánh giá tác động thay đổi đáng tin cậy hơn.
