from django import template
from django.contrib.admin.templatetags.admin_list import   result_hidden_fields , \
                                                result_headers,results


register = template.Library()

def submit_row(context):
    """
    Displays the row of buttons for delete and save.
    """
    opts = context['opts']
    change = context['change']
    is_popup = context['is_popup']
    save_as = context['save_as']
    return {
        'onclick_attrib': (opts.get_ordered_objects() and change
                            and 'onclick="submitOrderForm();"' or ''),
        'show_delete_link': (not is_popup and context['has_delete_permission']
                              and (change or context['show_delete'])),
        'show_save_as_new': not is_popup and change and save_as,
        'show_save_and_add_another': context['has_add_permission'] and
                            not is_popup and (not save_as or context['add']),
        'show_save_and_continue': not is_popup and context['has_change_permission'],
        'is_popup': is_popup,
        'show_save': True
    }
submit_row = register.inclusion_tag('kio_cal/submit_line.html', takes_context=True)(submit_row)

# django.contrib.admin.templatetags.admin_list
def article_result_list(cl):
    return {'cl': cl,
            'result_hidden_fields': list(result_hidden_fields(cl)),
            'result_headers': list(result_headers(cl)),
            'results': zip(cl.result_list,list(results(cl)))}
result_list = register.inclusion_tag("admin/kio_cal/article/change_list_results.html")(article_result_list)