# ![logo_50](https://github.com/steliospavlidis/wp-validator/assets/138578903/65cb8443-2fa8-4fde-85b9-c55c08a3f48f)

The WP-Validator is a powerful Python script designed to assist you in filtering a domain list and identifying those that utilize the WordPress platform.

## WP-Validator checks 3 key things

1) The HTTP status codes must be between 200 and 400
2) If wp-content is present
3) If wp-admin or wp-login is present


## Requirements

Python 3.8 or newer (tested up to 3.14). Install the dependencies with:

```bash
pip3 install -r requirements.txt
```

## Usage

```bash
python3 wp-validator.py [input_file] [output_file] [threads]
```

Example:

```bash
python3 wp-validator.py example-domains.txt found.txt 10
```

The input file has one domain or URL per line. Domains without `http://` or `https://` are checked over `http://` first and follow any redirects.
## Result

![run](https://github.com/steliospavlidis/wp-validator/assets/138578903/4ab5266f-b897-4c38-8dd3-3652b1b8f36f)


## Notes

- I recommend no more than 10 threads. Sites behind CDNs like Cloudflare can make results less reliable.
- The output file contains the **final URL** of each WordPress site after following redirects.
- The script may not be 100% accurate. Suggestions are welcome, so feel free to open an issue.
