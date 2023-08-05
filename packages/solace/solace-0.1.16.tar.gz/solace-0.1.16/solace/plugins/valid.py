""" Simple Data Validator Plugin for Solace """

from solace.context import Context
from solace.validator import SolaceValidator

async def is_valid_json(ctx: Context) -> Context:
    ctx.trace("start of is_valid_json plugin")
    async def is_valid_json_handler(validator: SolaceValidator) -> bool:
        # TODO: check if there is JSON data
        # and handle the case where there is no JSON present.
        json_data = await ctx.request.json()
        return validator(json_data)
    ctx.is_valid_json = is_valid_json_handler
    ctx.trace("end of is_valid_json")
    return ctx

async def is_valid_form(ctx: Context) -> Context:
    ctx.trace("start of is_valid_form plugin")
    # TODO: check if there is FORM data
    # and handle the case where there is no FORM present.
    async def is_valid_form_handler(validator: SolaceValidator) -> bool:
        form_data = await ctx.request.form()
        return validator(form_data)
    ctx.is_valid_form = is_valid_form_handler
    ctx.trace("end of is_valid_form plugin")
    return ctx
