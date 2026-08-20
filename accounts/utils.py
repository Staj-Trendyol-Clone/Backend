def set_attributes(instance, data, exclude=[]):
  for key, value in data.items():
    if key in exclude or not value:
      continue
    setattr(instance, key, value)