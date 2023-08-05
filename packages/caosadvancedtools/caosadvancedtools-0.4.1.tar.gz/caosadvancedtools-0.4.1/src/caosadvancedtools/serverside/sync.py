#!/usr/bin/env python3
# Sync data model for generic data analysis method
# A. Schlemmer, 09/2021

from caosadvancedtools.models import parser
model = parser.parse_model_from_yaml("model.yml")
model.sync_data_model()
