"""Business logic for accounts, called from views.py.

Views stay thin (parse request -> call a function here -> return a
serialized response); other apps import from here, never from
accounts/models.py directly, per docs/10-project-structure.md.
"""
