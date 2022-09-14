# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

import math
import numpy as np
import rpy2
from rpy2.robjects.packages import importr
from rpy2.robjects import r
from rpy2.robjects import IntVector
from nltk.corpus import stopwords


rpy2.robjects.r['options'](warn=-1)
importr("lpSolve")
importr("irr")


def kripp_alpha(m, voters, type="nominal", byrow=True):
    """
    :param m: a list containing the annotations labels
    :param voters: number of annotators
    :param type: type of difference function https://en.wikipedia.org/wiki/Krippendorff%27s_alpha
    :param byrow: if it is TRUE:
        the input m has to have this shape [A1_1, A1_2, A2_1, A2_2,...] AX_Y where X is the annotator id and Y is the item id
        if it is FALSE:
        the input m has to have this shape [A1_1, A2_1, A1_2, A2_2,...] AX_Y where X is the annotator id and Y is the item id
    :return:
    """
    mat = r.matrix(IntVector(m), nrow=voters, byrow=byrow) # Rows annotators, Items column
    alpha = r["kripp.alpha"](mat, type)
    return list(dict(zip(alpha.names, list(alpha)))['value'])[0]

def fleiss_R(m, voters, byrow=True):
    """
        :param m: a list containing the annotations labels
        :param voters: number of annotators
        :param byrow: if it is TRUE:
            the input m has to have this shape [A1_1, A1_2, A2_1, A2_2,...] AX_Y where X is the annotator id and Y is the item id
            if it is FALSE:
            the input m has to have this shape [A1_1, A2_1, A1_2, A2_2,...] AX_Y where X is the annotator id and Y is the item id
        :return:
    """
    mat = r["t"](r.matrix(IntVector(m), nrow=voters, byrow=byrow))
    alpha = r["kappam.fleiss"](mat)
    return list(dict(zip(alpha.names, list(alpha)))['value'])[0]
