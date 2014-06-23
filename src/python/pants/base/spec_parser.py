# coding=utf-8
# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

import os

from pants.base.address import BuildFileAddress, parse_spec
from pants.base.build_file import BuildFile


class SpecParser(object):
  """Parses goal target specs; either simple target addresses or else sibling (:) or descendant
  (::) selector forms
  """

  def __init__(self, root_dir, address_map):
    self._root_dir = root_dir
    self._address_map = address_map

  # DEPRECATED!  Specs with BUILD files in them shouldn't be allowed.
  def _get_dir(self, spec):
    path = spec.split(':', 1)[0]
    if os.path.isdir(path):
      return path
    else:
      if os.path.isfile(path):
        return os.path.dirname(path)
      else:
        return spec

  def parse_addresses(self, spec):
    if spec.endswith('::'):
      addresses = set()
      spec_rel_dir = self._get_dir(spec[:-len('::')])
      spec_dir = os.path.join(self._root_dir, spec_rel_dir)
      for root, _, _ in os.walk(spec_dir):
        build_file = BuildFile.from_cache(self._root_dir,
                                          os.path.join(spec_dir, root),
                                          must_exist=False)
        if build_file.exists():
          addresses.update(self._address_map.addresses_in_spec_path(build_file.spec_path))
      return addresses
    elif spec.endswith(':'):
      spec_rel_dir = self._get_dir(spec[:-len(':')])
      spec_dir = os.path.join(self._root_dir, spec_rel_dir)
      return set(self._address_map.addresses_in_spec_path(spec_dir))
    else:
      spec_path, target_name = parse_spec(spec)
      build_file = BuildFile(self._root_dir, spec_path)
      return set([BuildFileAddress(build_file, target_name)])

