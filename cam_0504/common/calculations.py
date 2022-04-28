def get_price_in_stotinki(price_in_leva):
    price_in_stotinki = price_in_leva * 100
    return price_in_stotinki


def get_price_for_one_unit(type_of_food, price_in_leva):
    price_in_stotinki = get_price_in_stotinki(price_in_leva)

    if type_of_food == 'Piece':
        return price_in_stotinki

    price_for_one_unit = price_in_stotinki / 1000
    return price_for_one_unit


def increase_value_by_percent(initial_value, percentage):
    if percentage == 0:
        return initial_value

    value_to_add = initial_value * (percentage / 100)
    increased_value = initial_value + value_to_add
    return increased_value


def calculate_price_return_in_leva(recipe_increase_percentage, ingredients):
    final = 0
    for ingredient in ingredients:
        ingredient_price_per_type = ingredient.ingredient.price_per_type
        ingredient_type = ingredient.ingredient.type
        ingredient_amount = ingredient.amount

        price_for_one_unit = get_price_for_one_unit(ingredient_type, ingredient_price_per_type)
        el_final_price = float(ingredient_amount) * float(price_for_one_unit)
        final += el_final_price
    end_price = final / 100
    increased_end_price = increase_value_by_percent(end_price, recipe_increase_percentage)
    return end_price, increased_end_price
