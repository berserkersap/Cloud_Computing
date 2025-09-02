import requests
import time
import sys
import atexit
import asyncio

async def send_request(session, url, payload):
    """Helper function to send a single async request."""
    request_start_time = time.time()
    try:
        async with session.post(url, json=payload, timeout=10) as response:
            response.raise_for_status()
            elapsed = time.time() - request_start_time
            return elapsed
    except Exception as e:
        print(f"An error occurred: {e}")
        return -1.0

async def run_test_async(server_url, rps, output_file):
    """
    Sends requests to the server at a specified rate and logs response times.
    This version uses asyncio and aiohttp for better performance at high RPS.
    """
    # aiohttp is needed for high-concurrency async requests.
    # It needs to be installed: pip install aiohttp
    import aiohttp

    print(f"Starting async test: Server URL='{server_url}', RPS={rps}, Output File='{output_file}'")
    
    duration = 60  # Run for 60 seconds
    total_requests = rps * duration
    
    payload = {"data": "This is a test string for the cloud computing assignment using FastAPI."}
    
    response_times = []

    def calculate_average():
        """Function to be called on script exit."""
        if response_times:
            valid_times = [t for t in response_times if t > 0]
            if valid_times:
                average_time = sum(valid_times) / len(valid_times)
                print("\n--- Test Finished ---")
                print(f"Total requests attempted: {len(response_times)}")
                print(f"Successful requests: {len(valid_times)}")
                print(f"Average Response Time: {average_time:.6f} seconds")
                with open("Output_fastapi.txt", "a") as f:
                    f.write(f"<{rps}, {average_time:.6f}>\n")

    atexit.register(calculate_average)

    start_time = time.time()
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(total_requests):
            task = asyncio.ensure_future(send_request(session, server_url, payload))
            tasks.append(task)
            # This simple sleep pattern helps in distributing requests over time.
            # For very high RPS, more sophisticated throttling might be needed.
            await asyncio.sleep(1.0 / rps)
        
        # Wait for all tasks to complete
        results = await asyncio.gather(*tasks)
        response_times.extend(results)

    # Write all results to file at the end
    with open(output_file, 'w') as f:
        for t in response_times:
            f.write(f"{t:.6f}\n")

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python fastapi_client.py <server_url> <requests_per_second> <output_file>")
        print("Note: Requires 'aiohttp' library. Install with 'pip install aiohttp'")
        sys.exit(1)
        
    server_endpoint = sys.argv[1] + '/encode'
    requests_per_second = int(sys.argv[2])
    output_filename = sys.argv[3]
    
    # Run the asynchronous test
    asyncio.run(run_test_async(server_endpoint, requests_per_second, output_filename))
