"""
Legal Agent - نظام إدارة البيانات القانونية
"""

__version__ = "1.0.0"
__author__ = "Legal Agent Team"

from .agent import LegalAgent
from .github_sync import GitHubSync

__all__ = ["LegalAgent", "GitHubSync"]
