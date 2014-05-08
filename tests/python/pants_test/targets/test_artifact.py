# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

from pants.targets.artifact import Artifact
from pants.targets.repository import Repository

from pants_test.testutils.base_test import BaseTest


class ArtifactTest(BaseTest):

  def test_validation(self):
    repo = self.make_target(target_type=Repository,
                            spec=":myRepo",
                            url="myUrl",
                            push_db="myPushDb")
    Artifact(org="testOrg", name="testName", repo=repo, description="Test")
    self.assertRaises(ValueError, Artifact,
                      org=1, name="testName", repo=repo, description="Test")
    self.assertRaises(ValueError, Artifact,
                      org="testOrg", name=1, repo=repo, description="Test")
    # This fails right now because of the horrible hack to make Respository
    # addressable
    # self.assertRaises(ValueError, Artifact,
    #                   org="testOrg", name="testName", repo=1, description="Test")
    self.assertRaises(ValueError, Artifact,
                      org="testOrg", name="testName", repo=repo, description=1)
