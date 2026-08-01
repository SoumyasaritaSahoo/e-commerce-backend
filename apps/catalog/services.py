"""Business logic for catalog, called from views.py.

Views stay thin (parse request -> call a function here -> return a
serialized response); other apps import from here, never from
catalog/models.py directly, per docs/10-project-structure.md.
"""
