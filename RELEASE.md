# Release Process Documentation

This document describes the automated release process for the django-mem0-client package.

## Prerequisites

1. **PyPI Account**: You need an account on [PyPI](https://pypi.org/)
2. **API Token**: Create an API token in your PyPI account settings
3. **Git Repository**: Ensure your code is committed and pushed to the main branch
4. **Dependencies**: Install required tools:
   ```bash
   pip install twine build wheel
   ```

## Configuration

### 1. PyPI Credentials

Configure your PyPI credentials using one of these methods:

**Method A: Environment Variables**
```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=your-pypi-api-token
```

**Method B: Twine Configuration**
```bash
twine configure
```

**Method C: .pypirc file**
Create `~/.pypirc`:
```ini
[distutils]
index-servers = pypi

[pypi]
username = __token__
password = your-pypi-api-token
```

### 2. GitHub Secrets (for automated releases)

Add these secrets to your GitHub repository:
- `PYPI_API_TOKEN`: Your PyPI API token

## Release Methods

### Method 1: Manual Release (Recommended)

Use the automated release script:

```bash
# Patch release (0.2.1 -> 0.2.2)
python release.py patch

# Minor release (0.2.1 -> 0.3.0)
python release.py minor

# Major release (0.2.1 -> 1.0.0)
python release.py major

# Specific version
python release.py --version 1.0.0

# Test release (uploads to Test PyPI)
python release.py patch --test

# Skip tests during release
python release.py patch --skip-tests
```

### Method 2: Using Makefile

```bash
# Show available commands
make help

# Patch release
make release-patch

# Minor release
make release-minor

# Major release
make release-major

# Test release
make release-test
```

### Method 3: GitHub Actions (Automatic)

Automatic releases are triggered when you push a git tag:

```bash
# Create and push a tag
git tag v0.2.2
git push origin v0.2.2
```

This will automatically:
1. Run tests across multiple Python/Django versions
2. Build the package
3. Upload to PyPI

## What the Release Script Does

The `release.py` script automates the entire release process:

1. **Version Management**:
   - Reads current version from `setup.py`
   - Bumps version according to semver rules
   - Updates `setup.py` with new version

2. **Changelog Updates**:
   - Updates `CHANGELOG.md` with new version and date
   - Replaces `[Updated]` section with proper version

3. **Quality Checks**:
   - Runs tests to ensure code quality
   - Checks git working directory status
   - Verifies PyPI credentials

4. **Package Building**:
   - Cleans previous build artifacts
   - Creates source distribution (`sdist`)
   - Creates wheel distribution (`bdist_wheel`)

5. **Publishing**:
   - Uploads to PyPI (or Test PyPI)
   - Provides package URL for verification

6. **Git Operations**:
   - Commits version changes
   - Creates annotated git tag
   - Pushes commits and tags to origin

## Manual Release Steps

If you prefer manual control:

```bash
# 1. Clean build artifacts
make clean

# 2. Run tests
make test

# 3. Update version in setup.py manually

# 4. Update CHANGELOG.md manually

# 5. Build package
make build

# 6. Upload to PyPI
twine upload dist/*

# 7. Git operations
git add setup.py CHANGELOG.md
git commit -m "Release version X.Y.Z"
git tag -a vX.Y.Z -m "Version X.Y.Z"
git push origin main --tags
```

## Testing Releases

Before publishing to the main PyPI, test your release:

```bash
# Upload to Test PyPI
python release.py patch --test

# Install from Test PyPI to verify
pip install --index-url https://test.pypi.org/simple/ django-mem0-client
```

## Version Numbering

This project follows [Semantic Versioning](https://semver.org/):

- **MAJOR** (X.0.0): Incompatible API changes
- **MINOR** (0.X.0): New functionality, backward compatible
- **PATCH** (0.0.X): Bug fixes, backward compatible

## Troubleshooting

### Common Issues

1. **Twine Upload Failed**:
   - Check PyPI credentials
   - Ensure package name is available
   - Verify version number is unique

2. **Tests Failed**:
   - Fix failing tests before release
   - Use `--skip-tests` flag only for emergency releases

3. **Git Issues**:
   - Ensure working directory is clean
   - Check git remote configuration
   - Verify push permissions

4. **Build Issues**:
   - Check `setup.py` configuration
   - Ensure all files are included in `MANIFEST.in`
   - Verify dependencies in `requirements.txt`

### Getting Help

- Check package on PyPI: https://pypi.org/project/django-mem0-client/
- View GitHub releases: https://github.com/xjodoin/django-mem0-client/releases
- Test PyPI: https://test.pypi.org/project/django-mem0-client/

## File Structure

```
django-mem0-client/
├── release.py              # Main release script
├── Makefile               # Convenience commands
├── MANIFEST.in            # Package file inclusion rules
├── requirements.txt       # Dependencies
├── setup.py              # Package configuration
├── CHANGELOG.md          # Version history
├── .github/
│   └── workflows/
│       └── release.yml   # GitHub Actions workflow
└── mem0client/           # Package source code
```

## Security Notes

- Never commit PyPI credentials to git
- Use API tokens instead of passwords
- Rotate API tokens periodically
- Use Test PyPI for testing releases
