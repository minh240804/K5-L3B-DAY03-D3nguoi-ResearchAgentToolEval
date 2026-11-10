---
name: text_cleaner
track: bonus
kind: local_formatter
provider: local
requires_env: []
inputs: [text]
outputs: [tool, text]
side_effect: false
---

Chuyển nội dung HTML hoặc Markdown thành văn bản thuần.
Tool không tải nội dung từ URL và không thay đổi dữ liệu bên ngoài.
