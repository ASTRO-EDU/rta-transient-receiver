#!/bin/bash

set -e 

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

test_dir=$script_dir/voeventhandler/test
printf "test_dir: $test_dir\n"

junit_tests_report_dir="$test_dir/test_logs/junit_reports"
mkdir -p "$junit_tests_report_dir"
rm -f "$junit_tests_report_dir/*"

coverage_report_dir="$test_dir/test_logs/coverage_reports"
mkdir -p "$coverage_report_dir"
rm -f "$coverage_report_dir/*"

python3 -m pytest -v -W ignore::DeprecationWarning --junitxml="$junit_tests_report_dir/unit_report.xml" --cov-config=$test_dir/.coveragerc --cov=$test_dir/../ $test_dir

echo "Code coverage report conversion in JUnit and HTML formats.."
coverage xml -o "$coverage_report_dir/coverage_report.xml"
coverage html -d "$coverage_report_dir/coverage_report_html"
printf "Test results: $junit_tests_report_dir \n"
printf "Coverage report: $coverage_report_dir \n"
