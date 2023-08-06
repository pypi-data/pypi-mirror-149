# -*- coding: UTF-8 -*-  
def before_all(context):
    # Seed empty data so steps do not need to check and create.
    context.db_config = {}

