# TOÀN TẬP ISSUES CỦA VRL GỐC (UPSTREAM VRL ARCHIVE)

Tập hợp dữ liệu toàn bộ các **Issues, Đề xuất tính năng (Feature Requests), Báo cáo lỗi (Bugs) và RFCs** được kéo trực tiếp từ kho lưu trữ chính thức của VRL trên GitHub:
- **Core Repository**: [`vectordotdev/vrl`](https://github.com/vectordotdev/vrl)
- **Integration Repository**: [`vectordotdev/vector`](https://github.com/vectordotdev/vector) (label: `domain: vrl`)

---

## 1. THỐNG KÊ TỔNG QUAN

- **Tổng số Open Issues (VRL Core)**: **258**
- **Tổng số Open Pull Requests (VRL Core)**: **40**
- **Tổng số Closed Issues kéo về (VRL Core)**: **9**
- **Tổng số Issues liên quan từ Vector (domain:vrl)**: **200**
- **Tổng số file Markdown chi tiết từng issue**: **272 file** (nằm trong thư mục `issues/`)

---

## 2. BẢN ĐỒ THƯ MỤC LƯU TRỮ

```text
vrl_upstream_issues/
├── README.md                           # File hướng dẫn & mục lục tổng quát
│
├── categorized/                        # BÁO CÁO PHÂN LOẠI THEO CHUYÊN ĐỀ
│   ├── bugs.md                         # Báo cáo toàn bộ Bugs, Panic, Lỗi Type Checker (19 issues)
│   ├── stdlib_functions.md             # Đề xuất hàm mới cho Standard Library (150 issues)
│   ├── performance_memory.md           # Tối ưu hóa hiệu năng, Zero-copy, RAM (2 issues)
│   └── rfc_and_proposals.md            # Các RFC và đề xuất mở rộng ngữ pháp (22 issues)
│
├── issues/                             # 272 FILE CHI TIẾT TỪNG ISSUE (MARKDOWN)
│   ├── vrl_#XXXX_title.md
│   └── ...
│
├── vrl_core_issues_open.json           # Dữ liệu JSON thô (Toàn bộ open issues của vrl)
├── vrl_core_prs_open.json              # Dữ liệu JSON thô (Toàn bộ open pull requests)
├── vrl_core_issues_closed.json         # Dữ liệu JSON thô (Các closed issues gần nhất)
└── vector_domain_vrl_issues.json       # Dữ liệu JSON thô (Các issues VRL từ repo vector)
```

---

## 3. TRA CỨU DANH MỤC TOP OPEN ISSUES NỔI BẬT

| #ID | Kho Nguồn | Tiêu Đề | Tác Giả | Bình Luận | File Chi Tiết |
| :--- | :--- | :--- | :--- | :---: | :--- |
| [#1960](https://github.com/vectordotdev/vrl/issues/1960) | `vrl` | feat(compiler): support first-class for loops with break and continue | @jimmystewpot | 3 | [Xem](../issues/vrl_1960_feat(compiler)__support_first-class_for_loops_with_break_and_continue.md) |
| [#1950](https://github.com/vectordotdev/vrl/issues/1950) | `vrl` | Missing `parse_uuid` / `parse_bool` / `parse_date` in VRL stdlib | @28515graj | 0 | [Xem](../issues/vrl_1950_Missing_`parse_uuid`___`parse_bool`___`parse_date`_in_VRL_stdlib.md) |
| [#1949](https://github.com/vectordotdev/vrl/issues/1949) | `vrl` | `slice!()` operates on bytes, not characters, silently corrupts multi-byte strings | @28515graj | 0 | [Xem](../issues/vrl_1949_`slice!()`_operates_on_bytes,_not_characters,_silently_corrupts_multi-byte_strin.md) |
| [#1902](https://github.com/vectordotdev/vrl/issues/1902) | `vrl` | FIPS compliance tracker | @pront | 0 | [Xem](../issues/vrl_1902_FIPS_compliance_tracker.md) |
| [#1859](https://github.com/vectordotdev/vrl/issues/1859) | `vrl` | Release tool: checkpointing to resume a failed publish | @pront | 0 | [Xem](../issues/vrl_1859_Release_tool__checkpointing_to_resume_a_failed_publish.md) |
| [#1851](https://github.com/vectordotdev/vrl/issues/1851) | `vrl` | chore: migrate from quickcheck to proptest for VRL Arbitrary impls | @pront | 0 | [Xem](../issues/vrl_1851_chore__migrate_from_quickcheck_to_proptest_for_VRL_Arbitrary_impls.md) |
| [#1845](https://github.com/vectordotdev/vrl/issues/1845) | `vrl` | chore(deps): consolidate wasm32 getrandom overrides to a single version | @pront | 0 | [Xem](../issues/vrl_1845_chore(deps)__consolidate_wasm32_getrandom_overrides_to_a_single_version.md) |
| [#1824](https://github.com/vectordotdev/vrl/issues/1824) | `vrl` | datadog_filter: wildcard_regex fails to match strings with trailing newline | @gwenaskell | 1 | [Xem](../issues/vrl_1824_datadog_filter__wildcard_regex_fails_to_match_strings_with_trailing_newline.md) |
| [#1805](https://github.com/vectordotdev/vrl/issues/1805) | `vrl` | VRL code formatter (ergonomics) | @pront | 0 | [Xem](../issues/vrl_1805_VRL_code_formatter_(ergonomics).md) |
| [#1799](https://github.com/vectordotdev/vrl/issues/1799) | `vrl` | `resolve_constant` on function arguments is unsound/not deterministic when earlier arguments have side effects | @thomasqueirozb | 0 | [Xem](../issues/vrl_1799_`resolve_constant`_on_function_arguments_is_unsound_not_deterministic_when_earli.md) |
| [#1693](https://github.com/vectordotdev/vrl/issues/1693) | `vrl` | `parse_user_agent("curl/8.7.1")` returns `"curl"` as the version | @andrey-mazo | 0 | [Xem](../issues/vrl_1693_`parse_user_agent(_curl_8.7.1_)`_returns_`_curl_`_as_the_version.md) |
| [#1692](https://github.com/vectordotdev/vrl/issues/1692) | `vrl` | Preserve numeric precision with `decimal` type | @benjamin-awd | 2 | [Xem](../issues/vrl_1692_Preserve_numeric_precision_with_`decimal`_type.md) |
| [#1638](https://github.com/vectordotdev/vrl/issues/1638) | `vrl` | `Function::return_kind` should be checked | @thomasqueirozb | 0 | [Xem](../issues/vrl_1638_`Function__return_kind`_should_be_checked.md) |
| [#1636](https://github.com/vectordotdev/vrl/issues/1636) | `vrl` | Support AES-GCM in `encrypt`/`decrypt` functions | @dodo0822 | 0 | [Xem](../issues/vrl_1636_Support_AES-GCM_in_`encrypt`_`decrypt`_functions.md) |
| [#1620](https://github.com/vectordotdev/vrl/issues/1620) | `vrl` | Disallow usage of implicit arithmetic methods for std types | @thomasqueirozb | 0 | [Xem](../issues/vrl_1620_Disallow_usage_of_implicit_arithmetic_methods_for_std_types.md) |
| [#1576](https://github.com/vectordotdev/vrl/issues/1576) | `vrl` | Add ed25519 signing | @Reasonable-Solutions | 0 | [Xem](../issues/vrl_1576_Add_ed25519_signing.md) |
| [#1561](https://github.com/vectordotdev/vrl/issues/1561) | `vrl` | `parse_klog` fails if the message contains newlines | @Ilmarii | 0 | [Xem](../issues/vrl_1561_`parse_klog`_fails_if_the_message_contains_newlines.md) |
| [#1560](https://github.com/vectordotdev/vrl/issues/1560) | `vrl` | `encode_proto` fails to encode a message if `google.protobuf.Struct` is used | @simplepad | 0 | [Xem](../issues/vrl_1560_`encode_proto`_fails_to_encode_a_message_if_`google.protobuf.Struct`_is_used.md) |
| [#1559](https://github.com/vectordotdev/vrl/issues/1559) | `vrl` | Testing random functions in unit tests | @simplepad | 0 | [Xem](../issues/vrl_1559_Testing_random_functions_in_unit_tests.md) |
| [#1558](https://github.com/vectordotdev/vrl/issues/1558) | `vrl` | Add `ord` and `chr` functions | @simplepad | 0 | [Xem](../issues/vrl_1558_Add_`ord`_and_`chr`_functions.md) |
| [#1548](https://github.com/vectordotdev/vrl/issues/1548) | `vrl` | parse_key_value problem when value missing | @perederyaev | 0 | [Xem](../issues/vrl_1548_parse_key_value_problem_when_value_missing.md) |
| [#1552](https://github.com/vectordotdev/vrl/issues/1552) | `vrl` | parse_key_value problem when value missing | @perederyaev | 2 | [Xem](../issues/vrl_1552_parse_key_value_problem_when_value_missing.md) |
| [#1543](https://github.com/vectordotdev/vrl/issues/1543) | `vrl` | `parse_timestamp()` function does not honnor all chrono's strftime() tokens (specifically the `%z` token) | @kquinsland01 | 0 | [Xem](../issues/vrl_1543_`parse_timestamp()`_function_does_not_honnor_all_chrono's_strftime()_tokens_(spe.md) |
| [#1540](https://github.com/vectordotdev/vrl/issues/1540) | `vrl` | RFC: Add Flamegraph Support to VRL Command for Performance Debugging | @jlambatl | 0 | [Xem](../issues/vrl_1540_RFC__Add_Flamegraph_Support_to_VRL_Command_for_Performance_Debugging.md) |
| [#1539](https://github.com/vectordotdev/vrl/issues/1539) | `vrl` | Update `parse_aws_vpc_flow_log` to version 7 of the VPC flow logs | @istimaldar | 5 | [Xem](../issues/vrl_1539_Update_`parse_aws_vpc_flow_log`_to_version_7_of_the_VPC_flow_logs.md) |
| [#1536](https://github.com/vectordotdev/vrl/issues/1536) | `vrl` | parse_key_value failed when string ends with delimiter | @alexeynl | 0 | [Xem](../issues/vrl_1536_parse_key_value_failed_when_string_ends_with_delimiter.md) |
| [#1537](https://github.com/vectordotdev/vrl/issues/1537) | `vrl` | unnest not preserving root field | @objectbased | 0 | [Xem](../issues/vrl_1537_unnest_not_preserving_root_field.md) |
| [#1535](https://github.com/vectordotdev/vrl/issues/1535) | `vrl` | xxHash functions not providing the correct output | @ryn9 | 4 | [Xem](../issues/vrl_1535_xxHash_functions_not_providing_the_correct_output.md) |
| [#1511](https://github.com/vectordotdev/vrl/issues/1511) | `vrl` | Casing is slow and computationally expensive. | @ForkingFrenzy | 3 | [Xem](../issues/vrl_1511_Casing_is_slow_and_computationally_expensive..md) |
| [#1509](https://github.com/vectordotdev/vrl/issues/1509) | `vrl` | When parsing a CEF message, incorrect ad fields are generated that contain a dot in the name | @esmelnikov | 0 | [Xem](../issues/vrl_1509_When_parsing_a_CEF_message,_incorrect_ad_fields_are_generated_that_contain_a_dot.md) |
| [#1503](https://github.com/vectordotdev/vrl/issues/1503) | `vrl` | Provide `arbitrary_precision` option for `serde_json` float conversions | @DominikMoelter | 5 | [Xem](../issues/vrl_1503_Provide_`arbitrary_precision`_option_for_`serde_json`_float_conversions.md) |
| [#1478](https://github.com/vectordotdev/vrl/issues/1478) | `vrl` | `from_unix_timestamp` should support float timestamps with subsecond precision | @garysassano | 1 | [Xem](../issues/vrl_1478_`from_unix_timestamp`_should_support_float_timestamps_with_subsecond_precision.md) |
| [#1471](https://github.com/vectordotdev/vrl/issues/1471) | `vrl` | Syslog rfc5424 parsing does not accept NILVALUE timestamp | @jinnatar | 4 | [Xem](../issues/vrl_1471_Syslog_rfc5424_parsing_does_not_accept_NILVALUE_timestamp.md) |
| [#1470](https://github.com/vectordotdev/vrl/issues/1470) | `vrl` | Performance bottleneck in kubernetes_logs source caused by excessive VRL BTree insert operations | @huanghuangzym | 4 | [Xem](../issues/vrl_1470_Performance_bottleneck_in_kubernetes_logs_source_caused_by_excessive_VRL_BTree_i.md) |
| [#1466](https://github.com/vectordotdev/vrl/issues/1466) | `vrl` | add a `parse_apache_casandra_log()` to VRL | @kquinsland01 | 0 | [Xem](../issues/vrl_1466_add_a_`parse_apache_casandra_log()`_to_VRL.md) |
| [#1454](https://github.com/vectordotdev/vrl/issues/1454) | `vrl` | Function parse_cef() does not parsed the string, but on playground.vrl.dev website the message is parsed | @esmelnikov | 1 | [Xem](../issues/vrl_1454_Function_parse_cef()_does_not_parsed_the_string,_but_on_playground.vrl.dev_websi.md) |
| [#1451](https://github.com/vectordotdev/vrl/issues/1451) | `vrl` | Remove all `#[allow]` and `#![allow]` exceptions | @pront | 0 | [Xem](../issues/vrl_1451_Remove_all_`#[allow]`_and_`#![allow]`_exceptions.md) |
| [#1449](https://github.com/vectordotdev/vrl/issues/1449) | `vrl` | Adding a function to calculate the event size in bytes | @omers | 0 | [Xem](../issues/vrl_1449_Adding_a_function_to_calculate_the_event_size_in_bytes.md) |
| [#1426](https://github.com/vectordotdev/vrl/issues/1426) | `vrl` | VRL function parse_tokens does not handle unescaped "\" | @CyBeRoni | 0 | [Xem](../issues/vrl_1426_VRL_function_parse_tokens_does_not_handle_unescaped__\_.md) |
| [#1429](https://github.com/vectordotdev/vrl/issues/1429) | `vrl` | Allow override grok patterns via aliases in `parse_groks` function | @piotrminkina | 1 | [Xem](../issues/vrl_1429_Allow_override_grok_patterns_via_aliases_in_`parse_groks`_function.md) |
| [#1419](https://github.com/vectordotdev/vrl/issues/1419) | `vrl` | del does not delete specified path during merge | @DimDroll | 0 | [Xem](../issues/vrl_1419_del_does_not_delete_specified_path_during_merge.md) |
| [#1405](https://github.com/vectordotdev/vrl/issues/1405) | `vrl` | Add redact() hashing with automatically rotated salt | @nemobis | 0 | [Xem](../issues/vrl_1405_Add_redact()_hashing_with_automatically_rotated_salt.md) |
| [#1386](https://github.com/vectordotdev/vrl/issues/1386) | `vrl` | Add bitwise operators for integers | @vruello | 1 | [Xem](../issues/vrl_1386_Add_bitwise_operators_for_integers.md) |
| [#1382](https://github.com/vectordotdev/vrl/issues/1382) | `vrl` | Add a dynamic variant of the `exists` function | @simplepad | 0 | [Xem](../issues/vrl_1382_Add_a_dynamic_variant_of_the_`exists`_function.md) |
| [#1371](https://github.com/vectordotdev/vrl/issues/1371) | `vrl` | xpath support | @juju4 | 0 | [Xem](../issues/vrl_1371_xpath_support.md) |
| [#1361](https://github.com/vectordotdev/vrl/issues/1361) | `vrl` | `format_int` bad output type | @JTKU | 0 | [Xem](../issues/vrl_1361_`format_int`_bad_output_type.md) |
| [#1352](https://github.com/vectordotdev/vrl/issues/1352) | `vrl` | parse_cef fails on logs with complex quoted values | @unitednf24 | 0 | [Xem](../issues/vrl_1352_parse_cef_fails_on_logs_with_complex_quoted_values.md) |
| [#1340](https://github.com/vectordotdev/vrl/issues/1340) | `vrl` | Byte strings/encoded payloads | @jimmystewpot | 3 | [Xem](../issues/vrl_1340_Byte_strings_encoded_payloads.md) |
| [#1313](https://github.com/vectordotdev/vrl/issues/1313) | `vrl` | Add option for VRL function parse_key_value to specify resulting key case | @alexeynl | 4 | [Xem](../issues/vrl_1313_Add_option_for_VRL_function_parse_key_value_to_specify_resulting_key_case.md) |
| [#1297](https://github.com/vectordotdev/vrl/issues/1297) | `vrl` | Introduce `break` for aborting iterations | @dr4gon123 | 1 | [Xem](../issues/vrl_1297_Introduce_`break`_for_aborting_iterations.md) |
| [#1266](https://github.com/vectordotdev/vrl/issues/1266) | `vrl` | Change `UnnecessaryCoalesce` error to a warning. | @pront | 0 | [Xem](../issues/vrl_1266_Change_`UnnecessaryCoalesce`_error_to_a_warning..md) |
| [#1257](https://github.com/vectordotdev/vrl/issues/1257) | `vrl` | Unexpected behaviour of the object_from_array VRL fuction | @usa4ev | 4 | [Xem](../issues/vrl_1257_Unexpected_behaviour_of_the_object_from_array_VRL_fuction.md) |
| [#1244](https://github.com/vectordotdev/vrl/issues/1244) | `vrl` | parse_json in VRL doesn't support json-like strings (with single quotes) | @nomalord | 3 | [Xem](../issues/vrl_1244_parse_json_in_VRL_doesn't_support_json-like_strings_(with_single_quotes).md) |
| [#1216](https://github.com/vectordotdev/vrl/issues/1216) | `vrl` | Unused expression checker improvements | @pront | 0 | [Xem](../issues/vrl_1216_Unused_expression_checker_improvements.md) |
| [#1200](https://github.com/vectordotdev/vrl/issues/1200) | `vrl` | Parsing function for binary data (struct) | @nomalord | 2 | [Xem](../issues/vrl_1200_Parsing_function_for_binary_data_(struct).md) |
| [#1193](https://github.com/vectordotdev/vrl/issues/1193) | `vrl` | parse_aws_alb_log function error failed to get field `client_host` | @mdesouky | 4 | [Xem](../issues/vrl_1193_parse_aws_alb_log_function_error_failed_to_get_field_`client_host`.md) |
| [#1189](https://github.com/vectordotdev/vrl/issues/1189) | `vrl` | Refactor compiler error codes | @pront | 0 | [Xem](../issues/vrl_1189_Refactor_compiler_error_codes.md) |
| [#1154](https://github.com/vectordotdev/vrl/issues/1154) | `vrl` | VRL error message for field assignment to non-object has a one-off typo in it | @bruceg | 0 | [Xem](../issues/vrl_1154_VRL_error_message_for_field_assignment_to_non-object_has_a_one-off_typo_in_it.md) |
| [#1139](https://github.com/vectordotdev/vrl/issues/1139) | `vrl` | Fold enumeration function | @jakedipity | 2 | [Xem](../issues/vrl_1139_Fold_enumeration_function.md) |
| [#1119](https://github.com/vectordotdev/vrl/issues/1119) | `vrl` | `FailedToApplyFilter` Error in `parse_grok()` improvements | @neuronull | 0 | [Xem](../issues/vrl_1119_`FailedToApplyFilter`_Error_in_`parse_grok()`_improvements.md) |

_...và còn hơn 212 issues khác được lưu trữ đầy đủ trong thư mục `issues/` và các báo cáo `categorized/`._
