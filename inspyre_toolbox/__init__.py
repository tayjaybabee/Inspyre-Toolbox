from inspyre_toolbox.core_helpers.logging import ROOT_ISL_DEVICE
from inspyre_toolbox.version_info import VERSION, FULL

LOG_DEVICE = ROOT_ISL_DEVICE

LOG = LOG_DEVICE.add_child(f'{__name__}')

if VERSION.pre_release:
    LOG.info(f"{FULL} ({VERSION.pr_full})")
    if VERSION.pr_type == 'dev':
        LOG.warning(f"{VERSION.pr_full} is a development version. ")
        LOG.warning("It is not recommended to use this version.")
        ROOT_ISL_DEVICE.adjust_level('debug')

LOG.debug('Inspyre Toolbox loaded.')
