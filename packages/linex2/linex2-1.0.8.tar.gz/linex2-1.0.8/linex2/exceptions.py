# This file includes code from:
# LINEX webtool
# Copyright (C) 2021  LipiTUM group, Chair of experimental Bioinformatics, Technical University of Munich
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from typing import Union, Tuple


class ParsingError(Exception):
    pass

class MolecularSpeciesError(Exception):
    pass

class ReferenceLipidError(Exception):
    pass

class MappingError(Exception):
    pass


class InputDataError(Exception):
    def __init__(self, message):
        super(InputDataError, self).__init__(message)
        self.message = message


class NotComputedError(Exception):
    def __init__(self, attribute_name: str,
                 function_name: Union[str, Tuple[str]] = None,
                 for_subset: bool = False):
        if function_name is None:
            super(NotComputedError, self).__init__(
                attribute_name
            )
        else:
            if for_subset:
                message = f"{attribute_name} has not been computed for {function_name}"
            else:
                message = f"{attribute_name} has not been computed yet,"\
                          f" please call {function_name} first!"
            super(NotComputedError, self).__init__(message)


class CorrelationError(Exception):
    def __init__(self, message, lipids):
        super(CorrelationError, self).__init__(message)

        self.lipids = lipids
        self.message = message


class PartialCorrelationError(Exception):
    def __init__(self, message, solver):
        super(PartialCorrelationError, self).__init__(message)

        self.solver = solver
        self.message = message


class SignificanceTestError(Exception):
    def __init__(self, message):
        super(SignificanceTestError, self).__init__(message)
