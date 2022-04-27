def create_recipe_ingredients(ingredients_queryset):
    return_result = []

    for ingredient in ingredients_queryset:
        name = ingredient.name
        amount = ingredient.amount

        full_ingredient_info = f'{name}: {amount} gr.'
        return_result.append(full_ingredient_info)

    return '; '.join(return_result)
