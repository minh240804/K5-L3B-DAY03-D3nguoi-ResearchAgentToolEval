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
| v0 | baseline | Đo hành vi gốc trước khi sửa prompt/tools | Không hợp lệ | Không hợp lệ | `runs/v0_B_base_gemini_20261110T172652632360.json` |
| v1 | `system_prompt.md` + `tools.yaml` | Làm rõ routing, query ngắn gọn và gọi đủ nguồn khi người dùng yêu cầu web + X | Không hợp lệ | Không hợp lệ | `runs/v1_B_base_gemini_20261110T190509281921.json` |
| v2 | `system_prompt.md` + `tools.yaml` | Làm rõ xác nhận yes/no trước hành động có side effect | — (v1 không hợp lệ) | 0.9000 | `runs/v2_B_base_openai_20261110T194931562980.json` |
| v3 |  |  |  |  |  |

V2 là run hợp lệ: provider `openai`, model `deepseek-ai/deepseek-v4.1-flash-1017`, 20/20 case được đo, 0 provider error, 18/20 pass. Các metric khác: tool-routing accuracy 0.9500, argument accuracy 0.9000, multiturn accuracy 1.0000. V0 và v1 không hợp lệ (lần lượt 5 và 4 provider errors), nên không dùng metric của chúng làm mốc so sánh. Dù v2 cải thiện so với các kết quả chẩn đoán trước đó, không thể quy toàn bộ thay đổi cho prompt/tools vì provider/model khác nhau giữa các run. V2 vẫn còn một lỗi `wrong_boundary` ở R12.

### B2. Failure Analysis

Lấy từ `results[*].result.failures` trong run JSON.

| Version | Case ID | Failure Type | Actual Tool Calls | What Failed | Hướng xử lý |
|---|---|---|---|---|---|
| v0 | R03_web_news_routing | wrong_tool (mismatch: wrong_arg_value) | `lookup(query="AI news artificial intelligence", topic="news", timeframe="day")` | Đã chọn đúng `lookup` nhưng query bị mở rộng; expected `query="AI"`. | V1 dùng quy tắc query ngắn gọn; case pass trong v1. |
| v0 | R08_out_of_scope | out_of_scope | `send(confirmed=true, ...)` | Gọi tool gửi cho yêu cầu ngoài phạm vi. | Thêm quy tắc ranh giới tool/hành động; case pass trong v1. |
| v0 | R10_missing_handle | missing_info | `timeline(screenname="sama", limit=5)` | Đoán handle khi người dùng chưa nêu tài khoản. | Yêu cầu hỏi lại khi thiếu thông tin thiết yếu; case pass trong v1. |
| v0 | R11_missing_url | missing_info | `fetch(url="https://openai.com/index/hello-gpt-4o/")` | Tự đoán URL thay vì hỏi người dùng. | Quy định chỉ fetch URL do người dùng cung cấp; v1 gặp provider error ở case này. |
| v0 | R12_confirm_before_send | wrong_boundary | `send(confirmed=true, ...)` | Gọi send ngay, không hỏi xác nhận trước. | Thêm quy tắc hỏi xác nhận trước hành động có side effect; v2 vẫn chưa đạt đúng response_type. |
| v0 | R13_parallel_web_and_tweets | wrong_tool (mismatch: missing_tool_call + wrong_arg_value) | `lookup(query="tin tức AI mới nhất hôm nay", ...)` | Bỏ thiếu `social_search` và mở rộng query. | Thêm quy tắc gọi cả `lookup` và `social_search`; case pass trong v1/v2. |
| v0 | M02_carryover_timeframe | wrong_arg_value | `lookup(query="robotics AI news", ...)` | Tự thêm từ vào query; expected `query="robotics"`. | Yêu cầu giữ query ngắn gọn; case pass trong v1/v2. |
| v1 | R01_user_tweets_routing | wrong_tool | `clarify(response_type="text", ...)` | Người dùng nêu Sam Altman nhưng agent hỏi lại handle thay vì gọi `timeline`. | Nêu rõ khi tên người được xác định thì dùng handle công khai đã biết; chỉ hỏi khi mơ hồ. |
| v1 | R12_confirm_before_send | wrong_boundary | `clarify(response_type="text", ...)` | Hỏi bằng kiểu text thay vì yes/no. | Bổ sung quy tắc yes/no; v2 vẫn fail do hỏi nội dung bản tin trước, chưa hỏi xác nhận. |
| v1 | M03_correction_handle | wrong_arg_value (mismatch: missing_tool_call) | `clarify(response_type="text", ...)` | Không tận dụng ngữ cảnh tên Andrej Karpathy và số lượng 3 ở các lượt trước. | Làm rõ sử dụng thông tin đã được bổ sung ở lượt trước; case pass trong v2. |
| v2 | R02_search_tweets_routing | wrong_tool (mismatch: extra_tool_call) | `social_search(query="GPT-5", search_type="Top", limit=10)` và `social_search(query="GPT-5", search_type="Latest", limit=10)` | Gọi cùng tool hai lần với hai kiểu sắp xếp; eval yêu cầu một lời gọi. | Chỉ gọi một lần theo một kiểu sắp xếp phù hợp yêu cầu; không tạo lời gọi lặp. |
| v2 | R12_confirm_before_send | wrong_boundary | `clarify(response_type="text", ...)` | Chưa gửi, nhưng xin nội dung bản tin bằng text thay vì hỏi xác nhận yes/no như eval yêu cầu. Vì nội dung chưa có trong request, đây là thiếu nội dung đồng thời không khớp hành vi mà case đang chấm. | Tách bước xin nội dung khỏi bước xác nhận; sau khi có nội dung cụ thể, hỏi xác nhận yes/no trước khi gửi. |

Phân tích chỉ gán lỗi hành vi cho case model đã trả kết quả; các provider-error cases không được tính là lỗi routing/args. Riêng v2 không có provider errors nên hai lỗi trong bảng là toàn bộ 2 case fail của run hợp lệ này.

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
