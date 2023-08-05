# /*******************************************************************************
#  * Copyright (c) 2021 Push Technology Ltd., All Rights Reserved.
#  *
#  * Use is subject to license terms.
#  *
#  * NOTICE: All information contained herein is, and remains the
#  * property of Push Technology. The intellectual and technical
#  * concepts contained herein are proprietary to Push Technology and
#  * may be covered by U.S. and Foreign Patents, patents in process, and
#  * are protected by trade secret or copyright law.
#  *******************************************************************************/
from diffusion import DiffusionError


class InvalidBranchMappingException(DiffusionError):
    """
    Exception indicating an invalid BranchMapping or
    BranchMappingTable.

    See Also: SessionTrees
    """
