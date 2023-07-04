import sys
import asyncio
import aiohttp
from tqdm import tqdm
from urllib.parse import urlparse

async def check_wordpress_domain(domain):
    try:
        if domain.startswith('http://') or domain.startswith('https://'):
            url = domain
        else:
            url = f"http://{domain}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=5) as response:
                if response.status < 200 or response.status >= 400:
                    return None

                try:
                    decoded_text = await response.text(encoding='utf-8')
                except UnicodeDecodeError:
                    return None

                if 'wp-content' in decoded_text and ('wp-admin' in decoded_text or 'wp-login' in decoded_text):
                    return domain, str(response.url)  # Return domain and redirect URL
    except (aiohttp.ClientError, asyncio.TimeoutError, ValueError):
        pass

    return None

async def check_wordpress_domains(input_file, output_file, threads):
    with open(input_file, 'r') as file:
        domains = file.read().splitlines()

    found_wordpress_domains = []

    progress_bar = tqdm(total=len(domains), desc='Checking Domains', unit='domain')

    sem = asyncio.Semaphore(threads)

    async def process_domain(domain):
        async with sem:
            result = await check_wordpress_domain(domain)
            if result:
                found_wordpress_domains.append(result)
                progress_bar.set_postfix(WordPress=len(found_wordpress_domains))

            progress_bar.update(1)

    await asyncio.gather(*[process_domain(domain) for domain in domains])

    progress_bar.close()

    with open(output_file, 'w') as file:
        for domain, redirect in found_wordpress_domains:
            file.write(f"{domain}\t{redirect}\n")

    with open(output_file, 'r') as file:
        lines = file.readlines()

    with open(output_file, 'w') as file:
        for line in lines:
            redirect_url = line.strip().split('\t')[1]
            file.write(f"{redirect_url}\n")

    return len(found_wordpress_domains)

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python script.py [input_file] [output_file] [threads]")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]
    threads = int(sys.argv[3])

    loop = asyncio.get_event_loop()
    num_wordpress_sites = loop.run_until_complete(check_wordpress_domains(input_file_path, output_file_path, threads))
    loop.close()

    print(f"Number of WordPress sites found: {num_wordpress_sites}")
