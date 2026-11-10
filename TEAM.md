# Team

## Thông tin nhóm

- Tên nhóm: D3nguoi
- Lớp: L3B
- Repo nhóm: https://github.com/minh240804/K5-L3-DAY03-D3nguoi-ResearchAgentToolEval.git
- URL repo, nhánh nộp, commit chốt: https://github.com/minh240804/K5-L3-DAY03-D3nguoi-ResearchAgentToolEval.git

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Vũ Quang Minh |  |  |  | Leader |
|   2 | Hoàng Minh Diệp | 2A202603764 | hoangminhdiepnd2004@gmail.com | https://github.com/diep142 | Member |
|   3 | Thành viên 3 |  |  |  | Member |


## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

Sao chép mục dưới đây cho từng thành viên.

## Vũ Quang Minh

### Phần việc phụ trách

- Tham gia chạy các phiên bản v2–v3.
- Xây dựng UI.
- Xây dựng tool mới.

### Đóng góp cụ thể

- Tham gia chạy và kiểm tra kết quả base eval cho v2–v3.
- Xây dựng UI chat bằng Streamlit, gồm chọn provider/model và phiên bản artifact, nhập request nhiều lượt, xem hoạt động tool call/tool result và lưu transcript.
- Xây dựng tool mới `text_cleaner` để chuyển HTML/Markdown được cung cấp thành văn bản thuần.

### Bằng chứng

- UI: [starter_v0/app.py](starter_v0/app.py).
- Tool mới: [starter_v0/tools/text_cleaner/tool.py](starter_v0/tools/text_cleaner/tool.py), [starter_v0/tools/text_cleaner/TOOL.md](starter_v0/tools/text_cleaner/TOOL.md), [starter_v0/tools/__init__.py](starter_v0/tools/__init__.py), [starter_v0/artifacts/tools.yaml](starter_v0/artifacts/tools.yaml).
- Run eval: [v2](starter_v0/runs/v2_B_base_openai_20261110T194931562980.json), [v3](starter_v0/runs/v3_B_base_openai_20261110T200349662898.json).
## Hoàng Minh Diệp

### Phần việc phụ trách

- Cải tiến prompt và tool ở v2–v3.
- Hoàn thiện nội dung báo cáo.

### Đóng góp cụ thể

- Tham gia rà soát lỗi từ các run eval và cải tiến hướng dẫn chọn tool, cách truyền query/arguments, xử lý yêu cầu nhiều nguồn và ranh giới xác nhận trước hành động có side effect trong system prompt và tool descriptions.
- Tham gia kiểm tra các lần chạy v2–v3, đối chiếu metric, provider errors và case thất bại để ghi nhận kết quả.
- Tổng hợp bằng chứng từ run JSON, version log và transcript; tham gia hoàn thiện các mục kết quả, phân tích lỗi và khó khăn trong báo cáo nhóm.

### Bằng chứng

- Prompt và khai báo tool: [starter_v0/artifacts/system_prompt.md](starter_v0/artifacts/system_prompt.md), [starter_v0/artifacts/tools.yaml](starter_v0/artifacts/tools.yaml).
- Kết quả eval: [v2](starter_v0/runs/v2_B_base_openai_20261110T194931562980.json), [v3](starter_v0/runs/v3_B_base_openai_20261110T200349662898.json), [version log](starter_v0/artifacts/version_log.csv).
- Báo cáo: [report/team/group_report.md](report/team/group_report.md).

## Thành viên 3

### Phần việc phụ trách

- Chạy và cải tiến prompt/tool ở v0–v1.
- Xây dựng eval cases.

### Đóng góp cụ thể

- Tham gia chạy base eval v0–v1, xem các case sai routing/arguments và dùng kết quả để định hướng cải tiến ban đầu cho system prompt và tool descriptions.
- Soạn và tổ chức eval cases nhóm thành 5 case single-turn và 5 case multi-turn; bổ sung mục tiêu kiểm tra, failure type và hành vi/tool mong đợi cho từng case.
- Chuẩn hóa cấu trúc eval group theo schema runner để expected tool calls dùng `name`/`args` và các lượt hội thoại dùng `role`/`content`.

### Bằng chứng
- Prompt và khai báo tool: [starter_v0/artifacts/system_prompt.md](starter_v0/artifacts/system_prompt.md), [starter_v0/artifacts/tools.yaml](starter_v0/artifacts/tools.yaml).
- Các run v0–v1: [v0](starter_v0/runs/v0_B_base_gemini_20261110T172652632360.json), [v1](starter_v0/runs/v1_B_base_gemini_20261110T190509281921.json).
- Eval cases nhóm: [starter_v0/data/eval_group.json](starter_v0/data/eval_group.json).

## B3. Kết quả Team Eval Cases

Kết quả chạy bộ 10 eval cases của nhóm với phiên bản v3, suite `group`:

| Chỉ số | Kết quả |
|---|---:|
| `total_cases` | 10 |
| `measured_cases` | 10 |
| `provider_error_cases` | 0 |
| `passed_cases` | 6 |
| `case_accuracy` | 0.6 |
| `tool_routing_accuracy` | 1.0 |
| `argument_accuracy` | 0.6 |
| `multiturn_accuracy` | 0.8 |

- `failure_counts`: `{'missing_info': 2, 'wrong_boundary': 1, 'wrong_tool': 1}`
- `observed_mismatch_counts`: `{'wrong_arg_value': 4}`
- Bằng chứng: [starter_v0/runs/v3_B_group_openai_20261110T231118443862.json](starter_v0/runs/v3_B_group_openai_20261110T231118443862.json).
