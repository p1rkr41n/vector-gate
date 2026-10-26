# [#941] Extract iv from ciphertext

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/941)
- **Status**: `OPEN`
- **Author**: [@vaboston](https://github.com/vaboston)
- **Created At**: `2024-07-11T19:15:03Z`
- **Updated At**: `2024-12-16T13:23:11Z`
- **Comments**: 6
- **Labels**: `type:enhancement`, `vrl:stdlib`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/941)

---

## Description

Based on what the following Logstash plugin does:
https://github.com/logstash-plugins/logstash-filter-cipher/blob/main/lib/logstash/filters/cipher.rb#L179
```ruby
  def do_decrypt(ciphertext_with_iv)
    ciphertext_with_iv = Base64.strict_decode64(ciphertext_with_iv) if @base64 == true
    encoded_iv = ciphertext_with_iv.byteslice(0..@iv_random_length)
    ciphertext = ciphertext_with_iv.byteslice(@iv_random_length..-1)

    with_cipher do |cipher|
      cipher.iv = encoded_iv
      plaintext = cipher.update(ciphertext) + cipher.final
      plaintext.force_encoding("UTF-8")
      plaintext
    end
  end
``` 

Would it be possible to add an option to specify the IV size, and do the extraction in the code? Currently, I am extracting via slices, but it would be much more convenient to have a dedicated option.
Thanks !

