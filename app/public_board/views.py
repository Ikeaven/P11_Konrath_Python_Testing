from flask import render_template
from . import public_board

from .. import clubs


@public_board.route("/clubs_list")
def clubs_list():
    return render_template("clubs_list.html", clubs=clubs)
