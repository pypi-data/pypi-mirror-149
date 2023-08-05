""" All constants needed for signal operations, can be called outside of this package
"""
from mongoengine import signals


pre_init = signals.pre_init
post_init = signals.post_init
pre_save = signals.pre_save
pre_save_post_validation = signals.pre_save_post_validation
post_save = signals.post_save
pre_delete = signals.pre_delete
post_delete = signals.post_delete
pre_bulk_insert = signals.pre_bulk_insert
post_bulk_insert = signals.post_bulk_insert
