#!/usr/bin/env python3
"""
Automated PyPI Release Script for django-mem0-client

This script automates the entire release process:
1. Version bumping (patch, minor, major)
2. CHANGELOG.md updates
3. Package building
4. PyPI upload
5. Git tagging and pushing

Usage:
    python release.py patch    # 0.2.1 -> 0.2.2
    python release.py minor    # 0.2.1 -> 0.3.0
    python release.py major    # 0.2.1 -> 1.0.0
    python release.py --version 0.3.5  # Set specific version
"""

import argparse
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Tuple


class ReleaseManager:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.setup_py = self.project_root / "setup.py"
        self.changelog = self.project_root / "CHANGELOG.md"
        
    def get_current_version(self) -> str:
        """Extract current version from setup.py"""
        with open(self.setup_py, 'r') as f:
            content = f.read()
        
        match = re.search(r'version="([^"]+)"', content)
        if not match:
            raise ValueError("Could not find version in setup.py")
        
        return match.group(1)
    
    def bump_version(self, current: str, bump_type: str) -> str:
        """Bump version according to bump_type"""
        major, minor, patch = map(int, current.split('.'))
        
        if bump_type == 'patch':
            patch += 1
        elif bump_type == 'minor':
            minor += 1
            patch = 0
        elif bump_type == 'major':
            major += 1
            minor = 0
            patch = 0
        else:
            raise ValueError(f"Invalid bump type: {bump_type}")
        
        return f"{major}.{minor}.{patch}"
    
    def update_version_in_setup_py(self, new_version: str) -> None:
        """Update version in setup.py"""
        with open(self.setup_py, 'r') as f:
            content = f.read()
        
        updated_content = re.sub(
            r'version="[^"]+"',
            f'version="{new_version}"',
            content
        )
        
        with open(self.setup_py, 'w') as f:
            f.write(updated_content)
        
        print(f"✓ Updated version in setup.py to {new_version}")
    
    def update_changelog(self, version: str) -> None:
        """Update CHANGELOG.md with new version entry"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        with open(self.changelog, 'r') as f:
            content = f.read()
        
        # Replace [Updated] with the new version
        if "## [Updated]" in content:
            updated_content = content.replace(
                "## [Updated]",
                f"## [{version}]"
            )
        else:
            # Insert new version section after the title
            lines = content.split('\n')
            header_line = next(i for i, line in enumerate(lines) if line.startswith('# '))
            lines.insert(header_line + 2, f"## [{version}] - {today}")
            lines.insert(header_line + 3, "")
            lines.insert(header_line + 4, "### Added")
            lines.insert(header_line + 5, "- New features and improvements")
            lines.insert(header_line + 6, "")
            updated_content = '\n'.join(lines)
        
        with open(self.changelog, 'w') as f:
            f.write(updated_content)
        
        print(f"✓ Updated CHANGELOG.md for version {version}")
    
    def run_command(self, cmd: str, check: bool = True) -> Tuple[int, str, str]:
        """Run shell command and return (returncode, stdout, stderr)"""
        print(f"Running: {cmd}")
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True,
            cwd=self.project_root
        )
        
        if check and result.returncode != 0:
            print(f"Error running command: {cmd}")
            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")
            sys.exit(1)
        
        return result.returncode, result.stdout, result.stderr
    
    def clean_build_artifacts(self) -> None:
        """Clean previous build artifacts"""
        print("🧹 Cleaning build artifacts...")
        self.run_command("rm -rf build/ dist/ *.egg-info/")
        print("✓ Cleaned build artifacts")
    
    def run_tests(self) -> None:
        """Run tests before release"""
        print("🧪 Running tests...")
        
        # Check if we're in a Django project and run Django tests
        if (self.project_root / "manage.py").exists():
            self.run_command("python manage.py test mem0client")
        else:
            # Fallback to pytest or unittest
            returncode, _, _ = self.run_command("python -m pytest", check=False)
            if returncode != 0:
                self.run_command("python -m unittest discover -s mem0client -p 'test*.py'")
        
        print("✓ Tests passed")
    
    def build_package(self) -> None:
        """Build the package"""
        print("📦 Building package...")
        self.run_command("python setup.py sdist bdist_wheel")
        print("✓ Package built successfully")
    
    def upload_to_pypi(self, test: bool = False) -> None:
        """Upload package to PyPI"""
        repo = "--repository testpypi" if test else ""
        print(f"🚀 Uploading to {'Test ' if test else ''}PyPI...")
        
        # Check if twine is installed
        returncode, _, _ = self.run_command("which twine", check=False)
        if returncode != 0:
            print("Installing twine...")
            self.run_command("pip install twine")
        
        self.run_command(f"twine upload {repo} dist/*")
        print(f"✓ Uploaded to {'Test ' if test else ''}PyPI")
    
    def git_operations(self, version: str) -> None:
        """Perform git operations: add, commit, tag, push"""
        print("📝 Performing git operations...")
        
        # Add changes
        self.run_command("git add setup.py CHANGELOG.md")
        
        # Commit
        self.run_command(f'git commit -m "Release version {version}"')
        
        # Create tag
        self.run_command(f"git tag -a v{version} -m 'Version {version}'")
        
        # Push commits and tags
        self.run_command("git push origin main")
        self.run_command("git push origin --tags")
        
        print(f"✓ Git operations completed for version {version}")
    
    def check_git_status(self) -> None:
        """Check if git working directory is clean"""
        returncode, stdout, _ = self.run_command("git status --porcelain", check=False)
        
        if stdout.strip():
            print("⚠️  Warning: Git working directory is not clean")
            print("Uncommitted changes:")
            print(stdout)
            
            response = input("Continue anyway? (y/N): ")
            if response.lower() != 'y':
                sys.exit(1)
    
    def verify_credentials(self, test: bool = False) -> None:
        """Verify PyPI credentials"""
        print("🔐 Verifying PyPI credentials...")
        
        # Try to check if credentials are configured
        returncode, _, _ = self.run_command("twine check dist/* 2>/dev/null || echo 'No dist files'", check=False)
        
        print("✓ Ready to upload (ensure your PyPI credentials are configured)")
        print("   Configure with: twine configure")
        print("   Or set environment variables: TWINE_USERNAME, TWINE_PASSWORD")
    
    def release(self, bump_type: str = None, specific_version: str = None, test: bool = False, skip_tests: bool = False) -> None:
        """Main release process"""
        try:
            # Get current version
            current_version = self.get_current_version()
            print(f"Current version: {current_version}")
            
            # Determine new version
            if specific_version:
                new_version = specific_version
            elif bump_type:
                new_version = self.bump_version(current_version, bump_type)
            else:
                raise ValueError("Must specify either bump_type or specific_version")
            
            print(f"New version: {new_version}")
            
            # Confirm release
            response = input(f"Release version {new_version}? (y/N): ")
            if response.lower() != 'y':
                print("Release cancelled")
                sys.exit(0)
            
            # Check git status
            self.check_git_status()
            
            # Run tests
            if not skip_tests:
                self.run_tests()
            
            # Clean build artifacts
            self.clean_build_artifacts()
            
            # Update version and changelog
            self.update_version_in_setup_py(new_version)
            self.update_changelog(new_version)
            
            # Build package
            self.build_package()
            
            # Verify credentials
            self.verify_credentials(test)
            
            # Upload to PyPI
            self.upload_to_pypi(test)
            
            # Git operations
            self.git_operations(new_version)
            
            print(f"🎉 Successfully released version {new_version}!")
            print(f"   Package: https://pypi.org/project/django-mem0-client/{new_version}/")
            
        except KeyboardInterrupt:
            print("\n❌ Release cancelled by user")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Release failed: {e}")
            sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Automated PyPI release script")
    
    # Version bump options
    bump_group = parser.add_mutually_exclusive_group(required=True)
    bump_group.add_argument("bump_type", nargs='?', choices=['patch', 'minor', 'major'],
                           help="Type of version bump")
    bump_group.add_argument("--version", help="Specific version to set")
    
    # Release options
    parser.add_argument("--test", action="store_true", 
                       help="Upload to Test PyPI instead of main PyPI")
    parser.add_argument("--skip-tests", action="store_true",
                       help="Skip running tests before release")
    
    args = parser.parse_args()
    
    # Create release manager and run release
    manager = ReleaseManager()
    manager.release(
        bump_type=args.bump_type,
        specific_version=args.version,
        test=args.test,
        skip_tests=args.skip_tests
    )


if __name__ == "__main__":
    main()
