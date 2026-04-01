import requests
import datetime
import time
import argparse

LOG_FILE = 'site_status.log'

def check_website(url, timeout=10):
    
    try:
        response = requests.get(url, timeout=timeout)
        status_code = response.status_code
        success = 200 <= status_code < 400
    except requests.exceptions.RequestException as e:
        status_code = None
        success = False
        error_msg = str(e)
    
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] {url}
"
    
    if success:
        log_entry += f'Status Code: {status_code} (Online)\n\n'
    else:
        log_entry += f'Error: {error_msg or "Connection Failed"} (Offline)\n\n'
    
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_entry)
    
    return success


def main():
    parser = argparse.ArgumentParser(description='Website status checker with logging')
    parser.add_argument('url', help='URL to check')
    parser.add_argument('--interval', '-i', type=int, default=300, help='Seconds between checks (0 for one-time check)')
    parser.add_argument('--timeout', '-t', type=int, default=10, help='Request timeout in seconds')
    parser.add_argument('--runs', '-r', type=int, default=0, help='Number of runs (0 for infinite)')
    
    args = parser.parse_args()

    print(f"Monitoring {args.url}... Logging to {LOG_FILE}")
    
    run_count = 0
    while args.runs == 0 or run_count < args.runs:
        check_website(args.url, args.timeout)
        run_count += 1
        if args.interval > 0:
            time.sleep(args.interval)
        else:
            break

if __name__ == '__main__':
    main()

# Example usage:
# Basic single check: python website_checker.py https://example.com
# Continuous monitoring: python website_checker.py https://example.com -i 60 -r 10