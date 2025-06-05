# Terminal REST Client

A simple, terminal-based REST API client implemented in Python. This script allows you to send HTTP requests to specified URLs, view formatted responses (including headers and body), and save them to a file. It's a lightweight alternative to tools like cURL for basic API testing and interaction directly from your command line.

## Features

- Supports common HTTP methods: GET, POST, PUT, DELETE, PATCH.
- Allows adding custom request headers.
- Supports sending raw data (`-d`) or JSON (`-j`) in the request body for methods like POST, PUT, and PATCH.
- Automatically sets `Content-Type: application/json` when JSON data is provided.
- Formats and prints the full HTTP response (status line, headers, and body).
- Pretty-prints JSON responses.
- Allows saving the complete response to a specified output file (`-o`).
- Verbose mode (`-v`) to print request details before sending.

## Usage

Here are some examples of how to use the `rest_client.py` script:

**1. Simple GET Request:**
```bash
python rest_client.py https://jsonplaceholder.typicode.com/todos/1
```

**2. POST Request with JSON Data:**
```bash
python rest_client.py https://jsonplaceholder.typicode.com/posts -m POST -j '{"title": "foo", "body": "bar", "userId": 1}'
```

**3. Adding Custom Headers:**
```bash
python rest_client.py https://api.example.com/data -H "Authorization: Bearer yourtoken" -H "X-Custom-Header: value"
```

**4. Sending Raw Data:**
```bash
python rest_client.py https://api.example.com/submit -m POST -d "raw data string"
```

**5. Saving Response to a File:**
```bash
python rest_client.py https://jsonplaceholder.typicode.com/comments -o comments_response.txt
```

**6. Verbose Mode:**
```bash
python rest_client.py https://jsonplaceholder.typicode.com/users/1 -v
```

## Command-line Arguments

The script accepts the following command-line arguments:

- `url`: (Required) The URL for the API request.
- `-m, --method {GET,POST,PUT,DELETE,PATCH}`: The HTTP method to use (default: GET).
- `-H, --header HEADER`: Add a custom header to the request (e.g., 'Authorization: Bearer token'). Can be specified multiple times.
- `-d, --data DATA`: Raw data to send in the request body. For POST, PUT, PATCH methods.
- `-j, --json JSON_DATA`: JSON data to send in the request body. Automatically sets Content-Type to application/json. For POST, PUT, PATCH methods.
- `-o, --output FILEPATH`: Path to a file where the full response (status, headers, body) will be saved.
- `-v, --verbose`: Print verbose output, including request details.

## License

This project is licensed under the MIT License. (You can replace this with your preferred license if different.)
