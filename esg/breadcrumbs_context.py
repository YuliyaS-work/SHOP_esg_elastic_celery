from django.urls import resolve, reverse

from .models import Rubric, Gas, Electro, Santeh, GasProduct, ElectroProduct, SantehProduct


# Универсальная карта моделей
RUBRIC_MODELS = {
    'Газификация': {
        'subrubric': Gas,
        'product': GasProduct,
    },
    'Электрика': {
        'subrubric': Electro,
        'product': ElectroProduct,
    },
    'Сантехника': {
        'subrubric': Santeh,
        'product': SantehProduct,
    },
}

def breadcrumbs_context(request):
    '''Генерауия крошек на старницах, содержащих карточки товаров.'''
    crumbs = [{'label': 'Главная', 'url': reverse('main')}]

    try:
        match = resolve(request.path_info)
        kwargs = match.kwargs
        view_name = match.view_name

        # Каталог
        if view_name.startswith('catalog') or 'rubric_name_translit' in kwargs:
            crumbs.append({'label': 'Каталог', 'url': reverse('catalog')})

        # Раздел
        rubric_name_translit = kwargs.get('rubric_name_translit')
        rubric = Rubric.objects.filter(name_translit=rubric_name_translit).first() if rubric_name_translit else None

        if rubric:
            crumbs.append({
                'label': rubric.rubric_name,
                'url': reverse('subrubrics', kwargs={'rubric_name_translit': rubric_name_translit})
            })

            model_map = RUBRIC_MODELS.get(rubric.rubric_name)

            # Подраздел
            subrubric_title_translit = kwargs.get('subrubric_title_translit')
            if subrubric_title_translit and model_map:
                SubrubricModel = model_map['subrubric']
                subrubric = SubrubricModel.objects.filter(title_translit=subrubric_title_translit).first()
                if subrubric:
                    crumbs.append({
                        'label': subrubric.title,
                        'url': reverse('products', kwargs={'rubric_name_translit': rubric_name_translit, 'subrubric_title_translit': subrubric_title_translit})
                    })

            # Товар
            product_title_translit = kwargs.get('product_title_translit')
            if product_title_translit and model_map:
                ProductModel = model_map['product']
                product = ProductModel.objects.filter(title_translit=product_title_translit).first()
                if product:
                    crumbs.append({
                        'label': product.title,
                        'url': reverse('product', kwargs={'rubric_name_translit': rubric_name_translit, 'subrubric_title_translit': subrubric_title_translit, 'product_title_translit': product_title_translit})
                    })

    except Exception as e:
        print(f'Breadcrumb error: {e}')

    return {'breadcrumbs': crumbs}