#!/usr/bin/env python3
import sys
import os
import pytest
import argparse
import coverage
from datetime import datetime

def setup_test_environment():
    """Set up the test environment"""
    # Ensure test data directory exists
    os.makedirs('tests/data', exist_ok=True)
    
    # Set environment variables for testing
    os.environ['TEST_ENV'] = 'testing'
    os.environ['TEST_DATA_DIR'] = os.path.abspath('tests/data')

def run_tests(args):
    """Run the test suite with specified options"""
    test_args = [
        '--verbose',
        '--strict-markers',
        '-ra',  # Show extra test summary info
        '--tb=short',  # Shorter traceback format
    ]

    # Add coverage options if requested
    if args.coverage:
        test_args.extend([
            '--cov=.',
            '--cov-report=term-missing',
            '--cov-report=html',
            '--no-cov-on-fail'
        ])

    # Add parallel execution if requested
    if args.parallel:
        test_args.extend(['-n', 'auto'])

    # Add specific test markers if provided
    if args.markers:
        test_args.extend(['-m', args.markers])

    # Add specific test paths if provided
    if args.test_path:
        test_args.extend(args.test_path)
    else:
        test_args.append('tests/')

    # Generate test report
    if args.report:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_dir = f'test_reports/report_{timestamp}'
        os.makedirs(report_dir, exist_ok=True)
        test_args.extend([
            f'--html={report_dir}/report.html',
            f'--junitxml={report_dir}/junit.xml'
        ])

    # Run the tests
    return pytest.main(test_args)

def cleanup_test_environment():
    """Clean up after test execution"""
    # Clean up any temporary files or test artifacts
    temp_files = [
        'tests/data/messages.json',
        'tests/data/tasks.json',
        'tests/data/notes.json',
        'tests/data/contributions.json'
    ]
    
    for file in temp_files:
        if os.path.exists(file):
            os.remove(file)

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Run the test suite')
    
    parser.add_argument(
        '--coverage',
        action='store_true',
        help='Run tests with coverage reporting'
    )
    
    parser.add_argument(
        '--parallel',
        action='store_true',
        help='Run tests in parallel'
    )
    
    parser.add_argument(
        '--markers',
        type=str,
        help='Run tests with specific markers (e.g., "not slow")'
    )
    
    parser.add_argument(
        '--report',
        action='store_true',
        help='Generate HTML and JUnit XML test reports'
    )
    
    parser.add_argument(
        '--test-path',
        nargs='+',
        help='Specific test paths to run'
    )
    
    return parser.parse_args()

def main():
    """Main entry point"""
    try:
        # Parse command line arguments
        args = parse_arguments()
        
        # Set up test environment
        setup_test_environment()
        
        # Run the tests
        result = run_tests(args)
        
        # Clean up
        cleanup_test_environment()
        
        # Exit with test result
        sys.exit(result)
        
    except KeyboardInterrupt:
        print("\nTest execution interrupted by user")
        cleanup_test_environment()
        sys.exit(1)
    except Exception as e:
        print(f"\nError running tests: {str(e)}")
        cleanup_test_environment()
        sys.exit(1)

if __name__ == '__main__':
    main()
