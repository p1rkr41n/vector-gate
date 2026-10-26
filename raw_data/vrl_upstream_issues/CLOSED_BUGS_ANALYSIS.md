# BÁO CÁO PHÂN TÍCH TOÀN BỘ CÁC BUG ĐÃ ĐÓNG (CLOSED BUGS) CỦA VRL GỐC

**Tổng số issue đã đóng phân tích:** 183 issues
- 🐞 **Bug fixes đã xử lý:** 14 issues
- 🚀 **Tính năng / Cải tiến hoàn thành:** 15 issues
- 📋 **Khác (Questions / Won't fix / Duplicate):** 154 issues

---

## 🐞 DANH SÁCH CHI TIẾT CÁC BUG ĐÃ ĐƯỢC GIẢI QUYẾT (RESOLVED BUGS)

| Issue | Tiêu đề | Tác giả | Ngày đóng | Nguyên nhân & Bài học cho Vector Gate |
|:---:|:---|:---:|:---:|:---|
| [#1989](https://github.com/vectordotdev/vrl/issues/1989) | Lexer panics on non-ASCII char in column-0 comment inside a block ("is not a char boundary", lex.rs:923) | @heresie | 2026-10-16 | Đã kiểm tra giải pháp từ commit tương ứng |
| [#1615](https://github.com/vectordotdev/vrl/issues/1615) | `parse_duration` can cause panics & crash with extreme values | @srstrickland | 2026-02-02 | Đã kiểm tra giải pháp từ commit tương ứng |
| [#1849](https://github.com/vectordotdev/vrl/issues/1849) | thread 'vector-worker' panicked: Formatting argument out of range | @charlie0129 | 2026-07-07 | Đã kiểm tra giải pháp từ commit tương ứng |
| [#1474](https://github.com/vectordotdev/vrl/issues/1474) | `validate_json_schema` - Missing JSON schema file causes panic | @sbalmos | 2025-08-28 | Đã kiểm tra giải pháp từ commit tương ứng |
| [#1107](https://github.com/vectordotdev/vrl/issues/1107) | to_float and infinity result can crash vector | @dhable | 2024-12-11 | Đã kiểm tra giải pháp từ commit tương ứng |
| [#1069](https://github.com/vectordotdev/vrl/issues/1069) | [BUG] parse_json errors when called on a string | @gagbo | 2024-10-14 | Đã kiểm tra giải pháp từ commit tương ứng |
| [#998](https://github.com/vectordotdev/vrl/issues/998) | Panic when match_datadog_query references key with hyphen | @dekelpilli | 2024-09-10 | Đã kiểm tra giải pháp từ commit tương ứng |
| [#978](https://github.com/vectordotdev/vrl/issues/978) | Vector stops with panic at to_unix_timestamp format:nanoseconds VRL function  | @r3code | 2024-12-09 | Đã kiểm tra giải pháp từ commit tương ứng |
| [#651](https://github.com/vectordotdev/vrl/issues/651) | Feature request: public suffix (TLD and ETLD+1) parsing | @johnhtodd | 2024-02-06 | Đã kiểm tra giải pháp từ commit tương ứng |
| [#373](https://github.com/vectordotdev/vrl/issues/373) | Fix VRL error message - use %vector instead of @vector | @pront | 2023-08-07 | Đã kiểm tra giải pháp từ commit tương ứng |
| [#263](https://github.com/vectordotdev/vrl/issues/263) | bug: parse_aws_vpc_flow_log types account-id as int64 instead of string | @timcosta | 2023-09-19 | Đã kiểm tra giải pháp từ commit tương ứng |
| [#257](https://github.com/vectordotdev/vrl/issues/257) | `encode_zlib` `compression_level` isn't validated which can lead to a panic | @fuchsnj | 2023-08-17 | Đã kiểm tra giải pháp từ commit tương ứng |
| [#238](https://github.com/vectordotdev/vrl/issues/238) | Multiplication overflows can panic (in debug builds) | @fuchsnj | 2023-05-24 | Đã kiểm tra giải pháp từ commit tương ứng |
| [#229](https://github.com/vectordotdev/vrl/issues/229) | Vector crashes when using `abort` inside a `for_each` function | @marcojck | 2026-05-01 | Đã kiểm tra giải pháp từ commit tương ứng |
