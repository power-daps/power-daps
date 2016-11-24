import common
import actions
from actions import deps_action, unit_test_action, package_action

def run():
    common.stop_if_failed(*deps_action.run())
    common.stop_if_failed(*unit_test_action.run())
    common.stop_if_failed(*package_action.run())

    return 0, ""

