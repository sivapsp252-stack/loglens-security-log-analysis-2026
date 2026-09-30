# LogLens – Simplified Security Log Analysis

LogLens is a cybersecurity project that analyzes web server security logs and detects common attack patterns.

## Project Overview

LogLens reads Apache/Nginx-style Common Log Format logs, extracts important request information, detects suspicious activity, and displays the results through a security dashboard.

The project is designed to process logs line-by-line so that large log files do not need to be loaded completely into memory.

## Features

### 1. Log Parser

The parser extracts:

- IP address
- Timestamp
- HTTP method
- Request path
- HTTP status code
- User agent

The parser processes the log file line-by-line.

### 2. Threat Detection

LogLens detects the following attack types:

- SQL Injection
- Cross-Site Scripting (XSS)
- Directory Traversal
- Brute Force Login Attempts

Detected attacks are assigned a severity level.

### 3. Security Dashboard

The React dashboard displays:

- Total requests
- Total detected attacks
- Attack rate
- Attack types
- Attacks per hour
- GeoIP attack locations
- Top attacking IP addresses

### 4. GeoIP

LogLens uses the MaxMind GeoLite2 City database to obtain approximate geographic information for public IP addresses.

Private or unknown IP addresses may not have geographic information.

### 5. Asynchronous Log Analysis

Large uploaded log files are processed asynchronously.

The workflow is:

```text
Upload Log
    ↓
Job ID
    ↓
Background Processing
    ↓
Poll Job Status
    ↓
Analysis Result
    ↓
Dashboard