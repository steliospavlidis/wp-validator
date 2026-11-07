import sys
import asyncio
import aiohttp
from tqdm import tqdm

REQUEST_TIMEOUT = aiohttp.ClientTimeout(total=5)


async def check_wordpress_domain(session, domain):
    try:
        if domain.startswith('http://') or domain.startswith('https://'):
            url = domain
        else:
            url = f"http://{domain}"

        async with session.get(url) as response:
            if response.status < 200 or response.status >= 400:
                return None

            # Markers are ASCII, so undecodable bytes (non-UTF-8 sites) are
            # replaced instead of making the whole check fail.
            decoded_text = await response.text(encoding='utf-8', errors='replace')

            if 'wp-content' in decoded_text and ('wp-admin' in decoded_text or 'wp-login' in decoded_text):
                return domain, str(response.url)  # Return domain and final URL after redirects
    except (aiohttp.ClientError, asyncio.TimeoutError, ValueError):
        pass

    return None


async def check_wordpress_domains(input_file, output_file, threads):
    with open(input_file, 'r') as file:
        domains = [line.strip() for line in file if line.strip()]

    found_wordpress_domains = []

    progress_bar = tqdm(total=len(domains), desc='Checking Domains', unit='domain')

    sem = asyncio.Semaphore(threads)

    async with aiohttp.ClientSession(timeout=REQUEST_TIMEOUT) as session:

        async def process_domain(domain):
            async with sem:
                result = await check_wordpress_domain(session, domain)
                if result:
                    found_wordpress_domains.append(result)
                    progress_bar.set_postfix(WordPress=len(found_wordpress_domains))

                progress_bar.update(1)

        await asyncio.gather(*[process_domain(domain) for domain in domains])

    progress_bar.close()

    # Save the final URL (after redirects) of each WordPress site
    with open(output_file, 'w') as file:
        for _domain, final_url in found_wordpress_domains:
            file.write(f"{final_url}\n")

    return len(found_wordpress_domains)


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python3 wp-validator.py [input_file] [output_file] [threads]")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]
    try:
        threads = int(sys.argv[3])
        if threads < 1:
            raise ValueError
    except ValueError:
        print("Error: [threads] must be a positive whole number, e.g. 10")
        sys.exit(1)

    num_wordpress_sites = asyncio.run(
        check_wordpress_domains(input_file_path, output_file_path, threads)
    )

    print(f"Number of WordPress sites found: {num_wordpress_sites}")
