from lightweb4py.persistence import Persistence


# Build a list of categories to display in web form's drop-down list boxes;
# put the item's category at the top of the list if it has a category, then put an empty category
# and the rest of the categories;
# if the item doesn't have a category, put an empty category at the top of the list
# and the rest of the categories after it.
# PARAMS:
# category_class - type (class) of the category as registered in Persistence
# item_class - type (class) of the item that is assigned a category
#     (contains a category id field) as registered in Persistence
# item_id - id of the item instance
# category_id_field - string name of the category id field in the item class
def build_choice_list(category_class, item_class, item_id, category_id_field):
    # Get the categories list - needed anyway by the form
    categories = Persistence.engine(category_class).get()
    final_list = []  # final list of categories for the list

    # get the edited item's instance and put its category on top of the categories list
    items = Persistence.engine(item_class).get(item_id)
    if items and items != []:  # if the item's instance found

        category_id = getattr(items[0], category_id_field)
        if category_id:  # if the item has a category assigned
            # search for the item's category in the existing categories
            category = [category for category in categories if category.id == category_id]
            if category and category != []:     # if the item's category exists in the list
                final_list.append(category[0])  # set the item's category as the first in the list
                categories.remove(category[0])

    # create an empty category and put it on top or next to the item's category
    empty_category = category_class()
    empty_category.id = None            # explicitly clear the id
    final_list.append(empty_category)

    # append the rest of the categories list
    final_list.extend(categories)

    return final_list


