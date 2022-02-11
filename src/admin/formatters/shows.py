from app.models.shows import ShowType


def format_date(view, context, model, name):
    return getattr(model, name).strftime("%B %d, %Y")


def format_duration(view, context, model, name):
    duration = getattr(model, name)
    return f"{duration} minute(s)" if model.type == ShowType.MOVIE else f"{duration} season(s)"


def format_rating(view, context, model, name):
    rating = getattr(model, name)
    return rating.code if rating is not None else "-"


def format_type(view, context, model, name):
    return getattr(model, name).value


def format_listed_in(view, context, model, name):
    return ", ".join([genre.name for genre in getattr(model, name)])


def format_title(view, context, model, name):
    return getattr(model, name)
