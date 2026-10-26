# Issue #1322: snakecase function is adding unnecessary underscores to delimit numbers

- **URL:** https://github.com/vectordotdev/vrl/issues/1322
- **Author:** @britton-from-notion
- **Status:** CLOSED (completed)
- **Created:** 2025-03-06T01:55:59Z
- **Closed:** 2025-03-10T18:26:08Z
- **Labels:** None

## Description

![Image](https://github.com/user-attachments/assets/51375a13-0a2d-4883-b0fe-61413e9b6e05)

[Here is an example in the playground](https://playground.vrl.dev/?state=eyJwcm9ncmFtIjoiLiwgZXJyID0gbWFwX3ZhbHVlcyguLCByZWN1cnNpdmU6IHRydWUpIC0%2BIHxrZXl8IHtcbiAgc25ha2VjYXNlKGtleSlcbn1cblxuaWYgZXJyICE9IG51bGwge1xuIGFib3J0XG59IiwiZXZlbnQiOnsibG93ZXJjYXNlIjoiYnVja2V0ZGV0YWlscyIsImxvd2VyY2FzZV9hbmRfbnVtYmVyIjoiczNidWNrZXRkZXRhaWxzIiwiY2FtZWxfYW5kX251bWJlciI6InMzQnVja2V0RGV0YWlscyIsInBhc2NhbCI6IkVLU0NsdXN0ZXIiLCJwYXNjYWxfYW5kX251bWJlciI6IkVLU0NsdXN0ZXIyTnVtYmVyIn0sImlzX2pzb25sIjpmYWxzZSwiZXJyb3IiOm51bGx9)

Given the following remap
```rust
., err = map_values(., recursive: true) -> |key| {
  snakecase(key)
}

if err != null {
 abort
}
```

and the following data

```json
{
   "lowercase": "bucketdetails",
   "lowercase_and_number":  "s3bucketdetails",
   "camel_and_number": "s3BucketDetails",
   "pascal": "EKSCluster",
   "pascal_and_number": "EKSCluster2Number"
}
```

the following results are output
```json
{
	"camel_and_number": "s_3_bucket_details",
	"lowercase": "bucketdetails",
	"lowercase_and_number": "s_3_bucketdetails",
	"pascal": "eks_cluster",
	"pascal_and_number": "eks_cluster_2_number"
}
```
