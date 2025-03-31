"""
    Module Name: Routes

    Description:
        Contains the web application routes.

    Author: Liav Barsheshet [312429269], Elshan Getdarov [313735136].
    Date: 09/10/2024.
"""
# Module Imports
from modules.synthesizer import Synthesizer

# Imports
from flask import Blueprint, render_template, request, jsonify, send_from_directory
from datetime import datetime
import re

# Creating entries.
app_routes = Blueprint('app_routes', __name__)


# Route for synthesize playground.
@app_routes.post('/synthesize')
def synthesize():
    # Parse the request body
    body = request.get_json()

    # Creating data env.
    data = {
        "program": body.get("program"),
        "linv": body.get("linv"),
        "p": [],
        "q": [],
    }

    # Parsing Inputs
    for key, value in body.items():
        match = re.match(r'^p(\d+)$', key)
        if not match:
            continue

        digit = match.group(1)

        data['p'].append(body.get(f"p{digit}"))
        data['q'].append(body.get(f"q{digit}"))

    # Insert Inputs
    synthesizer = Synthesizer(data)

    try:
        # Start Synthesizing.
        return synthesizer.synthesize()
    except Exception as e:
        return synthesizer.response.failed("Oops something went wrong!", synthesizer.logs + [f"Error: {str(e)}"])


# Route for benchmarks.
@app_routes.post('/benchmark')
def do_benchmark():
    # Parse the request body
    body = request.get_json()

    # Collecting tests
    tests = list((body["tests"]))

    # Stamping the initial time.
    bench_begin = datetime.now()

    # Test Results
    result = []

    try:
        for test in tests:
            start = datetime.now()

            # Creating synthesizer instance.
            synthesizer = Synthesizer(test)

            # Getting Benchmark Results
            output = synthesizer.synthesize(True)

            elapsed = (datetime.now() - start).total_seconds()

            # Collecting current test result.
            result.append({"elapsed": elapsed, "success": list(output) == test["assert"]})

        return jsonify({
            "result": result,
            "duration": (datetime.now() - bench_begin).total_seconds()
        }), 200

    except Exception as e:
        return jsonify({
            "error": str(e),
        }), 200


# Bench Route
@app_routes.get('/benchmark')
def benchmark():
    return render_template('bench.html')


# Readme Route
@app_routes.get('/readme')
def readme():
    return send_from_directory('./', 'README.md')


# Index Route
@app_routes.route('/')
def homepage():
    return render_template('index.html')


# Handles 404
@app_routes.app_errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app_routes.app_errorhandler(500)
def not_found_error(error):
    return render_template('500.html', error=str(error)), 500
