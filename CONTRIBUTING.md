# Contributing to Home Assistant New Relic Addons

Thank you for your interest in contributing! This guide will help you get started.

## Development Setup

### Prerequisites

- Home Assistant (for testing)
- Docker (for building the addon)
- Python 3.11+ (for local development)
- New Relic account with API access

### Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/georgehill10/home-assistant-newrelic.git
   cd home-assistant-newrelic
   ```

2. Make your changes to the addon code in `newrelic-metrics/`

3. Test locally (see Testing section below)

### Testing

#### Option 1: Test in Home Assistant

1. Copy the `newrelic-metrics` folder to your Home Assistant addons directory:
   ```bash
   cp -r newrelic-metrics /path/to/homeassistant/addons/
   ```

2. Restart Home Assistant or reload addons

3. Install and configure the addon from the Supervisor panel

4. Check the addon logs for any errors

#### Option 2: Test the Python script directly

1. Create a test configuration file:
   ```bash
   mkdir -p /tmp/test-data
   cat > /tmp/test-data/options.json << EOF
   {
     "api_key": "YOUR_API_KEY",
     "account_id": "YOUR_ACCOUNT_ID",
     "update_interval": 60,
     "queries": [
       {
         "name": "test_metric",
         "nrql": "SELECT count(*) FROM Transaction SINCE 5 minutes ago"
       }
     ]
   }
   EOF
   ```

2. Set environment variables:
   ```bash
   export SUPERVISOR_TOKEN="your_supervisor_token"
   ```

3. Run the script:
   ```bash
   python3 newrelic-metrics/newrelic_sensor.py
   ```

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and single-purpose

### Commit Messages

Use clear, descriptive commit messages:
- `feat: Add support for custom time ranges`
- `fix: Handle empty query results correctly`
- `docs: Update configuration examples`
- `refactor: Simplify error handling logic`

## Reporting Issues

When reporting issues, please include:

1. **Addon version**
2. **Home Assistant version**
3. **Full error message** from addon logs
4. **Configuration** (with sensitive data removed)
5. **Expected behavior** vs actual behavior
6. **Steps to reproduce**

## Feature Requests

We welcome feature requests! Please:

1. Check existing issues first
2. Describe the use case
3. Explain the expected behavior
4. Provide examples if possible

## Pull Request Process

1. **Fork** the repository
2. **Create a branch** for your feature/fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Test thoroughly**
5. **Update documentation** if needed
6. **Commit your changes**
7. **Push to your fork**
8. **Create a Pull Request**

### Pull Request Guidelines

- Provide a clear description of the changes
- Reference any related issues
- Include test results or screenshots if applicable
- Update CHANGELOG.md with your changes
- Ensure all tests pass

## Development Guidelines

### Adding New Features

1. Ensure the feature aligns with the addon's purpose
2. Keep it simple and user-friendly
3. Document configuration options
4. Add examples to the documentation
5. Consider backwards compatibility

### Fixing Bugs

1. Identify the root cause
2. Add error handling if needed
3. Test the fix thoroughly
4. Document any behavior changes

### Improving Documentation

- Fix typos or unclear explanations
- Add more examples
- Improve troubleshooting guides
- Keep documentation up-to-date with code

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Provide constructive feedback
- Focus on the issue, not the person
- Assume good intentions

## Questions?

If you have questions about contributing:
- Open a GitHub issue
- Check existing documentation
- Review closed issues for similar questions

Thank you for contributing!
