import requests
import time
import sys
import atexit
import asyncio
import aiohttp

# --- Configuration ---
# Set this to the endpoint you want to test.
# We are changing this back to hexadecimal conversion.
ENDPOINT_TO_TEST = "/reverse" 

# Predefined list of 10 strings for the 10-request test, as per the sample output.
STRINGS_FOR_10_TEST = [
    "5PKOHcL6OuxRd0xXHQ", "JHfJtHH9", "gZFEMAS2JA", "NkmPg9jT2uMwWvQ9",
    "lV0NTS", "tcmViV3cxd6J794H", "SKZpKaksPB1", "5ygFfJXEgn7ssgyuS",
    "mvZ5wv7qfk", "tD58eeUOLh"
]

# --- Helper Functions ---

async def send_single_request(session, url, data_payload):
    """Sends a single request and returns the response JSON and duration."""
    start_time = time.time()
    try:
        async with session.post(url, json=data_payload, timeout=15) as response:
            response.raise_for_status()
            response_json = await response.json()
            duration = time.time() - start_time
            return response_json, duration
    except Exception as e:
        print(f"Error during request: {e}", file=sys.stderr)
        return None, -1.0

# --- Test Functions ---

async def run_10_string_test(server_url, output_file):
    """Runs the 10-string test with detailed output format (parallel)."""
    print(f"Running 10-string test. Output will be saved to '{output_file}'")

    async with aiohttp.ClientSession() as session:
        # Create coroutines for all 10 requests at once
        tasks = [
            send_single_request(session, server_url, {"data": original})
            for original in STRINGS_FOR_10_TEST
        ]
        results = await asyncio.gather(*tasks)

    # Process results
    total_time = 0
    valid_requests = 0
    with open(output_file, 'w') as f:
        for original, (response_json, duration) in zip(STRINGS_FOR_10_TEST, results):
            if response_json and duration > 0:
                processed_key = "reversed"   # since you need reversed string now
                processed_string = response_json.get(processed_key, "Error: Key not found")
                f.write(f"Original: {original}\n")
                f.write(f"Reversed: {processed_string}\n")
                f.write("--------------------\n")
                total_time += duration
                valid_requests += 1
            else:
                f.write(f"Original: {original}\n")
                f.write(f"Reversed: Request Failed\n")
                f.write("--------------------\n")

        if valid_requests > 0:
            average_time = total_time / valid_requests
            f.write(f"average_response_time={average_time:.6f}\n")
        else:
            f.write("average_response_time=N/A (All requests failed)\n")
    print("10-string test complete.")

async def run_high_load_test(server_url, output_file, rps):
    """
    Runs a high-load test for a given RPS.
    - For 10,000 RPS submission, outputs only the average time.
    - For other RPS values, outputs every response time to a new line.
    """
    print(f"Running high-load test at {rps} RPS for 60 seconds. Output: '{output_file}'")
    
    duration = 60  # seconds
    total_requests_to_send = rps * duration
    payload = {"data": "high-load-test-string"}
    response_times = []

    async with aiohttp.ClientSession() as session:
        tasks = []
        # Create all tasks upfront
        for _ in range(total_requests_to_send):
            tasks.append(send_single_request(session, server_url, payload))
        
        # Gather results
        all_results = await asyncio.gather(*tasks)

        # Process results to get valid durations
        for _, duration in all_results:
            if duration > 0:
                response_times.append(duration)

    # Calculate and write the output based on the test type
    with open(output_file, 'w') as f:
        if not response_times:
            f.write("average_response_time=N/A (All requests failed)\n")
            print("High-load test complete. All requests failed.")
            return

        average_time = sum(response_times) / len(response_times)
        
        # Check if this is the specific 10,000 RPS submission case
        if rps == 10000:
            f.write(f"average_response_time={average_time:.6f}\n")
            print(f"High-load test (10000 RPS submission format) complete. Average time: {average_time:.6f}s")
        else:
            # General case: write every response time to the file
            for t in response_times:
                f.write(f"{t:.6f}\n")
            print(f"High-load test ({rps} RPS) complete. All response times saved to '{output_file}'.")
            print(f"Average Response Time (for your information): {average_time:.6f}s")


# --- Main Execution ---

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python updated_fastapi_client.py <roll_number> <server_base_url> <platform> <request_mode>")
        print("Example (10-string test): python updated_fastapi_client.py CB.EN.U4CSE19000 http://1.2.3.4 dockerswarm 10")
        print("Example (Submission RPS): python updated_fastapi_client.py CB.EN.U4CSE19000 http://1.2.3.4 kubernetes 10000")
        print("Example (General RPS):  python updated_fastapi_client.py CB.EN.U4CSE19000 http://1.2.3.4 kubernetes 5000")
        sys.exit(1)

    roll_number = sys.argv[1]
    server_base_url = sys.argv[2]
    platform = sys.argv[3].lower() # dockerswarm or kubernetes
    request_mode_str = sys.argv[4]

    if platform not in ['dockerswarm', 'kubernetes']:
        print("Error: Platform must be 'dockerswarm' or 'kubernetes'")
        sys.exit(1)

    # Construct the full URL for the API endpoint
    full_url = server_base_url.rstrip('/') + ENDPOINT_TO_TEST

    if request_mode_str == '10':
        # Special case for the 10-string detailed log submission file
        output_filename = f"{roll_number}{platform}10.txt"
        asyncio.run(run_10_string_test(full_url, output_filename))
    else:
        # General case for any RPS value
        try:
            rps = int(request_mode_str)
            if rps <= 0: raise ValueError
        except ValueError:
            print(f"Error: Invalid request_mode '{request_mode_str}'. Must be '10' for the special test, or a positive integer for RPS.")
            sys.exit(1)

        # Determine filename based on submission requirement or general use
        if rps == 10000:
            output_filename = f"{roll_number}{platform}10000.txt"
        else:
            output_filename = f"rate_{rps}.txt"

        asyncio.run(run_high_load_test(full_url, output_filename, rps))
