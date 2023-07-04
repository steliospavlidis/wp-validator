# ![logo_50](https://github.com/steliospavlidis/wp-validator/assets/138578903/65cb8443-2fa8-4fde-85b9-c55c08a3f48f)

The WP-Validator is a powerful Python script designed to assist you in filtering a domain list and identifying those that utilize the WordPress platform.

**WP-Validator checks 3 key things**

1) The HTTP status codes must be between 200 and 400
2) If wp-content is present
3) If wp-admin or wp-login is present


**Install the following packages by entering**

pip3 install asyncio aiohttp tqdm


**Run the script by entering**

python3 wp-validator.py [input_file] [output_file] [threads]

python3 wp-validator.py example-domains.txt found.txt 10

![run](https://github.com/steliospavlidis/wp-validator/assets/138578903/4ab5266f-b897-4c38-8dd3-3652b1b8f36f)


**Notes**
I would recommend limiting the number of threads to no more than 10, sometimes websites utilize CDN services like Cloudflare and it can pose challenges in obtaining precise and reliable results. Script may not be 100% accurate, I am looking into new ways of improving it, If you have any suggestions I would encourage you to share them without hesitation.
