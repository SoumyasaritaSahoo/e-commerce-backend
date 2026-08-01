"""Shared non-enum constants reused across multiple apps.

Empty for now — every concrete config value that exists today (JWT
lifetimes, DRF page size, etc.) already lives in config/settings/base.py,
which is the correct single source of truth for those. Add an entry here
only once an actual cross-app constant is needed (e.g. a shared limit or
default referenced by more than one app's code, not settings).
"""
