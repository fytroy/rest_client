import requests
import argparse
import json
import sys

def parse_headers(header_args):
    """Parses a list of header strings (e.g., 'Content-Type: application/json') into a dictionary."""
    headers = {}
    if header_args:
        for h in header_args:
            if ':' in h:
                key, value = h.split(':', 1)
                headers[key.strip()] = value.strip()
            else:
                print(f"Warning: Invalid header format '{h}'. Expected 'Key: Value'. Skipping.", file=sys.stderr)
    return headers

def format_response(response):
    """Formats the requests.Response object into a human-readable string, including headers."""
    formatted_output = []

    # Status Line
    formatted_output.append(f"HTTP/1.1 {response.status_code} {response.reason}")

    # Headers
    for header, value in response.headers.items():
        formatted_output.append(f"{header}: {value}")

    formatted_output.append("") # Empty line to separate headers from body

    # Body
    try:
        if response.headers.get('Content-Type', '').startswith('application/json'):
            formatted_output.append(json.dumps(response.json(), indent=2))
        else:
            formatted_output.append(response.text)
    except json.JSONDecodeError:
        formatted_output.append(response.text) # Fallback if not valid JSON

    return "\n".join(formatted_output)

def main():
    parser = argparse.ArgumentParser(
        description="A terminal-based REST API client to send requests and save responses."
    )

    parser.add_argument(
        "url",
        help="The URL for the API request."
    )
    parser.add_argument(
        "-m", "--method",
        choices=["GET", "POST", "PUT", "DELETE", "PATCH"],
        default="GET",
        help="The HTTP method to use (default: GET)."
    )
    parser.add_argument(
        "-H", "--header",
        action="append",
        help="Add a custom header to the request (e.g., 'Authorization: Bearer token'). Can be specified multiple times."
    )
    parser.add_argument(
        "-d", "--data",
        help="Raw data to send in the request body. For POST, PUT, PATCH methods."
    )
    parser.add_argument(
        "-j", "--json",
        help="JSON data to send in the request body. Automatically sets Content-Type to application/json. For POST, PUT, PATCH methods."
    )
    parser.add_argument(
        "-o", "--output",
        help="Path to a file where the full response (status, headers, body) will be saved."
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Print verbose output, including request details."
    )

    args = parser.parse_args()

    # Prepare headers
    headers = parse_headers(args.header)

    # Prepare data/json
    request_data = None
    request_json = None

    if args.json:
        try:
            request_json = json.loads(args.json)
            headers['Content-Type'] = headers.get('Content-Type', 'application/json')
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON provided for --json: {args.json}", file=sys.stderr)
            sys.exit(1)
    elif args.data:
        # Try to parse as JSON first, otherwise send as raw string
        try:
            request_json = json.loads(args.data)
            headers['Content-Type'] = headers.get('Content-Type', 'application/json')
        except json.JSONDecodeError:
            request_data = args.data

    if args.verbose:
        print(f"Request Method: {args.method}")
        print(f"Request URL: {args.url}")
        print(f"Request Headers: {json.dumps(headers, indent=2)}")
        if request_json:
            print(f"Request JSON Body: {json.dumps(request_json, indent=2)}")
        elif request_data:
            print(f"Request Raw Data Body: {request_data}")
        print("-" * 40)

    try:
        response = requests.request(
            method=args.method,
            url=args.url,
            headers=headers,
            data=request_data,
            json=request_json
        )

        formatted_res = format_response(response)

        # Print to terminal
        print(formatted_res)

        # Save to file if output path is provided
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(formatted_res)
            print(f"\nResponse successfully saved to: {args.output}")

    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()