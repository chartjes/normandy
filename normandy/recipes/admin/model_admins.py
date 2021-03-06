from django.contrib import admin
from django.template.loader import render_to_string

from normandy.recipes import models
from normandy.recipes.forms import RecipeAdminForm

from reversion.admin import VersionAdmin


@admin.register(models.Recipe)
class RecipeAdmin(VersionAdmin):
    form = RecipeAdminForm
    save_as = True
    list_display = [
        'name',
        'enabled',
        'action',
        'filter_expression',
    ]
    search_fields = ['name']

    list_filter = [
        ('enabled', admin.BooleanFieldListFilter),
        ('action', admin.RelatedOnlyFieldListFilter),
    ]

    fieldsets = [
        [None, {
            'fields': ['name', 'enabled', 'filter_expression']
        }],
        ['Action', {
            'fields': [
                'action',
                'arguments_json',
            ],
        }],
    ]


@admin.register(models.Action)
class ActionAdmin(VersionAdmin):
    list_display = ['name', 'implementation_hash']
    fieldsets = [
        [None, {
            'fields': [
                'name',
                'implementation_hash',
                'implementation',
                'arguments_schema_json',
                'recipe_list',
            ]
        }],
    ]

    readonly_fields = ['implementation_hash', 'recipe_list']

    def recipe_list(self, action):
        """List all recipes that the action is being used by."""
        return render_to_string('admin/field_recipe_list.html', {
            'recipes': action.recipes_used_by.order_by('name'),
        })
    recipe_list.short_description = 'Used in Recipes'
