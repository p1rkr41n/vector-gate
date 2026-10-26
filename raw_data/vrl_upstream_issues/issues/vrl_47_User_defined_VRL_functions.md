# [#47] User defined VRL functions

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/47)
- **Status**: `OPEN`
- **Author**: [@mohshami](https://github.com/mohshami)
- **Created At**: `2022-07-13T05:36:47Z`
- **Updated At**: `2026-06-01T14:17:06Z`
- **Comments**: 0
- **Labels**: `vrl:compiler`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/47)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Use Cases

We are currently migrating away from Logstash, but due to some scripts our clients use the fields need to be 1:1 identical to what Logstash generates. I have the following in my current vector configuration and it's needed in 3 different places.

```
  geo = del(."client-address-geo")
  ."client-address-geo".city_name = geo.city_name
  ."client-address-geo".continent_code = geo.continent_code
  ."client-address-geo".country_code2 = geo.country_code
  ."client-address-geo".country_code3 = geo.country_code
  ."client-address-geo".country_name = geo.country_name
  ."client-address-geo".ip = ."client-address"
  ."client-address-geo".latitude = to_float!(geo.latitude)
  ."client-address-geo".longitude = to_float!(geo.longitude)
  ."client-address-geo".location.lat = to_float!(geo.latitude)
  ."client-address-geo".location.lon = to_float!(geo.longitude)
  ."client-address-geo".postal_code = geo.postal_code
  ."client-address-geo".region_code = geo.region_code
  ."client-address-geo".region_name = geo.region_name
  ."client-address-geo".timezone = geo.timezone

  # client-address-isp doesn't need as much work
  ."client-address-isp".as_org = del(."client-address-isp".autonomous_system_organization)
  ."client-address-isp".asn = del(."client-address-isp".autonomous_system_number)
  ."client-address-isp".ip = ."client-address"

  if ip_cidr_contains!("127.0.0.0/8", string!(."client-address")) 
     ip_cidr_contains!("10.0.0.0/8", string!(."client-address")) 
     ip_cidr_contains!("172.16.0.0/12", string!(."client-address")) 
     ip_cidr_contains!("192.168.0.0/16", string!(."client-address")) 
     ip_cidr_contains!("169.254.0.0/16", string!(."client-address"))
  {
    del(."client-address-isp")
    del(."client-address-geo")
  }

  if exists(."client-address-geo".location) && ."client-address-geo".location == "0,0" {
    ."client-address-geo".location = ""
  }
  ```

Also, the `if ip_cidr_contains` block is repeated in other places as well. It would be very useful if I could define my own `is_bogon` and `massage_geodata` functions and use them across my configuration


### Attempted Solutions

One workaround I was thinking of was to store the geo data in a variable and then have that geo data manipulated by a VRL stored in a file. This would work for the `massage_geodata` function, but not for `is_bogon`

### Proposal

_No response_

### References

_No response_

### Version

0.23.0
