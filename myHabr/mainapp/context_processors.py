from blogapp.models import BlogCategories


def categories(request):
    _categories = BlogCategories.objects.order_by('id')
    return { 'BlogCategories' : _categories }