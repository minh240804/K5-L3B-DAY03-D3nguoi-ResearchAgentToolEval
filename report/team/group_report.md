# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm: D3nguoi
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md)
- Provider/model dùng cho v0–v3: gemini-3.6-flash

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

> 1–2 câu mô tả agent dùng để làm gì (cho team khác hiểu nhanh).

Ví dụ: "Research agent: tìm tin theo từ khóa / theo tài khoản, đọc URL, tổng hợp thành digest, và gửi lên Telegram khi được xác nhận."

**Cách chạy UI:**

> Lệnh chạy UI (ví dụ `streamlit run app.py`) và dependency đã thêm vào `starter_v0/requirements.txt`.

**Link dùng thử (deploy):**

> Dán link public để team khác mở thử ngay. Cách deploy nhanh bằng Cloudflare Tunnel xem README. Nếu deploy Vercel/Streamlit Cloud thì dán link đó.
>
> URL:

### A2. Tool agent có

> Liệt kê các tool agent đang dùng (gồm tool mới nhóm tự thêm). Mỗi tool 1 dòng: tên + làm được gì.

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | Hỏi người dùng để làm rõ thông tin còn thiếu và chờ lượt trả lời tiếp theo. | không |
| timeline | Lấy các bài đăng gần đây từ một tài khoản X theo tên handle. | không |
| social_search | Tìm bài đăng trên X theo từ khóa, sắp xếp mới nhất hoặc nổi bật. | không |
| lookup | Tìm thông tin trên web theo chủ đề và khoảng thời gian bằng Tavily. | không |
| fetch | Đọc nội dung của một URL bằng Firecrawl. | không |
| format | Định dạng các dữ liệu đã thu thập thành digest Markdown theo mẫu; không tự tìm dữ liệu. | không |
| send | Gửi nội dung lên kênh Telegram; chỉ gửi khi có xác nhận `confirmed=true`. | không |
| policy | Tìm các đoạn liên quan trong tài liệu chính sách nội bộ và trả kèm nguồn. | không |
| papers | Tìm bài báo trên arXiv và trả thông tin bài báo. | không |
| paper_text | Tải PDF arXiv, trích xuất văn bản cục bộ và lưu file PDF/văn bản. | không |

### A3. Câu hỏi mẫu để thử

> 3–5 câu hỏi/yêu cầu mẫu để team khác tự thử agent ngay.

1.
2.
3.

## 3. Giải pháp

> Tóm tắt các thay đổi chính trong `starter_v0/artifacts/system_prompt.md` và `starter_v0/artifacts/tools.yaml`, và tool mới nhóm viết (tên, làm gì, khi nào agent nên gọi).

-

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ `starter_v0/artifacts/version_log.csv` và `starter_v0/runs/*.json`. Chỉ dùng run có `provider_error_cases == 0` và `measured_cases == total_cases`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline | Đo hành vi gốc trước khi sửa prompt/tools | — | — | `runs/v0_B_base_gemini_20261110T172652632360.json` |
| v1 | `system_prompt.md` + `tools.yaml` | Làm rõ routing, query ngắn gọn và gọi đủ nguồn khi người dùng yêu cầu web + X | — | — | `runs/v1_B_base_gemini_20261110T190509281921.json` |
| v2 |  |  |  |  |  |
| v3 |  |  |  |  |  |

Chưa có run hợp lệ để đưa metric vào bảng: v0 có 5 provider error (15/20 case được đo), v1 có 4 provider error (16/20 case được đo). Số liệu chẩn đoán trong JSON lần lượt là case accuracy 0.5333 → 0.8125, tool-routing accuracy 0.6667 → 0.8750; không dùng để kết luận cải thiện vì hai run đều lỗi provider và số case đo được khác nhau. Trong các case có kết quả, R03, R08, R10, R13 và M02 chuyển từ fail ở v0 sang pass ở v1; R01 là lỗi routing mới ở v1.

### B2. Failure Analysis

Lấy từ `results[*].result.failures` trong run JSON.

| Version | Case ID | Failure Type | Actual Tool Calls | What Failed | Hướng xử lý |
|---|---|---|---|---|---|
| v1 | R01_user_tweets_routing | wrong_tool | `clarify(response_type="text", ...)` | Người dùng nêu rõ Sam Altman nhưng agent hỏi lại handle thay vì dùng `timeline(screenname="sama")`. | Chỉ hỏi handle nếu tên/tài khoản thực sự mơ hồ; cho phép dùng handle công khai đã biết khi tên người được nêu rõ. |
| v1 | R12_confirm_before_send | wrong_boundary | `clarify(response_type="text", ...)` | Agent hỏi bằng câu trả lời tự do, trong khi ranh giới gửi cần xác nhận yes/no. | Nêu trong prompt/schema rằng xác nhận gửi phải dùng `response_type="yes_no"`; chưa gọi `send` trước khi có đồng ý. |
| v1 | M03_correction_handle | wrong_arg_value (mismatch: missing_tool_call) | `clarify(response_type="text", ...)` | Không dùng ngữ cảnh: người dùng đã sửa tên thành Andrej Karpathy và yêu cầu 3 tweet; expected `timeline(screenname="karpathy", limit=3)`. | Cho phép dùng thông tin đã được làm rõ ở các lượt trước; chỉ hỏi lại nếu vẫn thiếu hoặc mơ hồ. |

Ở v0, R03 (query bị mở rộng), R08 (gọi `send` ngoài phạm vi), R10 (đoán handle), R13 (thiếu `social_search` và query quá dài), M02 (query bị mở rộng) đều fail; các case này pass ở v1. R11 không so sánh được vì v1 gặp provider error. Provider errors không được tính là lỗi routing/args; v0 có 5 và v1 có 4 trên tổng 20 case.

### B3. Team Eval Cases

Liệt kê đúng 10 case trong `starter_v0/data/eval_group.json` (5 single turn + 5 multi turn).

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
|  |  |  |  |

### B4. Live Chat Evidence

Lấy từ `starter_v0/transcripts/*.transcript.json`.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
|  |  |  |  |  |

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới (`tools/<tên>/`) |  |  |  |
| Unit test tool mới (≥ 3 test/tool) | `pytest` output (0 failed) |  |  |
| UI (lệnh chạy + link dùng thử) |  |  |  |

Tool unit tests: số test đã viết, và một ví dụ lỗi mà unit test bắt được nhưng eval không bắt được.

### B5. Bonus Evidence

Chỉ điền nếu nhóm làm bonus (ghi riêng, tối đa 10 điểm). Tool có sẵn (`send`, `policy`, `papers`, `paper_text`) không tự được bonus.

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Small Local Model | xem B7 |  |  |
| Hơn 3 tool mới (≥ 4) |  |  |  |
| `send` gửi thật lên Telegram sau xác nhận | transcript |  |  |
| Test challenge (0 skipped / regression test) | `pytest` output |  |  |

Test challenge: số bug tìm được trong tool có sẵn (nếu có), cách sửa, và test regression tương ứng.

### B7. Small Local Model Challenge (bonus)

Chỉ điền nếu nhóm làm bonus này.

| Version | Model (provider) | Prompt/Tools | case_accuracy | tool_routing | argument | multiturn | Run File |
|---|---|---|---|---|---|---|---|
| v3 | (cloud) | v3 |  |  |  |  |  |
| v3-<model> | (ollama) | v3 |  |  |  |  |  |
| v3-<model> | (ollama) | v3 |  |  |  |  |  |
| v4-local |  |  |  |  |  |  |  |
| v5-local |  |  |  |  |  |  |  |

Lỗi đặc thù của model nhỏ (đếm từ run JSON):

| Failure Pattern | Count | Example Case | Fix Tried | Helped? |
|---|---|---|---|---|
| wrong / hallucinated tool |  |  |  |  |
| invalid JSON args (`_invalid_json_arguments`) |  |  |  |  |
| no tool call / answered directly |  |  |  |  |
| missed `clarify` |  |  |  |  |
| repeated / unnecessary calls |  |  |  |  |

- Cái gì giúp model nhỏ gọi tool đúng hơn nhất? Bằng chứng?
- Bản prompt tối ưu cho local chạy trên model cloud thì sao?
- Khi nào nhóm sẽ chọn model local thay vì cloud cho agent này?

## 5. Khó khăn và cách xử lý

> Khó khăn chính và cách nhóm xử lý. Nếu gặp lỗi kỹ thuật (provider lỗi, hết quota API, tool không chạy), mô tả lỗi và dẫn bằng chứng: run JSON, log, ảnh chụp.

-

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong [TEAM.md](../../TEAM.md) và các báo cáo cá nhân `report/team/MSSV_HoTen.md`.

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- Fix nào thuộc `system_prompt.md`?
- Fix nào thuộc `tools.yaml`?
- Failure nào cần review thủ công thay vì chấm tự động?
- Nếu có thêm một vòng, nhóm sẽ thử giả thuyết nào?

## 8. Tài liệu tham khảo

-
