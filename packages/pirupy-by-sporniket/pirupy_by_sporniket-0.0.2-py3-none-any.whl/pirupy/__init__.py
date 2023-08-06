"""
---
(c) 2022 David SPORN
---
This file is part of PIRUPY.

PIRUPY is free software: you can redistribute it and/or modify it under the terms of
the GNU General Public License as published by the Free Software Foundation, either
version 3 of the License, or (at your option) any later version.

PIRUPY is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with PIRUPY.
If not, see <https://www.gnu.org/licenses/>. 
---
"""
from .piru import *

__all__ = [
    'pipeline', 'job',
    'before_all', 'after_all',
    'before_each', 'after_each'
]
