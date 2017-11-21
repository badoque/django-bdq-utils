class AbstractListMerger:

    def update_item(self, instance, *args, **kwargs):
        raise NotImplementedError()

    def create_item(self, instance, *args, **kwargs):
        raise NotImplementedError()

    def merge_itens(self, instance, itens_dct_list):
        import six
        from django.core.exceptions import ImproperlyConfigured

        Model = type(instance)

        if not self.list_attr_name or not isinstance(self.list_attr_name, six.string_types):
            raise ImproperlyConfigured('The property "list_attr_name" was not'
                ' defined in the ListMerger class')

        if not hasattr(instance, self.list_attr_name):
            raise AttributeError(type(instance).__name__+' does not have an attribute named \''+ self.list_attr_name +'\'')

        old_itens = list(getattr(instance, self.list_attr_name).all())
        old_itens_ids = [i.id for i in list(getattr(instance, self.list_attr_name).all())]
        new_itens_ids = [i.get('id', -1) for i in itens_dct_list]

        for item_dct in itens_dct_list:
            if item_dct.get('id', False) and item_dct['id'] in old_itens_ids:
                self.update_item(instance, **item_dct)

            elif item_dct.get('id', False) and item_dct['id'] not in old_itens_ids:
                if not getattr(instance, self.list_attr_name).filter(id=item_dct['id']).exists():
                    item_dct.pop('id')
                    self.create_item(instance, **item_dct)
            else:
                self.create_item(instance, **item_dct)

        for item in old_itens:
            if item.id not in new_itens_ids:
                item.delete()

class ListMerger(AbstractListMerger):

    def __init__(self, list_attr_name):
        self.list_attr_name = list_attr_name

    def update_item(self, instance, *args, **kwargs):
        getattr(instance, self.list_attr_name).filter(id=kwargs['id']).update(**kwargs)

    def create_item(self, instance, *args, **kwargs):
        getattr(instance, self.list_attr_name).create(**kwargs)



